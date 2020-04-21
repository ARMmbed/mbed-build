#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Configuration source abstraction."""
import json
import pathlib
from dataclasses import dataclass


@dataclass
class ConfigSource:
    """Configuration source abstraction.

    MbedOS build configuration is assembled from various sources:
    - targets.json
    - mbed_lib.json
    - mbed_app.json

    This class serves as a common interface for interrogating sources listed above.
    """

    file: pathlib.Path
    config: dict
    target_overrides: dict

    @classmethod
    def from_mbed_lib(cls, json_file: pathlib.Path) -> "ConfigSource":
        """Read mbed_lib.json file and build new ConfigSource."""
        contents = json.loads(json_file.read_text())
        namespace = contents["name"]
        config = contents.get("config", {})
        namespaced_config = _namespace_data(config, namespace)
        target_overrides = contents.get("target_overrides", {})
        namespaced_target_overrides = _namespace_data(target_overrides, namespace)
        return cls(file=json_file, config=namespaced_config, target_overrides=namespaced_target_overrides)


def _namespace_data(data: dict, namespace: str) -> dict:
    """Prefix each configuration key with a namespace."""
    return {_namespace_key(key, namespace): value for key, value in data.items()}


def _namespace_key(key: str, namespace: str) -> str:
    """Prefix configuration key with a namespace.

    Namespace is ConfigSource wide, and is resolved at source build time.

    It should be one of:
    - "target"
    - "app"
    - library name (where "mbed_lib.json" comes from)

    If given key is already namespaced, return it as is - this is going to be the case for
    keys from "target_overrides" entries. Keys from "config" usually need namespacing.
    """
    if "." in key:
        return key
    else:
        return f"{namespace}.{key}"
