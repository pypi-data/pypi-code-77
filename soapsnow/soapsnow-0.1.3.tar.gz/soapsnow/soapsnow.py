
import requests

class SOAPSnow:

    def __init__(self, user, pwd, url):

        self._usr = user
        self._pwd = pwd
        self._url = url
        self._xml_head = (
            '<soapenv:Envelope '
            'xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" '
            'xmlns:x="http://www.service-now.com/">'
            '<soapenv:Body>'
        )
        self._xml_tail = '</soapenv:Body></soapenv:Envelope>'

    def req(self, method, **query):
        payload  = f'{self._xml_head}<x:{method}>'
        payload += ''.join(
            [f'<{k}>{v}</{k}>' for k, v in query.items()]
        )
        payload += f'</x:{method}>{self._xml_tail}'
        response = requests.post(
            url  = self._url,
            data = payload,
            auth = (self._usr, self._pwd)
        )
        return response