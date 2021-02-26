import requests
from requests import RequestException

from blackpay.utils import retry


@retry(RequestException, tries=3, delay=5)
def request(method, request_url):
    try:
        response = requests.Session().request(method=method, url=request_url)
    except RequestException as e:
        raise RequestException(e, method, request_url)
    else:
        return response
