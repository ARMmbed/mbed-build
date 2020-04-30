#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Write out the computed configuration for a build."""
import json
import pathlib
from typing import Dict, Any, List

import click
from tabulate import tabulate

from mbed_build._internal.config.assemble_build_config import assemble_config
from mbed_build._internal.config.config import Config, Option, Macro


@click.command(help="Print the computed configuration for a build.")
@click.option("-m", "--mbed-target", required=True, help="A build target for an Mbed-enabled device, eg. K64F")
@click.option(
    "-p",
    "--program-path",
    type=click.Path(),
    default=".",
    help="Path to local Mbed program. By default is the current working directory.",
)
@click.option(
    "--format",
    type=click.Choice(["table", "json", "legacy"]),
    default="table",
    show_default=True,
    help="Set output format. To see maximum info use JSON format.",
)
def config(mbed_target: str, program_path: str, format: str) -> None:
    """Calculates the configuration for a build and prints it out.

    Each build of an Mbed program requires calculating the combined configuration
    taken from the target definition in targets.json and mbed_lib.json files in
    Mbed OS library and the program's own mbed_config.json config overrides file.

    This command prints out the combined config taking all these sources into account.

    Args:
        mbed_target: the build target you are wanting to run your app (eg. K64F)
        program_path: the path to the Mbed program
        format: the format to print the resulting config data

    """
    config = assemble_config(mbed_target, pathlib.Path(program_path))
    output_builders = {
        "table": _build_tabular_output,
        "json": _build_json_output,
        "legacy": _build_legacy_output,
    }
    output = output_builders[format](config)
    click.echo(output)


def _build_tabular_output(config: Config) -> str:
    parameter_table_headers = ["key", "macro name", "value"]

    parameters_data = []
    for option in _config_options_sorted_by_key(config):
        parameters_data.append([option.key, option.macro_name, option.value])
    parameters_table = tabulate(parameters_data, parameter_table_headers)

    macros_table_headers = ["name", "value"]
    macros_data = [[macro.name, macro.value] for macro in _config_macros_sorted_by_name(config)]
    macros_table = tabulate(macros_data, macros_table_headers)

    output_template = (
        "PARAMETER CONFIGURATION\n"
        "-----------------------\n"
        f"{parameters_table}\n"
        "\n"
        "MACRO CONFIGURATION\n"
        "-------------------\n"
        f"{macros_table}"
    )

    return output_template


def _build_json_output(config: Config) -> str:
    config_object: Dict[str, Any] = {"parameters": [], "macros": []}

    for option in _config_options_sorted_by_key(config):
        config_object["parameters"].append(
            {
                "key": option.key,
                "macro_name": option.macro_name,
                "value": option.value,
                "help_text": option.help_text,
                "set_by": option.set_by,
            }
        )

    for macro in _config_macros_sorted_by_name(config):
        config_object["macros"].append({"name": macro.name, "value": macro.value, "set_by": macro.set_by})

    return json.dumps(config_object, indent=4)


def _build_legacy_output(config: Config) -> str:
    """Output format to match that of legacy tools running mbed compile --config."""
    parameter_list = ""
    for option in _config_options_sorted_by_key(config):
        if option.value is not None:
            parameter_list += f'{option.key} = {option.value} (macro name: "{option.macro_name}")\n'
        else:
            parameter_list += f"{option.key} has no value\n"

    macro_list = ""
    for macro in _config_macros_sorted_by_name(config):
        if macro.value is not None:
            macro_list += f"{macro.name}={macro.value}\n"
        else:
            macro_list += f"{macro.name}\n"

    output_template = (
        "Configuration parameters\n"
        "------------------------\n"
        f"{parameter_list}\n"
        "\n"
        "Macros\n"
        "------\n"
        f"{macro_list}"
    )
    return output_template


def _config_options_sorted_by_key(config: Config) -> List[Option]:
    return sorted(config.options.values(), key=lambda item: item.key)


def _config_macros_sorted_by_name(config: Config) -> List[Macro]:
    return sorted(config.macros.values(), key=lambda item: item.name)
