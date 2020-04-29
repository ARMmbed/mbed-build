#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Entrypoint for development purposes."""
import click
from mbed_build.mbed_tools import build, config, export


@click.group()
def cli() -> None:
    """Group exposing the commands from the mbed-build package."""
    pass


cli.add_command(config)
cli.add_command(export)
cli.add_command(build)

cli()
