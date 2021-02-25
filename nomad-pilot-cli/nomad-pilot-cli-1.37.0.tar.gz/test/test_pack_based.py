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
from nomad_pilot_cli.models.pack_based import PackBased  # noqa: E501
from nomad_pilot_cli.rest import ApiException

class TestPackBased(unittest.TestCase):
    """PackBased unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test PackBased
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = nomad_pilot_cli.models.pack_based.PackBased()  # noqa: E501
        if include_optional :
            return PackBased(
                dimension = nomad_pilot_cli.models.dimension.Dimension(
                    weight = 1.337, 
                    height = 1.337, 
                    length = 1.337, 
                    width = 1.337, ), 
                ship_from = nomad_pilot_cli.models.address.Address(
                    first_name = 'John', 
                    last_name = '0', 
                    address1 = '0', 
                    address2 = '0', 
                    county = '0', 
                    city = '0', 
                    state = '0', 
                    country = '0', 
                    zip = '0', 
                    tin = '0', 
                    phone = '0', 
                    country_code = '142', 
                    id_card = '0', 
                    email = '0', 
                    company = '0', 
                    ecommerce_website_user_id = '0', ), 
                ship_to = nomad_pilot_cli.models.address.Address(
                    first_name = 'John', 
                    last_name = '0', 
                    address1 = '0', 
                    address2 = '0', 
                    county = '0', 
                    city = '0', 
                    state = '0', 
                    country = '0', 
                    zip = '0', 
                    tin = '0', 
                    phone = '0', 
                    country_code = '142', 
                    id_card = '0', 
                    email = '0', 
                    company = '0', 
                    ecommerce_website_user_id = '0', ), 
                bill = nomad_pilot_cli.models.address.Address(
                    first_name = 'John', 
                    last_name = '0', 
                    address1 = '0', 
                    address2 = '0', 
                    county = '0', 
                    city = '0', 
                    state = '0', 
                    country = '0', 
                    zip = '0', 
                    tin = '0', 
                    phone = '0', 
                    country_code = '142', 
                    id_card = '0', 
                    email = '0', 
                    company = '0', 
                    ecommerce_website_user_id = '0', ), 
                order_ref = 'SO224571', 
                seller_order_ref = 'E202010152223470377011119610GZ', 
                tracking_reference = 'SF1032566311525', 
                order_time = '0', 
                gross_weight = 1.53, 
                net_weight = 1.53, 
                total_price = 532.8, 
                currency = 'RMB', 
                mass_unit = 'Kilogram', 
                length_unit = 'Centimetre', 
                domestic_delivery_company = 'SF', 
                created_at = '2019-07-12T13:13:52.004637+01:00', 
                updated_at = '2019-07-12T13:13:52.004637+01:00', 
                pay_method = 'EASIPAY', 
                pay_merchant_name = 'Paypal', 
                pay_amount = 611.08, 
                pay_id = '2014030120394812', 
                paid_at = '2019-07-12T13:13:52.004637+01:00', 
                products_total_tax = 53.28, 
                shipping_cost = 25.0, 
                non_cash_deduction_amount = 0.0, 
                customer_note = 'This package is very important.', 
                cancel_reason = 'The customers updated the address.', 
                warehouse_code = '718595286704', 
                customer_id_ref = '0', 
                insurance_fee = 2.5, 
                express_type = 'BC', 
                payment_pay_id = '191028195204000214', 
                platform_name = 'youzan', 
                check_point = '0'
            )
        else :
            return PackBased(
        )

    def testPackBased(self):
        """Test PackBased"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
