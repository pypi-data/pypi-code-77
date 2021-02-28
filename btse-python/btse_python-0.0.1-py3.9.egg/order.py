import json

from btse_futures.constants import OrderType, Side, TimeInForce


class Order:
    """
    Class to represent a BTSE Order  

    ...

    Attributes
    ----------
    size : int  
        order quantity or size. e.g. 1  
    price : float  
        price. e.g. 7000.0  
    side: str
        order side. BUY or SELL  
    time_in_force: str 
        time the order is in force. Possible options defined in TimeInForce. e.g. GTC  
    symbol: str  
        instrument symbol. e.g. BTCPFC  
    type: str  
        order type. "LIMIT", "MARKET", or "OCO"  
    txType: str  
        transaction type  
    postOnly: bool  
        Is order post only?  
    reduceOnly: bool  
        Is order reduce only?  
    triggerPrice: float
        Trigger price. Relevant only for LIMIT and OCO order types  
    stopPrice: float  
        Stop price.
    trailValue: float  
        Trail value.  
    clOrderId: str  
        User defined order id  
    trigger: str  
        If an order is a stop loss or take profit order, then this parameter determines the trigger price.  
        Available values are: 1. markPrice = Mark Price (Default) and 2. lastPrice = Last transacted Price  

    Documentation: https://www.btse.com/apiexplorer/futures/?shell#tocs_orderformv2  

    """

    def __init__(self, size: int, price: float, side: str, time_in_force: str, symbol: str, type: str, txType: str, postOnly: bool, reduceOnly: bool, triggerPrice: float, stopPrice: float = None, trailValue: float = None, clOrderId: str = None, trigger: str = None) -> None:
        assert(isinstance(size, int))
        assert(isinstance(price, float))
        assert(isinstance(side, str))
        assert(isinstance(time_in_force, str))
        assert(isinstance(symbol, str))
        assert(isinstance(type, str))
        assert(isinstance(postOnly, bool))
        assert(isinstance(reduceOnly, bool))
        assert(isinstance(triggerPrice, float))

        self.size = size
        self.price = price
        self.side = side
        self.time_in_force = time_in_force
        self.symbol = symbol
        self.type = type
        self.txType = txType
        self.postOnly = postOnly
        self.reduceOnly = reduceOnly
        self.triggerPrice = triggerPrice
        self.stopPrice = stopPrice
        self.trailValue = trailValue
        self.clOrderId = clOrderId
        self.trigger = trigger

    @property
    def quantity(self):
        return self.size

    def to_json(self):
        json_string = json.dumps(self.order_without_none_values())
        print(f'json string: {json_string}')
        return json_string

    def order_without_none_values(self):
        order_dict = self.__dict__
        for key, value in list(order_dict.items()):
            if value is None:
                del order_dict[key]
        return order_dict


class OpenOrder:
    """
    open order endpoint response format
    https://www.btse.com/apiexplorer/futures/#tocs_positionrespv2_1

    Example:  
    --------  

    `{
        "orderType": 0,
        "price": 6875,
        "size": 4,
        "side": "BUY",
        "filledSize": 3,
        "orderValue": 20.625,
        "pegPriceMin": 0,
        "pegPriceMax": 0,
        "pegPriceDeviation": 0,
        "cancelDuration": 0,
        "timestamp": 1576661434072,
        "orderID": "string",
        "stealth": 0.2,
        "triggerOrder": true,
        "triggered": true,
        "triggerPrice": 0,
        "triggerOriginalPrice": 0,
        "triggerOrderType": 1001,
        "triggerTrailingStopDeviation": 0,
        "triggerStopPrice": 0,
        "symbol": "string",
        "trailValue": 0,
        "clOrderID": "market001",
        "reduceOnly": true,
        "orderState": "string"
    }`
    """

    def __init__(self) -> None:
        self.orderType = 0
        self.price = 0
        self.size = 0
        self.side = ''
        self.filledSize = 0
        self.orderValue = 0.0
        self.pegPriceMin = 0
        self.pegPriceMax = 0
        self.pegPriceDeviation = 0
        self.cancelDuration = 0
        self.timestamp = 0
        self.orderID = ''
        self.stealth = 0.0
        self.triggerOrder = ''
        self.triggered = ''
        self.triggerPrice = 0
        self.triggerOriginalPrice = 0
        self.triggerOrderType = 0
        self.triggerTrailingStopDeviation = 0
        self.triggerStopPrice = 0
        self.symbol = ''
        self.trailValue = 0
        self.clOrderID = ''
        self.reduceOnly = ''
        self.orderState = ''

    @staticmethod
    def from_dict(data):
        open_order = OpenOrder()
        open_order.orderType = data.get('orderType')
        open_order.price = data.get('price')
        open_order.size = data.get('size')
        open_order.side = data.get('side')
        open_order.filledSize = data.get('filledSize')
        open_order.orderValue = data.get('orderValue')
        open_order.pegPriceMin = data.get('pegPriceMin')
        open_order.pegPriceMax = data.get('pegPriceMax')
        open_order.pegPriceDeviation = data.get('pegPriceDeviation')
        open_order.cancelDuration = data.get('cancelDuration')
        open_order.timestamp = data.get('timestamp')
        open_order.orderID = data.get('orderID')
        open_order.stealth = data.get('stealth')
        open_order.triggerOrder = data.get('triggerOrder')
        open_order.triggered = data.get('triggered')
        open_order.triggerPrice = data.get('triggerPrice')
        open_order.triggerOriginalPrice = data.get('triggerOriginalPrice')
        open_order.triggerOrderType = data.get('triggerOrderType')
        open_order.triggerTrailingStopDeviation = data.get(
            'triggerTrailingStopDeviation')
        open_order.triggerStopPrice = data.get('triggerStopPrice')
        open_order.symbol = data.get('symbol')
        open_order.trailValue = data.get('trailValue')
        open_order.clOrderID = data.get('clOrderID')
        open_order.reduceOnly = data.get('reduceOnly')
        open_order.orderState = data.get('orderState')
        return open_order


class OrderResponseV21:
    """
    Order Response V2.1  
    Documentation -- https://www.btse.com/apiexplorer/futures/?shell#tocs_orderrespv2_1  
    """

    def __init__(self) -> None:
        self.status = 0
        self.symbol = ''
        self.orderType = 0
        self.price = 0.0
        self.side = ''
        self.size = 0
        self.orderID = ''
        self.timestamp = 0
        self.triggerPrice = 0.0
        self.trigger = ''
        self.deviation = 0.0
        self.stealth = 0.0
        self.message = ''
        self.avgFillPrice = 0.0
        self.fillSize = 0.0
        self.clOrderID = ''

    @staticmethod
    def from_dict(data):
        order_response_v21 = OrderResponseV21()
        order_response_v21.status = data.get('status')
        order_response_v21.symbol = data.get('symbol')
        order_response_v21.orderType = data.get('orderType')
        order_response_v21.price = data.get('price')
        order_response_v21.side = data.get('side')
        order_response_v21.size = data.get('size')
        order_response_v21.orderID = data.get('orderID')
        order_response_v21.timestamp = data.get('timestamp')
        order_response_v21.triggerPrice = data.get('triggerPrice')
        order_response_v21.trigger = data.get('trigger')
        order_response_v21.deviation = data.get('deviation')
        order_response_v21.stealth = data.get('stealth')
        order_response_v21.message = data.get('message')
        order_response_v21.avgFillPrice = data.get('avgFillPrice')
        order_response_v21.fillSize = data.get('fillSize')
        order_response_v21.clOrderID = data.get('clOrderID')
        return order_response_v21
