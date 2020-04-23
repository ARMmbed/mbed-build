#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
import pathlib
import tempfile
from unittest import TestCase

from mbed_build._internal.cmake_file import render_cmakelists_template, write_cmakelists_file


class TestRendersCMakeListsFile(TestCase):
    def test_returns_rendered_content(self):
        target_labels = ["foo", "bar"]
        feature_labels = ["foo", "bar"]
        component_labels = ["foo", "bar"]
        toolchain_name = "baz"
        result = render_cmakelists_template(target_labels, feature_labels, component_labels, toolchain_name)

        for label in target_labels + feature_labels + component_labels + [toolchain_name]:
            self.assertIn(label, result)


class TestWriteCMakeListsFile(TestCase):
    def test_writes_content_to_file(self):
        with tempfile.TemporaryDirectory() as directory:
            content = "Some rendered content"
            export_path = pathlib.Path(directory, "output")

            write_cmakelists_file(export_path, content)

            created_file = pathlib.Path(export_path, "CMakeLists.txt")
            self.assertTrue(created_file.is_file())
            self.assertEqual(created_file.read_text(), content)
