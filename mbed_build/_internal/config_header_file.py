#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Module in charge of mbed_config.h file generation."""
import pathlib

import jinja2

from typing import List
from mbed_build._internal.config.config import Config, Option, Macro
from mbed_build._internal.config.assemble_build_config import assemble_config

TEMPLATES_DIRECTORY = pathlib.Path("_internal", "templates")
TEMPLATE_NAME = "mbed_config.tmpl"


def generate_config_header_file(mbed_target: str, program_path: str) -> str:
    """Generate the program's mbed_config.h file containing the configuration definitions.

    Args:
        mbed_target: the target the application is being built for
        program_path: the path to the local Mbed program

    Returns:
        A string of rendered contents for the file.
    """
    config = assemble_config(mbed_target, pathlib.Path(program_path))
    return _render_config_header_template(config)


def _render_config_header_template(config: Config) -> str:
    """Renders the mbed_config.h template with the correct config definitions.

    Args:
        config: a Config object containing the combined configuration data for the build

    Returns:
        The rendered contents of the template with the config definitions included.
    """
    context = {
        "options": sorted(
            [(option.macro_name, str(option.value), option.set_by) for option in config.options.values()]
        ),
        "macros": sorted([(m.name, str(m.value or ""), m.set_by) for m in config.macros.values()]),
        "max_name_length": _max_field_length(
            list(config.options.values()), "macro_name", list(config.macros.values()), "name"
        ),
        "max_value_length": _max_field_length(
            list(config.options.values()), "value", list(config.macros.values()), "value"
        ),
    }
    env = jinja2.Environment(loader=jinja2.PackageLoader("mbed_build", str(TEMPLATES_DIRECTORY)))
    template = env.get_template(TEMPLATE_NAME)
    return template.render(context)


def _max_field_length(options: List[Option], option_field: str, macros: List[Macro], macro_field: str) -> int:
    option_elements = [str(getattr(o, option_field)) for o in options if getattr(o, option_field) is not None]
    macro_elements = [str(getattr(m, macro_field)) for m in macros if getattr(m, macro_field) is not None]
    return max([len(o) for o in option_elements + macro_elements] + [0])
