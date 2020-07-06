#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
import pathlib
from unittest import TestCase, mock

from click.testing import CliRunner

from mbed_build._internal.mbed_tools.build import build


class TestBuild(TestCase):
    def test_full_build_temporary_message(self):
        runner = CliRunner()
        result = runner.invoke(build, ["-m", "k64F", "-p", "somewhere"])

        self.assertEqual(result.output, "Full build is not yet supported.\n")

    @mock.patch("mbed_build._internal.mbed_tools.build.generate_cmakelists_file")
    @mock.patch("mbed_build._internal.mbed_tools.build.generate_config_header_file")
    @mock.patch("mbed_build._internal.mbed_tools.build.write_file")
    def test_config_only(self, write_file, generate_config_header_file, generate_cmakelists_file):
        mbed_target = "K64F"
        program_path = "somewhere"
        toolchain = "GCC_ARM"
        runner = CliRunner()
        result = runner.invoke(build, ["-m", mbed_target, "-p", program_path, "--config-only"])

        self.assertEqual(
            result.output,
            "The mbed_config.h and CMakeLists.txt files have been generated and successfully written to "
            f"'{program_path}'.\n",
        )
        generate_config_header_file.assert_called_once_with(mbed_target, program_path)
        generate_cmakelists_file.assert_called_once_with(mbed_target, program_path, toolchain)
        write_file.assert_has_calls(
            [
                mock.call(pathlib.Path(program_path), "CMakeLists.txt", generate_cmakelists_file.return_value),
                mock.call(pathlib.Path(program_path), "mbed_config.h", generate_config_header_file.return_value),
            ]
        )
