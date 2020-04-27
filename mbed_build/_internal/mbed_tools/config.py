#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Write out the computed configuration for a build."""
import json
import pathlib
from typing import Dict, Any

import click
from tabulate import tabulate

from mbed_build._internal.config.assemble_build_config import assemble_config, BuildConfig


@click.command(help="Print the computed configuration for a build.")
@click.option("-m", "--mbed_target", required=True, help="A build target for an Mbed-enabled device, eg. K64F")
@click.option(
    "-p",
    "--project-path",
    type=click.Path(),
    default=".",
    help="Path to local Mbed project. By default is the current working directory.",
)
@click.option(
    "--format",
    type=click.Choice(["table", "json", "legacy"]),
    default="table",
    show_default=True,
    help="Set output format. To see maximum info use JSON format.",
)
def config(mbed_target: str, project_path: str, format: str) -> None:
    """Calculates the configuration for a build and prints it out.

    Each build of an Mbed project requires calculating the combined configuration
    taken from the target definition in targets.json and mbed_lib.json files in
    Mbed OS library and the project's own mbed_config.json config overrides file.

    This command prints out the combined config taking all these sources into account.

    Args:
        mbed_target: the build target you are wanting to run your app (eg. K64F)
        project_path: the path to the Mbed project
        format: the format to print the resulting config data

    """
    build_config = assemble_config(mbed_target, pathlib.Path(project_path))
    output_builders = {
        "table": _build_tabular_output,
        "json": _build_json_output,
        "legacy": _build_legacy_output,
    }
    output = output_builders[format](build_config)
    click.echo(output)


def _build_tabular_output(config_data: BuildConfig) -> str:
    parameter_table_headers = ["key", "macro name", "value"]

    parameters_data = []
    for _, option in sorted(config_data.config.options.items(), key=lambda item: item[1].key):
        parameters_data.append([option.key, option.macro_name, option.value])
    parameters_table = tabulate(parameters_data, parameter_table_headers)

    macros_table_headers = ["name", "value"]
    macros_data = [[macro, ""] for macro in config_data.macros]
    macros_table = tabulate(macros_data, macros_table_headers)

    output_template = (
        f"PARAMETER CONFIGURATION\n"
        f"-----------------------\n"
        f"{parameters_table}\n"
        f"\n"
        f"MACRO CONFIGURATION\n"
        f"-------------------\n"
        f"{macros_table}"
    )

    return output_template


def _build_json_output(config_data: BuildConfig) -> str:
    config: Dict[str, Any] = {"parameters": [], "macros": []}

    for _, option in sorted(config_data.config.options.items(), key=lambda item: item[1].key):
        config["parameters"].append(
            {
                "key": option.key,
                "macro_name": option.macro_name,
                "value": option.value,
                "help_text": option.help_text,
                "set_by": option.set_by,
            }
        )

    for macro in config_data.macros:
        config["macros"].append({"name": macro})

    return json.dumps(config, indent=4)


def _build_legacy_output(config_data: BuildConfig) -> str:
    """Output format to match that of legacy tools running mbed compile --config."""
    parameter_list = ""
    for _, option in sorted(config_data.config.options.items(), key=lambda item: item[1].key):
        if option.value:
            parameter_list += f'{option.key} = {option.value} (macro name: "{option.macro_name}")\n'
        else:
            parameter_list += f"{option.key} has no value\n"

    macro_list = ""
    for macro in config_data.macros:
        macro_list += f"{macro}\n"

    output_template = (
        f"Configuration parameters\n"
        f"------------------------\n"
        f"{parameter_list}\n"
        f"\n"
        f"Macros\n"
        f"------\n"
        f"{macro_list}"
    )
    return output_template
