#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
from unittest import TestCase, mock

from mbed_build._internal.cmake_file import generate_cmakelists_file, _render_cmakelists_template


class TestGenerateCMakeListsFile(TestCase):
    @mock.patch("mbed_build._internal.cmake_file.get_target_by_name")
    def test_correct_arguments_passed(self, get_target_by_name):
        target = mock.Mock()
        target.labels = ["foo"]
        target.features = ["bar"]
        target.components = ["baz"]
        get_target_by_name.return_value = target
        mbed_target = "K64F"
        program_path = "blinky"
        toolchain_name = "GCC"

        result = generate_cmakelists_file(mbed_target, program_path, toolchain_name)

        get_target_by_name.assert_called_once_with(mbed_target, program_path)
        self.assertEqual(
            result,
            _render_cmakelists_template(
                get_target_by_name.return_value.labels,
                get_target_by_name.return_value.features,
                get_target_by_name.return_value.components,
                toolchain_name,
            ),
        )


class TestRendersCMakeListsFile(TestCase):
    def test_returns_rendered_content(self):
        target_labels = ["foo", "bar"]
        feature_labels = ["foo", "bar"]
        component_labels = ["foo", "bar"]
        toolchain_name = "baz"
        result = _render_cmakelists_template(target_labels, feature_labels, component_labels, toolchain_name)

        for label in target_labels + feature_labels + component_labels + [toolchain_name]:
            self.assertIn(label, result)
