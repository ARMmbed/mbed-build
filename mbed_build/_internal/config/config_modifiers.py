#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""This module contains config modifiers, which will mutate configuration.

Config modifiers are built from entries found in JSON files used by MbedOS applications.
Some of those entries aren't simple overrides, but involve more complex operations
like addition or removal of items from lists.
"""
from dataclasses import dataclass
from typing import Any, Callable, Optional

# Fix circular dependency problem
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mbed_build._internal.config.config import Config


@dataclass
class SetConfigValue:
    """Overwrite entry in config with new data."""

    key: str
    value: Any
    help: Optional[str]

    def __call__(self, config: "Config") -> None:
        """Mutate config by overwriting existing entry with new data."""
        existing = config["settings"].get(self.key)
        if existing:
            existing["value"] = self.value
        else:
            config["settings"][self.key] = {
                "value": self.value,
                "help": self.help,
            }

    @classmethod
    def build(cls, key: str, data: Any) -> "SetConfigValue":
        """Builds self from given data.

        Configuration source from the JSON files is represented in two distinct ways:
        - key -> value
        - key -> dict
        """
        if isinstance(data, dict):
            value = data["value"]
            help = data.get("help", None)
        else:
            value = data
            help = None

        return cls(key=key, value=value, help=help)


def build_modifier_from_config_entry(key: str, data: Any) -> Callable:
    """Config entries overwrite existing settings - build SetConfigValue modifier."""
    return SetConfigValue.build(key, data)


def build_modifier_from_target_override_entry(key: str, data: Any) -> Callable:
    """TODO: handle add/remove cumulative overrides."""
    return SetConfigValue.build(key, data)
