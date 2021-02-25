# coding: utf-8

"""
    Nomad Pilot

    This is the API descriptor for the Nomad Pilot API, responsible for shipping and logistics processing. Developed by [Samarkand Global](https://www.samarkand.global/) in partnership with [SF Express](https://www.sf-express.com/), [eSinotrans](http://air.esinotrans.com/), [sto](http://sto-express.co.uk/). Read the documentation online at [Nomad API Suite](https://api.samarkand.io/). - Install for node with `npm install nomad_pilot_cli` - Install for python with `pip install nomad-pilot-cli` - Install for Maven users `groupId, com.gitlab.samarkand-nomad; artifactId, nomad-pilot-cli`  # noqa: E501

    The version of the OpenAPI document: 1.37.0
    Contact: paul@samarkand.global
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import nomad_pilot_cli
from nomad_pilot_cli.models.package_item import PackageItem  # noqa: E501
from nomad_pilot_cli.rest import ApiException

class TestPackageItem(unittest.TestCase):
    """PackageItem unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test PackageItem
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = nomad_pilot_cli.models.package_item.PackageItem()  # noqa: E501
        if include_optional :
            return PackageItem(
                name = '0', 
                name_cn = '测试', 
                barcode = '0', 
                sku_number = 'SMK123', 
                quantity = 7, 
                price = 21.3, 
                brand = '0', 
                quantity_uom = '50G', 
                hs_code = '0', 
                country_of_origin = '0', 
                goldjet = nomad_pilot_cli.models.goldjet.Goldjet(
                    goods_ptcode = '0', ), 
                gross_weight = 1.337, 
                net_weight = 1.337, 
                customs_unit_code = '142, 007, 瓶, ...', 
                customs_unit_code_package = '142, 011, 140', 
                customs_unit_code_weight = '035', 
                customs_filing_id = '0', 
                spec = '25mm', 
                model = 'iPhone XR', 
                ingredients = '发酵乳杆菌Lc40（CECT5716），麦芽糊精，蔗糖，抗坏血酸钠', 
                customs_unit_code_cn = '瓶', 
                country_of_origin_iso = 'RU'
            )
        else :
            return PackageItem(
        )

    def testPackageItem(self):
        """Test PackageItem"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
