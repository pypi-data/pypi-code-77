import persistqueue
import pandas as pd
import time

symbol = "calendar"

q = persistqueue.SQLiteQueue(f'data/{symbol}', auto_commit=False)

start_time = time.time()
data = q.get()
print(("--- %s seconds ---" % (time.time() - start_time)))   
    




# data = pd.DataFrame(data, columns=['date','open', 'high', 'low','close','volume','spread'])
# data =  data.set_index(['date'])
print(data)

