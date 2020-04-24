#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Build configuration representation."""
import re
import itertools
from dataclasses import dataclass, field, fields
from typing import Any, Dict, List, Optional, Set, Tuple

from mbed_build._internal.config.source import Source


@dataclass
class Option:
    """Representation of configuration option."""

    value: Any
    macro_name: Optional[str]
    help_text: Optional[str]
    set_by: str
    key: str

    @classmethod
    def build(cls, key: str, data: Any, source: Source) -> "Option":
        """Build configuration option from config entry value.

        Config values are either complex data structures or simple values.
        This function handles both.

        Args:
            key: Namespaced configuration key
            data: Configuration data - a dict or a primitive
            source: Source from which option data came from - used for tracing overrides
        """
        if isinstance(data, dict):
            return cls(
                key=key,
                value=data.get("value"),
                macro_name=data.get("macro_name", _build_macro_name(key)),
                help_text=data.get("help"),
                set_by=source.name,
            )
        else:
            return cls(value=data, key=key, macro_name=_build_macro_name(key), help_text=None, set_by=source.name)

    def set_value(self, value: Any, source: Source) -> "Option":
        """Mutate self with new value."""
        self.value = value
        self.set_by = source.name
        return self


def _build_macro_name(config_key: str) -> str:
    """Build macro name for configuration key.

    All configuration variables require a macro name, so that they can be referenced in a header file.
    Some values in config define "macro_name", some don't. This helps generate consistent macro names
    for the latter.
    """
    sanitised_config_key = config_key.replace(".", "_").replace("-", "_").upper()
    return f"MBED_CONF_{sanitised_config_key}"


@dataclass
class TargetMetadata:
    """Representation of target metadata assembled during config parsing.

    This is where the cumulative attributes are stored.
    """

    macros: Set[str] = field(default_factory=set)
    features: Set[str] = field(default_factory=set)
    components: Set[str] = field(default_factory=set)
    labels: Set[str] = field(default_factory=set)
    device_has: Set[str] = field(default_factory=set)


METADATA_FIELDS = [f.name for f in fields(TargetMetadata)]
PREFIXED_METADATA_FIELDS = [f"target.{f}" for f in METADATA_FIELDS]
METADATA_OVERRIDE_KEYS = PREFIXED_METADATA_FIELDS + [
    f"{attr}_{suffix}" for attr, suffix in itertools.product(PREFIXED_METADATA_FIELDS, ["add", "remove"])
]


@dataclass
class Config:
    """Representation of build configuration."""

    options: Dict[str, Option] = field(default_factory=dict)
    target_metadata: TargetMetadata = field(default_factory=TargetMetadata)

    @classmethod
    def from_sources(cls, sources: List[Source]) -> "Config":
        """Interrogate each source in turn to create final Config."""
        config = Config()
        for source in sources:
            for key, value in source.config.items():
                _create_config_option(config, key, value, source)
            for key, value in source.target_overrides.items():
                if key in METADATA_OVERRIDE_KEYS:
                    _modify_config_target_metadata(config, key, value)
                else:
                    _update_config_option(config, key, value, source)
        return config


def _create_config_option(config: Config, key: str, value: Any, source: Source) -> None:
    """Mutates Config in place by creating a new Option."""
    config.options[key] = Option.build(key, value, source)


def _update_config_option(config: Config, key: str, value: Any, source: Source) -> None:
    """Mutates Config in place by updating the value of existing Option."""
    if key not in config.options:
        raise ValueError(f"Can't update option which does not exist. ({key}={value} from {source.name})")
    config.options[key].set_value(value, source)


def _modify_config_target_metadata(config: Config, key: str, value: Any) -> None:
    """Mutates Config in place by adding, removing or resetting the value of target metadata field."""
    key, modifier = _extract_target_modifier_data(key)
    if modifier == "add":
        new_value = getattr(config.target_metadata, key) | set(value)
    elif modifier == "remove":
        new_value = getattr(config.target_metadata, key) - set(value)
    else:
        new_value = set(value)
    setattr(config.target_metadata, key, new_value)


def _extract_target_modifier_data(key: str) -> Tuple[str, str]:
    regex = fr"""
            (?P<key>{'|'.join(METADATA_FIELDS)}) # attribute name (one of ACCUMULATING_OVERRIDES)
            _?                                   # separator
            (?P<modifier>(add|remove)?)          # modifier (add, remove or empty)
    """
    match = re.search(regex, key, re.VERBOSE)
    if not match:
        raise ValueError(f"Not a target modifier key {key}")
    return match["key"], match["modifier"]
