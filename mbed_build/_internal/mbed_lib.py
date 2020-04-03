#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Mbed lib file scanner."""
from pathlib import Path
from typing import Iterable

from mbed_build._internal.find_files import (
    find_files,
    exclude_legacy_directories,
    exclude_using_mbedignore,
    exclude_using_target_labels,
)


def find_mbed_lib_files(mbed_program_directory: Path, board_type: str) -> Iterable[Path]:
    """Return paths to all mbed_lib.json for a given target.

    Args:
        mbed_program_directory: Location of mbed program
        board_type: Name of the target to filter files for
    """
    mbed_lib_paths = find_files("mbed_lib.json", mbed_program_directory)
    mbed_lib_paths = exclude_legacy_directories(mbed_lib_paths)  # Should be cleaned in mbed-os source in the future
    mbed_lib_paths = exclude_using_mbedignore(mbed_program_directory, mbed_lib_paths)
    mbed_lib_paths = exclude_using_target_labels(mbed_program_directory, board_type, mbed_lib_paths)
    return mbed_lib_paths
