#! /usr/bin/python3
# -*- coding: utf-8 -*- 
# @File     :operations.py
# @Time     :2021/2/1
# @Author   :jiawei.li
# @Software :PyCharm
# @Desc     :None

import os

import ETAES.components as com
from ETAES.components import *
from ETAES.pipeline import Pipeline
from ETAES.utils.builder import build_config, build_paths
from ETAES import TASK_ID
import mlflow


def build_configurations(config_path):
    kwargs = build_config(config_path)
    if kwargs['basic']['status'] == 'offline':
        build_paths(task_id=TASK_ID, configs=kwargs)
        if 'experiment_id' in kwargs['basic'].keys():
            mlflow.set_experiment(str(kwargs['basic']['experiment_id']))
        else:
            mlflow.set_experiment(str(TASK_ID))
            mlflow.log_param('TASK_ID', str(TASK_ID))
    return kwargs


def build_pipeline(kwargs):
    # if js is not None:
    #     kwargs['basic']['js'] = js
    basic_cfg = kwargs['basic']
    if basic_cfg['status'] == 'online':
        # init_item = js
        components = [
            ExampleGen,
            StatisticsGen,
            SchemaGen,
            ExampleValidator,
            Transform,
            Loader,
            Predictor
        ]
    else:
        # init_item = os.path.join(basic_cfg['paths']['file_path'], basic_cfg['names']['file_name'])
        components = [
            ExampleGen,
            StatisticsGen,
            SchemaGen,
            ExampleValidator,
            Transform,
            Trainer,
            Evaluator,
            Pusher,
            Predictor
        ]
    # pipeline = Pipeline(components, kwargs, init_item)
    pipeline = Pipeline(components, kwargs)
    return pipeline


def excute_pipeline(pipeline, js):
    if js is not None:
        pipeline.kwargs['basic']['js'] = js
    else:
        basic_cfg = pipeline.kwargs['basic']
        js = os.path.join(basic_cfg['paths']['file_path'], basic_cfg['names']['file_name'])
    pipeline.set_init_item(js)
    result = pipeline.excute()
    return result




