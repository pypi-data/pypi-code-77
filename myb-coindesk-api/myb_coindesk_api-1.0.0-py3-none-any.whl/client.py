import requests
from datetime import datetime


class CurrencyPrice:

    def __init__(self, price_info, index, cryptocurrency, fiat_currency):
        time = price_info.get('time')
        if time:
            updated_at_iso = time.get('updatedISO')
            updated_at = datetime.fromisoformat(updated_at_iso)
            self.updated_at = updated_at.timestamp() * 1000
        self.cryptocurrency = cryptocurrency
        self.fiat_currency = fiat_currency
        self.price = price_info.get(index).get(fiat_currency).get('rate_float')


class CoindeskApi:

    def __init__(self, url='https://api.coindesk.com', fiat_currency='USD', verbose=False):
        self.api_url = url
        self.fiat_currency = fiat_currency
        self._verbose = verbose

    def _request(self, method, api_url, path):
        url = api_url + path

        if self._verbose:
            print(method, url)

        s = requests.Session()
        response = s.request(method, url)

        if response.status_code == 200:
            return response.json()
        elif response.content:
            raise Exception(str(response.status_code) + ": " + response.reason + ": " + str(response.content))
        else:
            raise Exception(str(response.status_code) + ": " + response.reason)

    def _current_price(self, index, cryptocurrency):
        request_result = self._request(
            'GET',
            self.api_url,
            f'/v1/{index}/currentprice/{self.fiat_currency}.json'
        )
        return CurrencyPrice(request_result, index, cryptocurrency, self.fiat_currency)

    def current_price(self, cryptocurrency):
        if cryptocurrency == 'BTC':
            return self._current_price('bpi', cryptocurrency)

        # Other currencies not supported by this client currently
        return None
