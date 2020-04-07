#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
import pathlib
import os

from unittest import mock
from click.testing import CliRunner
from pyfakefs.fake_filesystem_unittest import TestCase

from mbed_build._internal.mbed_tools.export import export
from mbed_build._internal import templates


class TestExport(TestCase):
    @mock.patch("mbed_build._internal.mbed_tools.export.generate_cmakelists_file")
    def test_export(self, mock_generate_cmakelists_file):
        # This is needed to have access to the templates directory in Patcher filesystem.
        self.setUpPyfakefs()
        self.fs.add_real_directory(os.path.dirname(templates.__file__))

        mock_file_contents = "Hello world"
        mock_generate_cmakelists_file.return_value = mock_file_contents

        output_dir = "some-directory"
        mbed_os_path = "mbed-os"
        mbed_target = "K64F"
        toolchain = "GCC"

        runner = CliRunner()
        result = runner.invoke(export, ["-o", output_dir, "-t", toolchain, "-m", mbed_target, "-p", mbed_os_path])
        self.assertEqual(result.exit_code, 0)
        mock_generate_cmakelists_file.assert_called_once_with(mbed_target, mbed_os_path, toolchain)

        exported_file = pathlib.Path(output_dir, "CMakeLists.txt")
        self.assertEqual(exported_file.read_text(), mock_file_contents)
