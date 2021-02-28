"""Module to extract infomation from api of the exchange 'Mercado Bitcoin'
"""

from typing import Dict, Iterator, List, Tuple
from itertools import repeat
import calendar
from datetime import  date, datetime
from enum import Enum
from pandas.core.frame import DataFrame
from mercado_bitcoin_dados.crypto_asset import CryptoAsset
from mercado_bitcoin_dados.model import (
    DayTradeSummary,
    Ticker,
    Trades,
    HistoricData,
    OrderBook)
import requests as re
import pandas as pd

class APIMethod(Enum):
    """APIMethod Class

    :param Enum: [description]
    :type Enum: [type]
    """      
    TICKER = 'ticker'
    ORDER_BOOK = 'orderbook'
    TRADES = 'trades'
    DAYTRADE = 'day-summary'
    

class MercadoBitcoinData:
    """
    Class to extract infomation from api of the exchange 'Mercado Bitcoin'
    https://www.mercadobitcoin.com.br/api-doc/
    """    
    api_url = 'https://www.mercadobitcoin.net/api'
    def _get_response(self,
            crypto_asset: CryptoAsset,
            api_method: APIMethod,
            path_params: Tuple = None,
            params: Dict  = None)-> re.Response:
        """Get the http response of the API

        :param crypto_asset: Crypto Asset
        :type crypto_asset: CryptoAsset
        :param api_method: API Method
        :type api_method: APIMethod
        :param path_params: Path params, defaults to None
        :type path_params: Tuple, optional
        :param params: Params, defaults to None
        :type params: Dict, optional
        :return: Http Response
        :rtype: re.Response
        """                   
        url_method = api_method.value
        build_url_tuple = (
            self.api_url,
            crypto_asset.code,
            url_method)
        if path_params:
            build_url_tuple += path_params
        url = '/'.join(build_url_tuple) + '/'

        response = re.get(url, params = params)
        response.raise_for_status()
        return response

    def get_response_ticker(self, crypto_asset : CryptoAsset) -> re.Response:
        """Get the ticker of the exchange 

        :param crypto_asset: Crypto Asset
        :type crypto_asset: Crypto Asset
        :return: HTTP response
        :rtype: re.Response
        """        

        return self._get_response(crypto_asset,APIMethod.TICKER)

    def get_ticker(self, crypto_asset : CryptoAsset) -> Ticker:
        """Get the ticker of the exchange of the crypto asset 

        :param crypto_asset: Crypto Asset
        :type crypto_asset: CryptoAsset
        :return: Returns the ticker of the exhange  
        :rtype: Ticker
        """        
        
        response = self.get_response_ticker(crypto_asset)
        return Ticker(**response.json()['ticker'])

    def get_response_orderbook(self, crypto_asset : CryptoAsset) -> re.Response:
        """Get the http response of the crypto asset in the exchange

        :param crypto_asset: Crypto Asset
        :type crypto_asset: CryptoAsset
        :return: Http Response
        :rtype: re.Response
        """        
      
        return self._get_response(crypto_asset,APIMethod.ORDER_BOOK)

    def get_orderbook(self, crypto_asset : CryptoAsset)-> OrderBook:
        """Get the current order book of the exchange

        Args:
            crypto_asset (CryptoAsset): CryptoAsset

        Returns:
            OrderBook: Orderbook
        """        
        response = self.get_response_orderbook(crypto_asset)
        return OrderBook.from_response(response)


    def get_response_trades_since_trade_id(self, crypto_asset : CryptoAsset, trade_id: int)-> re.Response:
        """Get the http response of the trades made in the exchange since the trade id  especified

        Args:
            crypto_asset (CryptoAsset): CryptoAsset
            trade_id (int): Trade id

        Returns:
            re.Response: Http Response
        """        
        params = {'since': trade_id}
        respose = self._get_response(crypto_asset,APIMethod.TRADES, params = params)
        return respose

    def get_trades_since_trade_id(self, crypto_asset : CryptoAsset, trade_id: int)-> DataFrame:
        """Get the trades made in the exchange since the trade id  especified

        Args:
            crypto_asset (CryptoAsset): CryptoAsset
            trade_id (int): Trade id

        Returns:
            DataFrame:  Trades ready to be analytzed through a pandas dataframe
        """        
        reponse = self.get_response_trades_since_trade_id(crypto_asset, trade_id)
        return Trades.from_trades_records(reponse.json())
    
    def get_trades_from(self, crypto_asset : CryptoAsset, from_date: datetime )-> DataFrame:
        """Get the trades from a date specified

        Args:
            crypto_asset (CryptoAsset): CryptoAsset
            from_date (datetime): From Date

        Returns:
            DataFrame: Trades ready to be analytzed through a pandas dataframe
        """        
        reponse = self.get_response_trades_from(crypto_asset, from_date)
        return Trades.from_trades_records(reponse.json())

    def _from_datetime_to_unix(self, from_date: datetime) -> int:
        """Transform a date to a unix timestamp

        Args:
            from_date (datetime): Date to be transformed

        Returns:
            int: Unix TimeStamp
        """        
        unix_timestamp = calendar.timegm(from_date.utctimetuple())
        return unix_timestamp

    def get_response_trades_from(self, crypto_asset : CryptoAsset, from_timestamp: int)-> re.Response:
        """[summary]

        Args:
            crypto_asset (CryptoAsset): [description]
            from_timestamp (int): [description]

        Returns:
            re.Response: [description]
        """        
        path_params =(str(from_timestamp),)
        respose = self._get_response(crypto_asset,APIMethod.TRADES, path_params=path_params)
        return respose

    def get_response_trades_from_to(
            self, 
            crypto_asset : CryptoAsset,
            from_timestamp: int,
            to_timestamp: int )-> re.Response:
        path_params =(str(from_timestamp),str(to_timestamp))
        """Get the trades from a date specified

        Args:
            crypto_asset (CryptoAsset): CryptoAsset
            from_date (datetime): From Date

        Returns:
            DataFrame: Trades ready to be analytzed through a pandas dataframe
        """   
        respose = self._get_response(crypto_asset,APIMethod.TRADES, path_params=path_params)
        return respose
    
    def get_trades_from_to(self, crypto_asset : CryptoAsset, from_date: datetime ,to_date: datetime  )-> DataFrame:
        reponse = self.get_response_trades_from_to(crypto_asset, from_date, to_date)
        return Trades.from_trades_records(reponse.json())

        
    def get_response_day_summary(
            self, 
            crypto_asset : CryptoAsset,
            day: date )-> re.Response:
        """[summary]

        :param crypto_asset: Crypto Asset
        :type crypto_asset: CryptoAsset
        :param day: Day
        :type day: date
        :return: Http Response
        :rtype: re.Response
        """           
        path_params= (str(day.year),str(day.month),str(day.day)) 
        return  self._get_response(crypto_asset,APIMethod.DAYTRADE, path_params=path_params)

    def get_day_summary(
            self, 
            crypto_asset : CryptoAsset,
            day: date )-> DayTradeSummary:
        """ Get Day Summary

        :param crypto_asset: Crypto Asset
        :type crypto_asset: CryptoAsset
        :param day: Day
        :type day: date
        :return: Day Trade Summary
        :rtype: DayTradeSummary
        """            
                       
        response = self.get_response_day_summary(crypto_asset,day)
        json_response = response.json()
        return DayTradeSummary(
                date.fromisoformat(json_response['date']),
                json_response['opening'],
                json_response['closing'],
                json_response['lowest'],
                json_response['highest'],
                json_response['volume'],
                json_response['quantity'],
                json_response['amount'],
                json_response['avg_price']
            )
    
    def _date_range(self, from_date: date, end_date:date)-> Iterator:
        """
        Create a range date from a range of dates

        Args:
            from_date (date): From Date
            end_date (date): To Date

        Returns:
            Iterator:  A date range object
        """        
        return (date.date() for date in pd.date_range(from_date,end_date))
    
    def get_day_summarys(
        self, 
        crypto_asset : CryptoAsset,
        dates: Iterator):
        """Get the days summary according to the input dates

        Args:
            crypto_asset (CryptoAsset): CryptoAsset
            dates (Iterator): dates

        Returns:
            [Iterator(DayTradeSummary)]: Day Summarys
        """        
        return map(
            self.get_day_summary,repeat(crypto_asset),
            dates)
    
    def get_historic_data(
        self,
        crypto_asset : CryptoAsset,
        from_date : date, 
        to_date : date)-> HistoricData:
        """Get the historic trade summary

        Args:
            crypto_asset (CryptoAsset): CryptoAsset
            from_date (date): From Date
            to_date (date): To Date

        Returns:
            HistoricData: Dataframe with the historic trade summary
        """        
        dates = self._date_range(from_date,to_date)
        summarys = self.get_day_summarys(crypto_asset,dates)
        return HistoricData.from_day_summarys(summarys)
