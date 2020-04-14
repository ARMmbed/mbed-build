#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
from unittest import TestCase

from mbed_build._internal.config.config import Config
from mbed_build._internal.config.config_action import (
    ConfigAction,
    SetConfigValueAction,
)


class TestConfigAction(TestCase):
    def test_from_config_entry_creates_overwrite_action(self):
        subject = ConfigAction.from_config_entry("some-key", 123)

        self.assertEqual(
            subject, SetConfigValueAction.build(key="some-key", data=123),
        )


class TestSetConfigValueAction(TestCase):
    def test_build_from_simple_value(self):
        subject = SetConfigValueAction.build("foo", "value")

        self.assertEqual(subject, SetConfigValueAction(key="foo", value="value", help=None))

    def test_build_from_complex_value(self):
        subject = SetConfigValueAction.build(
            "level", {"help": "TFM security level", "macro_name": "TFM_LVL", "value": 1}
        )

        self.assertEqual(subject, SetConfigValueAction(key="level", value=1, help="TFM security level"))

    def test_sets_new_value(self):
        config = Config()
        action = SetConfigValueAction(key="foo", value="value", help="help")

        config = action.apply(config)

        self.assertEqual(config.settings["foo"], {"value": "value", "help": "help"})

    def test_overwrites_existing_value(self):
        config = Config()
        config.settings["bar"] = {"value": "swag", "help": "please help"}
        action = SetConfigValueAction(key="bar", value=123, help=None)

        config = action.apply(config)

        self.assertEqual(config.settings["bar"], {"value": 123, "help": "please help"})
