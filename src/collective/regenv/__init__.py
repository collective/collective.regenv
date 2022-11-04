# -*- coding: utf-8 -*-
from collective.regenv.proxy import apply_plone_registry_monkey
from zope.i18nmessageid import MessageFactory

import os
import yaml


_ = MessageFactory("collective.regenv")


if os.environ.get("PLONE_REGISTRY_YAML"):
    with open(os.environ.get("PLONE_REGISTRY_YAML")) as fh:
        registry = yaml.safe_load(fh)
    apply_plone_registry_monkey(registry)
