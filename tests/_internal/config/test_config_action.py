#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
from unittest import TestCase

from mbed_build._internal.config.config import Config
from mbed_build._internal.config.config_action import (
    build_action_from_config_entry,
    SetConfigValue,
)


class TestBuildActionFromConfigEntry(TestCase):
    def test_builds_set_config_value_instance(self):
        subject = build_action_from_config_entry("some-key", 123)

        self.assertEqual(
            subject, SetConfigValue.build(key="some-key", data=123),
        )


class TestSetConfigValue(TestCase):
    def test_build_from_simple_value(self):
        subject = SetConfigValue.build("foo", "value")

        self.assertEqual(subject, SetConfigValue(key="foo", value="value", help=None))

    def test_build_from_complex_value(self):
        subject = SetConfigValue.build("level", {"help": "TFM security level", "macro_name": "TFM_LVL", "value": 1})

        self.assertEqual(subject, SetConfigValue(key="level", value=1, help="TFM security level"))

    def test_sets_new_value(self):
        config = Config()
        action = SetConfigValue(key="foo", value="value", help="help")

        config = action(config)

        self.assertEqual(config.settings["foo"], {"value": "value", "help": "help"})

    def test_overwrites_existing_value(self):
        config = Config()
        config.settings["bar"] = {"value": "swag", "help": "please help"}
        action = SetConfigValue(key="bar", value=123, help=None)

        config = action(config)

        self.assertEqual(config.settings["bar"], {"value": 123, "help": "please help"})
