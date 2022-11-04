from plone import api
from plone.registry import Record, Registry
from plone.registry.registry import _Records as _RecordsBase
from plone.registry.registry import Records  # BBB

import logging


logger = logging.getLogger(__name__)
_marker = object()


class RecordsProxy(_RecordsBase):
    def __init__(self, _records, overrides):
        self._records = _records
        self._overrides = overrides
        self._portal_path = "/".join(api.portal.get().getPhysicalPath())

    @property
    def _values(self):
        return self._records._values

    @property
    def _fields(self):
        return self._records._fields

    def get_value_from_overrides(self, name):
        registry_path = f"{self._portal_path}/{self._records.__parent__.id}"
        if registry_path in self._overrides:
            if name in self._overrides[registry_path]:
                return self._overrides[registry_path][name]
        return _marker

    def get_value(self, name, default=None):
        value = self.get_value_from_overrides(name)
        return (
            value if value is not _marker else self._records._values.get(name, default)
        )

    def __getitem__(self, name):
        value = self.get_value_from_overrides(name)
        record = self._records.__getitem__(name)
        if value is not _marker:
            # XXX: il field qui dovrebbe diventare readonly?
            record = Record(record.field, value, _validate=False)
            record.__name__ = name
            record.__parent__ = self._records.__parent__
        return record


def apply_plone_registry_monkey(override):
    def Registry_records(self):
        if isinstance(self._records, Records):
            self._migrateRecords()
        return RecordsProxy(self._records, override)

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

    logger.info("monkey patches applied")
