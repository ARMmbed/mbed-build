#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Utilities for building config modifiers."""
from typing import Any, Callable

from mbed_build._internal.config.config_modifiers import set_config_setting, set_target_attribute


def build_modifier_from_config_entry(key: str, data: Any) -> Callable:
    """Config entries always override config settings."""
    return set_config_setting.build(key, data)


def build_modifier_from_target_override_entry(key: str, data: Any) -> Callable:
    """Target override can be one of many things.

    Types of target overrides:
    - cumulative override (for a specific set of keys)
    - regular config setting override (everything else)
    """
    # Strip optional target prefix
    prefix = "target."
    if key.startswith(prefix):
        key = key[len(prefix) :]

    try:
        return set_target_attribute.build(key, data)
    except set_target_attribute.InvalidModifierData:
        return set_config_setting.build(key, data)
