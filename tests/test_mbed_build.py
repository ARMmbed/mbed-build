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
    @mock.patch("mbed_build.mbed_build._fetch_target_labels")
    @mock.patch("mbed_build.mbed_build._fetch_toolchain_labels")
    @mock.patch("mbed_build.mbed_build.render_cmakelists_template")
    def test_correct_arguments_passed(self, render_cmakelists_template, _fetch_toolchain_labels, _fetch_target_labels):
        target_name = "Target"
        toolchain_name = "GCC"
        generate_cmakelists_file(target_name, toolchain_name)

        _fetch_target_labels.assert_called_once_with(target_name)
        _fetch_toolchain_labels.assert_called_once_with(toolchain_name)
        render_cmakelists_template.assert_called_once_with(
            _fetch_target_labels.return_value, _fetch_toolchain_labels.return_value
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
