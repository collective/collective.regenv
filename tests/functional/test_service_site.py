import pytest


class TestSiteEndpointNoOverrides:
    @pytest.fixture(autouse=True)
    def _setup(self, request_api_factory, portal_f):
        self.api_session = request_api_factory(portal_f)

    @pytest.mark.parametrize(
        "key,expected",
        [
            ("plone.site_title", "Plone site"),
            ("plone.default_language", "en"),
            ("plone.available_languages", ["en"]),
        ],
    )
    def test_response_type(self, key, expected):
        response = self.api_session.get("/@site")
        data = response.json()
        assert isinstance(data, dict)
        assert data[key] == expected


class TestSiteEndpointWithOverridesFromFile:
    @pytest.fixture(autouse=True)
    def _setup(self, request_api_factory, portal_f_from_file):
        self.api_session = request_api_factory(portal_f_from_file)

    @pytest.mark.parametrize(
        "key,expected",
        [
            ("plone.site_title", "Novo site Plone"),
            ("plone.default_language", "pt-br"),
            ("plone.available_languages", ["pt-br", "es", "it"]),
        ],
    )
    def test_response_type(self, key, expected):
        response = self.api_session.get("/@site")
        data = response.json()
        assert isinstance(data, dict)
        assert data[key] == expected


class TestSiteEndpointWithOverridesFromEnv:
    @pytest.fixture(autouse=True)
    def _setup(self, request_api_factory, portal_f_from_env):
        self.api_session = request_api_factory(portal_f_from_env)

    @pytest.mark.parametrize(
        "key,expected",
        [
            ("plone.site_title", "New Plone Site"),
            ("plone.default_language", "eu"),
            ("plone.available_languages", ["eu", "de"]),
        ],
    )
    def test_response_type(self, key, expected):
        response = self.api_session.get("/@site")
        data = response.json()
        assert isinstance(data, dict)
        assert data[key] == expected
