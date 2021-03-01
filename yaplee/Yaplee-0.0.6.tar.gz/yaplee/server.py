import subprocess
import os
import socket
import sys
if(os.name == 'nt'):
    import win32api
    import win32con

class Server:
    def __init__(self, server_port):
        self.server_foldername = 'pages/.server'
        self.port = server_port

    def RemoveDir(self, dir_):
        dir_ = dir_.replace('\\', '/')
        for r,d,f in os.walk(dir_):
            for i in d:
                self.RemoveDir(r+'/'+i)
            for i in f:
                i = i.replace('/', '')
                os.unlink(r+'/'+i)
            for i in d:
                os.rmdir(r+'/'+i)

    def CheckSystem(self):
        a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        local_connection = ('127.0.0.1', self.port)
        CHECK_PORT = a_socket.connect_ex(local_connection)
        a_socket.close()
        if(CHECK_PORT != 0):
            if(os.path.isdir(self.server_foldername)):
                self.RemoveDir(self.server_foldername)
                os.rmdir(self.server_foldername)
            os.mkdir(self.server_foldername)
            if(os.name == 'nt'):
                win32api.SetFileAttributes(self.server_foldername, win32con.FILE_ATTRIBUTE_HIDDEN)
        else:
            print('Server starting error on port '+str(self.port)+', Is the yaplee server started by another file?')
            sys.exit(0)

    def Stop(self):
        if(os.path.isdir(self.server_foldername)):
            self.RemoveDir(self.server_foldername)
            os.rmdir(self.server_foldername)
