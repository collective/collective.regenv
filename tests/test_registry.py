from plone import api

import pytest


PARAMETRIZE_TESTS = {
    "base": [
        ("plone.site_title", "Plone site"),
        ("plone.default_language", "en"),
        ("plone.available_languages", ["en"]),
    ],
    "yaml_path": [
        ("plone.site_title", "Novo site Plone"),
        ("plone.default_language", "pt-br"),
        ("plone.available_languages", ["pt-br", "es", "it"]),
    ],
    "yaml_from_var": [
        ("plone.site_title", "New Plone Site"),
        ("plone.default_language", "eu"),
        ("plone.available_languages", ["eu", "de"]),
    ],
}


class TestRegistryNoOverrides:
    @pytest.fixture(autouse=True)
    def setup(self, portal):
        self.portal = portal
        self.registry = self.portal.portal_registry

    @pytest.mark.parametrize(
        "key,expected_value",
        PARAMETRIZE_TESTS["base"],
    )
    def test_registry_overrides(self, key: str, expected_value: str | list[str]):
        """Test registry overrides."""
        assert api.portal.get_registry_record(key) == expected_value

    @pytest.mark.parametrize(
        "key,expected_value",
        PARAMETRIZE_TESTS["base"],
    )
    def test_registry_get_item(self, key: str, expected_value: str | list[str]):
        """Test registry __getitem__."""
        assert self.portal.portal_registry[key] == expected_value

    def test_registry_get_item_keyerror(self):
        """Test registry __getitem__."""
        with pytest.raises(KeyError) as exc_info:
            self.portal.portal_registry["non.existent.key"]
        assert str(exc_info.value) == "'non.existent.key'"


class TestRegistryYamlPath:
    @pytest.fixture(autouse=True)
    def setup(self, portal_from_file):
        self.portal = portal_from_file
        self.registry = self.portal.portal_registry

    @pytest.mark.parametrize(
        "key,expected_value",
        PARAMETRIZE_TESTS["yaml_path"],
    )
    def test_registry_overrides(self, key: str, expected_value: str | list[str]):
        """Test registry overrides."""
        assert api.portal.get_registry_record(key) == expected_value

    @pytest.mark.parametrize(
        "key,expected_value",
        PARAMETRIZE_TESTS["yaml_path"],
    )
    def test_registry_get_item(self, key: str, expected_value: str | list[str]):
        """Test registry __getitem__."""
        assert self.portal.portal_registry[key] == expected_value

    def test_registry_get_item_keyerror(self):
        """Test registry __getitem__."""
        with pytest.raises(KeyError) as exc_info:
            self.portal.portal_registry["non.existent.key"]
        assert str(exc_info.value) == "'non.existent.key'"


class TestRegistryYamlFromVar:
    @pytest.fixture(autouse=True)
    def setup(self, portal_from_env):
        self.portal = portal_from_env
        self.registry = self.portal.portal_registry

    @pytest.mark.parametrize(
        "key,expected_value",
        PARAMETRIZE_TESTS["yaml_from_var"],
    )
    def test_registry_overrides(self, key: str, expected_value: str | list[str]):
        """Test registry overrides."""
        assert api.portal.get_registry_record(key) == expected_value

    @pytest.mark.parametrize(
        "key,expected_value",
        PARAMETRIZE_TESTS["yaml_from_var"],
    )
    def test_registry_get_item(self, key: str, expected_value: str | list[str]):
        """Test registry __getitem__."""
        assert self.portal.portal_registry[key] == expected_value

    def test_registry_get_item_keyerror(self):
        """Test registry __getitem__."""
        with pytest.raises(KeyError) as exc_info:
            self.portal.portal_registry["non.existent.key"]
        assert str(exc_info.value) == "'non.existent.key'"
