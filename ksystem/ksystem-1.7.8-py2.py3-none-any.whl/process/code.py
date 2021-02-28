#!/usr/bin/env python3
# coding=utf-8



# ----------------------------------------------------------------------------------------------------
# 类 code
# ----------------------------------------------------------------------------------------------------
# 变更履历：
# 2020-12-30 | Zou Mingzhe   | Ver0.1  | 初始版本
# ----------------------------------------------------------------------------------------------------
# MAP：
# 已测试 | Version(self, ...)           | 版本显示
# ----------------------------------------------------------------------------------------------------
from ztools  import xls
# ----------------------------------------------------------------------------------------------------
class code(xls):
    """
    code类，信息编码处理。
    """
    def __init__(self, format):
        self.__version = "0.1"
        self.__format = format
        self.__dict = None
# ----------------------------------------------------------------------------------------------------
    def get_format(self):
        return self.__format
# ----------------------------------------------------------------------------------------------------
    def get_dict(self):
        return self.__dict
# ----------------------------------------------------------------------------------------------------
    def build(self, path):
        """
        构建字典。
        """
        # 读取字典数据
        dict_ibook = self.ReadInfo(path)
        size_isheet = self.ReadObj(path, dict_ibook.index('size'))
        class_isheet = self.ReadObj(path, dict_ibook.index('class'))
        # 建立字典
        info = {}
        # 建立尺寸字典
        size = {}
        for i in range(len(size_isheet)):
            size[size_isheet[i][0]] = size_isheet[i][1]
        # 建立分类字典
        code = {}
        class1 = {}
        class2 = {}
        supplier = {}
        class_to_code = {}
        supplier_to_code = {}
        for i in range(len(class_isheet)):
            code[class_isheet[i][0]] = class_isheet[i][1]
            class2[class_isheet[i][0]] = class_isheet[i][2]
            class1[class_isheet[i][0]] = class_isheet[i][3]
            supplier[class_isheet[i][0]] = class_isheet[i][4]
            class_to_code[class_isheet[i][2]] = class_isheet[i][0]
            supplier_to_code[class_isheet[i][4]] = class_isheet[i][0]
        # 合并字典
        self.__dict = {}
        self.__dict['size'] = size
        self.__dict['code'] = code
        self.__dict['class1'] = class1
        self.__dict['class2'] = class2
        self.__dict['supplier'] = supplier
        self.__dict['class_to_code'] = class_to_code
        self.__dict['supplier_to_code'] = supplier_to_code
        return self.__dict
# ----------------------------------------------------------------------------------------------------
    def barcode(self, supplier, article, size):
        """
        生成条码。
        """
        prefix = self.__dict['code'][supplier]
        suffix = self.__dict['size'][size]
        return prefix + article + suffix
# ----------------------------------------------------------------------------------------------------
    def encode(self, inf):
        """
        信息编码。
        """
        ret = dict.fromkeys(self.__format, None)
        # 编码固定数据
        ret['颜色'] = '-'
        ret['积分商品'] = '是'
        ret['会员折扣'] = '是'
        ret['库存上限'] = 100
        ret['库存下限'] = 0
        ret['拼音码'] = ''
        ret['商品状态'] = '启用'
        ret['商品描述'] = ''
        # 编码输入数据
        ret['条码'] = self.barcode(inf['分类'], inf['货号'], inf['尺码'])
        ret['供货商'] = self.__dict['supplier'][inf['分类']]
        for key in inf:
            if key == '价格':
                ret['进货价（必填）'] = inf['价格']
                ret['销售价（必填）'] = inf['价格']
                ret['批发价'] = inf['价格']
                ret['会员价'] = inf['价格']
            elif key == '名称':
                name = inf['名称']
                if ((name == None) or (name == "")):
                    name = self.__dict['code'][inf['分类']] + inf['货号']
                ret['名称（必填）'] = name
            elif key == '分类':
                ret['分类（必填）'] = inf['分类']
            elif key == '数量':
                ret['库存量（必填）'] = inf['数量']
            elif key == '补货':
                continue
            else:
                ret[key] = inf[key]
        # print(ret)
        if list(ret.keys()) != self.__format:
            print('error')
            return None
        return ret
# ----------------------------------------------------------------------------------------------------
