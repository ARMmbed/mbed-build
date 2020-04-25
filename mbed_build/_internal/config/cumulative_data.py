#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Ability to parse cumulative attributes from Sources."""
import itertools
import re
from dataclasses import dataclass, field, fields
from typing import Any, Iterable, Set, Tuple


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mbed_build._internal.config.source import Source


@dataclass
class CumulativeData:
    """Representation of cumulative attributes assembled during Source parsing."""

    macros: Set[str] = field(default_factory=set)
    features: Set[str] = field(default_factory=set)
    components: Set[str] = field(default_factory=set)
    labels: Set[str] = field(default_factory=set)
    device_has: Set[str] = field(default_factory=set)

    @classmethod
    def from_sources(cls, sources: Iterable["Source"]) -> "CumulativeData":
        """Interrogate each Source in turn to create final CumulativeData."""
        data = CumulativeData()
        for source in sources:
            for key, value in source.cumulative_overrides.items():
                _modify_field(data, key, value)
        return data


def _modify_field(data: CumulativeData, key: str, value: Any) -> None:
    """Mutates CumulativeData in place by adding, removing or resetting the value of a field."""
    key, modifier = _extract_target_modifier_data(key)
    if modifier == "add":
        new_value = getattr(data, key) | set(value)
    elif modifier == "remove":
        new_value = getattr(data, key) - set(value)
    else:
        new_value = set(value)
    setattr(data, key, new_value)


METADATA_FIELDS = [f.name for f in fields(CumulativeData)]
PREFIXED_METADATA_FIELDS = [f"target.{f}" for f in METADATA_FIELDS]
METADATA_OVERRIDE_KEYS = PREFIXED_METADATA_FIELDS + [
    f"{attr}_{suffix}" for attr, suffix in itertools.product(PREFIXED_METADATA_FIELDS, ["add", "remove"])
]


def _extract_target_modifier_data(key: str) -> Tuple[str, str]:
    regex = fr"""
            (?P<key>{'|'.join(METADATA_FIELDS)}) # attribute name (one of ACCUMULATING_OVERRIDES)
            _?                                   # separator
            (?P<modifier>(add|remove)?)          # modifier (add, remove or empty)
    """
    match = re.search(regex, key, re.VERBOSE)
    if not match:
        raise ValueError(f"Not a target modifier key {key}")
    return match["key"], match["modifier"]
