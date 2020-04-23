#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Configuration assembly."""
import pathlib

from mbed_build._internal.config.config import Config


def assemble_config(mbed_target: str, mbed_program_directory: pathlib.Path) -> Config:
    """Assemble Config for given target and program directory.

    The structure and configuration of MbedOS requires us to do multiple passes over
    configuration assembly, as each Source can modify filtering rules applied to finding libs.
    """
    return Config()
