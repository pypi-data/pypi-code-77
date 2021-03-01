import yahoofinancials as yf 
from enum import Enum

EXCHANGES = {"NasdaqGS": "^IXIC",
            }
    
def get_market_price_list(index_json: dict):
    index_code = list(index_json.keys())[0]
    return index_json[index_code]['prices']

def returns(market_price_list: list):
    start_price = market_price_list[0]['close']
    end_price = market_price_list[-1]['close']
    market_return = (end_price / start_price)
    return market_return

def annualise(market_return: float, period: float):
    return (market_return **(1/period)) - 1
