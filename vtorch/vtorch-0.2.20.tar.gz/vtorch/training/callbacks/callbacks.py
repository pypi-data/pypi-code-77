from typing import Any, Dict, List, Optional, Union

from .clearml_reporter import ClearMLReporterI, ClearMLReporterNull
from .early_stopping import EarlyStoppingI, EarlyStoppingNull


class Callbacks:
    def __init__(
        self, clearml_reporter: Optional[ClearMLReporterI] = None, early_stopping: Optional["EarlyStoppingI"] = None
    ) -> None:
        self.clearml_reporter = clearml_reporter or ClearMLReporterNull()
        self.early_stopping = early_stopping or EarlyStoppingNull()

    def clearml_update_parameters(self, parameters: Dict[str, Any]) -> None:
        self.clearml_reporter.update_parameters(parameters)

    def add_clearml_tags(self, tags: Union[List[str], str]) -> None:
        self.clearml_reporter.add_tags(tags)

    def clearml_report_scalar(self, title: str, series: str, value: Union[int, float], iteration: int) -> None:
        self.clearml_reporter.report_scalar(title=title, series=series, value=value, iteration=iteration)

    def add_metric(self, val_metrics: Dict[str, float]) -> None:
        self.early_stopping.add_metric(val_metrics)

    def should_stop_early(self) -> bool:
        return self.early_stopping.should_stop_early()

    def is_best_so_far(self) -> bool:
        return self.early_stopping.is_best_so_far()
