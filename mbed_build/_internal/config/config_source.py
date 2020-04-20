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

    namespace: str
    file: pathlib.Path
    config: dict
    target_overrides: dict

    @classmethod
    def from_mbed_lib(cls, json_file: pathlib.Path) -> "ConfigSource":
        """Read mbed_lib.json file and build new ConfigSource."""
        contents = json.loads(json_file.read_text())
        namespace = contents["name"]
        config = contents.get("config", {})
        target_overrides = contents.get("target_overrides", {})
        return cls(namespace=namespace, file=json_file, config=config, target_overrides=target_overrides)
