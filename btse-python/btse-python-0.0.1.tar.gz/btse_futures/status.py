class Status:
    """
    A class to represent Status.

    ...

    Attributes
    ----------
    code : int
        status code
    message : str
        the message
    description: str
        description

    """

    def __init__(self, code: int, message: str, description: str) -> None:
        self.code = code
        self.message = message
        self.description = description


def get_status_by_code(code) -> Status:
    """
    Returns the status code, message, and description for a given code  

    2: ORDER_INSERTED = Order is inserted successfully  
    6: ORDER_CANCELLED = Order is cancelled successfully  
    4: ORDER_FULLY_TRANSACTED = Order is fully transacted  
    5: ORDER_PARTIALLY_TRANSACTED = Order is partially transacted  
    9: TRIGGER_INSERTED = Trigger Order is inserted successfully  
    10: TRIGGER_ACTIVATED = Trigger Order is activated successfully  
    28: TRANSFER_UNSUCCESSFUL = Transfer funds between spot and futures is unsuccessful  
    27: TRANSFER_SUCCESSFUL = Transfer funds between futures and spot is successful  
    1003: ORDER_LIQUIDATION = Order is undergoing liquidation  
    1004: ORDER_ADL = Order is undergoing ADL  
    64: STATUS_LIQUIDATION = Account is undergoing liquidation  
    12: ERROR_UPDATE_RISK_LIMIT = Error in updating risk limit  
    15: ORDER_REJECTED = Order is rejected  
    16: ORDER_NOTFOUND = Order is not found with the order ID or clOrderID provided  
    41: ERROR_INVALID_RISK_LIMIT = Invalid risk limit was specified  
    8: INSUFFICIENT_BALANCE = Insufficient balance in account  
    101: FUTURES_ORDER_PRICE_OUTSIDE_LIQUIDATION_PRICE = Futures order is outside of liquidation price  
    1: MARKET_UNAVAILABLE = Futures market is unavailable  
    """
    status_map = {
        '2': Status(2, 'ORDER_INSERTED', 'Order is inserted successfully'),
        '6': Status(6, 'ORDER_CANCELLED', 'Order is cancelled successfully'),
        '4': Status(4, 'ORDER_FULLY_TRANSACTED', 'Order is fully transacted'),
        '5': Status(5, 'ORDER_PARTIALLY_TRANSACTED', 'Order is partially transacted'),
        '9': Status(9, 'TRIGGER_INSERTED', 'Trigger Order is inserted successfully'),
        '10': Status(10, 'TRIGGER_ACTIVATED', 'Trigger Order is activated successfully'),
        '28': Status(28, 'TRANSFER_UNSUCCESSFUL', 'Transfer funds between spot and futures is unsuccessful'),
        '27': Status(27, 'TRANSFER_SUCCESSFUL', 'Transfer funds between futures and spot is successful'),
        '1003': Status(1003, 'ORDER_LIQUIDATION', 'Order is undergoing liquidation'),
        '1004': Status(1004, 'ORDER_ADL', 'Order is undergoing ADL'),
        '64': Status('STATUS_LIQUIDATION', 'Account is undergoing liquidation'),
        '12': Status(12, 'ERROR_UPDATE_RISK_LIMIT', 'Error in updating risk limit'),
        '15': Status(15, 'ORDER_REJECTED', 'Order is rejected'),
        '16': Status(16, 'ORDER_NOTFOUND', 'Order is not found with the order ID or clOrderID provided'),
        '41': Status(41, 'ERROR_INVALID_RISK_LIMIT', 'Invalid risk limit was specified'),
        '8': Status(8, 'INSUFFICIENT_BALANCE', 'Insufficient balance in account'),
        '101': Status(101, 'FUTURES_ORDER_PRICE_OUTSIDE_LIQUIDATION_PRICE', 'Futures order is outside of liquidation price'),
        '1': Status(1, 'MARKET_UNAVAILABLE', 'Futures market is unavailable')

    }
    return status_map.get(code)
