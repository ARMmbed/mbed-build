#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
import pathlib
import os

from click.testing import CliRunner
from pyfakefs.fake_filesystem_unittest import TestCase

from mbed_build._internal.mbed_tools.export import export
from mbed_build._internal import templates


class TestExport(TestCase):
    templates_directory = os.path.dirname(templates.__file__)

    def test_export(self):
        """This is needed to have access to the templates directory in Patcher filesystem."""
        self.setUpPyfakefs()
        self.fs.add_real_directory(self.templates_directory)

        output_dir = "some_directory"
        mbed_target = "K64F"
        mbed_toolchain = "GCC"

        runner = CliRunner()
        result = runner.invoke(export, ["-o", output_dir, "-t", mbed_toolchain, "-m", mbed_target])
        self.assertEqual(result.exit_code, 0)

        exported_file = pathlib.Path(output_dir, "CMakeLists.txt")
        text = exported_file.read_text()
        self.assertIn(mbed_target, text)
        self.assertIn(mbed_toolchain, text)
