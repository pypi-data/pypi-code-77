import numpy as np

class BasicJob:
    def __init__(self, df, inputs):
        self.df = df
        self.inputs = inputs
        pass

        ## gets a signal data

    def set(self, name, data, index=None, symbol=None):

        if (data is not None):
            self.df.loc[self.df.index[-1], "session:" + name] = data

        return self.df.loc[self.df.index[-1]]["session:" + name]

    def getOutputCol(self):
        return "result"

    def result(self, resultList, colname=None, fillType="front"):

        if isinstance(resultList, np.ndarray):
            resultList = np.pad(resultList, (self.df.shape[0] - len(resultList), 0), 'constant', constant_values=(np.nan))

        self.df[self.getOutputCol()] = resultList

        return self.df[self.getOutputCol()]

    ## This method adds a signal
    def signal(self, name, data=None, index=-1, symbol=None):

        if ("session:" + name not in self.df.columns):
            self.df["session:" + name] = None

        if (data is not None):
            self.df.loc[self.df.index[index], "session:" + name] = data

        if ("session:" + name in self.df.columns):
            data = self.df.loc[self.df.index[index]]["session:" + name]

        return data

    def getInputValue(self, input):

        if isinstance(input, dict):
            if "value" in input:
                return input["value"]

        return input

    def get(self, name, index=None):

        # if its a key of inputs - lets export the right column
        if name in self.inputs:
            if isinstance(self.inputs[name], str):
                return self.get(self.getInputValue(self.inputs[name]), index)
            if self.inputs[name]["type"] == "dataInput":
                return self.get(self.getInputValue(self.inputs[name]["value"]), index)

        data = None
        if (name + ":y" in self.df.columns):
            data = self.df[name + ":y"]
        elif (name + ":close" in self.df.columns):
            data = self.df[name + ":close"]
        elif ("session:" + name in self.df.columns):
            data = self.df["session:" + name]
        elif (name in self.df.columns):
            data = self.df[name]
        else:
            data = self.inputs[name]

        return data

    def getAsArray(self, name, index=None):

        data = self.get(name, index=index)

        return data.values

    ## This method combines all params and combine as a dataframe
    def df(self):
        return self.df

    ## This method adds a signal
    def var(self, name, data=None, symbol=None):

        if ("session:" + name not in self.df.columns):
            self.df["session:" + name] = None

        index = -1
        if (data is not None):
            self.df.loc[self.df.index[index], "session:" + name] = data
        else:
            index = -2

        if ("session:" + name in self.df.columns):
            data = self.df.loc[self.df.index[index]]["session:" + name]

        return data

