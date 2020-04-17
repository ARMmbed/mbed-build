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
        name = contents["name"]

        config = contents.get("config", {})
        namespaced_config = {_add_namespace(key, name): value for key, value in config.items()}

        namespaced_target_overrides = {}
        target_overrides = contents.get("target_overrides", {})
        for key, value in target_overrides.items():
            namespaced_target_overrides[key] = {_add_namespace(key, name): value for key, value in value.items()}

        return cls(file=json_file, config=namespaced_config, target_overrides=namespaced_target_overrides)


def _add_namespace(key, namespace):
    # If key is already namespaced, don't touch it
    if "." in key:
        return key
    return f"{namespace}.{key}"
