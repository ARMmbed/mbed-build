#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
from pathlib import Path
from fnmatch import fnmatch
from typing import Callable, Iterable


ExcludeCallable = Callable[[Path], bool]


def find_files(file_name: str, root_dir: str, exclude: Iterable[ExcludeCallable] = []) -> Iterable[Path]:
    found_files = Path(root_dir).rglob(file_name)

    def is_excluded(file):
        return any(fn(file) for fn in exclude)

    return (file for file in found_files if not is_excluded(file))


def exclude_listed_in_mbedignore(path_to_ignore_file: Path) -> bool:
    lines = path_to_ignore_file.read_text().splitlines()
    pattern_lines = (line for line in lines if line.strip() and not line.startswith("#"))
    ignore_root = path_to_ignore_file.parent

    patterns = tuple(str(ignore_root.joinpath(pattern)) for pattern in pattern_lines)

    def is_excluded(file: Path):
        is_ignored = any(fnmatch(file, pattern) for pattern in patterns)
        return is_ignored

    return is_excluded
