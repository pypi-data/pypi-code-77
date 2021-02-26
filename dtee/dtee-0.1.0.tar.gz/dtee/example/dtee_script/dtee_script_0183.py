#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/1/26 18:34
# @Author: SHAW
# @QQ:838705177
# -----------------------

from dtee.dtrule import DTKeyRule, DTParserRule, DTParserRegxRule

# Is using this script
FLAG = True

# flag rule
keyrules = (
    DTKeyRule(2, 6, '0183'),
)

# parse rule
parserules = (
    DTParserRule(2,6,"MLZ"),
    DTParserRegxRule(r'QN=(?P<QN>.*?);'),
    DTParserRegxRule(r'PW=(?P<PW>.*?);'),
    DTParserRegxRule(r'SN=(?P<SN>.*?);'),
    DTParserRegxRule(r'Flag=(?P<Flag>.*?);'),
    DTParserRegxRule(r'DataTime=(?P<DataTime>.*?)&&'),
)

# callback
def partternback(data,stream):
    print("partternback 0183:",data)