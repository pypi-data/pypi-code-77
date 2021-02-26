#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/1/26 9:28
# @Author: SHAW
# @QQ:838705177
# -----------------------

'''
    One parser has many rules(rule for parsing)
'''

import logging
from .dtrule import ParserMixin

logger = logging.getLogger(__name__)

class DTParser(object):
    def __init__(self,rules):
        assert isinstance(rules, (list, tuple, ParserMixin,)), "Rule must be list,tuple,DTRule,DTRegxRule"
        self._rules = rules

    def parse(self,data,callback=None):
        tmpdict=dict()
        for rule in self._rules:
            if rule.flag:
                rule.data2dict(data,tmpdict)
        if callback:
            callback(tmpdict)
        return tmpdict

