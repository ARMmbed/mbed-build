#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Configuration assembly algorithm."""
import itertools
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Set

from mbed_build._internal.config.config import Config
from mbed_build._internal.config.cumulative_data import CumulativeData
from mbed_build._internal.config.source import Source
from mbed_build._internal.find_files import LabelFilter, filter_files, find_files


@dataclass
class BuildConfig:
    """Representation of build configuration."""

    config: Config
    macros: Set[str]


def assemble_config(mbed_target: str, mbed_program_directory: Path) -> BuildConfig:
    """Assemble BuildConfig for given target and program directory.

    The structure and configuration of MbedOS requires us to do multiple passes over
    configuration files, as each pass might affect which configuration files should be included
    in the final configuration.
    """
    target_source = Source.from_target(mbed_target, mbed_program_directory)
    mbed_lib_files = find_files("mbed_lib.json", mbed_program_directory)
    return _assemble_config(target_source, mbed_lib_files)


def _assemble_config(target_source: Source, mbed_lib_files: Iterable[Path]) -> BuildConfig:
    previous_cumulative_data = None
    current_cumulative_data = CumulativeData.from_sources([target_source])
    while True:
        filtered_files = _filter_files(mbed_lib_files, current_cumulative_data)
        mbed_lib_sources = [Source.from_mbed_lib(file, current_cumulative_data.labels) for file in filtered_files]
        all_sources = list(itertools.chain([target_source], mbed_lib_sources))
        previous_cumulative_data = current_cumulative_data
        current_cumulative_data = CumulativeData.from_sources(all_sources)

        if previous_cumulative_data == current_cumulative_data:
            break

    config = Config.from_sources(all_sources)
    return BuildConfig(config=config, macros=current_cumulative_data.macros)


def _filter_files(files: Iterable[Path], cumulative_data: CumulativeData) -> Iterable[Path]:
    filters = (
        LabelFilter("TARGET", cumulative_data.labels),
        LabelFilter("FEATURE", cumulative_data.features),
        LabelFilter("COMPONENT", cumulative_data.components),
    )
    return filter_files(files, filters)