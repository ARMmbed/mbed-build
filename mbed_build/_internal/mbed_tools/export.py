#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Export top-level CMakeLists.txt command."""
import pathlib

import click

from mbed_build.mbed_build import generate_cmakelists_file, write_cmakelists_file


@click.command()
@click.option(
    "-o",
    "--output-directory",
    type=click.Path(),
    required=True,
    help="Destination for exported top-level CMakeLists.txt file.",
)
@click.option(
    "-t",
    "--toolchain",
    type=click.Choice(["ARM6", "GCC"]),
    required=True,
    help="The toolchain you are using to build your app.",
)
@click.option("-m", "--mbed_target", required=True, help="A build target for an Mbed-enabled device, eg. K64F")
@click.option(
    "-p",
    "--project-path",
    type=click.Path(),
    default=".",
    help="Path to local Mbed project. By default is the current working directory.",
)
def export(output_directory: str, toolchain: str, mbed_target: str, project_path: str) -> None:
    """Exports a top-level CMakeLists.txt file to the specified directory.

    The parameters set in the CMake file will be dependent on the combination of
    toolchain and Mbed target provided and these can then control which parts of
    Mbed OS is included in the build.

    Args:
        output_directory: where the top-level CMakeLists.txt should be exported to
        toolchain: the toolchain you are using to build your app (eg. GCC, ARM5 etc.)
        mbed_target: the build target you are wanting to run your app (eg. K64F)
        project_path: the path to the local Mbed project

    Raises:
        InvalidExportOutputDirectory: it's not possible to export to the output directory provided
    """
    cmake_file_contents = generate_cmakelists_file(mbed_target, project_path, toolchain)
    write_cmakelists_file(pathlib.Path(output_directory), cmake_file_contents)
    click.echo(f"The program-level CMake file has been successfully exported to directory '{str(output_directory)}'")
