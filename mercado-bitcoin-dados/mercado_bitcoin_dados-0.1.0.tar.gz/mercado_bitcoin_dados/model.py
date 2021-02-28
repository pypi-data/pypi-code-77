from dataclasses import dataclass, asdict
from typing import  Iterator, List
from datetime import  date

import pandas as pd
import numpy as np

@dataclass
class DayTradeSummary:
    date: date
    opening: float
    closing: float
    lowest: float
    highest: float
    volume: float
    quantity: float
    amount: float
    avg_price: float

@dataclass
class Ticker:
    open: float
    high: float
    low: float
    vol: float
    last: float
    buy: float
    sell: float
    date: int


class OrderBook:
    COLUMNS = ['price','size']
    def __init__(self, asks : pd.DataFrame, bids: pd.DataFrame) -> None:
        self.asks = asks
        self.bids = bids

    @property
    def asks (self)-> pd.DataFrame:
        return self._asks

    @asks.setter
    def asks(self,asks : pd.DataFrame ):
        self._validate_dataframe(asks)
        self._asks = asks

    @property
    def bids (self) -> pd.DataFrame:
        return self._bids

    @bids.setter
    def bids(self,bids : pd.DataFrame ):
        self._validate_dataframe(bids)
        self._bids = bids

    def _validate_dataframe( self,orders : pd.DataFrame):
        assert isinstance(orders,pd.DataFrame), "orders should be a pandas DataFrame"
        assert orders.columns.isin(self.COLUMNS).all()

    @classmethod
    def from_response(cls, response):
        asks_orders = response.json()['asks']
        bids_orders = response.json()['bids']
        asks = OrderBook.from_orders_list(asks_orders)
        bids = OrderBook.from_orders_list(bids_orders)
        return cls(asks, bids)

    @classmethod
    def from_orders_list(cls, orders: List)-> pd.DataFrame:
        array = np.array(orders)
        return pd.DataFrame(array, columns = cls.COLUMNS)

class Trades (pd.DataFrame):
    TRADE_COLUMNS = ['tid','date','type','price','amount']
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    
    def assert_columns (self):
        assert self.columns.isin(self.TRADE_COLUMNS).all()

    @classmethod
    def from_trades_records(cls, trades: list)-> pd.DataFrame:
        return cls.from_records(trades)


class HistoricData (pd.DataFrame):
    @classmethod
    def from_day_summary(cls, day_summary: DayTradeSummary)-> pd.DataFrame:
        data = asdict(day_summary)
        data.pop('date')
        return cls.from_records(data,index=[day_summary.date])
    @classmethod
    def from_day_summarys(cls, day_summarys: Iterator)-> pd.DataFrame:
        data = [asdict(day_summary) for day_summary in day_summarys ]
        return cls.from_records(data,index='date')
    
    def get_day_summary(self, day: date):
        summary_dict = self.loc[day].to_dict()
        summary_dict['date']= day
        return DayTradeSummary(**summary_dict)