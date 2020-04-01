#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
from pathlib import Path
from fnmatch import fnmatch
from typing import Iterable


def find_files(file_name: str, directory: Path) -> Iterable[Path]:
    """Recursively find files matching name under given directory."""
    return directory.rglob(file_name)


def exclude_using_mbedignore(mbedignore_path: Path, paths: Iterable[Path]) -> Iterable[Path]:
    """Filter out given paths based on rules found in .mbedignore file.

    Patterns in .mbedignore use unix shell-style wildcards (fnmatch). It means
    that functionality, although similar is different to that found in
    .gitignore and friends.

    Args:
        mbedignore_file: Path to .mbedignore.
        paths: Paths to filter.
    """
    patterns = _build_mbedignore_patterns(mbedignore_path)
    return [path for path in paths if not _matches_mbedignore_patterns(path, patterns)]


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
