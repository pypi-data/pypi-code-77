import datetime
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import click

from .click_helper import ClickHelper, ConfigEntry

class ApiHelper(object):
    class ConnectionError(Exception):
        """Raised when the api server could be requested."""
        pass

    class ServerError(Exception):
        """Raised when the api server returns an error."""
        pass

    @classmethod
    def get_status(cls):
        try:
            response = cls.send_api_request('/status', 'GET')
            if response.status_code != 200:
                raise cls.ServerError(f'Error requesting status (code {response.status_code})')
            data = response.json()
        except requests.ConnectionError:
            raise cls.ConnectionError('Connection to traint servers could not be established.')

        return data['status']

    @classmethod
    def get_usecases(cls):
        try:
            response = cls.send_api_request('/usecases', 'GET')
            if response.status_code == 200:
                if not response.json():
                    usecases = []
                else:
                    usecases = response.json()
            else:
                raise cls.ServerError(f'Error requesting usecases (code {response.status_code})')
        except requests.ConnectionError:
            raise cls.ConnectionError('Connection to traint servers could not be established.')

        return usecases

    @classmethod
    def get_data(cls):
        try:
            response = cls.send_api_request('/data', 'GET')
            if response.status_code == 200:
                if not response.json():
                    data = []
                else:
                    data = response.json()
            else:
                raise cls.ServerError(f'Error requesting data (code {response.status_code})')
        except requests.ConnectionError:
            raise cls.ConnectionError('Connection to traint servers could not be established.')

        return data

    @classmethod 
    def upload_data_file(cls, file_path, data_id):
        file = open(file_path, 'rb')
        fields = {
            'user_file': ('file.csv', file),
            'data_id': data_id,
        }
        try:
            response = cls.send_api_request('/data/upload', 'POST', data=MultipartEncoder(fields=fields))
            if response.status_code != 200:
                raise cls.ServerError(f'Error uploading data (code {response.status_code})')
        except requests.ConnectionError:
            raise cls.ConnectionError('Connection to traint servers could not be established.')

        return response.text

    @classmethod
    def get_trainings(cls, usecase_name):
        try:
            response = cls.send_api_request('/trainings', 'GET', params={'usecase_name': usecase_name})
            if response.status_code == 200:
                if not response.json():
                    trainings = []
                else:
                    trainings = response.json()
            else:
                raise cls.ServerError(f'Error requesting trainings (code {response.status_code})')
        except requests.ConnectionError:
            raise cls.ConnectionError('Connection to traint servers could not be established.')

        # create date string for current timezone
        for training in trainings:
            training['start'] = datetime.datetime.fromtimestamp(training['start']/1000).strftime('%Y-%m-%d %H:%M:%S')

        return trainings

    @classmethod
    def start_training(cls, data_id, target, trainer_type, usecase_name, options):
        fields = {
            'data_id': data_id,
            'target': target,
        }
        if trainer_type:
            fields['trainer_type'] = trainer_type
        if usecase_name:
            fields['usecase_name'] = usecase_name
        if options:
            fields['options'] = options

        try:
            response = cls.send_api_request('/training/start', 'POST', data=MultipartEncoder(fields=fields))
            if response.status_code != 200:
                msg = response.json().get('error', 'Training command failed')
                raise cls.ServerError(f'{msg} (code {response.status_code})')
        except requests.ConnectionError:
            raise cls.ConnectionError('Connection to traint servers could not be established.')

        return True

    @classmethod
    def get_models(cls):
        try:
            response = cls.send_api_request('/models', 'GET')
            if response.status_code == 200:
                if not response.json():
                    models = []
                else:
                    models = response.json()
            else:
                raise cls.ServerError(f'Error requesting models (code {response.status_code})')
        except requests.ConnectionError:
            raise cls.ConnectionError('Connection to traint servers could not be established.')

        # create date string for current timezone
        for model in models:
            model['last_updated'] = datetime.datetime.fromtimestamp(model['last_updated']/1000).strftime('%Y-%m-%d %H:%M:%S')

        return models

    @classmethod
    def stage_model(cls, usecase_name, version, stage):
        fields = {
            'usecase_name': usecase_name,
            'version': version,
            'stage': stage,
        }
        try:
            response = cls.send_api_request('/model/stage', 'POST', data=MultipartEncoder(fields=fields))
            if response.status_code == 200:
                model = response.json()
            else:
                msg = response.json().get('error', 'Error staging model')
                raise cls.ServerError(f'{msg} (code {response.status_code})')
        except requests.ConnectionError:
            raise cls.ConnectionError('Connection to traint servers could not be established.')

        # create date string for current timezone
        model['last_updated'] = datetime.datetime.fromtimestamp(model['last_updated']/1000).strftime('%Y-%m-%d %H:%M:%S')

        return model

    @classmethod
    def send_api_request(cls, path:str, verb: str, params=None, data=None):
        api_base_url = ClickHelper.get_config_value(ConfigEntry.API_BASE_URL)
        api_token = ClickHelper.get_config_value(ConfigEntry.API_TOKEN)

        if not api_base_url or not api_token:
            raise click.UsageError('CLI not configured yet, please run \'traint setup\'')

        headers = {"Authorization": f'Bearer {api_token}'}
        if data:
            headers['Content-Type'] = data.content_type

        return requests.request(verb, url=f'{api_base_url}{path}', headers=headers, params=params, data=data)
