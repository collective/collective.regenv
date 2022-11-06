from collective.regenv.monkey import apply_plone_registry_monkey
from collective.regenv.testing import COLLECTIVE_REGISTRY_INTEGRATION_TESTING
from plone import api

import unittest


class TestBugs(unittest.TestCase):
    layer = COLLECTIVE_REGISTRY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]

    def test_registry_override(self):
        self.assertEqual(api.portal.get_registry_record("plone.smtp_host"), "localhost")

        apply_plone_registry_monkey(
            {
                "/{}/portal_registry".format(self.portal.getId()): {
                    "plone.smtp_host": "smtp.example.org",
                }
            }
        )
        self.assertEqual(
            api.portal.get_registry_record("plone.smtp_host"), "smtp.example.org"
        )
