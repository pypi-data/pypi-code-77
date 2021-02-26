#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/1/26 15:34
# @Author: SHAW
# @QQ:838705177
# -----------------------
import importlib
import os

from dtee.dtparttern import DTParttern
from dtee.dtparser import DTParser
from dtee.dtmanager import DTParserManager

BaseDir = os.path.dirname(__file__)
filename = os.path.basename(__file__)

dtparsermanager = DTParserManager(
    eofmethod="read_bytes",
    num_bytes=1024,
    partial=True)

for file in os.listdir(BaseDir):
    if file != filename and file.startswith('dtee'):
        filename,filenameext = os.path.splitext(file)
        module = importlib.import_module("dtee_script."+filename)
        if module.FLAG:
            keyrules = module.keyrules
            parserules = module.parserules
            partternback = getattr(module,'partternback',None)
            dtparser = DTParser(parserules)
            dtparttern = DTParttern(module.__name__,dtparser,keyrules,partternback)
            dtparsermanager.add_parttern(dtparttern)