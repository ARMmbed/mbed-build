#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Modify values in Config.target.*."""
import itertools
from dataclasses import dataclass
from typing import Any, Callable, List, cast
from typing_extensions import Literal

# Fix circular dependency problem
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mbed_build._internal.config.config import Config


class InvalidModifierData(Exception):
    """Raised when data given to builder is not valid for target attribute modifier."""


ACCUMULATING_OVERRIDES = ("extra_labels", "macros", "device_has", "features", "components")
MODIFIERS = ("add", "remove")
ALL_ACCUMULATING_OVERRIDES = ACCUMULATING_OVERRIDES + tuple(
    f"{attr}_{suffix}" for attr, suffix in itertools.product(ACCUMULATING_OVERRIDES, MODIFIERS)
)


def build(key: str, data: Any) -> Callable:
    """Attempt to build a target attribute modifier.

    A key for this modifier needs to follow a spec from old tools implementation:
    - start with "target."
    - the part after "target." is one of ACCUMULATING_OVERRIDES
    """
    # Key following a spec would:
    prefix = "target."
    if not key.startswith(prefix):
        raise InvalidModifierData

    key = key[len(prefix) :]  # Strip "target." prefix
    if key in ALL_ACCUMULATING_OVERRIDES:
        override_key, override_type = key.rsplit("_", maxsplit=1)
        override_key = cast(AccumulatingOverrideKey, override_key)
        if override_type == "add":
            return AppendToTargetAttribute(key=override_key, value=data)
        if override_type == "remove":
            return RemoveFromTargetAttribute(key=override_key, value=data)

    raise InvalidModifierData


AccumulatingOverrideKey = Literal["extra_labels", "macros", "device_has", "features", "components", "features"]


@dataclass
class AppendToTargetAttribute:
    """Append value to one of the targets attributes."""

    key: AccumulatingOverrideKey
    value: List[str]

    def __call__(self, config: "Config") -> None:
        """Mutate config by appending value to key."""
        config["target"][self.key] = config["target"][self.key] | set(self.value)


@dataclass
class RemoveFromTargetAttribute:
    """Remove value from one of the targets attributes."""

    key: AccumulatingOverrideKey
    value: List[str]

    def __call__(self, config: "Config") -> None:
        """Mutate config by removing value from key."""
        config["target"][self.key] = config["target"][self.key] - set(self.value)
