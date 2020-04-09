#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
from dataclasses import dataclass
from enum import Enum
from typing import Any


class ConfigActionType(Enum):
    """Type of action."""

    ADD = 1
    REMOVE = 2
    OVERWRITE = 3


class ConfigLayerAction:
    action_type: ConfigActionType
    for_target: str
    value: Any
    key: str

    @classmethod
    def from_config_entry(self, name: str, value: Any):
        pass

    @classmethod
    def from_target_override_entry(self, name: str, value: Any):
        pass
