#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
import pathlib
import tempfile
from unittest import TestCase, mock

from mbed_build.exceptions import InvalidExportOutputDirectory
from mbed_build.mbed_build import generate_cmakelists_file, export_cmakelists_file


class TestGenerateCMakeListsFile(TestCase):
    @mock.patch("mbed_build.mbed_build.render_cmakelists_template")
    @mock.patch("mbed_build.mbed_build.get_target_by_name")
    def test_correct_arguments_passed(self, get_target_by_name, render_cmakelists_template):
        target = mock.Mock()
        get_target_by_name.return_value = target
        mbed_target = "K64F"
        project_path = "blinky"
        toolchain_name = "GCC"

        generate_cmakelists_file(mbed_target, project_path, toolchain_name)

        get_target_by_name.assert_called_once_with(mbed_target, project_path)
        render_cmakelists_template.assert_called_once_with(
            target.labels, target.features, target.components, toolchain_name,
        )


class TestExportCMakeListsFile(TestCase):
    def test_export_dir_is_file(self):
        with tempfile.TemporaryDirectory() as directory:
            bad_export_dir = pathlib.Path(directory, "some_file.txt")
            bad_export_dir.touch()
            with self.assertRaises(InvalidExportOutputDirectory):
                export_cmakelists_file(bad_export_dir, "some contents")

    @mock.patch("mbed_build.mbed_build.write_cmakelists_file")
    def test_correct_arguments_passed(self, write_cmakelists_file):
        fake_dir = pathlib.Path("some_directory")
        contents = "some file contents"
        export_cmakelists_file(fake_dir, contents)

        write_cmakelists_file.assert_called_once_with(fake_dir, contents)
