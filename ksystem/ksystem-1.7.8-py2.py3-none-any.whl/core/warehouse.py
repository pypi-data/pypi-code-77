#!/usr/bin/env python3
# coding=utf-8
# ----------------------------------------------------------------------------------------------------
import sys
from ztools import xls
from ztools import tprint
from ztools import progressbar
from ztools import AnsiStyle as style
from ztools import AnsiFore as fore
from ztools import AnsiBack as back
# ----------------------------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------------------------
# 类 stock
# ----------------------------------------------------------------------------------------------------
# 变更履历：
# 2021-02-21 | Zou Mingzhe   | Ver0.1  | 初始版本
# ----------------------------------------------------------------------------------------------------
# MAP：
# 已测试 | Version(self, ...)           | 版本显示
# ----------------------------------------------------------------------------------------------------
class stock(xls):
    """
    stock类，库存处理。
    """
    def __init__(self, code):
        self.__version = "0.1"
        self.__format = None
        self.__stock = {}
        self.__code = code
# ----------------------------------------------------------------------------------------------------
    def build(self, in_path, show_progress = True):
        """
        读取in_path文件内库存记录并按条码存储。
        """
        # 数据处理
        data_ibook = self.ReadInfo(in_path)
        for idx1 in range(len(data_ibook)):
            data_isheet = self.ReadObj(in_path, idx1)
            # 处理库存格式
            if self.__format == None:
                self.__format = data_isheet[0]
            elif self.__format != data_isheet[0]:
                print("error in %s.%s format %s different %s" % \
                    (self.__class__.__name__, \
                    sys._getframe().f_code.co_name, \
                    self.__format, data_isheet[0]))
                continue
            # 处理库存记录
            if show_progress:
                bar = progressbar()
            length = len(data_isheet) - 1
            for idx2 in range(1, length + 1):
                item = data_isheet[idx2]
                value = dict(zip(self.__format, item))
                barcode = value['条码']
                rec = self.select(barcode)
                if rec == None:
                    self.__stock[barcode] = value
                else:
                    print("error in %s.%s barcode %s exist %s" % \
                        (self.__class__.__name__, \
                        sys._getframe().f_code.co_name, \
                        barcode, str(rec)))
                    continue
                if show_progress:
                    bar.number(idx2, length, title = data_ibook[idx1], show = True)
            if show_progress:
                bar.EOF()
        return self.__stock
# ----------------------------------------------------------------------------------------------------
    def select(self, barcode):
        """
        库存查找，按条码查找库存。
        """
        try:
            # 按条码查找记录
            rec = self.__stock[barcode]
            return rec
        except:
            # 无库存记录返回空
            return None
# ----------------------------------------------------------------------------------------------------
    def insert(self, info):
        """
        库存增加，按条码增加库存。
        """
        try:
            # 按条码查找记录
            rec = self.__stock[barcode]
            # 存在记录返回空
            return None
        except:
            # 无库存记录增加库存
            barcode = "123456"
            rec = "error"
            return rec
# ----------------------------------------------------------------------------------------------------
    def delete(self, barcode):
        """
        库存删除，按条码删除库存。
        """
        try:
            # 按条码查找记录
            rec = self.__stock[barcode]
            # 删除该条记录
            del self.__stock[barcode]
            # 返回被删除记录
            return rec
        except:
            # 无库存记录返回空
            return None
# ----------------------------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------------------------
# 类 entry
# ----------------------------------------------------------------------------------------------------
# 变更履历：
# 2021-01-02 | Zou Mingzhe   | Ver0.1  | 初始版本
# ----------------------------------------------------------------------------------------------------
# MAP：
# 已测试 | Version(self, ...)           | 版本显示
# ----------------------------------------------------------------------------------------------------
class entry(xls):
    """
    entry类，入库处理。
    """
    def __init__(self, code, stock):
        self.__version = "0.1"
        self.__stock = stock
        self.__code = code
        self.__temp = None
# ----------------------------------------------------------------------------------------------------
    def __preprocess_file(self, in_path):
        """
        预处理，将in_path文件内每条记录按尺码展开为多条记录。
        """
        info = [['名称', '分类', '货号', '价格', '补货', '尺码', '数量']]
        # 数据处理
        data_ibook = self.ReadInfo(in_path)
        for idx in range(len(data_ibook)):
            data_isheet = self.ReadObj(in_path, idx)
            for item in data_isheet[1:]:
                for siz in range(6, len(item)):
                    if item[siz] != None and item[siz] != '':
                        rec = []
                        rec.append(item[0])
                        rec.append(item[1])
                        rec.append(item[2])
                        rec.append(item[3])
                        rec.append(item[4])
                        rec.append(data_isheet[0][siz])
                        rec.append(item[siz])
                        info.append(rec)
        return info
