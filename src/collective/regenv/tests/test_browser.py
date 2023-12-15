from collective.regenv.browser import COLLECTIVE_REGENV_ACKNOWLEDGED
from collective.regenv.browser import RegenvViewlet
from collective.regenv.testing import COLLECTIVE_REGISTRY_INTEGRATION_TESTING
from plone import api
from unittest import mock

import unittest


class TestBrowser(unittest.TestCase):
    layer = COLLECTIVE_REGISTRY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.viewlet = RegenvViewlet(self.portal, self.request, None, None)

    def test_viewlet_no_overrides(self):
        self.assertFalse(self.viewlet.available(), False)

    def test_viewlet_with_unrelated_overrides(self):
        with mock.patch(
            "collective.regenv.browser.registry",
            {"/other-site": {"foo": "bar"}},
        ):
            self.assertFalse(self.viewlet.available())

    def test_viewlet_with_overrides(self):
        with mock.patch(
            "collective.regenv.browser.registry",
            {"/".join(self.portal.getPhysicalPath()): {"foo": "bar"}},
        ):
            self.assertTrue(self.viewlet.available())

    def test_viewlet_with_overrides_but_cookie_active(self):
        with mock.patch(
            "collective.regenv.browser.registry",
            {"/".join(self.portal.getPhysicalPath()): {"foo": "bar"}},
        ):
            self.assertTrue(self.viewlet.available())

            self.request.cookies[COLLECTIVE_REGENV_ACKNOWLEDGED] = "true"

            self.assertFalse(self.viewlet.available())

    def test_view_that_sets_the_cookie(self):
        # There is a view that can be used cookie to disable the viewlet
        view = api.content.get_view(
            "acknowledge_collective_regenv",
            self.portal,
            self.request,
        )
        view()
        self.assertTrue(self.request.response.cookies[COLLECTIVE_REGENV_ACKNOWLEDGED])
