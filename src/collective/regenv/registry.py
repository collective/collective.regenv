from BTrees.OOBTree import OOBTree
from plone import api
from plone.registry import Record
from plone.registry.registry import _Records as _RecordsBase
from typing import Any

import logging


logger = logging.getLogger(__name__)
_marker = object()


class RecordsProxy(_RecordsBase):
    """Proxy for plone.registry Records that allows overriding values from a dict."""

    def __init__(self, _records: _RecordsBase, overrides: dict[str, Any]):
        self._records = _records
        self._overrides = overrides
        self._portal_path: str = "/".join(api.portal.get().getPhysicalPath())

    @property
    def _values(self) -> OOBTree:
        return self._records._values

    @property
    def _fields(self) -> OOBTree:
        return self._records._fields

    def get_value_from_overrides(self, name: str) -> Any:
        """Get value from overrides dict, or return _marker if not found."""
        parent_path = self._records.__parent__.id
        registry_path = f"{self._portal_path}/{parent_path}"
        logger.debug(f"Get_value {registry_path} {name}")
        try:
            return self._overrides[registry_path][name]
        except KeyError:
            return _marker

    def get_value(self, name: str, default: Any = None) -> Any:
        value = self.get_value_from_overrides(name)
        return (
            value if value is not _marker else self._records._values.get(name, default)
        )

    def __getitem__(self, name: str) -> Record:
        value = self.get_value_from_overrides(name)
        record = self._records.__getitem__(name)
        if value is not _marker:
            # XXX: il field qui dovrebbe diventare readonly?
            record = Record(record.field, value, _validate=False)
            record.__name__ = name
            record.__parent__ = self._records.__parent__
        return record
