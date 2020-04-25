#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Build configuration representation."""
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, Optional

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
            source: Source from which option data came - used for tracing overrides
        """
        if isinstance(data, dict):
            return cls(
                key=key,
                value=data.get("value"),
                macro_name=data.get("macro_name", _build_macro_name(key)),
                help_text=data.get("help"),
                set_by=source.human_name,
            )
        else:
            return cls(value=data, key=key, macro_name=_build_macro_name(key), help_text=None, set_by=source.human_name)

    def set_value(self, value: Any, source: Source) -> "Option":
        """Mutate self with new value."""
        self.value = value
        self.set_by = source.human_name
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
class Config:
    """Representation of build configuration."""

    options: Dict[str, Option] = field(default_factory=dict)

    @classmethod
    def from_sources(cls, sources: Iterable[Source]) -> "Config":
        """Interrogate each source in turn to create final Config."""
        config = Config()
        for source in sources:
            for key, value in source.config.items():
                _create_config_option(config, key, value, source)
            for key, value in source.config_overrides.items():
                _update_config_option(config, key, value, source)
        return config


def _create_config_option(config: Config, key: str, value: Any, source: Source) -> None:
    """Mutates Config in place by creating a new Option."""
    config.options[key] = Option.build(key, value, source)


def _update_config_option(config: Config, key: str, value: Any, source: Source) -> None:
    """Mutates Config in place by updating the value of existing Option."""
    if key not in config.options:
        raise ValueError(f"Can't update option which does not exist. ({key}={value} from {source.human_name})")
    config.options[key].set_value(value, source)
