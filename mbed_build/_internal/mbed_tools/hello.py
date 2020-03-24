#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Hello command."""
import click


@click.command()
def hello():
    """Prints Hello."""
    click.echo("Hello.")
