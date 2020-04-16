#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
import re
from dataclasses import dataclass
from typing import Any, Callable, List, Literal, get_args

# Fix circular dependency problem
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mbed_build._internal.config.config import Config


CumulativeOverrideName = Literal["features"]

CUMULATIVE_OVERRIDES = get_args(CumulativeOverrideName)
CUMULATIVE_OVERRIDE_KEY_REGEX = re.compile(
    f"(?P<field_name>{'|'.join(CUMULATIVE_OVERRIDES)})_(?P<override_type>add|remove)"
)


class UnableToBuildCumulativeModifier(Exception):
    """Raised when data given to builder is not valid for cumulative modifier."""


def build(key: str, data: Any) -> Callable:
    """Attempt to build a cumulative override modifier."""
    cumulative_key_match = re.search(CUMULATIVE_OVERRIDE_KEY_REGEX, key)
    if not cumulative_key_match:
        raise UnableToBuildCumulativeModifier
    if cumulative_key_match["override_type"] == "add":
        return AppendToConfig(key=cumulative_key_match["field_name"], value=data)
    if cumulative_key_match["override_type"] == "remove":
        return RemoveFromConfig(key=cumulative_key_match["field_name"], value=data)


@dataclass
class AppendToConfig:
    """Append value to one of the config cumulative attributes."""

    key: CumulativeOverrideName
    value: List[str]

    def __call__(self, config: "Config") -> None:
        """Mutate config by appending value to key."""
        existing = config.get(self.key, set())
        config[self.key] = existing | set(self.value)


@dataclass
class RemoveFromConfig:
    """Remove value from one of the config cumulative attributes."""

    key: CumulativeOverrideName
    value: List[str]

    def __call__(self, config: "Config") -> None:
        """Mutate config by removing value from key."""
        existing = config.get(self.key, set())
        config[self.key] = existing - set(self.value)
