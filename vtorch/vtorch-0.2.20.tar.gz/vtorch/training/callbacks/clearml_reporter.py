import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union

from clearml import Task


class ClearMLReporterI(ABC):
    @classmethod
    @abstractmethod
    def create(cls, experiment_name: str, separate_language: bool = True) -> "ClearMLReporterI":
        pass

    @abstractmethod
    def report_scalar(self, title: str, series: str, value: Union[int, float], iteration: int) -> None:
        pass

    @abstractmethod
    def update_parameters(self, parameters: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def add_tags(self, tags: Union[List[str], str]) -> None:
        pass


class ClearMLReporterNull(ClearMLReporterI):
    @classmethod
    def create(cls, experiment_name: str, separate_language: bool = True) -> "ClearMLReporterNull":
        return cls()

    def report_scalar(self, title: str, series: str, value: Union[int, float], iteration: int) -> None:
        pass

    def update_parameters(self, parameters: Dict[str, Any]) -> None:
        pass

    def add_tags(self, tags: Union[List[str], str]) -> None:
        pass


class ClearMLReporter(ClearMLReporterI):
    def __init__(self, task: Task) -> None:
        self.task = task
        self.logger = self.task.get_logger()

    @classmethod
    def create(cls, experiment_name: str, separate_language: bool = True) -> "ClearMLReporter":
        # The project name be inferred from the folder we are launching from
        # I.e. when we train any model we do `python run_scripts/train_model.py --config...`
        # And that is launched directly from the project folder, which can be the default project name
        project_name = os.path.basename(os.path.abspath(os.path.curdir))
        language: str = "lang_unk"
        if separate_language:
            language = "lang_" + experiment_name.split("_")[0]
            experiment_name = "_".join(experiment_name.split("_")[1:])
        trains_task = Task.init(
            project_name=project_name,
            task_name=experiment_name,
            auto_resource_monitoring=True,
            auto_connect_arg_parser=False,  # The config file path. Maybe it's needed?
        )
        obj = cls(trains_task)
        obj.add_tags([language])
        obj.task.set_resource_monitor_iteration_timeout(1e9)
        return obj

    def report_scalar(self, title: str, series: str, value: Union[int, float], iteration: int) -> None:
        self.logger.report_scalar(title=title, series=series, value=value, iteration=iteration)

    def update_parameters(self, parameters: Dict[str, Any]) -> None:
        self.task.connect(parameters)

    def add_tags(self, tags: Union[List[str], str]) -> None:
        self.task.add_tags(tags)
