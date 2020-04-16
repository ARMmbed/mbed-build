#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Build configuration abstraction layer."""
from dataclasses import dataclass, field
from typing import List

from mbed_build._internal.config.config_layer import ConfigLayer


@dataclass
class Config:
    """Represents a build configuration."""

    settings: dict = field(default_factory=dict)

    @classmethod
    def from_layers(cls, layers: List[ConfigLayer]) -> "Config":
        """Create configuration from layers."""
        config = cls()
        for layer in layers:
            config = layer.apply(config)
        return config
