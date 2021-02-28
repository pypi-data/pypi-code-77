#!/usr/bin/env python3
# coding=utf-8
# ----------------------------------------------------------------------------------------------------
import sqlite3
from ztools import xls
# ----------------------------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------------------------
# 类 sizeDB
# ----------------------------------------------------------------------------------------------------
# 变更履历：
# 2020-12-30 | Zou Mingzhe   | Ver0.1  | 初始版本
# ----------------------------------------------------------------------------------------------------
# MAP：
# 已测试 | build(self, ...)             | 构建字典
# ----------------------------------------------------------------------------------------------------
class sizeDB(xls):
    """
    sizeDB类，构建尺码编码数据库。
    """
    def __init__(self, path = None):
        self.__version = "0.1"
        self.__size2code = None
        self.__code2size = None
        if path != None:
            self.build(path)
        self.__conn = sqlite3.connect(":memory:")
    def __del__(self):
        self.__conn.close()
# ----------------------------------------------------------------------------------------------------
    def build(self, path):
        """
        构建字典。
        """
        # 读取字典数据
        dict_ibook = self.ReadInfo(path)
        size_isheet = self.ReadObj(path, dict_ibook.index('size'))
        # 建立尺码字典
        self.__size2code = {}
        self.__code2size = {}
        for item in size_isheet[1:]:
            # print(item)
            self.__size2code[item[0]] = item[1]
            self.__code2size[item[1]] = item[0]
        return self.__size2code, self.__code2size
# ----------------------------------------------------------------------------------------------------
    def code(self, size):
        """
        查询字典。
        """
        self.__size2code[size]
# ----------------------------------------------------------------------------------------------------
    def size(self, code):
        """
        查询字典。
        """
        self.__code2size[code]
# ----------------------------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------------------------
# 类 classDB
# ----------------------------------------------------------------------------------------------------
# 变更履历：
# 2020-12-30 | Zou Mingzhe   | Ver0.1  | 初始版本
# ----------------------------------------------------------------------------------------------------
# MAP：
# 已测试 | build(self, ...)             | 构建字典
# ----------------------------------------------------------------------------------------------------
class classDB(xls):
    """
    classDB类，构建分类编码数据库。
    """
    def __init__(self, path = None):
        self.__version = "0.1"
        self.__class2code = None
        self.__code2class1 = None
        self.__code2class2 = None
        if path != None:
            self.build(path)
        self.__conn = sqlite3.connect(":memory:")
    def __del__(self):
        self.__conn.close()
# ----------------------------------------------------------------------------------------------------
    def build(self, path):
        """
        构建字典。
        """
        # 读取字典数据
        dict_ibook = self.ReadInfo(path)
        class_isheet = self.ReadObj(path, dict_ibook.index('supplier'))
        # 建立分类字典
        self.__class2code = {}
        self.__code2class1 = {}
        self.__code2class2 = {}
        for item in class_isheet[1:]:
            # print(item)
            self.__class2code[item[3]] = item[1]
            self.__code2class1[item[1]] = item[2]
            self.__code2class2[item[1]] = item[3]
        return self.__class2code, self.__code2class2
# ----------------------------------------------------------------------------------------------------
    def code(self, class2):
        """
        查询字典。
        """
        self.__class2code[class2]
# ----------------------------------------------------------------------------------------------------
    def class1(self, code):
        """
        查询字典。
        """
        self.__code2class1[code]
# ----------------------------------------------------------------------------------------------------
    def class2(self, code):
        """
        查询字典。
        """
        self.__code2class2[code]
# ----------------------------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------------------------
# 类 supplierDB
# ----------------------------------------------------------------------------------------------------
# 变更履历：
# 2020-12-30 | Zou Mingzhe   | Ver0.1  | 初始版本
# ----------------------------------------------------------------------------------------------------
# MAP：
# 已测试 | build(self, ...)             | 构建字典
# ----------------------------------------------------------------------------------------------------
class supplierDB(xls):
    """
    supplierDB类，构建供应商编码数据库。
    """
    def __init__(self, path = None):
        self.__version = "0.1"
        self.__supplier2code = None
        self.__code2supplier = None
        if path != None:
            self.build(path)
        self.__conn = sqlite3.connect(":memory:")
    def __del__(self):
        self.__conn.close()
# ----------------------------------------------------------------------------------------------------
    def build(self, path):
        """
        构建字典。
        """
        # 读取字典数据
        dict_ibook = self.ReadInfo(path)
        supplier_isheet = self.ReadObj(path, dict_ibook.index('supplier'))
        # 建立供应商字典
        self.__supplier2code = {}
        self.__code2supplier = {}
        for item in supplier_isheet[1:]:
            # print(item)
            self.__supplier2code[item[4]] = item[1]
            self.__code2supplier[item[1]] = item[4]
        return self.__supplier2code, self.__code2supplier
# ----------------------------------------------------------------------------------------------------
    def code(self, supplier):
        """
        查询字典。
        """
        self.__supplier2code[supplier]
# ----------------------------------------------------------------------------------------------------
    def supplier(self, code):
        """
        查询字典。
        """
        self.__code2supplier[code]
# ----------------------------------------------------------------------------------------------------


