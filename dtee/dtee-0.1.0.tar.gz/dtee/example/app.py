#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2020//24 16:04
# @Author: SHAW
# @QQ:838705177
# -----------------------
from tornado.options import options
from tornado.ioloop import IOLoop
import logging

from config import *
from server import DTCloudTcpServer
from tools import init_logging
from dtee_script.dtee_main import dtparsermanager

async def handle_data(data):
    '''manager callback'''
    print("handle_data data:",data)

dtparsermanager.add_callback(handle_data)

def main():
    init_logging()
    logging.info("Start listening，port:%s", options.port)
    server = DTCloudTcpServer(dtparsermanager)
    server.listen(options.port)
    server.start()
    IOLoop.current().start()

if __name__ == '__main__':
    main()

