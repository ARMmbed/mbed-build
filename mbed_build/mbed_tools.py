#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Integration with https://github.com/ARMmbed/mbed-tools."""
from mbed_build._internal.mbed_tools.build import build
from mbed_build._internal.mbed_tools.config import config
from mbed_build._internal.mbed_tools.export import export


build = build
config = config
export = export
