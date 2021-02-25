#oding = utf-8
# -*- coding:utf-8 -*-
import flask, json
from flask import request
class easyapi():
    def __init__(self, name):
        self.web = flask.Flask(name)
    def service_init(self):
        self.service=self.web.route
    def getvalue(self,key):
        return request.values.get(key)
    def run(self,host:str="0.0.0.0",port:int=18888,debug:bool=False):
        self.web.run(debug=debug,port = port,host=host)