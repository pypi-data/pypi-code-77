from __future__ import annotations

from ds_discovery.intent.synthetic_intent import SyntheticIntentModel
from ds_discovery.managers.synthetic_property_manager import SyntheticPropertyManager
from ds_discovery.components.abstract_common_component import AbstractCommonComponent

__author__ = 'Darryl Oatridge'


class SyntheticBuilder(AbstractCommonComponent):

    REPORT_CATALOG = 'catalog'
    REPORT_FIELDS = 'field_description'

    @classmethod
    def from_uri(cls, task_name: str, uri_pm_path: str, username: str, uri_pm_repo: str=None, pm_file_type: str=None,
                 pm_module: str=None, pm_handler: str=None, pm_kwargs: dict=None, default_save=None,
                 reset_templates: bool=None, template_path: str=None, template_module: str=None,
                 template_source_handler: str=None, template_persist_handler: str=None, align_connectors: bool=None,
                 default_save_intent: bool=None, default_intent_level: bool=None, order_next_available: bool=None,
                 default_replace_intent: bool=None, has_contract: bool=None) -> SyntheticBuilder:
        """ Class Factory Method to instantiates the components application. The Factory Method handles the
        instantiation of the Properties Manager, the Intent Model and the persistence of the uploaded properties.
        See class inline docs for an example method

         :param task_name: The reference name that uniquely identifies a task or subset of the property manager
         :param uri_pm_path: A URI that identifies the resource path for the property manager.
         :param username: A user name for this task activity.
         :param uri_pm_repo: (optional) A repository URI to initially load the property manager but not save to.
         :param pm_file_type: (optional) defines a specific file type for the property manager
         :param pm_module: (optional) the module or package name where the handler can be found
         :param pm_handler: (optional) the handler for retrieving the resource
         :param pm_kwargs: (optional) a dictionary of kwargs to pass to the property manager
         :param default_save: (optional) if the configuration should be persisted. default to 'True'
         :param reset_templates: (optional) reset connector templates from environ variables. Default True
                                (see `report_environ()`)
         :param template_path: (optional) a template path to use if the environment variable does not exist
         :param template_module: (optional) a template module to use if the environment variable does not exist
         :param template_source_handler: (optional) a template source handler to use if no environment variable
         :param template_persist_handler: (optional) a template persist handler to use if no environment variable
         :param align_connectors: (optional) resets aligned connectors to the template. default Default True
         :param default_save_intent: (optional) The default action for saving intent in the property manager
         :param default_intent_level: (optional) the default level intent should be saved at
         :param order_next_available: (optional) if the default behaviour for the order should be next available order
         :param default_replace_intent: (optional) the default replace existing intent behaviour
         :param has_contract: (optional) indicates the instance should have a property manager domain contract
         :return: the initialised class instance
         """
        pm_file_type = pm_file_type if isinstance(pm_file_type, str) else 'json'
        pm_module = pm_module if isinstance(pm_module, str) else cls.DEFAULT_MODULE
        pm_handler = pm_handler if isinstance(pm_handler, str) else cls.DEFAULT_PERSIST_HANDLER
        _pm = SyntheticPropertyManager(task_name=task_name, username=username)
        _intent_model = SyntheticIntentModel(property_manager=_pm, default_save_intent=default_save_intent,
                                             default_intent_level=default_intent_level,
                                             order_next_available=order_next_available,
                                             default_replace_intent=default_replace_intent)
        super()._init_properties(property_manager=_pm, uri_pm_path=uri_pm_path, default_save=default_save,
                                 uri_pm_repo=uri_pm_repo, pm_file_type=pm_file_type, pm_module=pm_module,
                                 pm_handler=pm_handler, pm_kwargs=pm_kwargs, has_contract=has_contract)
        return cls(property_manager=_pm, intent_model=_intent_model, default_save=default_save,
                   reset_templates=reset_templates, template_path=template_path, template_module=template_module,
                   template_source_handler=template_source_handler, template_persist_handler=template_persist_handler,
                   align_connectors=align_connectors)

    @classmethod
    def scratch_pad(cls) -> SyntheticIntentModel:
        """ A class method to use the Components intent methods as a scratch pad"""
        return super().scratch_pad()

    @property
    def pm(self) -> SyntheticPropertyManager:
        return self._component_pm

    @property
    def intent_model(self) -> SyntheticIntentModel:
        return self._intent_model

    @property
    def tools(self) -> SyntheticIntentModel:
        return self._intent_model

    def run_component_pipeline(self, size: int, intent_levels: [str, int, list]=None, seed: int=None):
        """Runs the components pipeline from source to persist"""
        result = self.intent_model.run_intent_pipeline(size=size, intent_levels=intent_levels, seed=seed)
        self.save_persist_canonical(result)

    def setup_bootstrap(self, domain: str=None, project_name: str=None, path: str=None, file_type: str=None):
        """ Creates a bootstrap simulator with a SyntheticBuilder. Note this does not set the source

        :param domain: (optional) The domain this simulator sits within for example 'Healthcare' or 'Financial Services'
        :param project_name: (optional) a project name that will replace the hadron naming on file prefix
        :param path: (optional) a path added to the template path default
        :param file_type: (optional) a file_type for the persisted file, default is 'parquet'
        """
        file_type = file_type if isinstance(file_type, str) else 'parquet'
        project_name = project_name if isinstance(project_name, str) else 'hadron'
        file_name = self.pm.file_pattern(name='dataset', project=project_name, path=path, file_type=file_type,
                                         versioned=True)
        self.set_persist(uri_file=file_name)
        report_list = [{'report': self.REPORT_CATALOG, 'file_type': 'csv'}]
        self.set_report_persist(reports=report_list, project=project_name, path=path)
        self.set_description(f"A domain specific {domain} simulated {project_name} dataset for {self.pm.task_name}")
