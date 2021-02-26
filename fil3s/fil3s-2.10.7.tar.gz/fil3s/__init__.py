#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from fil3s.classes.defaults import Files,Formats,Code,gfp,gdate

# shortcuts.
FilePath = Formats.FilePath 
String = Formats.String 
Boolean = Formats.Boolean 
Integer = Formats.Integer 
Date = Formats.Date
File = Files.File
Directory = Files.Directory
Zip = Files.Zip
Image = Files.Image
Bytes = Files.Bytes
Dictionary = Files.Dictionary
Array = Files.Array
Script = Code.Script
Python = Code.Python

# version.
import fil3s
try: version = int(fil3s.Files.load(fil3s.gfp.base(__file__)+".version.py").replace("\n","").replace(" ",""))
except: version = None