# ----------------------------------------------------------------------------------------------------
    def preprocess(self, in_path, out_path):
        """
        预处理，将in_path中指定的文件合并为out_path文件，每个in_path中文件为一个sheet。
        1.in_path文件名作为sheet名
        2.in_path文件内每条记录按尺码展开为多条记录
        """
        name = []
        info = []
        x = type(in_path)
        if not (x is list or x is tuple):
            in_path = [in_path]
        for filepath in in_path:
            # 将in_path文件名作为sheet名
            filename = self.get_name(filepath)
            name.append(filename.split('.')[0])
            # 将in_path文件内每条记录按尺码展开为多条记录
            info.append(self.__preprocess_file(filepath))
        # 数据输出
        self.WriteObjMulti(out_path, name, info)
# ----------------------------------------------------------------------------------------------------
    def check_error(self, keys, values1, values2):
        """
        检查错误。
        """
        tp1 = tprint()
        tp2 = tprint()
        print('check error:')
        for i in range(min(len(values1), len(values2))):
            c = fore.green if (values1[i] == values2[i]) else fore.red
            tp1.color(str(values1[i]) + ' ', c)
            tp2.color(str(values2[i]) + ' ', c)
        tp1.flush()
        tp2.flush()
# ----------------------------------------------------------------------------------------------------
    def check(self, in_path, out_path):
        """
        检查重复，检查是否有重复录入，若有则检查录入信息是否一致，一致则合并，不一致则打印错误。
        """
        einf = [['名称', '分类', '货号', '价格', '补货', '尺码', '数量']]
        info = [['名称', '分类', '货号', '价格', '补货', '尺码', '数量']]
        temp = {}
        # 数据处理
        data_ibook = self.ReadInfo(in_path)
        for idx in range(len(data_ibook)):
            data_isheet = self.ReadObj(in_path, idx)
            for item in data_isheet[1:]:
                #key = item[2] + item[5]
                # 以条码作为key
                key = self.__code.barcode(item[1], item[2], item[5])
                # 检查是否有重复录入？
                try:
                    # 有重复录入则录入信息是否一致？
                    error = 0
                    rec = temp[key]
                    if rec[0] != item[0]:
                        error =  error + 1
                    # if rec[1] != item[1]:
                    #     error =  error + 1
                    if rec[3] != item[3]:
                        error =  error + 1
                    
                    if error == 0:
                        item[6] = int(rec[6]) + int(item[6])
                        temp[key] = item
                    else:
                        self.check_error(info[0], item, rec)
                        einf.append(item)
                except:
                    # 无重复录入则录入
                    temp[key] = item
        class_to_code = self.__code.get_dict()['class_to_code']
        # 保存录入信息
        for key in temp:
            value = temp[key]
            # 检查是否有库存商品？
            result = self.__stock.select(key)
            if result != None:
                # 有库存商品则录入信息是否一致？
                error = 0
                res = []
                res.append(result['名称（必填）'])
                res.append(class_to_code[result['分类（必填）']])
                res.append(result['货号'])
                res.append(int(float(result['销售价（必填）'])))
                res.append('')
                res.append(result['尺码'])
                res.append(result['库存量'])
                if value[0] and value[0] != res[0]:
                    error =  error + 1
                if int(float(value[3])) != res[3]:
                    error =  error + 1
                if value[5] != res[5]:
                    error =  error + 1
                
                if error == 0:
                    value[6] = int(res[6]) + int(value[6])
                    info.append(value)
                else:
                    self.check_error(info[0], value, res)
                    einf.append(value)
            else:
                # 无库存商品则录入
                info.append(value)
        self.WriteObjMulti(out_path, ['check', 'error'], [info, einf])
# ----------------------------------------------------------------------------------------------------
    def entry(self, in_path, out_path):
        """
        入库。
        """
        info = [self.__code.get_format()]
        data_ibook = self.ReadInfo(in_path)
        data_isheet = self.ReadObj(in_path, data_ibook.index('check'))
        for item in data_isheet[1:]:
            # 对录入信息进行编码
            rec = self.__code.encode(dict(zip(data_isheet[0], item)))
            info.append(list(rec.values()))
            # print(list(rec.values()))
        self.WriteObj(out_path, 'output', info)
# ----------------------------------------------------------------------------------------------------
