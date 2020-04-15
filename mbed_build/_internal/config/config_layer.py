#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Layered approach to applying config sources to Config class."""
from dataclasses import dataclass
from typing import Callable, Iterable, List

from mbed_build._internal.config.config_source import ConfigSource
from mbed_build._internal.config.config_modifiers import (
    build_modifier_from_config_entry,
    build_modifier_from_target_override_entry,
)

# Fix circular dependency problem
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mbed_build._internal.config.config import Config


@dataclass
class ConfigLayer:
    """ConfigLayer is a simple container of modifiers which can be used to build Config.

    This class has two purposes:
    - translate ConfigSource into a list of modifiers which can be applied to the Config
    - track the origin of incoming changes
    """

    config_source: ConfigSource
    modifiers: Iterable[Callable]

    def apply(self, config: "Config") -> "Config":
        """Apply all modifiers to the Config."""
        for modifier in self.modifiers:
            config = modifier(config)
        return config

    @classmethod
    def from_config_source(cls, config_source: ConfigSource, target_labels: List[str]) -> "ConfigLayer":
        """Return new instance of ConfigLayer built from ConfigSource data.

        This method translates data found in ConfigSource into modifiers specific to the given target.
        """
        modifiers_from_config = [
            build_modifier_from_config_entry(key=key, data=data) for key, data in config_source.config.items()
        ]

        modifiers_from_target_overrides: List[Callable] = []
        allowed_target_labels = ["*"] + target_labels
        for target_label, overrides in config_source.target_overrides.items():
            if target_label in allowed_target_labels:
                modifiers_from_target_overrides.extend(
                    build_modifier_from_target_override_entry(key=key, data=data) for key, data in overrides.items()
                )

        return cls(config_source=config_source, modifiers=(modifiers_from_config + modifiers_from_target_overrides))
