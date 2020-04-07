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
    @mock.patch("mbed_build._internal.mbed_tools.export.get_build_attributes_by_board_type")
    def test_export(self, mock_get_build_attributes):
        # This is needed to have access to the templates directory in Patcher filesystem.
        self.setUpPyfakefs()
        self.fs.add_real_directory(os.path.dirname(templates.__file__))

        mock_build_attributes = mock.Mock()
        mock_build_attributes.labels = frozenset(["label"])
        mock_build_attributes.features = frozenset(["feature"])
        mock_build_attributes.components = frozenset(["component"])
        mock_get_build_attributes.return_value = mock_build_attributes

        output_dir = "some_directory"
        mbed_os_path = "mbed-os"
        mbed_target = "K64F"
        mbed_toolchain = "GCC"

        runner = CliRunner()
        result = runner.invoke(
            export, ["-o", output_dir, "-t", mbed_toolchain, "-m", mbed_target, "-p", mbed_os_path]
        )
        self.assertEqual(result.exit_code, 0)

        exported_file = pathlib.Path(output_dir, "CMakeLists.txt")
        self.assertTrue(exported_file.is_file())
