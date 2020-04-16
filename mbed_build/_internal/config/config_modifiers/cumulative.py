#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Operate on sets of values stored in Config."""
import re
from dataclasses import dataclass
from typing import Any, Callable, List, Literal, cast

# Fix circular dependency problem
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mbed_build._internal.config.config import Config


CumulativeOverrideKey = Literal["features"]


class UnableToBuildCumulativeModifier(Exception):
    """Raised when data given to builder is not valid for cumulative modifier."""


CUMULATIVE_OVERRIDES = ["features"]
CUMULATIVE_OVERRIDE_KEY_REGEX = re.compile(
    f"(?P<override_key>{'|'.join(CUMULATIVE_OVERRIDES)})_(?P<override_type>add|remove)"
)


def build(key: str, data: Any) -> Callable:
    """Attempt to build a cumulative override modifier."""
    cumulative_key_match = re.search(CUMULATIVE_OVERRIDE_KEY_REGEX, key)
    if cumulative_key_match:
        override_type = cumulative_key_match["override_type"]
        override_key = cast(CumulativeOverrideKey, cumulative_key_match["override_key"])

        if override_type == "add":
            return AppendToConfig(key=override_key, value=data)
        if override_type == "remove":
            return RemoveFromConfig(key=override_key, value=data)

    raise UnableToBuildCumulativeModifier


@dataclass
class AppendToConfig:
    """Append value to one of the config cumulative attributes."""

    key: CumulativeOverrideKey
    value: List[str]

    def __call__(self, config: "Config") -> None:
        """Mutate config by appending value to key."""
        config[self.key] = config[self.key] | set(self.value)


@dataclass
class RemoveFromConfig:
    """Remove value from one of the config cumulative attributes."""

    key: CumulativeOverrideKey
    value: List[str]

    def __call__(self, config: "Config") -> None:
        """Mutate config by removing value from key."""
        config[self.key] = config[self.key] - set(self.value)
