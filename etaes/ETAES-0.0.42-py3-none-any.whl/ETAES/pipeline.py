#! /usr/bin/python3
# -*- coding: utf-8 -*- 
# @File     :pipeline.py
# @Time     :2021/2/1
# @Author   :jiawei.li
# @Software :PyCharm
# @Desc     :None

class Pipeline(object):
    def __init__(self, components, kwargs):
        # self.temp_item = temp_item
        self.components = components
        self.kwargs = kwargs

    def set_init_item(self, init_item):
        self.temp_item = init_item

    def excute(self):
        if self.temp_item is not None:
            temp_item = self.temp_item
            for component in self.components:
                temp_item = component(self.kwargs, temp_item).excute()
            return temp_item
        else:
            return None
