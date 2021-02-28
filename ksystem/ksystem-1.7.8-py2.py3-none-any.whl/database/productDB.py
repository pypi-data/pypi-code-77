#!/usr/bin/env python3
# coding=utf-8
# ----------------------------------------------------------------------------------------------------
import sqlite3
from ztools import xls
# ----------------------------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------------------------
# 类 productDB
# ----------------------------------------------------------------------------------------------------
# 变更履历：
# 2020-12-30 | Zou Mingzhe   | Ver0.1  | 初始版本
# ----------------------------------------------------------------------------------------------------
# MAP：
# 已测试 | Version(self, ...)           | 版本显示
# ----------------------------------------------------------------------------------------------------
class productDB(xls):
    """
    productDB类，构建商品数据库。
    """
    def __init__(self, path = None):
        self.__version = "0.1"
        self.__info = None
        self.__dict = None
        if path != None:
            self.build(path)
        self.__conn = sqlite3.connect(":memory:")
    def __del__(self):
        self.__conn.close()
# ----------------------------------------------------------------------------------------------------
    def build(self, path):
        """
        构建商品数据库。
        """
        # 读取字典数据
        data_ibook = self.ReadInfo(path)
        data_isheet = self.ReadObj(path, 0)
        # 建立商品数据库
        # print('商品数据库建立中...')
        self.__info = {}
        for item in data_isheet[1:]:
            rec = dict(zip(data_isheet[0], item))
            self.__info[rec['条码']] = rec
            # print(rec)
        # print('商品数据库建立完毕！')
        return self.__info
# ----------------------------------------------------------------------------------------------------
    def search(self, key, value = None):
        """
        搜索商品数据库。
        """
        if value != None:
            ret = []
            for item in self.__info:
                rec = self.__info[item]
                if rec[key] == value:
                    ret.append(rec)
            return ret
        else:
            return self.__info[key]
# ----------------------------------------------------------------------------------------------------
