#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Accumulate values in Config.<attribute>."""
import itertools
from dataclasses import dataclass
from typing import Any, Callable, List, Literal, cast

# Fix circular dependency problem
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mbed_build._internal.config.config import Config


class UnableToBuildCumulativeModifier(Exception):
    """Raised when data given to builder is not valid for cumulative modifier."""


# TODO: potentially add more accumulating properties here.
# Two projects this has been tested against:
# - mbed-cloud-client-example
# - mbed-os-example-blinky
# only contain "features_add" and "features_remove".
ACCUMULATING_OVERRIDES = ("features",)
MODIFIERS = ("add", "remove")
ALL_ACCUMULATING_OVERRIDES = ACCUMULATING_OVERRIDES + tuple(
    f"{attr}_{suffix}" for attr, suffix in itertools.product(ACCUMULATING_OVERRIDES, MODIFIERS)
)


def build(key: str, data: Any) -> Callable:
    """Attempt to build a cumulative override modifier.

    A key for this modifier needs to follow a spec from old tools implementation:
    - start with "target."
    - the part after "target." is one of ACCUMULATING_OVERRIDES
    """
    # Key following a spec would:
    if not key.startswith("target."):
        raise UnableToBuildCumulativeModifier

    key = key[7:]  # Strip "target." prefix
    if key in ALL_ACCUMULATING_OVERRIDES:
        override_key, override_type = key.rsplit("_", maxsplit=1)
        override_key = cast(CumulativeOverrideKey, override_key)
        if override_type == "add":
            return AppendToConfig(key=override_key, value=data)
        if override_type == "remove":
            return RemoveFromConfig(key=override_key, value=data)

    raise UnableToBuildCumulativeModifier


CumulativeOverrideKey = Literal["features"]


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
