import hashlib
import hmac
import time
import typing


class ApiKey:
    """
    A class to represent an ApiKey.

    ...

    Attributes
    ----------
    api_key : str
        the api key
    secret : str
        the secret

    """

    def __init__(self, api_key, secret) -> None:
        self.api_key = api_key
        self.secret = secret


def create_authentication_headers(apikey: ApiKey, path: str, data) -> typing.Dict[str, str]:
    """
    Generates authentication headers.

    3 headers are set for authentication. These are:  
    btse-api  
    btse-nonce  
    btse-sign  

    Parameters
    ----------
    apikey : ApiKey
        ApiKey object that contains the apikey and secret
    path : str
        URL path (URLs are scheme://host:post/path?query)
    data
        JSON string representation of data that constitutes the request body

    Returns
    -------
    dict: typing.Dict[str, str]
        Returns dictionary with the 3 required headers as keys and their values.

    """
    nonce = str(int(time.time()*1000))
    message = path + nonce + data

    signature = _signature(apikey, message)
    headers = {
        'btse-api': apikey.api_key,
        'btse-nonce': nonce,
        'btse-sign': signature
    }

    return headers


def _signature(apikey: ApiKey, message):
    """Generate hex digest of the HMAC of the message"""
    signature = hmac.new(bytes(apikey.secret, 'latin-1'),
                         msg=bytes(message, 'latin-1'), digestmod=hashlib.sha384).hexdigest()
    return signature
