from .registry import _marker
from .registry import RecordsProxy
import logging
from OFS.PropertyManager import PropertyManager
from plone.registry import Registry
from plone.registry.registry import Records


logger = logging.getLogger(__name__)


def apply_plone_registry_monkey(overrides):
    def Registry_records(self):
        if isinstance(self._records, Records):
            self._migrateRecords()
        return RecordsProxy(self._records, overrides)

    def Registry_get(self, name, default=None):
        return self.records.get_value(name, default=default)

    def Registry__getitem__(self, name):
        value = self.records.get_value(name, default=_marker)
        if value is _marker:
            raise KeyError(name)
        return value

    Registry.records = property(Registry_records)
    Registry.get = Registry_get
    Registry.__getitem__ = Registry__getitem__

    logger.info("monkey patches for portal_registry applied")


def apply_propertymanager_monkey(overrides):
    # TODO: security decorator
    # @security.protected(access_contents_information)
    def PropertyManager_getProperty(self, id, d=None):
        registry_path = "/".join(self.getPhysicalPath())
        logger.debug("getProperty %s %s %s", self, registry_path, id)
        try:
            return overrides[registry_path][id]
        except KeyError:
            return self._orig_getProperty(id, d)

    # TODO: security decorator
    # @security.protected(access_contents_information)
    # def PropertyManager_propdict(self):
    #     registry_path = "/".join(self.getPhysicalPath())
    #     logger.debug("propdict %s %s", self, self._properties, registry_path)
    #     prop_overrides = overrides.get(registry_path)
    #     dict = {}
    #     for p in self._properties:
    #         dict[p['id']] = p
    #         if prop_overrides and p["id"] in prop_overrides:
    #             p['id']["mode"] = ""
    #     return dict

    # TODO: security decorator
    # @security.protected(access_contents_information)
    def PropertyManager_propertyMap(self):
        """Return a tuple of mappings, giving meta-data for properties.

        Return copies of the real definitions for security.
        """
        # return tuple(dict.copy() for dict in self._propertyMap())
        registry_path = "/".join(self.getPhysicalPath())
        logger.debug("propertyMap %s %s", self, self._properties, registry_path)
        prop_overrides = overrides.get(registry_path)
        pmap = []
        for dict in self._propertyMap():
            p = dict.copy()
            if prop_overrides and p["id"] in prop_overrides:
                p["mode"] = ""
            pmap.append(p)
        return tuple(pmap)

    PropertyManager._orig_getProperty = PropertyManager.getProperty
    PropertyManager.getProperty = PropertyManager_getProperty
    # PropertyManager.propdict = PropertyManager_propdict
    PropertyManager.propertyMap = PropertyManager_propertyMap
    logger.info("monkey patches for PropertyManager applied")
