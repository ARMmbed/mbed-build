#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Module in charge of CMake file generation."""
import pathlib
from typing import Iterable

import jinja2
from mbed_targets import get_target_by_name

TEMPLATES_DIRECTORY = pathlib.Path("_internal", "templates")
TEMPLATE_NAME = "CMakeLists.tmpl"


def generate_cmakelists_file(mbed_target: str, program_path: str, toolchain_name: str) -> str:
    """Generate the top-level CMakeLists.txt file containing the correct definitions for a build.

    Args:
        mbed_target: the target the application is being built for
        program_path: the path to the local Mbed program
        toolchain_name: the toolchain to be used to build the application

    Returns:
        A string of rendered contents for the file.
    """
    target_build_attributes = get_target_by_name(mbed_target, program_path)
    return _render_cmakelists_template(
        target_build_attributes.labels,
        target_build_attributes.features,
        target_build_attributes.components,
        toolchain_name,
    )


def _render_cmakelists_template(
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
