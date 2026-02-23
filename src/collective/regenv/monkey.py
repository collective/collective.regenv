from collective.regenv.registry import _marker
from collective.regenv.registry import RecordsProxy
from collective.regenv.settings import get_settings
from OFS.PropertyManager import PropertyManager
from plone.registry import Registry
from plone.registry.registry import Records
from typing import Any

import logging


logger = logging.getLogger(__name__)


def apply_plone_registry_monkey(overrides: dict[str, Any]):
    """Apply monkey patches to plone.registry.Registry to support overrides."""

    def records_property(self):
        if isinstance(self._records, Records):
            self._migrateRecords()
        return RecordsProxy(self._records, overrides)

    def registry_get(self, name, default=None):
        return self.records.get_value(name, default=default)

    def registry_getitem(self, name):
        value = self.records.get_value(name, default=_marker)
        if value is _marker:
            raise KeyError(name)
        return value

    Registry.records = property(records_property)
    Registry.get = registry_get
    Registry.__getitem__ = registry_getitem

    logger.info("Monkey patches for portal_registry applied")


def apply_propertymanager_monkey(overrides: dict[str, dict[str, Any]]):
    """Apply monkey patches to OFS.PropertyManager to support overrides."""

    def get_property(self, id, d=None):  # noqa: A002
        property_path = "/".join(self.getPhysicalPath())
        logger.debug(f"getProperty {self} {property_path} {id}")
        try:
            return overrides[property_path][id]
        except KeyError:
            return self._orig_getProperty(id, d)

    def property_map(self):
        """Return a tuple of mappings, giving meta-data for properties.

        Return copies of the real definitions for security.
        """
        # return tuple(dict.copy() for dict in self._propertyMap())
        registry_path = "/".join(self.getPhysicalPath())
        logger.debug("propertyMap %s %s", self, self._properties, registry_path)
        prop_overrides = overrides.get(registry_path)
        pmap = []
        for item in self._propertyMap():
            p = item.copy()
            if prop_overrides and p["id"] in prop_overrides:
                p["mode"] = ""
            pmap.append(p)
        return tuple(pmap)

    if not hasattr(PropertyManager, "_orig_getProperty"):
        # Avoid applying the monkey patch multiple times,
        # which would cause infinite recursion
        original_getProperty = PropertyManager.getProperty
        PropertyManager._orig_getProperty = original_getProperty
        PropertyManager.getProperty = get_property
        PropertyManager.propertyMap = property_map
        logger.info("Monkey patches for PropertyManager applied")


def initialize():
    """Initialize monkey patches."""
    settings = get_settings()
    apply_plone_registry_monkey(settings.registry_overrides)
    apply_propertymanager_monkey(settings.property_overrides)
