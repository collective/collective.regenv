from collections.abc import Generator
from collective.regenv.testing import FUNCTIONAL_TESTING
from collective.regenv.testing import INTEGRATION_TESTING
from pathlib import Path
from Products.CMFPlone.Portal import PloneSite
from pytest import MonkeyPatch
from pytest_plone import fixtures_factory
from zope.component.hooks import setSite

import pytest


pytest_plugins = ["pytest_plone"]


globals().update(
    fixtures_factory((
        (FUNCTIONAL_TESTING, "functional"),
        (INTEGRATION_TESTING, "integration"),
    ))
)


@pytest.fixture(scope="session")
def regenv_yaml_factory(pytestconfig):
    """Fixture for the path to the YAML file with test data."""

    def factory(filename: str = "tests-01.yaml") -> Path:
        root_dir = Path(pytestconfig.rootdir)
        return root_dir / "tests" / "_resources" / filename

    return factory


@pytest.fixture(scope="session")
def regenv_yaml_path(regenv_yaml_factory) -> Path:
    """Fixture for the path to the YAML file with test data."""
    return regenv_yaml_factory("tests-01.yaml")


@pytest.fixture(scope="session")
def regenv_yaml_contents(regenv_yaml_factory) -> str:
    """Fixture for the contents of the YAML file with test data."""
    path = regenv_yaml_factory("tests-02.yaml")
    return path.read_text()


@pytest.fixture(scope="class")
def portal_factory(integration_class):
    """Fixture for class-based tests."""
    from collective.regenv.monkey import initialize

    def factory(
        env_var: str = "", env_value: str = ""
    ) -> Generator[PloneSite, None, None]:
        if hasattr(integration_class, "testSetUp"):
            integration_class.testSetUp()
        with MonkeyPatch.context() as mp:
            portal = integration_class["portal"]
            setSite(portal)
            if env_var and env_value:
                mp.setenv(env_var, env_value)
            # Always initialize monkey patches,
            # as the test may rely on them even if no overrides are provided
            initialize()
            yield portal
        if hasattr(integration_class, "testTearDown"):
            integration_class.testTearDown()

    return factory


@pytest.fixture(scope="class")
def portal(portal_factory):
    """Fixture for class-based tests."""

    yield from portal_factory()


@pytest.fixture(scope="class")
def portal_from_file(portal_factory, regenv_yaml_path):
    """Fixture for class-based tests."""
    from collective.regenv.settings import VAR_PATH

    yield from portal_factory(VAR_PATH, str(regenv_yaml_path))


@pytest.fixture(scope="class")
def portal_from_env(portal_factory, regenv_yaml_contents):
    """Fixture for class-based tests."""
    from collective.regenv.settings import VAR_CONTENT

    yield from portal_factory(VAR_CONTENT, regenv_yaml_contents)
