#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""This module contains config actions, which will mutate configuration.

Config actions are built from entries found in JSON files used by MbedOS applications.
Some of those entries aren't simple overrides, but involve more complex operations
like addition or removal of items from lists.
"""
from abc import ABC, abstractmethod, abstractclassmethod
from dataclasses import dataclass
from typing import Any, Optional

# Fix circular dependency problem
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mbed_build._internal.config.config import Config


class ConfigAction(ABC):
    """Common interface for all the actions."""

    @abstractmethod
    def apply(self, config: "Config") -> "Config":
        """Interface for apply method."""
        ...

    @abstractclassmethod
    def build(cls, key: str, data: Any) -> "ConfigAction":
        """Interface for build method."""
        ...

    @staticmethod
    def from_config_entry(key: str, data: Any) -> "ConfigAction":
        """Config entries overwrite existing settings."""
        return SetConfigValueAction.build(key, data)

    @staticmethod
    def from_target_override_entry(key: str, data: Any) -> "ConfigAction":
        """Target overrides come in three shapes: addition, removal and override."""
        # TODO: implement add/remove parsed out from the key
        return SetConfigValueAction.build(key, data)


@dataclass
class SetConfigValueAction(ConfigAction):
    """Overwrite entry in config with new data."""

    key: str
    value: Any
    help: Optional[str]

    def apply(self, config: "Config") -> "Config":
        """Mutate config by overwriting existing entry with new data."""
        existing = config.settings.get(self.key, {})
        override = {"value": self.value}
        if self.help:
            override["help"] = self.help
        config.settings[self.key] = {**existing, **override}
        return config

    @classmethod
    def build(cls, key: str, data: Any) -> "SetConfigValueAction":
        """Builds action from given data.

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
