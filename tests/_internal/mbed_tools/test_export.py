#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
import pathlib
from unittest import TestCase, mock

from click.testing import CliRunner

from mbed_build._internal.mbed_tools.export import export


class TestExport(TestCase):
    @mock.patch("mbed_build._internal.mbed_tools.export.click.echo")
    @mock.patch("mbed_build._internal.mbed_tools.export.generate_cmakelists_file")
    @mock.patch("mbed_build._internal.mbed_tools.export.write_cmakelists_file")
    def test_export(self, mock_write_cmakelists_file, mock_generate_cmakelists_file, mock_echo):
        mock_file_contents = "Hello world"
        mock_generate_cmakelists_file.return_value = mock_file_contents
        output_dir = "some-directory"
        project_path = "blinky"
        mbed_target = "K64F"
        toolchain = "GCC"

        runner = CliRunner()
        result = runner.invoke(export, ["-o", output_dir, "-t", toolchain, "-m", mbed_target, "-p", project_path])

        self.assertEqual(result.exit_code, 0)
        mock_generate_cmakelists_file.assert_called_once_with(mbed_target, project_path, toolchain)
        mock_write_cmakelists_file.assert_called_once_with(
            pathlib.Path(output_dir), mock_generate_cmakelists_file.return_value
        )
        mock_echo.assert_called_once_with(
            f"The program-level CMake file has been successfully exported to directory '{str(output_dir)}'"
        )

    @mock.patch("mbed_build._internal.mbed_tools.export.click.echo")
    @mock.patch("mbed_build._internal.mbed_tools.export.generate_cmakelists_file")
    @mock.patch("mbed_build._internal.mbed_tools.export.write_cmakelists_file")
    def test_export_default_project_path(self, mock_write_cmakelists_file, mock_generate_cmakelists_file, mock_echo):
        mock_file_contents = "Hello world"
        mock_generate_cmakelists_file.return_value = mock_file_contents
        output_dir = "some-directory"
        mbed_target = "K64F"
        toolchain = "GCC"

        runner = CliRunner()
        result = runner.invoke(export, ["-o", output_dir, "-t", toolchain, "-m", mbed_target])

        self.assertEqual(result.exit_code, 0)
        mock_generate_cmakelists_file.assert_called_once_with(mbed_target, ".", toolchain)
        mock_write_cmakelists_file.assert_called_once_with(
            pathlib.Path(output_dir), mock_generate_cmakelists_file.return_value
        )
        mock_echo.assert_called_once_with(
            f"The program-level CMake file has been successfully exported to directory '{str(output_dir)}'"
        )
