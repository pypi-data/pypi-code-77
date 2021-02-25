#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : shcedule_demo
# @Time         : 2021/2/25 4:15 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 


import schedule
from meutils.pipe import *
from meutils.log_utils import logger4feishu


def func(packages="meutils ", pip='pip'):
    """

    :param packages: 开个分割
    :param pip:
    :return:
    """
    cmd = f"""
    {pip} install -U --no-cache-dir -i https://mirror.baidu.com/pypi/simple {packages} 
    && {pip} install -U --no-cache-dir -i https://pypi.python.org/pypi {packages}
    """

    status, output = magic_cmd(cmd)
    output = output | xjoin
    if 'Successfully installed' in output:
        update_info = output.split()[-1]
        logger4feishu('CM镜像更新', f"更新内容: {update_info}")


schedule.every(10).minute.do(func)

if __name__ == '__main__':

    while True:
        schedule.run_pending()
