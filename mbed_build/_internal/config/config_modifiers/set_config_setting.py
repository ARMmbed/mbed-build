#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Create or update entries in Config.settings."""
from dataclasses import dataclass
from typing import Any, Callable, Optional

# Fix circular dependency problem
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mbed_build._internal.config.config import Config


def build(key: str, data: Any) -> Callable:
    """Builds SetConfigSetting from given data.

    Configuration source from the JSON files is represented in two distinct ways:
    - key -> value
    - key -> dict
    """
    if isinstance(data, dict):
        value = data["value"]
        help = data.get("help", None)
    else:
        value = data
        help = None

    return SetConfigSetting(key=key, value=value, help=help)


@dataclass
class SetConfigSetting:
    """Overwrite entry in config with new data."""

    key: str
    value: Any
    help: Optional[str]

    def __call__(self, config: "Config") -> None:
        """Mutate config by overwriting existing entry with new data."""
        existing = config["settings"].get(self.key)
        if existing:
            existing["value"] = self.value
        else:
            config["settings"][self.key] = {
                "value": self.value,
                "help": self.help,
            }
