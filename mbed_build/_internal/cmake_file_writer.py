#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
import pathlib


def write_cmakelists_file(output_directory: pathlib.Path, file_contents: str) -> None:
    """Writes out the CMakeLists.txt file to the output directory.

    If the intermediate directories to the output directory don't exist,
    this function will create them.

    This function will overwrite any existing CMakeLists.txt file in the
    output directory.

    Args:
        output_directory: path to directory where we want the CMakeLists.txt to go
        file_contents: the contents of the CMakeLists.txt file
    """
    output_directory.mkdir(parents=True, exist_ok=True)
    output_file = output_directory.joinpath("CMakeLists.txt")
    output_file.write_text(file_contents)
