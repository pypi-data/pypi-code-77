import requests
import json
import urllib.parse
import os

class SoraException(Exception):
    pass

class Sora():
    _cert_path = None
    def __init__(self, api_key):
        if "." in api_key or len(api_key) < 20:
            raise SoraException("Invalid API key")
        if type(api_key) != str:
            raise TypeError("API key must be a string")
        self._config = {
            "base_url": "verify.soraid.com",
            "api_key": api_key,
        }

    def _add_self_signed_cert(self, path):
        if path is None:
            return
        if not os.path.exists(path):
            raise ValueError("SSL cert path does not exist")
        self._cert_path = path

    def _override_base_url(self, base_url):
        if type(base_url) != str:
            raise TypeError("Base URL must be a string")
        self._config["base_url"] = base_url

    def _make_sora_request(self, path, method, params=None, grpc=False):
        if grpc:
            raise NotImplementedError("GRPC not yet supported")
        if not self._config:
            raise RuntimeError("Must call init() before making a Sora request.")

        url = urllib.parse.urlunparse(("https", self._config['base_url'], path, None, None, None))
        if method.upper() == "GET":
            assert not params
            response = requests.get(url,
                headers={
                    "authorization": f"Bearer {self._config['api_key']}",
                },
                verify=self._cert_path,
            )
        elif method.upper() == "POST":
            response = requests.post(url,
                data=json.dumps(params),
                headers={
                    "authorization": f"Bearer {self._config['api_key']}",
                },
                verify=self._cert_path,
            )
        if response.status_code != 200:
            raise SoraException(f"{response.status_code} {response.reason}: {response.text}")
        return response.json()


    def create_login_session(self, params=None):
        return self._make_sora_request("/v1/login_sessions", "POST", params)

    def get_login_session(self, login_id):
        return self._make_sora_request(f"/v1/login_sessions/{login_id}", 'GET')

    def create_verification_session(self, params=None):
        return self._make_sora_request("/v1/verification_sessions", "POST", params)

    def get_verification_session(self, verification_id):
        return self._make_sora_request(f"/v1/verification_sessions/{verification_id}", 'GET')

