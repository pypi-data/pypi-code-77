
import timeit


class PythonOfflineBacktraderLogic:
    def __init__(self, algo, trader, traderType, pd_dataframe, from_date, to_date, assets, options, process_id, isAWebSocketCall=False):    
        self.algo = algo
        self.trader = trader
        self.assets = assets
        self.percentage = 0
        self.df = pd_dataframe
        self.traderType = traderType
        self.from_date = self.getDateTimeFromISO8601String(from_date)
        self.to_date = self.getDateTimeFromISO8601String(to_date)
        print("from", self.from_date)
        print("to", self.to_date)
        self.lastPercentage = 0
        self.process_id = process_id
        self.isAWebSocketCall = isAWebSocketCall
        self.slidingWindowSize = options["windowSize"]
        pass
    
    
    def getDateTimeFromISO8601String(self, s):
        import datetime
        import dateutil.parser
        d = dateutil.parser.parse(s)
        return d

    def startThread(self):

        # if its async, run as a new thread
        def runAsThread():
            try:
                loop = asyncio.new_event_loop()
                loop.run_until_complete(self.runAllDatas())
            except Exception as e:
                print("Thread Error", e)
                self.onError(e)
                
        thread1 = threading.Thread(target = runAsThread)
        thread1.start()
        
        
        return True
    
    async def runAllDatas(self):
        
        self.sendStartInfo()
        
        try:

            dataframeLength = self.df.shape[0]
            correcTrader = generateCorrectTrader(self.traderType)
            self.charts = correcTrader("", "", "", self.df, {"assets": self.assets, "imIn": False, "imOut": True}, self.process_id)
            index = 0
            for row in self.df.itertuples(index=True, name='Pandas'):

                if (index >= self.slidingWindowSize and row.date > self.from_date):
                    window = self.df[index-self.slidingWindowSize: index]

                    currentDate = self.df["date"][index]
                    beforeImIn = self.charts.imIn()
                    
                    self.charts.currentSlidingIndex = index
                    await self.runAlgo(self.charts)

                    await self.runTrader(self.charts)
                    
                    if (beforeImIn == False and self.charts.imIn() == True):
                        ## changed from out to in safe timestampindex
                        self.charts.setInDate(self.df["date"][index])
                    elif (beforeImIn == True and self.charts.imIn() == False):
                        self.charts.setInDate(None)
                        
                    self.charts.updateInTime(currentDate)
                    
                    self.percentage = index / dataframeLength

                    if (self.percentage - self.lastPercentage > 0.01):
                        self.sendProgressInfo()
                        self.lastPercentage = self.percentage

                index = index + 1

            if (not self.isAWebSocketCall):
                ## calculate the results
                print(self.charts.inputs)

            print("FINISHED")
            self.sendFinished()
            self.onFinished()
            
        except Exception as e:
                print("Thread Error", e)
                self.onError(e)
                
        return True
    
    def getResults(self):
        self.charts.inputs["date"] = self.charts.inputs["date"].apply(lambda x: x.isoformat())
        return {
            'definition': self.charts.definition,
            'data': json.loads(self.charts.inputs.to_json(orient='records')),
            'tradingActions': self.charts.tradingActions
        }
    
    def sendFinished(self):
        if (self.isAWebSocketCall):
            try:
                sendDataMessage({'cmd': "onCallPythonTraderOfflineFinished", 'process_id': self.process_id, 'results': self.getResults()})
            except Exception as e:
                print("## Error in Sending finished trader data", e)
                pass

        return True
    
    def sendErrorInfo(self, error):
        if (self.isAWebSocketCall):
            try:
                sendDataMessage({'cmd': "onCallPythonTraderOfflineErrorOccured", 'process_id': self.process_id, 'error': str(error)})
            except Exception as e:
                print("## Error in Sending started trader data", e)
                pass

        return True
    
    def sendStartInfo(self):
        if (self.isAWebSocketCall):
            try:
                sendDataMessage({'cmd': "onCallPythonTraderOfflineStarted", 'process_id': self.process_id})
            except Exception as e:
                print("## Error in Sending started trader data", e)
                pass

        return True
    
    def sendProgressInfo(self):
        
        process_id = self.process_id
        progress = {"percentage": self.percentage}
        
         # if its async, run as a new thread
        def sendData():
            try:
                sendDataMessage({'cmd': "onCallPythonTraderOfflineProgress", "progress": progress, 'process_id': process_id})
            except Exception as e:
                print("## Error in Sending progress trader data", e)
                pass

            return True
              
        if (self.isAWebSocketCall):  
            thread1 = threading.Thread(target = sendData)
            thread1.start()
        
        return True
    
    async def runAlgo(self, chart):
        
        name = "algo_"+self.algo["name"]
        if (inspect.iscoroutinefunction(traderAlgorithmCallbacks[name]["process"])):
            result = await asyncio.wait([traderAlgorithmCallbacks[name]["process"]( chart)], return_when=asyncio.FIRST_COMPLETED)
        else:
            result = traderAlgorithmCallbacks[name]["process"]( chart)

        return result
    
    async def runTrader(self, chart):
        
        name = "trader_"+self.trader["name"]
        if (inspect.iscoroutinefunction(traderAlgorithmCallbacks[name]["process"])):
            result = await asyncio.wait([traderAlgorithmCallbacks[name]["process"]( chart)], return_when=asyncio.FIRST_COMPLETED)
        else:
            result = traderAlgorithmCallbacks[name]["process"]( chart)

        return result
    
    def onError(self, err):
        global offlineRunningBacktraders
        self.sendErrorInfo(err)
        offlineRunningBacktraders.pop(self.process_id)
        return True
    
    def onFinished(self):
        global offlineRunningBacktraders
        offlineRunningBacktraders.pop(self.process_id)
        return True
    
    def onCanceled(self):
        global offlineRunningBacktraders
        offlineRunningBacktraders.pop(self.process_id)
        return True
    
    
    



def callPythonTraderOffline(algorithms, traders, traderType, dataframe, from_date, to_date, process_id, trader_options=None, websocket=False):
    global offlineRunningBacktraders
    data = dataframe["data"]   
    if ("data" in data):
        data = data["data"]
    assets = dataframe["assets"]   
    algo =  algorithms[0]
    trader =  traders[0]
    options = {"windowSize": 30}
    if (trader_options is not None):
        options = trader_options

    df = pd.DataFrame.from_dict(data)
    df['Datetime'] = pd.to_datetime(df['date'])
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index("Datetime")

    offlineRunningBacktraders[process_id] = PythonOfflineBacktraderLogic(algo, trader, traderType, df, from_date, to_date, assets, options, process_id, websocket!=False)
    offlineRunningBacktraders[process_id].startThread()

    return True
