import pandas as pd
import numpy as np

from coinlib.BasicJob import BasicJob

class StatisticRuleJob(BasicJob):
    #, name, group, inputs, df, indicator, worker
    def __init__(self, df, inputs, statisticId, worker):
        super(StatisticRuleJob, self).__init__(df, inputs)
        self.statisticId = statisticId
        self.worker = worker
        self.result_col = None

        pass

    def getOutputCol(self):
        return "r_"+self.statisticId

    def getResultColumns(self):
        return self.result_col

    def result(self, resultList, colname=None, fillType="front"):
        ret = super().result(resultList, colname, fillType)

        self.result_col = ret.to_numpy()

        return self.result_col
