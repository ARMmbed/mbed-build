#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Mbed lib file scanner."""
from pathlib import Path
from typing import Iterable

from mbed_build._internal.find_files import find_files, BoardLabelFilter, MbedignoreFilter


def find_mbed_lib_files(mbed_program_directory: Path, board_type: str) -> Iterable[Path]:
    """Return paths to all mbed_lib.json for a given target.

    Args:
        mbed_program_directory: Location of mbed program
        board_type: Name of the target to filter files for
    """
    board_label_filter = BoardLabelFilter(board_type, mbed_program_directory)
    # Temporary workaround, which replicates hardcoded ignore rules from old tools.
    # Legacy list of ignored directories is longer, however "TESTS" and
    # "TEST_APPS" were the only ones that actually exist in the MbedOS source.
    # Ideally, this should be solved by putting an `.mbedignore` file in the root of MbedOS repo,
    # similarly to what the code below pretends is happening.
    legacy_ignore = MbedignoreFilter(("*/TESTS", "*/TEST_APPS"))
    return find_files("mbed_lib.json", mbed_program_directory, [legacy_ignore, board_label_filter])
