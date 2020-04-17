#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
from unittest import TestCase

from mbed_build._internal.config.config_modifiers.set_config_setting import (
    build,
    SetConfigSetting,
)
from tests._internal.config.factories import ConfigFactory


class TestSetConfigSetting(TestCase):
    def test_sets_new_value(self):
        config = ConfigFactory()
        modifier = SetConfigSetting(key="foo", value="value", help="help")

        modifier(config)

        self.assertEqual(config["settings"]["foo"], {"value": "value", "help": "help"})

    def test_overwrites_existing_value(self):
        config = ConfigFactory(settings={"bar": {"value": "swag", "help": "please help"}})
        modifier = SetConfigSetting(key="bar", value=123, help=None)

        modifier(config)

        self.assertEqual(config["settings"]["bar"], {"value": 123, "help": "please help"})


class TestBuild(TestCase):
    def test_build_from_simple_value(self):
        subject = build("foo", "value")

        self.assertEqual(subject, SetConfigSetting(key="foo", value="value", help=None))

    def test_build_from_complex_value(self):
        subject = build("level", {"help": "TFM security level", "macro_name": "TFM_LVL", "value": 1})

        self.assertEqual(subject, SetConfigSetting(key="level", value=1, help="TFM security level"))
