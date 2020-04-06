#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
from pathlib import Path
from unittest import TestCase, mock

from mbed_build._internal.mbed_lib import find_mbed_lib_files


class TestFindMbedLibFiles(TestCase):
    @mock.patch("mbed_build._internal.mbed_lib.find_files", autospec=True)
    @mock.patch("mbed_build._internal.mbed_lib.BoardLabelFilter", autospec=True)
    @mock.patch("mbed_build._internal.mbed_lib.MbedignoreFilter", autospec=True)
    def test_finds_mbed_lib_files_using_appropriate_filters(self, MbedignoreFilter, BoardLabelFilter, find_files):
        mbed_program_directory = Path("some-program")
        board_type = "K64F"

        subject = find_mbed_lib_files(mbed_program_directory, board_type)

        self.assertEqual(subject, find_files.return_value)
        find_files.assert_called_once_with(
            "mbed_lib.json", mbed_program_directory, [MbedignoreFilter.return_value, BoardLabelFilter.return_value]
        )
        MbedignoreFilter.assert_called_once_with(("*/TESTS", "*/TEST_APPS"))
        BoardLabelFilter.assert_called_once_with(board_type, mbed_program_directory)
