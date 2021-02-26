#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2020/11/30 16:23
# @Author: SHAW
# @QQ:838705177
# -----------------------
import datetime
import json
import logging
import os

from tornado.options import options

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


def init_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s -%(module)s:%(filename)s-L%(lineno)d-%(levelname)s: %(message)s')
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    logging.info("Current log level is : %s", logging.getLevelName(logger.getEffectiveLevel()))

def killport(port):
    with os.popen('netstat -ano | findstr {}'.format(port)) as taskinfo:
        line = taskinfo.readline()
        aList = line.split()
    pid = aList[4]
    os.popen('taskkill /pid %s /f' % pid)

def test_killport():

    port =options['port']
    killport(port)

if __name__ == '__main__':
    test_killport()