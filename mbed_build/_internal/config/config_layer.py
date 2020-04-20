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
        namespace = config_source.namespace
        modifiers = []
        for key, data in config_source.config.items():
            modifiers.append(build_modifier_from_config_entry(key=_namespace(key, namespace), data=data))

        allowed_target_labels = ["*"] + target_labels
        for target_label, overrides in config_source.target_overrides.items():
            if target_label in allowed_target_labels:
                for key, data in overrides.items():
                    modifiers.append(
                        build_modifier_from_target_override_entry(key=_namespace(key, namespace), data=data)
                    )

        return cls(config_source=config_source, modifiers=modifiers)


def _namespace(key: str, namespace: str) -> str:
    """Prefix configuration key with a namespace.

    Namespace is ConfigSource wide, and is resolved at source build time.

    It should be one of:
    - "target"
    - "application"
    - library name (where "mbed_lib.json" comes from)

    If given key is already namespaced, return it as is - this is going to be the case for
    keys from "target_overrides" entries. Keys from "config" usually need namespacing.
    """
    if "." in key:
        return key
    else:
        return f"{namespace}.{key}"
