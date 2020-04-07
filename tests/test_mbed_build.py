#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
import pathlib
from unittest import TestCase, mock

from pyfakefs.fake_filesystem_unittest import Patcher
from mbed_build.exceptions import InvalidExportOutputDirectory
from mbed_build.mbed_build import generate_cmakelists_file, export_cmakelists_file


class TestGenerateCMakeListsFile(TestCase):
    @mock.patch("mbed_build.mbed_build._fetch_toolchain_labels")
    @mock.patch("mbed_build.mbed_build.render_cmakelists_template")
    @mock.patch("mbed_build.mbed_build.get_build_attributes_by_board_type")
    def test_correct_arguments_passed(self, get_build_attributes_by_board_type, render_cmakelists_template, _fetch_toolchain_labels):
        target_build_attributes = mock.Mock()
        get_build_attributes_by_board_type.return_value = target_build_attributes
        mbed_target = "K64F"
        mbed_os_path = "mbed-os"
        toolchain_name = "GCC"

        generate_cmakelists_file(mbed_target, mbed_os_path, toolchain_name)

        get_build_attributes_by_board_type.assert_called_once_with(mbed_target, mbed_os_path)
        _fetch_toolchain_labels.assert_called_once_with(toolchain_name)
        render_cmakelists_template.assert_called_once_with(
            target_build_attributes.labels,
            target_build_attributes.features,
            target_build_attributes.components,
            _fetch_toolchain_labels.return_value,
        )


class TestExportCMakeListsFile(TestCase):
    def test_export_dir_is_file(self):
        with Patcher():
            fake_dir = pathlib.Path("some_directory")
            fake_dir.mkdir(parents=True, exist_ok=True)
            bad_export_dir = pathlib.Path(fake_dir, "some_file.txt")
            bad_export_dir.touch()
            with self.assertRaises(InvalidExportOutputDirectory):
                export_cmakelists_file(bad_export_dir, "some contents")

    @mock.patch("mbed_build.mbed_build.write_cmakelists_file")
    def test_correct_arguments_passed(self, write_cmakelists_file):
        fake_dir = pathlib.Path("some_directory")
        contents = "some file contents"
        export_cmakelists_file(fake_dir, contents)

        write_cmakelists_file.assert_called_once_with(fake_dir, contents)
