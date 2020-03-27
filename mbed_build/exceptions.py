#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Public exceptions raised by the package."""
from mbed_tools_lib.exceptions import ToolsError


class MbedBuildError(ToolsError):
    """Base public exception for the mbed-devices package."""


class InvalidExportOutputDirectory(MbedBuildError):
    """It is not possible to export to the provided output directory."""
