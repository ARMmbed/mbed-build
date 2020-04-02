#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Mbed lib file scanner."""
from pathlib import Path
from typing import Iterable

from mbed_build._internal.find_files import find_files, exclude_using_mbedignore


def find_mbed_lib_files(directory: Path) -> Iterable[Path]:
    """Finds all mbed lib files."""
    mbed_lib_paths = find_files("mbed_lib.json", directory)

    mbedignore_paths = find_files(".mbedignore", directory)
    for mbedignore_path in mbedignore_paths:
        mbed_lib_paths = exclude_using_mbedignore(mbedignore_path, mbed_lib_paths)

    return mbed_lib_paths
