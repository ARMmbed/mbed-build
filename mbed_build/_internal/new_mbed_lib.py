#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Mbed lib file scanner."""
from pathlib import Path
from typing import Iterable
from mbed_targets import get_build_attributes_by_board_type

from mbed_build._internal.new_find_files import find_files, LabelFilter


def find_mbed_lib_files(mbed_program_directory: Path, board_type: str) -> Iterable[Path]:
    """Return paths to all mbed_lib.json for a given target.

    Args:
        mbed_program_directory: Location of mbed program
        board_type: Name of the target to filter files for
    """
    build_attributes = get_build_attributes_by_board_type(board_type, mbed_program_directory)
    label_filters = [
        LabelFilter("TARGET", build_attributes.labels),
        LabelFilter("FEATURE", build_attributes.features),
        LabelFilter("COMPONENT", build_attributes.components),
    ]
    return find_files("mbed_lib.json", mbed_program_directory, label_filters)
