# -*- coding: utf-8 -*-
from plone.app.testing import FunctionalTesting, IntegrationTesting, PloneSandboxLayer

import collective.regenv


class CollectiveRegistryLayer(PloneSandboxLayer):
    # defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.regenv)


COLLECTIVE_REGISTRY_FIXTURE = CollectiveRegistryLayer()


COLLECTIVE_REGISTRY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_REGISTRY_FIXTURE,),
    name="CollectiveRegistryLayer:IntegrationTesting",
)


COLLECTIVE_REGISTRY_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_REGISTRY_FIXTURE,),
    name="CollectiveRegistryLayer:FunctionalTesting",
)
