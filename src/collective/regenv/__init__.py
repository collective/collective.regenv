# -*- coding: utf-8 -*-
from collective.regenv.monkey import apply_plone_registry_monkey
from collective.regenv.monkey import apply_propertymanager_monkey
from zope.i18nmessageid import MessageFactory

import os
import yaml


_ = MessageFactory("collective.regenv")


registry = None

if os.environ.get("PLONE_REGISTRY_YAML"):
    with open(os.environ.get("PLONE_REGISTRY_YAML")) as fh:
        registry = yaml.safe_load(fh)

elif os.environ.get("PLONE_REGISTRY_YAML_CONTENT"):
    registry = yaml.safe_load(os.environ.get("PLONE_REGISTRY_YAML_CONTENT"))

if registry is not None:
    if not isinstance(registry, dict):
        raise ValueError(
            "PLONE_REGISTRY_YAML must point to a YAML file with a dictionary. Alternatively PLONE_REGISTRY_YAML_CONTENT must have a dictionary in YAML format"
        )
    if list(filter(lambda x: x.endswith("portal_registry"), registry.keys())):
        apply_plone_registry_monkey(registry)
    if list(filter(lambda x: not x.endswith("portal_registry"), registry.keys())):
        apply_propertymanager_monkey(registry)
