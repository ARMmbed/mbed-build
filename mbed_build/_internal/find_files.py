#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
from pathlib import Path
from typing import Iterable


def find_files(file_name, root_dir, exclude=[]) -> Iterable[Path]:
    found_files = Path(root_dir).rglob(file_name)

    def is_excluded(file):
        return any(fn(file) for fn in exclude)

    return (file for file in found_files if not is_excluded(file))
