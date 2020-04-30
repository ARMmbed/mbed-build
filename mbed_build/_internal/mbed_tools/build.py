#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Build an Mbed program."""
import pathlib

import click

from mbed_build._internal.config_header_file import generate_config_header_file
from mbed_build._internal.write_files import write_file


@click.command(help="Build an Mbed program. (Currently only config building implemented)")
@click.option("-m", "--mbed-target", required=True, help="A build target for an Mbed-enabled device, eg. K64F")
@click.option(
    "-p",
    "--program-path",
    type=click.Path(),
    default=".",
    help="Path to local Mbed program. By default is the current working directory.",
)
@click.option(
    "-c", "--config-only", is_flag=True, default=False, help="Only generate the mbed_config.h file for the build."
)
def build(mbed_target: str, program_path: str, config_only: bool) -> None:
    """Build an Mbed program.

    Triggers a build, which is made up of the following stages:
    1. Generate and write out mbed_config.h file containing the config definitions
    2. Generate a top-level CMake file (not yet implemented)
    3. Trigger a build via CMake (not yet implemented)

    Args:
        mbed_target: the build target you are wanting to run your app (eg. K64F)
        program_path: the path to the Mbed program
        config_only: stop the build after the config stage

    """
    # ToDo - this logic will have to change as more build functionality is implemented
    if not config_only:
        click.echo("Full build is not yet supported.")
    else:
        header_file_contents = generate_config_header_file(mbed_target, program_path)
        write_file(pathlib.Path(program_path), "mbed_config.h", header_file_contents)
        click.echo(f"The mbed_config.h file has been generated and successfully written to '{program_path}'.")
