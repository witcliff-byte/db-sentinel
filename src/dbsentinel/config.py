"""Configuration loading and validation for db-sentinel."""
from pathlib import Path

import yaml


class ConfigError(Exception):
    """Raised when the configuration file is missing or invalid."""


REQUIRED_SECTIONS = ("mysql", "backup")


def load_config(path):
    """Load and validate a YAML config file. Returns a dict.

    Raises ConfigError if the file is missing, malformed, or invalid.
    """
    path = Path(path)
    if not path.exists():
        raise ConfigError(f"Config file not found: {path}")

    try:
        data = yaml.safe_load(path.read_text()) or {}
    except yaml.YAMLError as exc:
        raise ConfigError(f"Invalid YAML in {path}: {exc}") from exc

    for section in REQUIRED_SECTIONS:
        if section not in data:
            raise ConfigError(f"Missing required section: '{section}'")

    retention = data["backup"].get("retention_days", 0)
    if not isinstance(retention, int) or retention < 1:
        raise ConfigError("backup.retention_days must be a positive integer")

    return data
