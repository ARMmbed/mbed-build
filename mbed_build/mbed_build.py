#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
import pathlib
from typing import List

from mbed_build._internal.cmake_file_writer import write_cmakelists_file
from mbed_build._internal.cmake_renderer import render_cmakelists_template
from mbed_build.exceptions import NotValidExportOutputDirectory


def generate_cmakelists_file(target_name: str, toolchain_name: str) -> str:
    """Generate the top-level CMakeLists.txt file containing the correct definitions for a build.

    Args:
        target_name: the build target for the device the application is being built for
        toolchain_name: the toolchain to be used to build the application

    Returns:
        A string of rendered contents for the file.
    """
    target_labels = _fetch_target_labels(target_name)
    toolchain_labels = _fetch_toolchain_labels(toolchain_name)
    return render_cmakelists_template(target_labels, toolchain_labels)


def export_cmakelists_file(output_directory: pathlib.Path, file_contents: str) -> None:
    """Writes out file contents to a CMakeLists.txt file in the output directory.

    Args:
        output_directory: the destination directory for the exported top-level CMakeLists.txt file
        file_contents: the contents of the top-level CMakeLists.txt file
    """
    if output_directory.is_file():
        raise NotValidExportOutputDirectory("Output directory cannot be a path to a file.")
    write_cmakelists_file(output_directory, file_contents)


def _fetch_target_labels(target_name: str) -> List[str]:
    # ToDo: Hook this up to mbed-targets
    return [target_name]


def _fetch_toolchain_labels(toolchain_name: str) -> List[str]:
    # ToDo: Hook this up to return toolchain-specific labels
    return [toolchain_name]
