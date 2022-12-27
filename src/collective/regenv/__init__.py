# -*- coding: utf-8 -*-
from collective.regenv.monkey import apply_plone_registry_monkey
from collective.regenv.monkey import apply_propertymanager_monkey
from zope.i18nmessageid import MessageFactory

import os
import yaml


_ = MessageFactory("collective.regenv")


if os.environ.get("PLONE_REGISTRY_YAML"):
    with open(os.environ.get("PLONE_REGISTRY_YAML")) as fh:
        registry = yaml.safe_load(fh)
    if not isinstance(registry, dict):
        raise ValueError(
            "PLONE_REGISTRY_YAML must point to a YAML file with a dictionary"
        )
    if registry.keys().filter(lambda x: x.endswith("portal_registry")):
        apply_plone_registry_monkey(registry)
    if registry.keys().filter(lambda x: not x.endswith("portal_registry")):
        apply_propertymanager_monkey(registry)
