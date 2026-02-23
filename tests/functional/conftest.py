from collections.abc import Generator
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.restapi.testing import RelativeSession
from Products.CMFPlone.Portal import PloneSite
from pytest import MonkeyPatch
from urllib3 import request
from zope.component.hooks import setSite

import pytest


@pytest.fixture(scope="class")
def portal_f_factory(functional_class):
    """Fixture for class-based tests."""
    from collective.regenv.monkey import initialize

    def factory(
        env_var: str = "", env_value: str = ""
    ) -> Generator[PloneSite, None, None]:
        if hasattr(functional_class, "testSetUp"):
            functional_class.testSetUp()
        with MonkeyPatch.context() as mp:
            portal = functional_class["portal"]
            setSite(portal)
            if env_var and env_value:
                mp.setenv(env_var, env_value)
            # Always initialize monkey patches,
            # as the test may rely on them even if no overrides are provided
            initialize()
            yield portal
            if env_var:
                mp.delenv(env_var)
        if hasattr(functional_class, "testTearDown"):
            functional_class.testTearDown()

    return factory


@pytest.fixture(scope="class")
def portal_f(portal_f_factory):
    """Fixture for class-based tests."""

    yield from portal_f_factory()


@pytest.fixture(scope="class")
def portal_f_from_file(portal_f_factory, regenv_yaml_path):
    """Fixture for class-based tests."""
    from collective.regenv.settings import VAR_PATH

    yield from portal_f_factory(VAR_PATH, str(regenv_yaml_path))


@pytest.fixture(scope="class")
def portal_f_from_env(portal_f_factory, regenv_yaml_contents):
    """Fixture for class-based tests."""
    from collective.regenv.settings import VAR_CONTENT

    yield from portal_f_factory(VAR_CONTENT, regenv_yaml_contents)


@pytest.fixture()
def request_api_factory():
    def factory(portal):
        url = portal.absolute_url()
        api_session = RelativeSession(f"{url}/++api++")
        request.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        return api_session

    return factory
