#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Module to generate application's CMake file."""
import pathlib
from typing import Iterable
from mbed_targets.mbed_target_build_attributes import MbedTargetBuildAttributes
from mbed_build._internal.cmake_file import render_cmakelists_template, write_cmakelists_file
from mbed_build.exceptions import InvalidExportOutputDirectory


def generate_cmakelists_file(target_build_attributes: MbedTargetBuildAttributes, toolchain_name: str) -> str:
    """Generate the top-level CMakeLists.txt file containing the correct definitions for a build.

    Args:
        target_build_attributes: the build attributes for the target the application is being built for
        toolchain_name: the toolchain to be used to build the application

    Returns:
        A string of rendered contents for the file.
    """
    toolchain_labels = _fetch_toolchain_labels(toolchain_name)
    return render_cmakelists_template(
        target_build_attributes.labels,
        target_build_attributes.features,
        target_build_attributes.components,
        toolchain_labels,
    )


def export_cmakelists_file(output_directory: pathlib.Path, file_contents: str) -> None:
    """Writes out file contents to a CMakeLists.txt file in the output directory.

    Args:
        output_directory: the destination directory for the exported top-level CMakeLists.txt file
        file_contents: the contents of the top-level CMakeLists.txt file

    Raises:
        InvalidExportOutputDirectory: if provided output directory is invalid
    """
    if output_directory.is_file():
        raise InvalidExportOutputDirectory("Output directory cannot be a path to a file.")
    write_cmakelists_file(output_directory, file_contents)


def _fetch_toolchain_labels(toolchain_name: str) -> Iterable[str]:
    # ToDo: Hook this up to return toolchain-specific labels
    return [toolchain_name]
