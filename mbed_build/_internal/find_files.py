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
    """Filters out given Path objects based on `.mbedignore` rules."""
    patterns = _build_mbedignore_patterns(mbedignore_file)
    return (file for file in files if not _matches_patterns(file, patterns))


def _build_mbedignore_patterns(mbedignore_file: Path) -> Iterable[str]:
    lines = mbedignore_file.read_text().splitlines()
    pattern_lines = (line for line in lines if line.strip() and not line.startswith("#"))
    ignore_root = mbedignore_file.parent
    patterns = tuple(str(ignore_root.joinpath(pattern)) for pattern in pattern_lines)
    return patterns


def _matches_patterns(file: Path, patterns: Iterable[str]) -> bool:
    stringified = str(file)
    return any(fnmatch(stringified, pattern) for pattern in patterns)
