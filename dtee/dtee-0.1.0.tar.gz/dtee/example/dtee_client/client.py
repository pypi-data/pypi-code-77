import datetime

from tornado import ioloop, gen, iostream
from tornado.tcpclient import TCPClient

'''mock local client'''

async def local_request(DATA):
    stream = await TCPClient().connect( host='localhost',port= 8064 )
    try:
        await stream.write(DATA.encode('utf-8'))
    except iostream.StreamClosedError:
        pass

async def main():
    DATA1 = '##0183QN=123;PW=123456;SN=a123456;Flag=5;DataTime=20201203133147&&A000\r\n'

    DATA2 = '##0660QN=321;PW=123456;SN=a123456;Flag=5;DataTime=20201203141923;MsgId=107&&5000\r\n'

    DATA = DATA1
    await local_request(DATA)


if __name__ == '__main__':
    ioloop.IOLoop.current().run_sync( main )
