import persistqueue
from ejtraderMT import Metatrader
from datetime import date, timedelta
import time
import pandas as pd
import os

start_time = time.time()
api = Metatrader()


active = ['EURUSD','GBPUSD', 'AUDUSD']
timeframe = "M1"


try:
    os.makedirs('data')
except OSError:
    pass


start_date = date(2017, 1, 1)
end_date = date(2021, 1, 1)
delta = timedelta(days=30)
delta2 = timedelta(days=30)

while start_date <= end_date:
    fromDate = start_date.strftime("%d/%m/%Y")
    toDate = start_date
    toDate +=  delta2
    toDate = toDate.strftime("%d/%m/%Y")
    for symbol in active:
        df = api.historyDataFrame(symbol,timeframe,fromDate,toDate)
        df =df.drop(columns={'real_volume'})
        df.isnull().sum().sum() # there are no nans
        df.fillna(method="ffill", inplace=True)
        df = df.loc[~df.index.duplicated(keep = 'first')]
        df = df.dropna()
        df = df.fillna(method="ffill")
        df = df.dropna()
        df.to_csv (f'data/{symbol}.csv',  mode='a', header=False)
        print(f'writing to database... from: {fromDate} to {toDate} symbol: {symbol}')
        start_date += delta
        print('Sleeping 3 sec...')
        time.sleep(3)

         

for symbol in active:
    q = persistqueue.SQLiteQueue(f'data/{symbol}', auto_commit=True)
    df = pd.read_csv(f'data/{symbol}.csv')
    q.put(df)
    # Get directory name
    MODELFILE = f'data/{symbol}.csv'
    try:
        os.remove(MODELFILE)
    except OSError:
        pass

print(("--- %s seconds ---" % (time.time() - start_time)))    



        











