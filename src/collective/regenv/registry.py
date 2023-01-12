from plone import api
from plone.registry import Record
from plone.registry.registry import _Records as _RecordsBase

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
        registry_path = "{}/{}".format(self._portal_path, self._records.__parent__.id)
        logger.debug("get_value %s %s", registry_path, name)
        try:
            return self._overrides[registry_path][name]
        except KeyError:
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
