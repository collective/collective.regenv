from collective.regenv.browser import browser
from collective.regenv.browser.browser import COLLECTIVE_REGENV_ACKNOWLEDGED
from collective.regenv.browser.browser import RegenvViewlet
from plone import api

import pytest


@pytest.fixture
def patch_registry(monkeypatch):
    """Fixture to patch the registry for testing."""

    def factory(paths: set[str]):
        def mocked():
            return paths

        monkeypatch.setattr(browser, "_all_paths", mocked)

    return factory


class TestRegenvViewlet:
    @pytest.fixture(autouse=True)
    def setup(self, portal, integration_class):
        self.portal = portal
        self.portal_path = "/".join(self.portal.getPhysicalPath())
        self.request = integration_class["request"]
        self.viewlet = RegenvViewlet(self.portal, self.request, None, None)

    def test_viewlet_no_overrides(self):
        assert self.viewlet.available() is False

    def test_viewlet_with_unrelated_overrides(self, patch_registry):
        patch_registry({"/other-site"})
        assert self.viewlet.available() is False

    def test_viewlet_with_overrides(self, patch_registry):
        patch_registry({"/other-site", self.portal_path})
        assert self.viewlet.available() is True

    def test_viewlet_with_overrides_but_cookie_active(self, patch_registry):
        patch_registry({"/other-site", self.portal_path})
        assert self.viewlet.available() is True
        # Set cookie
        self.request.cookies[COLLECTIVE_REGENV_ACKNOWLEDGED] = "true"
        assert self.viewlet.available() is False

    def test_view_that_sets_the_cookie(self, patch_registry):
        # There is a view that can be used cookie to disable the viewlet
        view = api.content.get_view(
            "acknowledge_collective_regenv",
            self.portal,
            self.request,
        )
        view()
        cookie = self.request.response.cookies[COLLECTIVE_REGENV_ACKNOWLEDGED]
        assert cookie["value"] == "true"
        assert cookie["Max-Age"] == "604800"
