import json
import copy
from http import HTTPStatus


def format_status(status):
    return f"{status} {HTTPStatus(status).phrase}"


def response_type(func):
    def wrapper(parent, body=None, status=200, headers={}):
        all_headers = copy.copy(parent.app.headers)
        body, rheaders = func(parent, body, status)
        all_headers["Content-Length"] = len(body)
        for k, v in rheaders.items():
            all_headers[k] = v
        all_headers.update(headers)

        list_headers = []
        for key, value in all_headers.items():
            if not value:
                return
            list_headers.append((key, str(value)))

        return format_status(status), list_headers, body
    return wrapper


class VResponse():
    def __init__(self, app):
        self.app = app

    def __call__(self, status=200, message=None, headers={}, **kwargs):
        data = {
            "response" : status,
            "message" : HTTPStatus(status).phrase if message is None else message,
            **kwargs
        }
        return self.json(data, status=status, headers=headers)


    @response_type
    def text(self, body, status):
        if body is None:
            r = "Status" if status < 400 else "Error"
            body = f"{r} {status}: {HTTPStatus(status).description}"
        body = body.encode("utf-8")
        headers = {"Content-Type" : "text/txt"}
        return body, headers

    @response_type
    def json(self, body, status):
        body = json.dumps(body).encode("utf-8")
        headers = {"Content-Type" : "application/json"}
        return body, headers

    @response_type
    def raw(self, body, status):
        headers = {"Content-Type" : "application/octet-stream"}
        if type(body) == bytes:
            return body, headers
        elif type.body == str:
            return body.encode("utf-8"), headers
        else:
            return str(body).encode("utf-8"), headers
