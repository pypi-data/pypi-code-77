from quantifin.equity import Stock
from quantifin.util import markets

def CAPM(risk_free: float, market_premium: float, beta: float):
    return risk_free + beta * (market_premium - risk_free)

def gordon_growth_valuation(current_dividend: float, req_rate: float, growth_rate: float):
    if  __any_negative_value([current_dividend, req_rate]):
        raise ValueError("Invalid value. Either current_dividend or required rate is negative")
    return round((current_dividend * (growth_rate + 1)) / (req_rate - growth_rate), 3)

def __any_negative_value(values: list):
    for val in values:
        if val < 0:
             return True
    return False