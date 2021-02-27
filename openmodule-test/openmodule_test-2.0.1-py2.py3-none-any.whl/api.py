from urllib.parse import urljoin

import requests_mock


class ApiMocker:
    host = None

    def __init__(self, mocker):
        self.mocker = mocker
        assert self.host, "you need to set a host"

    def server_url(self, url):
        new_url = urljoin(self.host, url)
        if not new_url.endswith("/") and "?" not in new_url:
            new_url += "/"
        return new_url

    def ok(self):
        self.mocker.get(requests_mock.ANY, status_code=200)
        self.mocker.post(requests_mock.ANY, status_code=200)
        self.mocker.put(requests_mock.ANY, status_code=200)
        self.mocker.delete(requests_mock.ANY, status_code=200)

    def timeout_status(self):
        self.mocker.get(requests_mock.ANY, status_code=408)
        self.mocker.post(requests_mock.ANY, status_code=408)
        self.mocker.put(requests_mock.ANY, status_code=408)
        self.mocker.delete(requests_mock.ANY, status_code=408)

    def unavailable(self):
        self.mocker.get(requests_mock.ANY, status_code=503)
        self.mocker.post(requests_mock.ANY, status_code=503)
        self.mocker.put(requests_mock.ANY, status_code=503)
        self.mocker.delete(requests_mock.ANY, status_code=503)

    def server_error(self):
        self.mocker.get(requests_mock.ANY, status_code=500)
        self.mocker.post(requests_mock.ANY, status_code=500)
        self.mocker.put(requests_mock.ANY, status_code=500)
        self.mocker.delete(requests_mock.ANY, status_code=500)

    def invalid_auth(self):
        self.mocker.get(requests_mock.ANY, status_code=403)
        self.mocker.post(requests_mock.ANY, status_code=403)
        self.mocker.get(requests_mock.ANY, status_code=403)
        self.mocker.post(requests_mock.ANY, status_code=403)

    def bad_request(self):
        self.mocker.get(requests_mock.ANY, status_code=400)
        self.mocker.post(requests_mock.ANY, status_code=400)
        self.mocker.get(requests_mock.ANY, status_code=400)
        self.mocker.post(requests_mock.ANY, status_code=400)

    def not_found(self):
        self.mocker.get(requests_mock.ANY, status_code=404)
        self.mocker.post(requests_mock.ANY, status_code=404)
        self.mocker.get(requests_mock.ANY, status_code=404)
        self.mocker.post(requests_mock.ANY, status_code=404)
