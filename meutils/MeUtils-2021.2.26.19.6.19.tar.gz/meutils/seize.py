#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : seize
# @Time         : 2021/2/26 6:51 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : xgb/lgb 参数https://www.jianshu.com/p/1100e333fcab


from meutils.pipe import *
from xgboost import XGBClassifier
from sklearn.datasets import make_classification


def run(n_estimators=1000000):
    X, y = make_classification(n_estimators)

    clf = XGBClassifier(learning_rate=1/n_estimators, n_estimators=n_estimators, n_jobs=-1)

    try:
        clf.set_params(tree_method='gpu_hist', predictor='gpu_predictor')
    except Exception as e:
        logger.warning(e)


    finally:
        clf.fit(X, y, eval_set=[(X, y), (X, y)], verbose=n_estimators/100)


if __name__ == '__main__':
    with timer('seize'):
        run(100)

