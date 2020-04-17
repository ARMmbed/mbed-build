#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Modify values in Config.target.*."""
import re
from dataclasses import dataclass
from typing import Callable, List, Tuple, cast
from typing_extensions import Literal

# Fix circular dependency problem
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mbed_build._internal.config.config import Config


class InvalidModifierData(Exception):
    """Raised when data given to builder is not valid for target attribute modifier."""


def build(key: str, data: List[str]) -> Callable:
    """Attempt to build a target attribute modifier.

    A key for this modifier needs to follow a spec from old tools implementation:
    - start with "target."
    - the part after "target." is one of ACCUMULATING_OVERRIDES

    Args:
        key: A key identifying target attribute, must have "target." prefix
        data: A list of overrides to add or remove from target attributes
    """
    try:
        key, modifier = _extract_key_and_modifier(key)
    except ValueError:
        raise InvalidModifierData

    if modifier == "add":
        return AppendToTargetAttribute(key=key, value=data)
    if modifier == "remove":
        return RemoveFromTargetAttribute(key=key, value=data)
    return OverwriteTargetAttribute(key=key, value=data)


AccumulatingOverrideKey = Literal["extra_labels", "macros", "device_has", "features", "components"]


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


@dataclass
class OverwriteTargetAttribute:
    """Overwrite value in one of the targets attributes."""

    key: AccumulatingOverrideKey
    value: List[str]

    def __call__(self, config: "Config") -> None:
        """Mutate config by removing value from key."""
        config["target"][self.key] = set(self.value)


ACCUMULATING_OVERRIDES = ("extra_labels", "macros", "device_has", "features", "components")


def _extract_key_and_modifier(key: str) -> Tuple[AccumulatingOverrideKey, str]:
    regex = fr"""
            (?P<key>{'|'.join(ACCUMULATING_OVERRIDES)}) # attribute name (one of ACCUMULATING_OVERRIDES)
            _?                                          # separator
            (?P<modifier>(add|remove)?)                 # modifier (add, remove or empty)
    """
    match = re.search(regex, key, re.VERBOSE)
    if not match:
        raise ValueError
    key = cast(AccumulatingOverrideKey, match["key"])
    return key, match["modifier"]
