# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import pst.restapi


class PstRestapiLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)
        self.loadZCML(package=pst.restapi)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "pst.restapi:default")


PST_RESTAPI_FIXTURE = PstRestapiLayer()


PST_RESTAPI_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PST_RESTAPI_FIXTURE,), name="PstRestapiLayer:IntegrationTesting"
)


PST_RESTAPI_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PST_RESTAPI_FIXTURE,), name="PstRestapiLayer:FunctionalTesting"
)


PST_RESTAPI_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(PST_RESTAPI_FIXTURE, REMOTE_LIBRARY_BUNDLE_FIXTURE, z2.ZSERVER_FIXTURE),
    name="PstRestapiLayer:AcceptanceTesting",
)
