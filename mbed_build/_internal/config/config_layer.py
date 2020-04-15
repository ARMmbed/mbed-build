#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Layered approach to applying config sources to Config class."""
from dataclasses import dataclass
from typing import Callable, Iterable, List

from mbed_build._internal.config.config_source import ConfigSource
from mbed_build._internal.config.config_action import (
    build_action_from_config_entry,
    build_action_from_target_override_entry,
)

# Fix circular dependency problem
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mbed_build._internal.config.config import Config


@dataclass
class ConfigLayer:
    """ConfigLayer is a simple container of actions which can be used to build Config."""

    actions: Iterable[Callable]

    def apply(self, config: "Config") -> "Config":
        """Apply all actions to the Config."""
        for action in self.actions:
            config = action(config)
        return config

    @classmethod
    def from_config_source(cls, config_source: ConfigSource, target_labels: List[str]) -> "ConfigLayer":
        """Return new instance of ConfigLayer built from ConfigSource data.

        This method translates data found in ConfigSource into ConfigActions specific to target.
        """
        actions_from_config = [
            build_action_from_config_entry(key=key, data=data) for key, data in config_source.config.items()
        ]

        actions_from_target_overrides: List[Callable] = []
        allowed_target_labels = ["*"] + target_labels
        for target_label, overrides in config_source.target_overrides.items():
            if target_label in allowed_target_labels:
                actions_from_target_overrides.extend(
                    build_action_from_target_override_entry(key=key, data=data) for key, data in overrides.items()
                )

        return cls(actions_from_config + actions_from_target_overrides)
