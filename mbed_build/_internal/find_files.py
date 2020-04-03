#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""File scanner."""
from pathlib import Path
from fnmatch import fnmatch
from typing import Iterable, List
from mbed_targets import get_build_attributes_by_board_type


def find_files(file_name: str, directory: Path) -> Iterable[Path]:
    """Recursively find files matching name under given directory."""
    return directory.rglob(file_name)


_LEGACY_DIRS = [
    "TEST",
    "TEST_APPS",
]


def exclude_legacy_directories(paths: Iterable[Path]) -> List[Path]:
    """Filter out given paths using legacy directory list.

    WARNING: This should be removed when mbed-os is cleaned up
    """
    return [path for path in paths if not any(legacy_dir in str(path) for legacy_dir in _LEGACY_DIRS)]


def exclude_using_mbedignore(directory: Path, paths: Iterable[Path]) -> List[Path]:
    """Filter out given paths based on rules found in .mbedignore files.

    Patterns in .mbedignore use unix shell-style wildcards (fnmatch). It means
    that functionality, although similar is different to that found in
    .gitignore and friends.

    Args:
        mbedignore_file: Path to .mbedignore.
        paths: Paths to filter.

    Returns:
        List of paths.
    """
    result = list(paths)
    mbedignore_paths = find_files(".mbedignore", directory)
    for mbedignore_path in mbedignore_paths:
        patterns = _build_mbedignore_patterns(mbedignore_path)
        result = [path for path in result if not _matches_mbedignore_patterns(path, patterns)]
    return result


def exclude_using_target_labels(mbed_program_directory: Path, board_type: str, paths: Iterable[Path]) -> List[Path]:
    """Filter out given paths using target labels retrieved from mbed-targets.

    Args:
        mbed_program_directory: Path to mbed program, used by mbed-targets to retrieve target build attributes.
        board_type: Board type, used by mbed-targets to retrieve target build attributes.
        paths: Paths to filter.
    """
    build_attributes = get_build_attributes_by_board_type(board_type, mbed_program_directory)
    result = list(paths)
    result = exclude_using_labels("TARGET", build_attributes.labels, result)
    result = exclude_using_labels("FEATURE", build_attributes.features, result)
    result = exclude_using_labels("COMPONENT", build_attributes.components, result)
    return result


def exclude_using_labels(label_type: str, allowed_label_values: Iterable[str], paths: Iterable[Path]) -> List[Path]:
    """Filter out given path objects using path labelling rules.

    If a path is labelled with given type, but contains label value which is
    not allowed, it will be filtered out.

    An example of labelled path is "/mbed-os/rtos/source/TARGET_CORTEX/mbed_lib.json",
    where label type is "TARGET" and label value is "CORTEX".

    For example, given a label type "FEATURE" and allowed values ["FOO"]:
    - "/path/FEATURE_FOO/somefile.txt" will not be filtered out
    - "/path/FEATURE_BAZ/somefile.txt" will be filtered out
    - "/path/FEATURE_FOO/FEATURE_BAR/somefile.txt" will be filtered out

    Args:
        label_type: Type of label.
        allowed_label_values: Labels which are allowed for given type.
        paths: Paths to filter.
    """
    result = []
    allowed_labels = set(f"{label_type}_{label_value}" for label_value in allowed_label_values)
    for path in paths:
        labels = set(part for part in path.parts if label_type in part)
        if labels.issubset(allowed_labels):
            result.append(path)
    return result


def _build_mbedignore_patterns(mbedignore_path: Path) -> Iterable[str]:
    """Return patterns extracted from .mbedignore file.

    Filters out commented out and empty lines.
    Prefixes each rule with the directory location of the .mbedignore file.

    Args:
        mbedignore_path: Path to .mbedignore.
    """
    lines = mbedignore_path.read_text().splitlines()
    pattern_lines = (line for line in lines if line.strip() and not line.startswith("#"))
    ignore_root = mbedignore_path.parent
    patterns = tuple(str(ignore_root.joinpath(pattern)) for pattern in pattern_lines)
    return patterns


def _matches_mbedignore_patterns(path: Path, patterns: Iterable[str]) -> bool:
    """Check if given path matches one of the .mbedignore patterns."""
    stringified = str(path)
    return any(fnmatch(stringified, pattern) for pattern in patterns)
