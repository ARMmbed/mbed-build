#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Entrypoint for development purposes."""
import click
from mbed_build.mbed_tools import config, export


@click.group()
def cli():
    pass


cli.add_command(config)
cli.add_command(export)

cli()
