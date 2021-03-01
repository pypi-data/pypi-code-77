import unittest
from pathlib import Path
import json

from quantifin.util import markets


class TestCase(unittest.TestCase):
    def setUp(self):
        #self.stock = Stock("AAPL")
        self.base_path = Path(__file__).parent
        self.index_json = self.read_json(str(self.base_path) + "/resource/market_price.json")
    
    def read_json(self, file_path):
        with open (file_path) as f:
            json_dict = json.load(f)
        return json_dict

    def test_get_market_price_list(self):
        index_price_list = markets.get_market_price_list(self.index_json)
        index_code = list(self.index_json.keys())[0]
        self.assertEqual(index_price_list, self.index_json[index_code]['prices']) 


    def test_get_market_return(self):
        annual_return = 13597.9658203125  / 7729.31982421875

        index_price_list = markets.get_market_price_list(self.index_json)
        self.assertAlmostEqual(markets.returns(index_price_list), annual_return, 3)
    
    def test_get_annualised_market_return(self):
        market_returns = markets.returns(markets.get_market_price_list(self.index_json))
        annualised_return = markets.annualise(market_returns, 2)
        self.assertEqual(annualised_return, (((13597.9658203125  / 7729.31982421875) ** (1/2)) - 1))
        

