#coding:utf-8
import os

def file_exists(path):
    if not os.path.exists(path):
        return True
    else:
        return False


def file_remove(path):
    os.remove(path)


def create_folder(path):
    os.mkdir(path)
    
def path_get_file_name(path):
    return path.split('\\')[-1]

def file_name_get_suffix_name(fill_name):
    return fill_name.split('.')[-1]