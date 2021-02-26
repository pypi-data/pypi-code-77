#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/1/25 16:24
# @Author: SHAW
# @QQ:838705177
# -----------------------
from tornado.tcpserver import TCPServer

class DTCloudTcpServer(TCPServer):


    def __init__(self,dpm,*args,**kwargs):
        self.dpm = dpm
        super(DTCloudTcpServer, self).__init__(*args,**kwargs)

    async def handle_stream(self, stream, address):
        await self.dpm.run(stream, address)

