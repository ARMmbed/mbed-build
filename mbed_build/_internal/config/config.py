#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Build configuration abstraction layer."""
from typing import Any, Dict, List, Optional
from typing_extensions import TypedDict

from mbed_build._internal.config.config_layer import ConfigLayer


class Setting(TypedDict):
    """Represents a config setting."""

    help: Optional[str]
    value: Any


class Config(TypedDict):
    """Represents a build configuration."""

    settings: Dict[str, Setting]


def build_config_from_layers(layers: List[ConfigLayer]) -> Config:
    """Create configuration from layers."""
    config = Config(settings={})
    for layer in layers:
        layer.apply(config)
    return config
