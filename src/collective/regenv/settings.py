from collective.regenv import logger
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Any

import os
import yaml


VAR_PATH = "PLONE_REGISTRY_YAML"
VAR_CONTENT = "PLONE_REGISTRY_YAML_CONTENT"


@dataclass
class Settings:
    """Settings dataclass."""

    registry_overrides: dict[str, dict[str, Any]] = field(default_factory=dict)
    property_overrides: dict[str, dict[str, Any]] = field(default_factory=dict)

    @property
    def all_paths(self) -> set[str]:
        """Get all paths from settings."""
        return set(self.registry_overrides.keys()) | set(self.property_overrides.keys())


def _load_yaml(path_from_env: str) -> dict[str, Any]:
    """Load YAML from environment variables."""
    data = {}
    path = Path(path_from_env)
    if path.is_file() and path.exists():
        with path.open() as fh:
            data = yaml.safe_load(fh)
    return data


def prepare_settings(raw_settings: dict[str, Any]) -> Settings:
    """Filter settings."""
    registry_overrides = {}
    property_overrides = {}
    for registry_path, overrides in raw_settings.items():
        group = (
            registry_overrides
            if registry_path.endswith("portal_registry")
            else property_overrides
        )
        group[registry_path] = overrides

    return Settings(
        registry_overrides=registry_overrides,
        property_overrides=property_overrides,
    )


def _sanity_check_settings(settings: dict[str, Any]) -> bool:
    """Sanity check settings."""
    if not isinstance(settings, dict):
        logger.error(
            "PLONE_REGISTRY_YAML must point to a YAML file with a dictionary. "
            "Alternatively PLONE_REGISTRY_YAML_CONTENT must have a dictionary "
            "in YAML format"
        )
        return False
    return True


def get_settings() -> Settings:
    """Get settings from environment variables."""
    settings = Settings()
    raw_settings = {}
    if path := os.environ.get(VAR_PATH):
        raw_settings = _load_yaml(path)
    elif raw_data := os.environ.get(VAR_CONTENT):
        raw_settings = yaml.safe_load(raw_data)
    if raw_settings and _sanity_check_settings(raw_settings):
        settings = prepare_settings(raw_settings)
    else:
        logger.info("No valid settings found in environment variables")
        settings = Settings()
    return settings
