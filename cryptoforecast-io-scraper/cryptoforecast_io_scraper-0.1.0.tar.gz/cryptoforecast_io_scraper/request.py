from __future__ import absolute_import, print_function, unicode_literals

import json
import requests

from cryptoforecast_io_scraper import exceptions


class DataReq(object):
    """
    CryptoForecast.io Scraper
    """

    GENERAL_URL = 'https://cryptoforecast.io'
    PREDICTION_API = '{0}/api/prediction-screener'.format(GENERAL_URL)

    def __init__(self, al='en-US', last_req_time=None, inter_req_time=20):
        """
        Initialize default values for params
        """
        # set user defined options used globally
        self.al = al
        self.last_req_time = last_req_time
        self.inter_req_time = inter_req_time
        self.aiohttp_session = None
        self.cookies = dict(
            requests.get(
                'https://cryptoforecast.io').cookies.items()
        )

    @staticmethod
    def _handle_req_response(response, resp_text, trim_chars=0):
        # check if the response contains json and throw an exception otherwise
        # Google mostly sends 'application/json' in the Content-Type header,
        # but occasionally it sends 'application/javascript
        # and sometimes even 'text/javascript
        if 'application/json' in response.headers['Content-Type'] or \
                'application/javascript' in response.headers['Content-Type'] or \
                'text/javascript' in response.headers['Content-Type']:

            # trim initial characters
            # some responses start with garbage characters, like ")]}',"
            # these have to be cleaned before being passed to the json parser
            content = resp_text[trim_chars:]

            # parse json
            return json.loads(content)
        else:
            # this is often the case when the amount of keywords in the payload for the IP
            # is not allowed by Google
            raise exceptions.ResponseError('The request failed: CryptoForecast.io returned a '
                                           'response with code {0}.'.format(response.status_code), response=response)

    def _get_data(self, url=PREDICTION_API, trim_chars=0, **kwargs):
        """Send a request to CryptoForecast.io and return the JSON response as a Python object

        :param url: the url to which the request will be sent
        :param trim_chars: how many characters should be trimmed off the beginning of the content of the response
            before this is passed to the JSON parser
        :param kwargs: any extra key arguments passed to the request builder (usually query parameters or data)
        :return:
        """
        s = requests.session()
        s.headers.update({'accept-language': self.al})
        response = s.get(url, cookies=self.cookies, **kwargs)

        return DataReq._handle_req_response(response, response.text, trim_chars=trim_chars)

    async def _async_get_data(self):
        raise NotImplementedError
