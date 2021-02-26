#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .request import request
from .response import response

class BaseWallet:
    def __init__(self, token):
        self._TOKEN = token

    def _request(self, method, request_url):
        return response(request(method, request_url))


class Wallet(BaseWallet):

    def create_invoice(self):
        method = 'get'
        request_url = f'http://127.0.0.1:5000/generate?public_key='
        return self._request(method, request_url + self._TOKEN)

    def invoice_status(self, bill_id):
        method = 'get'
        request_url = f'http://127.0.0.1:5000/status?id={bill_id}&public_key='
        return self._request(method, request_url + self._TOKEN)