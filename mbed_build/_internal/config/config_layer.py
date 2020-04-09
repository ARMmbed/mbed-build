#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Layered approach to applying config sources to Config class."""
from dataclasses import dataclass
from typing import Iterable

from mbed_build._internal.config.config_layer_action import ConfigLayerAction
from mbed_build._internal.config.config_source import ConfigSource


# Fix circular dependency problem
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mbed_build._internal.config.config import Config


@dataclass
class ConfigLayer:
    """ConfigLayer lists actions which can be applied to Config instance in order to modify its contents."""

    actions: Iterable[ConfigLayerAction]

    def apply(self, config: "Config") -> "Config":
        """Apply all layers actions to the Config."""
        for action in self.actions:
            config = action.apply(config)
        return config

    @classmethod
    def from_config_source(cls, config_source: ConfigSource) -> "ConfigLayer":
        """Return new instance of ConfigLayer, with actions built from ConfigSource."""
        actions_from_config = [
            ConfigLayerAction.from_config_entry(name=name, value=value) for name, value in config_source.config.items()
        ]

        actions_from_target_overrides = []
        for target_label, overrides in config_source.target_overrides.items():
            for name, value in overrides.items():
                actions_from_target_overrides.append(
                    ConfigLayerAction.from_target_override_entry(name=name, value=value)
                )

        return cls(actions_from_config + actions_from_target_overrides)
