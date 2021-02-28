import json


class Wallet:
    """
    [
        {
            "trackingID": 0,
            "queryType": 0,
            "activeWalletName": "string",
            "wallet": "CROSS@",
            "username": "string",
            "walletTotalValue": 0,
            "totalValue": 100,
            "marginBalance": 100,
            "availableBalance": 100,
            "unrealisedProfitLoss": 0,
            "maintenanceMargin": 0,
            "leverage": 0,
            "openMargin": 0,
            "assets": [
                {
                    "balance": 0.20183537,
                    "assetPrice": 7158.844999999999,
                    "currency": "BTC"
                }
            ],
            "assetsInUse": [
                {
                    "balance": 0.01,
                    "assetPrice": 7158.844999999999,
                    "currency": "BTC"
                }
            ]
        }
    ]
    https://www.btse.com/apiexplorer/futures/#tocs_walletresponse
    """

    def __init__(self) -> None:
        self.trackingID = 0
        self.queryType = 0
        self.activeWalletName = ''
        self.wallet = ''
        self.username = ''
        self.walletTotalValue = 0
        self.totalValue = 0
        self.marginBalance = 0
        self. availableBalance = 0
        self.unrealisedProfitLoss = 0
        self.maintenanceMargin = 0
        self.leverage = 0
        self.openMargin = 0
        self.assets = []
        self.assetsInUse = []

    @staticmethod
    def from_dict(data):
        wallet = Wallet()
        wallet.trackingID = data.get('trackingID')
        wallet.queryType = data.get('queryType')
        wallet.activeWalletName = data.get('activeWalletName')
        wallet.wallet = data.get('wallet')
        wallet.username = data.get('username')
        wallet.walletTotalValue = data.get('walletTotalValue')
        wallet.totalValue = data.get('totalValue')
        wallet.marginBalance = data.get('marginBalance')
        wallet.availableBalance = data.get('availableBalance')
        wallet.unrealisedProfitLoss = data.get('unrealisedProfitLoss')
        wallet.maintenanceMargin = data.get('maintenanceMargin')
        wallet.leverage = data.get('leverage')
        wallet.openMargin = data.get('openMargin')
        wallet.assets = [Asset.from_dict(data)
                         for data in data.get('assets')]
        wallet.assetsInUse = [Asset.from_dict(
            data) for data in data.get('assetsInUse')]
        return wallet

    def __str__(self):
        exclusion_list = ['assets', 'assetsInUse']
        _string = ', '.join(
            [f'{k} : {v}' for k, v in self.__dict__.items() if k not in exclusion_list])
        _string = _string + '\n assets =>' + ', '.join([f'{str(asset)}' for asset in self.assets]) + '\n assetsInUse =>' + ', '.join([
            str(assetsInUse) for assetsInUse in self.assetsInUse])
        return _string


class Asset:
    """
    {
        "balance": 0.20183537,
        "assetPrice": 7158.844999999999,
        "currency": "BTC"
    }
    https://www.btse.com/apiexplorer/futures/#tocs_customizewalletobj
    """

    def __init__(self) -> None:
        self.balance = 0
        self.assetPrice = 0
        self.currency = ''

    def from_dict(data):
        asset = Asset()
        asset.balance = data.get('balance')
        asset.assetPrice = data.get('assetPrice')
        asset.currency = data.get('currency')
        return asset

    def __str__(self):
        return ', '.join([f'{k} : {v}' for k, v in self.__dict__.items()])
