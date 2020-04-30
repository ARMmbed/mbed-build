#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Export top-level CMakeLists.txt command."""
import pathlib

import click

from mbed_build._internal.cmake_file import generate_cmakelists_file
from mbed_build._internal.write_files import write_file


@click.command(
    help="This is an unfinished implementation of export. It only exports the initial Mbed OS 'key folder names'."
)
@click.option(
    "-o",
    "--output-directory",
    type=click.Path(),
    required=True,
    help="Destination for exported CMakeLists.txt file containing directory keys.",
)
@click.option(
    "-t",
    "--toolchain",
    type=click.Choice(["ARM6", "GCC"]),
    required=True,
    help="The toolchain you are using to build your app.",
)
@click.option("-m", "--mbed-target", required=True, help="A build target for an Mbed-enabled device, eg. K64F")
@click.option(
    "-p",
    "--program-path",
    type=click.Path(),
    default=".",
    help="Path to local Mbed program. By default is the current working directory.",
)
def export(output_directory: str, toolchain: str, mbed_target: str, program_path: str) -> None:
    """Exports a top-level CMakeLists.txt file to the specified directory.

    The parameters set in the CMake file will be dependent on the combination of
    toolchain and Mbed target provided and these can then control which parts of
    Mbed OS is included in the build.

    Args:
        output_directory: where the top-level CMakeLists.txt should be exported to
        toolchain: the toolchain you are using to build your app (eg. GCC, ARM5 etc.)
        mbed_target: the build target you are wanting to run your app (eg. K64F)
        program_path: the path to the local Mbed program

    Raises:
        InvalidExportOutputDirectory: it's not possible to export to the output directory provided
    """
    cmake_file_contents = generate_cmakelists_file(mbed_target, program_path, toolchain)
    write_file(pathlib.Path(output_directory), "CMakeLists.txt", cmake_file_contents)
    click.echo(f"The program-level CMake file has been successfully exported to directory '{str(output_directory)}'")
