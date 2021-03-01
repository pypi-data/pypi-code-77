# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from pst.restapi.testing import PST_RESTAPI_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that pst.restapi is properly installed."""

    layer = PST_RESTAPI_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if pst.restapi is installed."""
        self.assertTrue(self.installer.isProductInstalled("pst.restapi"))

    def test_browserlayer(self):
        """Test that IPstRestapiLayer is registered."""
        from pst.restapi.interfaces import IPstRestapiLayer
        from plone.browserlayer import utils

        self.assertIn(IPstRestapiLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = PST_RESTAPI_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = api.portal.get_tool("portal_quickinstaller")
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstallProducts(["pst.restapi"])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if pst.restapi is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled("pst.restapi"))

    def test_browserlayer_removed(self):
        """Test that IPstRestapiLayer is removed."""
        from pst.restapi.interfaces import IPstRestapiLayer
        from plone.browserlayer import utils

        self.assertNotIn(IPstRestapiLayer, utils.registered_layers())
