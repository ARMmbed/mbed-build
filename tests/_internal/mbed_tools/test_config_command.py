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
from tests._internal.config.factories import BuildConfigFactory, OptionFactory


@mock.patch("mbed_build._internal.mbed_tools.config._build_legacy_output")
@mock.patch("mbed_build._internal.mbed_tools.config._build_json_output")
@mock.patch("mbed_build._internal.mbed_tools.config._build_tabular_output")
@mock.patch("mbed_build._internal.mbed_tools.config.assemble_config")
class TestConfig(TestCase):
    mbed_target = "K64F"
    project_path = "somewhere"

    def test_config_table(self, assemble_config, build_tabular_output, build_json_output, build_legacy_output):
        runner = CliRunner()
        result = runner.invoke(config, ["-m", self.mbed_target, "-p", self.project_path])

        self.assertEqual(result.exit_code, 0)
        assemble_config.assert_called_once_with(self.mbed_target, pathlib.Path(self.project_path))
        build_tabular_output.assert_called_once_with(assemble_config.return_value)
        build_json_output.assert_not_called()
        build_legacy_output.assert_not_called()

    def test_config_json(self, assemble_config, build_tabular_output, build_json_output, build_legacy_output):
        runner = CliRunner()
        result = runner.invoke(config, ["-m", self.mbed_target, "-p", self.project_path, "--format", "json"])

        self.assertEqual(result.exit_code, 0)
        assemble_config.assert_called_once_with(self.mbed_target, pathlib.Path(self.project_path))
        build_tabular_output.assert_not_called()
        build_json_output.assert_called_once_with(assemble_config.return_value)
        build_legacy_output.assert_not_called()

    def test_config_legacy(self, assemble_config, build_tabular_output, build_json_output, build_legacy_output):
        runner = CliRunner()
        result = runner.invoke(
            config, ["-m", self.mbed_target, "-p", self.project_path, "--format", "json", "--format", "legacy"]
        )

        self.assertEqual(result.exit_code, 0)
        assemble_config.assert_called_once_with(self.mbed_target, pathlib.Path(self.project_path))
        build_tabular_output.assert_not_called()
        build_json_output.assert_not_called()
        build_legacy_output.assert_called_once_with(assemble_config.return_value)


class TestBuildTabularOutput(TestCase):
    def test_builds(self):
        option = OptionFactory()
        macro = "I_AM_A_MACRO"
        config_data = BuildConfigFactory()
        config_data.config.options[option.key] = option
        config_data.macros.add(macro)

        parameters_table = tabulate([[option.key, option.macro_name, option.value]], ["key", "macro name", "value"])
        macros_table = tabulate([[macro, " "]], ["name", "value"])
        expected_output = (
            f"PARAMETER CONFIGURATION\n"
            f"-----------------------\n"
            f"{parameters_table}\n"
            f"\n"
            f"MACRO CONFIGURATION\n"
            f"-------------------\n"
            f"{macros_table}"
        )

        result = _build_tabular_output(config_data)
        self.assertEqual(result, expected_output)


class TestBuildJSONOutput(TestCase):
    def test_builds(self):
        option = OptionFactory()
        macro = "I_AM_A_MACRO"
        config_data = BuildConfigFactory()
        config_data.config.options[option.key] = option
        config_data.macros.add(macro)

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
            "macros": [{"name": macro}],
        }

        result = _build_json_output(config_data)
        self.assertEqual(result, json.dumps(expected_config, indent=4))


class TestBuildLegacyOutput(TestCase):
    def test_builds(self):
        option = OptionFactory()
        macro = "I_AM_A_MACRO"
        config_data = BuildConfigFactory()
        config_data.config.options[option.key] = option
        config_data.macros.add(macro)

        expected_output = (
            f"Configuration parameters\n"
            f"------------------------\n"
            f'{option.key} = {option.value} (macro name: "{option.macro_name}")\n\n'
            f"\n"
            f"Macros\n"
            f"------\n"
            f"{macro}\n"
        )

        result = _build_legacy_output(config_data)
        self.assertEqual(result, expected_output)
