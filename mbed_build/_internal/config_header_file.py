#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Module in charge of mbed_config.h file generation."""
import pathlib

import jinja2

from typing import Iterable, Any
from mbed_build._internal.config.config import Config
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


def ljust(value: Any, width: int) -> str:
    """Returns the string representation of a value left justified in a string of specified length."""
    return str(value).ljust(width)


def _render_config_header_template(config: Config) -> str:
    """Renders the mbed_config.h template with the correct config definitions.

    Args:
        config: a Config object containing the combined configuration data for the build

    Returns:
        The rendered contents of the template with the config definitions included.
    """
    options = list(config.options.values())
    macros = list(config.macros.values())
    context = {
        "options": sorted(options, key=lambda option: option.macro_name),
        "macros": sorted(macros, key=lambda macro: macro.name),
        "max_name_length": max(_max_attribute_length(options, "macro_name"), _max_attribute_length(macros, "name")),
        "max_value_length": max(_max_attribute_length(options, "value"), _max_attribute_length(macros, "value")),
    }
    env = jinja2.Environment(loader=jinja2.PackageLoader("mbed_build", str(TEMPLATES_DIRECTORY)))
    env.filters["ljust"] = ljust
    template = env.get_template(TEMPLATE_NAME)
    return template.render(context)


def _max_attribute_length(objects: Iterable[object], attribute: str) -> int:
    attrs = (getattr(o, attribute) for o in objects)
    try:
        return max(len(str(attr)) for attr in attrs if attr is not None)
    except ValueError:  # no attrs found
        return 0
