import json
import logging
import socket

import requests
from requests.api import get

from btse_futures.auth import ApiKey, create_authentication_headers
from btse_futures.order import OpenOrder, Order, OrderResponseV21
from btse_futures.position import Position
from btse_futures.wallet import Wallet

PATH_ROOT = '/api/v2.1'

# create logger
logger = logging.getLogger("btse-futures")
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s")

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
# Get User wallet


class RestClient:
    def __init__(self, apikey: ApiKey, btse_url: str) -> None:
        self.apikey = apikey
        self.btse_url = btse_url

    def get_user_wallet(self):
        path = f'{PATH_ROOT}/user/wallet'
        body = ''
        r = requests.get(self.btse_url + path,
                         headers=create_authentication_headers(self.apikey, path, body))
        data = r.json()
        logger.debug(f'get_user_wallet => {data}')
        wallets = [Wallet.from_dict(wallet) for wallet in data]
        return wallets

    def set_leverage(self, symbol, leverage):
        path = f'{PATH_ROOT}/leverage'
        body = {
            'symbol': symbol,
            'leverage': leverage
        }
        r = requests.post(
            self.btse_url + path, json=body, headers=create_authentication_headers(self.apikey, path, json.dumps(body)))
        data = r.json()
        logger.debug(data)

    def create_order(self, order: Order):
        path = f'{PATH_ROOT}/order'
        r = requests.post(self.btse_url + path, json=order.__dict__,
                          headers=create_authentication_headers(self.apikey, path, order.to_json()))
        data = r.text
        logger.debug(f'created orders: {data}')
        #created_orders = [OrderResponseV21.from_dict(created_order) for created_order in data]
        return data

    def get_open_orders(self):
        path = f'{PATH_ROOT}/user/open_orders'
        body = ''
        r = requests.get(
            self.btse_url + path, headers=create_authentication_headers(self.apikey, path, body))
        data = r.json()
        open_orders = [OpenOrder.from_dict(oo) for oo in data]
        return open_orders

    def get_open_positions(self):
        path = f'{PATH_ROOT}/user/positions'
        body = ''
        r = requests.get(self.btse_url + path,
                         headers=create_authentication_headers(self.apikey, path, body))
        data = r.json()
        positions = [Position.from_dict(position) for position in data]
        return positions

    def cancel_order(self, order_id, symbol, client_order_id=None):
        # TODO: implement a way to reconcile using client_order_id
        order_cancel_params = {
            'orderID': order_id,
            'symbol': symbol
        }
        path = f'{PATH_ROOT}/order'
        r = requests.delete(self.btse_url + path, params=order_cancel_params,
                            headers=create_authentication_headers(self.apikey, path, ''))
        data = r.json()
        return OrderResponseV21.from_dict(data)

    def cancel_all_orders(self, symbol: str):
        """
        Cancel all orders for a market.

        Parameters
        ----------
        symbol : str
            Symbol representing the market

        Returns
        -------
        List of cancelled orders
        """
        order_cancel_params = {
            'symbol': symbol
        }
        path = f'{PATH_ROOT}/order'
        r = requests.delete(self.btse_url + path, params=order_cancel_params,
                            headers=create_authentication_headers(self.apikey, path, ''))
        logger.debug(
            f'status code: {r.status_code}, response: {r.json()}')
        if r.status_code == 200:
            data = r.json()
            cancelled_orders_response = [OrderResponseV21.from_dict(
                cancelled_order_response) for cancelled_order_response in data]
            return cancelled_orders_response
        else:
            return r.json()
