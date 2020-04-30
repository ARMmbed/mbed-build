#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
import pathlib
from unittest import TestCase, mock

from mbed_build._internal.config_header_file import (
    generate_config_header_file,
    _render_config_header_template,
    _max_attribute_length,
)
from tests._internal.config.factories import ConfigFactory, OptionFactory, MacroFactory


class TestGenerateConfigHeaderFile(TestCase):
    @mock.patch("mbed_build._internal.config_header_file.assemble_config")
    def test_correct_arguments_passed(self, assemble_config):
        config = ConfigFactory()
        assemble_config.return_value = config
        mbed_target = "K64F"
        program_path = "mbed_program"

        result = generate_config_header_file(mbed_target, program_path)

        assemble_config.assert_called_once_with(mbed_target, pathlib.Path(program_path))
        self.assertEqual(result, _render_config_header_template(config))


class TestRendersConfigHeaderFile(TestCase):
    def test_returns_rendered_content(self):
        config = ConfigFactory()
        result = _render_config_header_template(config)

        for value in config.options.values():
            self.assertIn(value, result)
        for value in config.macros.values():
            self.assertIn(value, result)


class TestMaxFieldLength(TestCase):
    def test_correct_max_lengths(self):
        macros = [MacroFactory(name="not max"), MacroFactory(name="I am the longest name with a length of 41")]

        result = _max_attribute_length(macros, "name")
        self.assertEqual(result, 41)

    def test_correct_length_with_non_string(self):
        macros = [MacroFactory(value=None), MacroFactory(value=12345)]

        result = _max_attribute_length(macros, "value")
        self.assertEqual(result, 5)

    def test_max_length_no_attr(self):
        macros = [MacroFactory(value=None), MacroFactory(value=None)]

        result = _max_attribute_length(macros, "value")
        self. assertEqual(result, 0)
