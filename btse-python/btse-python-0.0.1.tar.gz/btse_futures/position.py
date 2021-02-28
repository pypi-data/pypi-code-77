class Position:
    """
    positions endpoint response format  
    https://www.btse.com/apiexplorer/futures/#tocs_positionrespv2_1  
    {
        "marginType": 0,
        "entryPrice": 0,
        "markPrice": 71126.6,
        "symbol": "BTCPFC",
        "side": "BUY",
        "orderValue": 441.8492,
        "settleWithAsset": "BTC",
        "unrealizedProfitLoss": -0.23538014,
        "totalMaintenanceMargin": 2.366912551,
        "size": 62,
        "liquidationPrice": 0,
        "isolatedLeverage": 25,
        "adlScoreBucket": 2,
        "liquidationInProgress": false,
        "timestamp": 1576661434072,
        "currentLeverage": 0
    }
    """

    def __init__(self) -> None:
        self.marginType = 0
        self.entryPrice = 0
        self.markPrice = 0.0
        self.symbol = ''
        self.side = ''
        self.orderValue = 0.0
        self.settleWithAsset = ''
        self.unrealizedProfitLoss = 0.0
        self.totalMaintenanceMargin = 0.0
        self.size = 0
        self.liquidationPrice = 0
        self.isolatedLeverage = 0
        self.adlScoreBucket = 0
        self.liquidationInProgress = ''
        self.timestamp = 0
        self.currentLeverage = 0

    @staticmethod
    def from_dict(data):
        position = Position()
        position.marginType = data.get('marginType')
        position.entryPrice = data.get('entryPrice')
        position.markPrice = data.get('markPrice')
        position.symbol = data.get('symbol')
        position.side = data.get('side')
        position.orderValue = data.get('orderValue')
        position.settleWithAsset = data.get('settleWithAsset')
        position.unrealizedProfitLoss = data.get('unrealizedProfitLoss')
        position.totalMaintenanceMargin = data.get('totalMaintenanceMargin')
        position.size = data.get('size')
        position.liquidationPrice = data.get('liquidationPrice')
        position.isolatedLeverage = data.get('isolatedLeverage')
        position.adlScoreBucket = data.get('adlScoreBucket')
        position.liquidationInProgress = data.get('liquidationInProgress')
        position.timestamp = data.get('timestamp')
        position.currentLeverage = data.get('currentLeverage')
        return position
