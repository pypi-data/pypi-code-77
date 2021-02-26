#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/1/26 9:28
# @Author: SHAW
# @QQ:838705177
# -----------------------

'''
    dtmanager manage partterns
'''
import asyncio
import logging
import traceback

from tornado.iostream import StreamClosedError

logger = logging.getLogger(__name__)

class DTParserManager(object):

    def __init__(self,eofmethod="read_bytes",*eofargs,**eofkwargs):
        self.EOFARGS = eofargs
        self.EOFKWARGS = eofkwargs
        self.EOFMETHOD = eofmethod
        self._partterns = list()
        self._callback=None

    async def run(self,stream,address):
        try:
            while True:
                data = await getattr(stream,self.EOFMETHOD)(*self.EOFARGS,**self.EOFKWARGS)
                parseddata = self.data_parse(data,stream)
                if asyncio.iscoroutinefunction(self._callback):
                    await self._callback(parseddata)
                elif isinstance(self._callback,callable):
                    self._callback(parseddata)
        except StreamClosedError:
            logger.warning("Lost client at host %s", address)
        except Exception as e:
            traceback.print_exc()
            logger.warning("Exception Occur:%s", e)

    def add_parttern(self,dataparttern):
        self._partterns.append(dataparttern)

    def data_parse(self,data,stream):
        for parttern in self._partterns:
            parseddata = parttern.parse_data(data)
            if parseddata and stream:
                try:
                    parttern.data_callback(parseddata,stream)
                except AttributeError:
                    pass
                return parseddata
        return False

    def add_callback(self,callback=None):
        if callback:self._callback = callback
