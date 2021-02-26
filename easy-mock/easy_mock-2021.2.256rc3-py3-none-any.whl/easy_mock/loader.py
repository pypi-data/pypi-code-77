# -*- coding: utf-8 -*-
# Created by mcwT <machongwei_vendor@sensetime.com> on 2021/02/25.
import importlib
import os
import sys
import types
from typing import Tuple, Dict, Union, Text, List, Callable

from easy_mock import common


def prepare_path(path):
    if not os.path.exists(path):
        err_msg = f"path not exist: {path}"
        common.log().error(err_msg)
        raise FileNotFoundError(err_msg)

    if not os.path.isabs(path):
        path = os.path.join(os.getcwd(), path)

    return path


def locate_file(start_path: Text, file_name: Text) -> Text:
    """ locate filename and return absolute file path.
        searching will be recursive upward until system root dir.
    """
    if os.path.isfile(start_path):
        start_dir_path = os.path.dirname(start_path)
    elif os.path.isdir(start_path):
        start_dir_path = start_path
    else:
        raise FileNotFoundError(f"invalid path: {start_path}")

    file_path = os.path.join(start_dir_path, file_name)
    if os.path.isfile(file_path):
        # ensure absolute
        return os.path.abspath(file_path)

    # system root dir
    # Windows, e.g. 'E:\\'
    # Linux/Darwin, '/'
    parent_dir = os.path.dirname(start_dir_path)
    if parent_dir == start_dir_path:
        raise FileNotFoundError(f"{file_name} not found in {start_path}")

    # locate recursive upward
    return locate_file(parent_dir, file_name)


def locate_file_list(start_path: Text, name_end: Text) -> List:
    """Find all the files ending with [name_end] params in the folder and return absolute file path.
    """
    if os.path.isdir(start_path):
        start_dir_path = start_path
    else:
        raise FileNotFoundError(f"invalid path: {start_path}")

    # This will return a list of all file names
    file_list = []
    for fn in os.listdir(start_dir_path):
        if fn.endswith(name_end):
            file_list.append(os.path.join(start_path, fn))

    return file_list


def locate_processor_py(start_path: Text) -> Text:
    """ locate processor.py file and return file path
    """
    try:
        processor_path = locate_file(start_path, "processor.py")
    except FileNotFoundError:
        processor_path = None
    return processor_path


def load_module_functions(module) -> Dict[Text, Callable]:
    """ load python module functions.
    """
    module_functions = {}

    for name, item in vars(module).items():
        if isinstance(item, types.FunctionType):
            module_functions[name] = item

    return module_functions


def load_processor_func() -> Dict[Text, Callable]:
    """ load processor.py project module functions
    """
    try:
        from os.path import abspath, join, dirname
        sys.path.insert(0, join(abspath(dirname(__file__)), os.getcwd()))
        imported_module = importlib.import_module("processor")
    except Exception as e:
        common.log().error(f"error occurred in processor.py: {e}")
        sys.exit(1)

    # reload to refresh previously loaded module
    imported_module = importlib.reload(imported_module)
    return load_module_functions(imported_module)
