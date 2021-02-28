class Side:
    BUY = 'BUY'
    SELL = 'SELL'


class TimeInForce:
    GTC = 'GTC'  # Good Til Cancel (default value on BTSE)
    IOC = 'IOC'  # Immediate or Cancel
    FIVEMIN = 'FIVEMIN'  # 5 mins
    HOUR = 'HOUR'  # 1 hour
    TWELVEHOUR = 'TWELVEHOUR'  # 12 hours
    DAY = 'DAY'  # 1 day
    WEEK = 'WEEK'  # 1 week
    MONTH = 'MONTH'  # 1 month


class OrderType:
    LIMIT = 'LIMIT'
    MARKET = 'MARKET'
    OCO = 'OCO'


class TxType:
    LIMIT = 'LIMIT'  # default value on BTSE
    STOP = 'STOP'  # Stop Loss Orders
    TRIGGER = 'TRIGGER'  # Take Profit orders

