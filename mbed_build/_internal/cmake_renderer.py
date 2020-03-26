#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
import pathlib

import jinja2

TEMPLATES_DIRECTORY = pathlib.Path("_internal", "templates")
TEMPLATE_NAME = "CMakeLists.tmpl"


def _render_cmakelists_template() -> str:
    """Loads the CMakeLists.txt file template and renders it with the correct details.

    Returns:
        The contents of the rendered CMakeLists.txt template.
    """

    env = jinja2.Environment(loader=jinja2.PackageLoader("mbed_build", str(TEMPLATES_DIRECTORY)),)
    template = env.get_template(TEMPLATE_NAME)
    context = {"hello": "Hello", "world": "World"}
    return template.render(context)


def write_cmakelists_file(output_directory: str) -> None:
    """Writes out the CMakeLists.txt file to the output directory.

    If the intermediate directories to the output directory don't exist,
    this function will create them.

    This function will overwrite any existing CMakeLists.txt file in the
    output directory.

    Args:
        output_directory: path to directory where we want the CMakeLists.txt to go
    """

    export_directory = pathlib.Path(output_directory)
    export_directory.mkdir(parents=True, exist_ok=True)

    output_file = export_directory.joinpath("CMakeLists.txt")
    output_file.write_text(_render_cmakelists_template())
