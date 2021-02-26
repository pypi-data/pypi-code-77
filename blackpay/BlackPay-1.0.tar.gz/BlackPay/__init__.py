#!/usr/bin/env python
# -*- coding: utf-8 -*-
from blackpay.wallets import Wallet


class Wallet:
    def __new__(cls, wallet_token=None):
        if public_key:
            return P2PWallet(token=public_key)
        else:
            raise AttributeError('Enter wallet_token or p2p_token')
