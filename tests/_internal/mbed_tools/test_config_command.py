#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
import json
import pathlib
from unittest import TestCase, mock

from click.testing import CliRunner
from tabulate import tabulate

from mbed_build._internal.mbed_tools.config import (
    config,
    _build_tabular_output,
    _build_json_output,
    _build_legacy_output,
)
from tests._internal.config.factories import ConfigFactory, OptionFactory, MacroFactory


@mock.patch("mbed_build._internal.mbed_tools.config.assemble_config", return_value=ConfigFactory())
class TestConfig(TestCase):
    mbed_target = "K64F"
    project_path = "somewhere"

    def test_config_table(self, assemble_config):
        runner = CliRunner()
        result = runner.invoke(config, ["-m", self.mbed_target, "-p", self.project_path])

        self.assertEqual(result.exit_code, 0)
        self.assertIn(_build_tabular_output(assemble_config.return_value), result.output)
        assemble_config.assert_called_once_with(self.mbed_target, pathlib.Path(self.project_path))

    def test_config_json(self, assemble_config):
        runner = CliRunner()
        result = runner.invoke(config, ["-m", self.mbed_target, "-p", self.project_path, "--format", "json"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn(_build_json_output(assemble_config.return_value), result.output)
        assemble_config.assert_called_once_with(self.mbed_target, pathlib.Path(self.project_path))

    def test_config_legacy(self, assemble_config):
        runner = CliRunner()
        result = runner.invoke(
            config, ["-m", self.mbed_target, "-p", self.project_path, "--format", "json", "--format", "legacy"]
        )

        self.assertEqual(result.exit_code, 0)
        self.assertIn(_build_legacy_output(assemble_config.return_value), result.output)
        assemble_config.assert_called_once_with(self.mbed_target, pathlib.Path(self.project_path))


class TestBuildTabularOutput(TestCase):
    def test_builds(self):
        option = OptionFactory()
        macro = MacroFactory()
        config = ConfigFactory()
        config.options[option.key] = option
        config.macros[macro.name] = macro

        parameters_table = tabulate([[option.key, option.macro_name, option.value]], ["key", "macro name", "value"])
        macros_table = tabulate([[macro.name, macro.value]], ["name", "value"])
        expected_output = (
            "PARAMETER CONFIGURATION\n"
            "-----------------------\n"
            f"{parameters_table}\n"
            "\n"
            "MACRO CONFIGURATION\n"
            "-------------------\n"
            f"{macros_table}"
        )

        result = _build_tabular_output(config)
        self.assertEqual(result, expected_output)


class TestBuildJSONOutput(TestCase):
    def test_builds(self):
        option = OptionFactory()
        macro = MacroFactory()
        config = ConfigFactory()
        config.options[option.key] = option
        config.macros[macro.name] = macro

        expected_config = {
            "parameters": [
                {
                    "key": option.key,
                    "macro_name": option.macro_name,
                    "value": option.value,
                    "help_text": option.help_text,
                    "set_by": option.set_by,
                }
            ],
            "macros": [{"name": macro.name, "value": macro.value, "set_by": macro.set_by}],
        }

        result = _build_json_output(config)
        self.assertEqual(result, json.dumps(expected_config, indent=4))


class TestBuildLegacyOutput(TestCase):
    def test_builds(self):
        option = OptionFactory()
        macro = MacroFactory()
        config = ConfigFactory()
        config.options[option.key] = option
        config.macros[macro.name] = macro

        expected_output = (
            "Configuration parameters\n"
            "------------------------\n"
            f'{option.key} = {option.value} (macro name: "{option.macro_name}")\n\n'
            "\n"
            "Macros\n"
            "------\n"
            f"{macro.name}={macro.value}\n"
        )

        result = _build_legacy_output(config)
        self.assertEqual(result, expected_output)

    def test_builds_value_none(self):
        option = OptionFactory()
        option.value = None
        macro = MacroFactory()
        macro.value = None
        config = ConfigFactory()
        config.options[option.key] = option
        config.macros[macro.name] = macro

        expected_output = (
            "Configuration parameters\n"
            "------------------------\n"
            f"{option.key} has no value\n\n"
            "\n"
            "Macros\n"
            "------\n"
            f"{macro.name}\n"
        )

        result = _build_legacy_output(config)
        self.assertEqual(result, expected_output)
