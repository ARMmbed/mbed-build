#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
import pathlib
from pyfakefs.fake_filesystem_unittest import Patcher
from unittest import TestCase, mock
from mbed_build._internal.cmake_renderer import _render_cmakelists_template, write_cmakelists_file


class TestWriteCMakeListsFile(TestCase):
    @mock.patch("mbed_build._internal.cmake_renderer._render_cmakelists_template")
    def test_writes_content_to_file(self, _render_cmakelists_template):
        with Patcher():
            content = "Some rendered content"
            _render_cmakelists_template.return_value = content
            export_path = pathlib.Path("tests", "output")

            write_cmakelists_file(str(export_path))

            created_file = pathlib.Path(export_path, "CMakeLists.txt")
            self.assertTrue(created_file.is_file())
            self.assertEqual(created_file.read_text(), content)


class TestRendersCMakeListsFile(TestCase):
    def test_returns_rendered_content(self):
        result = _render_cmakelists_template()

        self.assertEqual(result, "Hello World")
