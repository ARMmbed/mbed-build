#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
from unittest import TestCase

from mbed_build._internal.cmake_renderer import render_cmakelists_template


class TestRendersCMakeListsFile(TestCase):
    def test_returns_rendered_content(self):
        target_labels = ["foo", "bar"]
        toolchain_labels = ["baz"]
        result = render_cmakelists_template(target_labels, toolchain_labels)

        for label in target_labels:
            self.assertIn(label, result)
        for label in toolchain_labels:
            self.assertIn(label, result)
