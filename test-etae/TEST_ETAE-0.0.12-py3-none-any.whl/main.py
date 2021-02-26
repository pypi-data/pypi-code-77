#! /usr/bin/python3
# -*- coding: utf-8 -*- 
# @File     :main.py
# @Time     :2021/2/7
# @Author   :jiawei.li
# @Software :PyCharm
# @Desc     :None


# from TEST_ETAE.main import infer
import pandas as pd
import json
import sys
import os
from ETAES.operations import excute_pipeline, build_pipeline, build_configurations

def init(kwargs):
    return build_pipeline(kwargs)

def infer(pipeline, inputs):
    return excute_pipeline(pipeline, inputs)

if __name__ == '__main__':
    _, config_path = sys.argv
    kwargs = build_configurations(config_path)
    print(os.getcwd())

    if kwargs['basic']['status'] == 'online':

        waybills_df = pd.read_csv(f'{os.getcwd()}/TEST_ETAE/data/waybills.csv')
        waybills_df.drop(['Unnamed: 0'], axis=1, inplace=True)
        waybills_str = waybills_df[:3].to_json(orient="records")
        waybills_js = json.loads(waybills_str)


        kwargs['basic']['task_id'] = '1614076401'
        pipeline = init(kwargs)
        result = infer(pipeline, inputs=waybills_js)
    else:
        pipeline = init(kwargs)
        result = infer(pipeline, inputs=None)

    print(result)


    # result = infer()
    # print(result)
