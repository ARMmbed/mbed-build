#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Mbed lib file scanner."""
from pathlib import Path
from typing import Dict, Iterable

from mbed_build._internal.find_files import (
    find_files,
    exclude_using_mbedignore,
    exclude_not_labelled,
)


def find_mbed_lib_files(mbed_program_directory: Path, board_type: str) -> Iterable[Path]:
    """Return paths to all mbed_lib.json for a given target.

    When discovering mbed_lib.json files, the following filtering is applied:
    - paths matching patterns from .mbedignore files will be excluded
    - paths not matching target labels will be excluded

    Args:
        mbed_program_directory: Location of mbed program
        board_type: Name of the target to filter files for
    """
    mbed_lib_paths = find_files("mbed_lib.json", mbed_program_directory)

    mbedignore_paths = find_files(".mbedignore", mbed_program_directory)
    for mbedignore_path in mbedignore_paths:
        mbed_lib_paths = exclude_using_mbedignore(mbedignore_path, mbed_lib_paths)

    target_labels = _get_all_target_labels(mbed_program_directory, board_type)
    if target_labels:
        for label_type, allowed_label_values in target_labels.items():
            mbed_lib_paths = exclude_not_labelled(label_type, allowed_label_values, mbed_lib_paths)

    return mbed_lib_paths


def _get_all_target_labels(mbed_program_directory: Path, board_type: str) -> Dict:
    """TODO."""
    pass
