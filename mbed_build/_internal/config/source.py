#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Configuration source abstraction."""
from dataclasses import dataclass
import json
from pathlib import Path
from typing import List, Tuple

from mbed_targets import get_target_by_board_type
from mbed_build._internal.config.cumulative_data import METADATA_OVERRIDE_KEYS


@dataclass
class Source:
    """Configuration source abstraction.

    MbedOS build configuration is assembled from various sources:
    - targets.json
    - mbed_lib.json
    - mbed_app.json

    This class provides a common interface to configuration data.
    """

    human_name: str
    namespace: str
    config: dict
    config_overrides: dict
    cumulative_overrides: dict

    @classmethod
    def from_mbed_lib(cls, file: Path, target_labels: List[str]) -> "Source":
        """Build Source from mbed_lib.json file.

        Args:
            file: Path to mbed_lib.json file
            target_labels: Labels for which "target_overrides" should apply
        """
        data = json.loads(file.read_text())
        target_overrides = data.get("target_overrides", {})
        target_specific_overrides = _filter_target_overrides(target_overrides, target_labels)
        config_overrides, cumulative_overrides = _split_target_overrides_by_type(target_specific_overrides)
        return cls(
            human_name=f"Source from file: {file}",
            namespace=data["name"],
            config=data.get("config", {}),
            cumulative_overrides=cumulative_overrides,
            config_overrides=config_overrides,
        )

    @classmethod
    def from_target(cls, mbed_target: str, mbed_program_directory: Path) -> "Source":
        """Build Source from retrieved mbed_targets.Target data."""
        target = get_target_by_board_type(mbed_target, mbed_program_directory)
        return cls(
            human_name=f"mbed_target.Target for {mbed_target}",
            namespace="target",
            config=target.config,
            config_overrides={},
            cumulative_overrides={
                "features": target.features,
                "components": target.components,
                "labels": target.labels,
            },
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


def _split_target_overrides_by_type(data: dict) -> Tuple[dict, dict]:
    """Split target override data into config overrides and cumulative overrides."""
    config_overrides = {}
    cumulative_overrides = {}
    for key, value in data.items():
        if key in METADATA_OVERRIDE_KEYS:
            cumulative_overrides[key] = value
        else:
            config_overrides[key] = value
    return config_overrides, cumulative_overrides


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
