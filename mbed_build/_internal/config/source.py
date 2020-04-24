#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Configuration source abstraction."""
from dataclasses import dataclass
import json
from pathlib import Path
from typing import List

from mbed_targets import get_target_by_board_type


@dataclass
class Source:
    """Configuration source abstraction.

    MbedOS build configuration is assembled from various sources:
    - targets.json
    - mbed_lib.json
    - mbed_app.json

    This class provides a common interface to configuration data.
    It also handles data normalisation, to fix inconsistencies between sources:
    - namespacing
    - override filtering for specific target labels
    """

    name: str
    config: dict
    target_overrides: dict

    @classmethod
    def from_mbed_lib(cls, file: Path, target_labels: List[str]) -> "Source":
        """Build Source from mbed_lib.json file.

        Args:
            file: Path to mbed_lib.json file
            target_labels: Labels for which "target_overrides" should apply
        """
        data = json.loads(file.read_text())
        namespace = data["name"]
        config = data.get("config", {})
        target_overrides = data.get("target_overrides", {})
        label_specific_target_overrides = _filter_target_overrides(target_overrides, target_labels)
        return cls(
            config=_namespace_data(config, namespace),
            target_overrides=_namespace_data(label_specific_target_overrides, namespace),
            name=str(file),
        )

    @classmethod
    def from_target(cls, mbed_target: str, mbed_program_directory: Path) -> "Source":
        """Build Source from retrieved mbed_targets.Target data."""
        target = get_target_by_board_type(mbed_target, mbed_program_directory)
        namespace = "target"
        config = target.config
        target_overrides = {
            "features": target.features,
            "components": target.components,
            "labels": target.labels,
        }
        return cls(
            config=_namespace_data(config, namespace),
            target_overrides=_namespace_data(target_overrides, namespace),
            name=f"mbed_target.Target for {mbed_target}",
        )


def _filter_target_overrides(data: dict, allowed_labels: List[str]) -> dict:
    """Flatten and filter target overrides.

    Ensures returned dictionary only contains configuration settings applicable to given allowed labels.
    """
    flattened = {}
    for target_label, overrides in data.items():
        if target_label == "*" or target_label in allowed_labels:
            flattened.update(overrides)
    return flattened


def _namespace_data(data: dict, namespace: str) -> dict:
    """Prefix configuration key with a namespace.

    Namespace is ConfigSource wide, and is resolved at source build time.

    It should be one of:
    - "target"
    - "app"
    - library name (where "mbed_lib.json" comes from)

    If given key is already namespaced, return it as is - this is going to be the case for
    keys from "target_overrides" entries. Keys from "config" usually need namespacing.
    """
    namespaced = {}
    for key, value in data.items():
        if "." not in key:
            key = f"{namespace}.{key}"
        namespaced[key] = value
    return namespaced
