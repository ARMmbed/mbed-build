#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
from pathlib import Path
from unittest import TestCase, mock

from mbed_build._internal.mbed_lib import find_mbed_lib_files


class TestFindMbedLibFiles(TestCase):
    @mock.patch("mbed_build._internal.mbed_lib.find_files", autospec=True)
    @mock.patch("mbed_build._internal.mbed_lib.exclude_using_mbedignore", autospec=True)
    @mock.patch("mbed_build._internal.mbed_lib.exclude_using_target_labels", autospec=True)
    @mock.patch("mbed_build._internal.mbed_lib.exclude_legacy_directories", autospec=True)
    def test_filters_mbed_lib_json_paths_using_exclusion_rules(
        self, exclude_legacy_directories, exclude_using_target_labels, exclude_using_mbedignore, find_files
    ):
        mbed_program_directory = Path("some-program")
        board_type = "K64F"

        subject = find_mbed_lib_files(mbed_program_directory, board_type)

        self.assertEqual(subject, exclude_using_target_labels.return_value)
        find_files.assert_called_once_with("mbed_lib.json", mbed_program_directory)

        exclude_legacy_directories.assert_called_once_with(find_files.return_value)
        exclude_using_mbedignore.assert_called_once_with(
            mbed_program_directory, exclude_legacy_directories.return_value
        )
        exclude_using_target_labels.assert_called_once_with(
            mbed_program_directory, board_type, exclude_using_mbedignore.return_value
        )
