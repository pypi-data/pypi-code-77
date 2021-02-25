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
from nomad_pilot_cli.models.dimension import Dimension  # noqa: E501
from nomad_pilot_cli.rest import ApiException

class TestDimension(unittest.TestCase):
    """Dimension unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Dimension
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = nomad_pilot_cli.models.dimension.Dimension()  # noqa: E501
        if include_optional :
            return Dimension(
                weight = 1.337, 
                height = 1.337, 
                length = 1.337, 
                width = 1.337
            )
        else :
            return Dimension(
        )

    def testDimension(self):
        """Test Dimension"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
