import requests
from .utils import RequestConstructor
from .exceptions import TriggerError

class IFlowly():

    def __init__(self, api_key):
        self.requester = RequestConstructor(api_key)

    def get_flow(self, flow_name):
        return Flow(flow_name, self.requester)

class Flow():

    FLOW_GET_URL = 'https://api.iflowly.com/v1/flows/{flow_name}/'

    def __init__(self, flow_name, requester):
        self.requester = requester
        self.__get_flow(flow_name)

    def __set_attrs_from_response(self, response):
        self.id = response.get('id')
        self.name = response.get('name')
        self.deleted = response.get('deleted')
        self.active = response.get('active')

    def __get_flow(self, flow_name):
        url = self.requester.transform_url('flows', flow_name)
        response = self.requester.request('get', url)
        self.__set_attrs_from_response(response)

    def run_event(self, event_name):
        PATH = '{flow_id}/execute-event/{event_name}'.format(flow_id=self.id, event_name=event_name)
        URL = self.requester.transform_url('flows', PATH)
        response = self.requester.request('post', URL)


    def run_trigger(self, trigger_name):
        PATH = '{flow_id}/execute-trigger/{trigger_name}'.format(flow_id=self.id, trigger_name=trigger_name)
        URL = self.requester.transform_url('flows', PATH)
        try:
            response = self.requester.request('post', URL)
        except requests.exceptions.HTTPError as e:
            response_json = e.response.json()
            detail = response_json.get('detail')
            raise TriggerError(detail) from None

    def get_initial_state(self):
        raise NotImplementedError('TODO:: Help us implement this')
