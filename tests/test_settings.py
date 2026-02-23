from collective.regenv import settings
from pytest import MonkeyPatch

import pytest


@pytest.mark.parametrize(
    "filename,expected",
    [
        ["tests-01.yaml", True],
        ["tests-02.yaml", True],
        ["wrong-name.yaml", False],
    ],
)
def test__load_yaml(regenv_yaml_factory, filename: str, expected: bool):
    """Test _load_yaml."""
    path = regenv_yaml_factory(filename)
    data = settings._load_yaml(path)
    assert isinstance(data, dict)
    assert ("/plone/portal_registry" in data) is expected


def test_prepare_settings(regenv_yaml_path):
    """Test _load_yaml."""
    raw_data = settings._load_yaml(regenv_yaml_path)
    result = settings.prepare_settings(raw_data)
    assert isinstance(result, settings.Settings)
    assert isinstance(result.registry_overrides, dict)
    registry_path = "/plone/portal_registry"
    assert registry_path in result.registry_overrides
    assert (
        result.registry_overrides[registry_path]["plone.site_title"]
        == "Novo site Plone"
    )
    assert isinstance(result.property_overrides, dict)


@pytest.mark.parametrize(
    "value,expected",
    [
        [{"key": "value"}, True],
        ["not a dict", False],
        [[], False],
    ],
)
def test__sanity_check_settings(value: dict | list | str, expected: bool):
    """Test _sanity_check_settings."""
    assert settings._sanity_check_settings(value) is expected


@pytest.mark.parametrize(
    "env_vars,expected,site_title",
    [
        [[settings.VAR_PATH], True, "Novo site Plone"],
        [[settings.VAR_CONTENT], True, "New Plone Site"],
        [
            [settings.VAR_PATH, settings.VAR_CONTENT],
            True,
            "Novo site Plone",
        ],
        [[], False, None],
    ],
)
def test_get_settings(
    regenv_yaml_path,
    regenv_yaml_contents,
    env_vars: list[str],
    expected: bool,
    site_title: str | None,
):
    """Test get_settings."""
    with MonkeyPatch.context() as mp:
        for env_var in env_vars:
            env_value = (
                regenv_yaml_path
                if env_var == settings.VAR_PATH
                else regenv_yaml_contents
            )
            mp.setenv(env_var, env_value)
        result = settings.get_settings()
        assert isinstance(result, settings.Settings)
        registry_path = "/plone/portal_registry"
        result_registry_overrides = result.registry_overrides.get(registry_path, {})
        plone_site_title = result_registry_overrides.get("plone.site_title")
        assert (plone_site_title is not None) is expected
        assert plone_site_title == site_title
