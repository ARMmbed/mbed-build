#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Interface for building modifiers."""
from typing import Any, Callable

from mbed_build._internal.config.config_modifiers import set_config_setting


def build_modifier_from_config_entry(key: str, data: Any) -> Callable:
    """Config entries overwrite existing settings - build SetConfigValue modifier."""
    return set_config_setting.build(key, data)


def build_modifier_from_target_override_entry(key: str, data: Any) -> Callable:
    """TODO: handle add/remove cumulative overrides."""
    return set_config_setting.build(key, data)
