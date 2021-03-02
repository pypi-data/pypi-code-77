import cgi
import functools
from http.server import BaseHTTPRequestHandler, HTTPServer
import re
from typing import Iterable, List, Optional, Tuple
from urllib.parse import urlparse, parse_qsl
from intercom_test.cases import hash_from_fields
from intercom_test.utils import FilteredDictView, optional_key

NameValuePair = Tuple[str, str]

def run_server(stub_cases: Iterable[dict], port:int = 8000) -> None:
    server_address = ('', port)
    httpd = HTTPServer(server_address, StubHandler)
    
    httpd.stub_cases = {}
    for case in stub_cases:
        case_key = make_case_key(
            case['method'].lower(),
            case['url'],
            case.get('request body')
        )
        h = hash_from_fields(case_key)
        httpd.stub_cases[h] = case
    
    httpd.serve_forever()

class StubHandler(BaseHTTPRequestHandler):
    def __getattr__(self, name):
        if name.startswith('do_'):
            http_method = name[3:].lower()
            return functools.partial(self.do_single_request, method)
        return super().__getattr__(name)
    
    def do_single_request(self, method: str) -> None:
        request_body = self.rfile.read(int(self.headers.get('Content-Length')))
        request_content_type = self.headers.get('Content-Type')
        if request_content_type:
            base_content_type, content_type_params = cgi.parse_header(request_content_type)
            request_body_is_json = base_content_type == 'application/json'
            for request_body_charset in optional_key(content_type_params, 'charset'):
                if not (request_body_is_json and request_body_charset.lower() != 'utf-8'):
                    request_body = request_body.decode(request_body_charset)
            if request_body_is_json:
                request_body = json.load(request_body)
        
        case_key = make_case_key(
            method,
            self.path,
            request_body
        )
        case = self.server.stub_cases.get(case_key)
        if case is None:
            # Oops, 404 time
            self.send_error(404)
        else:
            response_code = case.get('response status', 200)
            
            response_body = case['response body']
            response_body_jsonic = not isinstance(response_body, (str, bytes))
            
            response_headers = case.get('response headers', ())
            response_charset = HTTPCharset()
            if hasattr(response_headers, 'items') and callable(response_headers.items):
                response_headers = response_headers.items()
            if isinstance(response_body, str):
                response_headers = _headers_with_default_content_type(response_headers, 'text/plain')
                response_charset.name = 'utf-8'
                response_body = response_body.encode(response_charset.name)
            elif isinstance(response_body, bytes):
                response_headers = _headers_with_default_content_type(response_headers, 'application/octet-stream')
            else:
                response_headers = _jsonic_response_body_headers(response_headers)
                response_body = json.dumps(response_body).encode('ASCII')
            
            self.send_response(response_code)
            for name, value in response_headers:
                if response_charset.should_add_to(name, value):
                    value += response_charset.charset_param()
                self.send_header(name, value)
            self.end_headers()
            self.wfile.write(response_body)


def make_case_key(method: str, url: str, request_body) -> dict:
    path, qsparams = url_parts(url)
    return dict(
        method=method,
        path=path,
        qsparams=qsparams,
        request_body=request_body,
    )

def url_parts(raw_url: str) -> Tuple[str, List[NameValuePair]]:
    url = urlparse(raw_url)
    return (
        url.path,
        sorted(parse_qsl(url.query))
    )

def _jsonic_response_body_headers(headers: Iterable[Tuple[str, str]]) -> Iterable[NameValuePair]:
    for item in headers:
        if item[0].lower() != 'content-type':
            yield item
    yield ('Content-Type', 'application/json')

def _headers_with_default_content_type(headers: Iterable[Tuple[str, str]], default_content_type: str) -> Iterable[NameValuePair]:
    content_type_given = False
    for item in headers:
        if item[0].lower() == 'content-type':
            content_type_given = True
        yield item
    
    if not content_type_given:
        yield ('Content-Type', default_content_type)

class HTTPCharset:
    def __init__(self, name: Optional[str] = None):
        super().__init__()
        self.name = name
    
    def should_add_to(self, header: str, value: str) -> bool:
        if self.name is None:
            return False
        if header.lower() != 'content-type':
            return False
        if 'charset' in cgi.parse_header(value)[1]:
            return False
        return True
    
    def charset_param(self, ) -> str:
        return ";charset={}".format(self.name)
