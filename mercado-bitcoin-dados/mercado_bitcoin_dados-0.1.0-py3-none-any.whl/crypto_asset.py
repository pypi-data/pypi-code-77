"""Module that 

Module wich specifies the supporte currenccies for 'mercado bitcoin api'
"""
from enum import Enum


class CryptoAsset(Enum):
    """Crypto Asset Representation
    """
    
    ASRFT = ('ASRFT' , 'Fan Token ASR')
    ATMFT = ('ATMFT' , 'Fan Token ATM')
    BCH = ('BCH' , 'Bitcoin Cash')
    BTC = ('BTC' , 'Bitcoin')
    CAIFT = ('CAIFT' , 'Fan Token CAI')
    CHZ = ('CHZ' , 'Chiliz')
    ETH = ('ETH' , 'Ethereum')
    GALFT = ('GALFT' , 'Fan Token GAL')
    IMOB01 = ('IMOB01' , 'None')
    JUVFT = ('JUVFT' , 'Fan Token JUV')
    LINK = ('LINK' , 'CHAINLINK')
    LTC = ('LTC' , 'Litecoin')
    MBCONS01 = ('MBCONS01' , 'Cota de Consórcio 01')
    MBCONS02 = ('MBCONS02' , 'Cota de Consórcio 02')
    MBFP01 = ('MBFP01' , 'None')
    MBPRK01 = ('MBPRK01' , 'Precatório MB SP01')
    MBPRK02 = ('MBPRK02' , 'Precatório MB SP02')
    MBPRK03 = ('MBPRK03' , 'Precatório MB BR03')
    MBPRK04 = ('MBPRK04' , 'Precatório MB RJ04')
    MBVASCO01 = ('MBVASCO01' , 'MBVASCO01')
    MCO2 = ('MCO2' , 'MCO2')
    PAXG = ('PAXG' , 'PAX Gold')
    PSGFT = ('PSGFT' , 'Fan Token PSG')
    USDC = ('USDC' , 'USD Coin')
    WBX = ('WBX' , 'WiBX')
    XRP = ('XRP' , 'XRP')
    def __init__(self, code:str, description:str):
        """Create a Crypto Asset 

        Args:
            code (str): Mercado Bitcoin Representation of the crypto asset
            description (str): Descriton of the crypto asset
        """        
        self.code = code      
        self.description = description   