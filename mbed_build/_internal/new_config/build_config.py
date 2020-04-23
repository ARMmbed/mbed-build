#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
import pathlib
from mbed_targets import get_target_by_board_type
from typing import Callable, List

from mbed_build._internal.new_config.config import Config, TargetMetadata
from mbed_build._internal.new_config.source import Source
from mbed_build._internal.find_files import find_files, filter_files, LabelFilter


def assemble_config(mbed_target: str, mbed_program_directory: pathlib.Path) -> Config:
    # Initial config is required to calculate first pass filters
    mbed_target_source = Source.from_target(mbed_target, mbed_program_directory)
    config = Config.from_sources([mbed_target_source])

    filters = _build_filters(config.target_metadata)
    all_mbed_lib_files = find_files("mbed_lib.json", mbed_program_directory)
    filtered_lib_files = filter_files(all_mbed_lib_files, filters)
    mbed_lib_sources = [Source.from_mbed_lib(file, config.target_metadata.labels) for file in filtered_lib_files]
    config = Config.from_sources([mbed_target_source] + mbed_lib_sources)
    return config


def _build_filters(target_metadata: TargetMetadata) -> List[Callable]:
    return [
        LabelFilter("TARGET", target_metadata.labels),
        LabelFilter("FEATURE", target_metadata.features),
        LabelFilter("COMPONENT", target_metadata.components),
    ]
