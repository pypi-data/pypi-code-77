#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/1/25 16:24
# @Author: SHAW
# @QQ:838705177
# -----------------------
from tornado.options import define

define("port", default=8064, help="TCP port to listen on")