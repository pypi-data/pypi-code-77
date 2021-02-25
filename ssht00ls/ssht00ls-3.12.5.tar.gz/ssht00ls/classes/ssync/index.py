#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import os, cl1, syst3m, sys
from fil3s import *
from r3sponse import r3sponse

# index.
def index(path):
	indexed, dir, ids = Dictionary(path=False, dictionary={}), Files.Directory(path=path), []
	for _path_ in dir.paths(recursive=True, files_only=True, banned=[gfp.clean(f"{path}/Icon\r")], banned_names=[".DS_Store", "__pycache__"]):
		if _path_ not in ids and "/__pycache__/" not in _path_ and "/.DS_Store" not in _path_: 
			indexed[_path_] = gfp.mtime(path=_path_, format="seconds")
			ids.append(_path_)
	for _path_ in dir.paths(recursive=True, dirs_only=True, banned=[gfp.clean(f"{path}/Icon\r")], banned_names=[".DS_Store", "__pycache__"]):
		id = _path_+" (d)"
		if os.listdir(_path_) == []: id += " (e)"
		if id not in ids and "/__pycache__/" not in _path_ and "/.DS_Store" not in _path_: 
			indexed[id] = gfp.mtime(path=_path_, format="seconds")
			ids.append(id)
	return indexed.sort(alphabetical=True)

# main.
if __name__ == "__main__":

	# arguments.
	path = cl1.get_argument("--path")
	json = cl1.arguments_present(["--json", "-j"])

	# checks.
	if not Files.exists(path):
		r3sponse.log(response=r3sponse.error(f"Path [{path}] does not exist."), json=json)
	elif not os.path.isdir(path):
		r3sponse.log(response=r3sponse.error(f"Path [{path}] is not a directory."), json=json)

	# handler.
	dict = index(path)
	r3sponse.log(json=json, response=r3sponse.success(f"Successfully indexed {len(dict)} files from directory [{path}].", {
		"index":dict,
	}))