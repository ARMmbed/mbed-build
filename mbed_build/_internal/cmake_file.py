#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Module in charge of CMake file generation."""
import pathlib
from typing import Iterable

import jinja2

TEMPLATES_DIRECTORY = pathlib.Path("_internal", "templates")
TEMPLATE_NAME = "CMakeLists.tmpl"


def render_cmakelists_template(
    target_labels: Iterable[str], feature_labels: Iterable[str], component_labels: Iterable[str], toolchain_name: str,
) -> str:
    """Loads the CMakeLists.txt file template and renders it with the correct details.

    Args:
        target_labels: target-specific magic mbed-os directory names that need to be included in the build
        feature_labels: target-specific magic mbed-os feature directory names that need to be included in the build
        component_labels: target-specific magic mbed-os component directory names that need to be included in the build
        toolchain_name: the toolchain-specific magic mbed-os directory name that need to be included in the build

    Returns:
        The contents of the rendered CMake file.
    """
    env = jinja2.Environment(loader=jinja2.PackageLoader("mbed_build", str(TEMPLATES_DIRECTORY)),)
    template = env.get_template(TEMPLATE_NAME)
    context = {
        "target_labels": target_labels,
        "feature_labels": feature_labels,
        "component_labels": component_labels,
        "toolchain_name": toolchain_name,
    }
    return template.render(context)


def write_cmakelists_file(output_directory: pathlib.Path, file_contents: str) -> None:
    """Writes out the CMakeLists.txt file to the output directory.

    If the intermediate directories to the output directory don't exist,
    this function will create them.

    This function will overwrite any existing CMakeLists.txt file in the
    output directory.

    Args:
        output_directory: path to directory where we want the CMakeLists.txt to go
        file_contents: the contents of the CMakeLists.txt file
    """
    output_directory.mkdir(parents=True, exist_ok=True)
    output_file = output_directory.joinpath("CMakeLists.txt")
    output_file.write_text(file_contents)
