import logging
from typing import Optional, List, Any, Callable
import os

from pydantic import BaseModel

from .services import DeeployService, GitService, ModelWrapper, ExplainerWrapper
from .models import Repository, ClientConfig, Deployment, CreateDeployment, DeployOptions
from .enums import PredictionMethod, ExplainerType
from .common import delete_all_contents_in_directory, directory_exists, directory_empty


class Client(object):
    """ 
    A class for interacting with Deeploy
    """

    __config: ClientConfig

    def __init__(self, access_key: str, secret_key: str, host: str, workspace_id: str,
                 local_repository_path: str, branch_name: str = None) -> None:
        """Initialise the Deeploy client
        """
        self.__config = ClientConfig(**{
            'access_key': access_key,
            'secret_key': secret_key,
            'host': host,
            'workspace_id': workspace_id,
            'local_repository_path': local_repository_path,
            'branch_name': branch_name,
            'repository_id': '',
        })
        

        self.__git_service = GitService(local_repository_path)
        self.__deeploy_service = DeeployService(
            access_key,
            secret_key,
            host
        )

        if not self.__are_clientoptions_valid(self.__config):
            raise Exception('Client options not valid')

        repository_in_workspace, repository_id = self.__is_git_repository_in_workspace()

        if not repository_in_workspace:
            raise Exception(
                'Repository was not found in the Deeploy workspace. Make sure you have connected it before')
        else:
            self.__config.repository_id = repository_id

        return

    def deploy(self, model: Any, options: DeployOptions, explainer: Any = None, overwrite: bool = False,
               commit_message: str = None) -> Deployment:
        """Deploy a model on Deeploy

        Parameters
        ----------
        model: Any
            The class instance of an ML model. Supports 
        options: DeployOptions
            The deploy options class containing the deployment options
        explainer: Any, optional
            The class instance of an optional model explainer
        overwrite: boolean, optional
            Whether or not to overwrite files that are in the 'model' and 'explainer' 
            folders in the git folder. Defaults to False
        commit_message: str, optional
            Commit message to use
        """
        logging.info('Pulling from the remote repository...')
        self.__git_service.pull()
        logging.info('Successfully pulled from the remote repository.')

        logging.info('Saving the model to disk...')
        model_wrapper = ModelWrapper(model, pytorch_model_file_path=options.pytorch_model_file_path)
        self.__prepare_model_directory(overwrite)
        model_folder = os.path.join(
            self.__config.local_repository_path, 'model')
        model_wrapper.save(model_folder)
        self.__git_service.add_folder_to_staging('model')
        commit_message = ':sparkles: Add new model'

        if explainer:
            logging.info('Saving the explainer to disk...')
            explainer_wrapper = ExplainerWrapper(explainer)
            self.__prepare_explainer_directory(overwrite)
            explainer_folder = os.path.join(
                self.__config.local_repository_path, 'explainer')
            explainer_wrapper.save(explainer_folder)
            self.__git_service.add_folder_to_staging('explainer')
            commit_message += ' and explainer'
            explainer_type = explainer_wrapper.get_explainer_type()
        else:
            explainer_type = ExplainerType.NO_EXPLAINER

        logging.info('Committing and pushing the result to the remote.')
        commit_sha = self.__git_service.commit(commit_message)
        self.__git_service.push()

        deployment_options = {
            'repository_id': self.__config.repository_id,
            'name': options.name,
            'description': options.description,
            # TODO: example input & output
            'example_input': options.example_input,
            'example_output': options.example_output,
            'model_type': model_wrapper.get_model_type().value,
            'model_class_name': options.model_class_name,
            'method': options.method,
            'model_serverless': options.model_serverless,
            'branch_name': self.__git_service.get_current_branch_name(),
            'commit_sha': commit_sha,
            'explainer_type': explainer_type.value,
            'explainer_serverless': options.explainer_serverless
        }

        deployment = self.__deeploy_service.create_deployment(
            self.__config.workspace_id, CreateDeployment(**deployment_options))

        return deployment

    def __are_clientoptions_valid(self, config: ClientConfig) -> bool:
        """Check if the supplied options are valid
        """
        try:
            self.__deeploy_service.get_workspace(config.workspace_id)
        except Exception as e:
            raise e

        return True

    def __is_git_repository_in_workspace(self) -> (bool, str):
        remote_url = self.__git_service.get_remote_url()
        workspace_id = self.__config.workspace_id

        repositories = self.__deeploy_service.get_repositories(workspace_id)
        correct_repositories = list(
            filter(lambda x: x.git_ssh_pull_link == remote_url, repositories))

        if len(correct_repositories) != 0:
            repository_id = correct_repositories[0].id
            return True, repository_id

        return False, None

    def __prepare_model_directory(self, overwrite=False) -> None:
        model_folder_path = os.path.join(
            self.__config.local_repository_path, 'model')
        if not directory_exists(model_folder_path):
            try:
                os.mkdir(model_folder_path)
            except OSError:
                logging.error("Creation of the directory %s failed" %
                              model_folder_path)
        elif not directory_empty(model_folder_path):
            if not overwrite:
                raise Exception(
                    'The folder %s is not empty. Pass \'overwrite=True\' to overwrite contents.' % model_folder_path)
            delete_all_contents_in_directory(model_folder_path)
            self.__git_service.delete_folder_from_staging('model')
        else:  # folder exists and empty
            pass
        return

    def __prepare_explainer_directory(self, overwrite=False) -> None:
        explainer_folder_path = os.path.join(
            self.__config.local_repository_path, 'explainer')
        if not directory_exists(explainer_folder_path):
            try:
                os.mkdir(explainer_folder_path)
            except OSError:
                logging.error("Creation of the directory %s failed" %
                              explainer_folder_path)
        elif not directory_empty(explainer_folder_path):
            if not overwrite:
                raise Exception(
                    'The folder %s is not empty. Pass \'overwrite=True\' to overwrite contents.' % explainer_folder_path)
            delete_all_contents_in_directory(explainer_folder_path)
        else:  # folder exists and empty
            pass
        self.__git_service.delete_folder_from_staging('explainer')
        return
