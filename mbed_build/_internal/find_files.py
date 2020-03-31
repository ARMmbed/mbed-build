#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
from pathlib import Path
from fnmatch import fnmatch
from typing import Iterable


def find_files(file_name: str, directory: str) -> Iterable[Path]:
    """Recursively find files under given directory."""
    return Path(directory).rglob(file_name)


def exclude_using_mbedignore(mbedignore_file: Path, files: Iterable[Path]) -> Iterable[Path]:
    """Filters out given Path objects based on `.mbedignore` rules.

    TODO: improve docs - mention that rules are rooted in mbedignore and use unix file matching
    """
    patterns = _build_mbedignore_patterns(mbedignore_file)
    return [file for file in files if not _matches_mbedignore_patterns(file, patterns)]


def exclude_not_labelled(label_type: str, allowed_label_values: Iterable[str], files: Iterable[Path]) -> Iterable[Path]:
    """Filters out given Path objects using target labelling rules.

    We distinguish three label types: TARGET, COMPONENT, FEATURE.

    An example of labelled path is "/mbed-os/rtos/source/TARGET_CORTEX/mbed_lib.json",
    where label type is "TARGET" and label value is "CORTEX".

    This function will filter out labelled paths that don't have matching values for given type.

       >>> exclude_not_labelled(label_type="COMPONENT", labels=["BAR"], files=[
       ...   pathlib.Path("/COMPONENT_FOO/COMPONENT_BAR/foo.txt"),
       ...   pathlib.Path("/COMPONENT_BAZ/bar.txt"),
       ...   pathlib.Path("/TARGET_X/x.txt"),
       ... ])
       >>> print(filtered)
    """

    result = []
    allowed_values = set(allowed_label_values)
    for file in files:
        label_values = set(_extract_label_values(file, label_type))
        if label_values.issubset(allowed_values):
            result.append(file)
    return result


def _build_mbedignore_patterns(mbedignore_file: Path) -> Iterable[str]:
    lines = mbedignore_file.read_text().splitlines()
    pattern_lines = (line for line in lines if line.strip() and not line.startswith("#"))
    ignore_root = mbedignore_file.parent
    patterns = tuple(str(ignore_root.joinpath(pattern)) for pattern in pattern_lines)
    return patterns


def _matches_mbedignore_patterns(file: Path, patterns: Iterable[str]) -> bool:
    stringified = str(file)
    return any(fnmatch(stringified, pattern) for pattern in patterns)


def _is_labelled(file: Path, label_type: str) -> bool:
    return f"{label_type}_" in str(file)


def _extract_label_values(file: Path, label_type: str) -> Iterable[str]:
    return (part for part in file.parts if label_type in part)
