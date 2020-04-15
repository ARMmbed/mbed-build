#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
from unittest import TestCase

from mbed_build._internal.config.config_modifiers import (
    build_modifier_from_config_entry,
    build_modifier_from_target_override_entry,
    SetConfigValue,
)
from tests._internal.config.factories import ConfigFactory


class TestBuildModifierFromConfigEntry(TestCase):
    def test_builds_set_config_value_modifier(self):
        subject = build_modifier_from_config_entry("some-key", 123)

        self.assertEqual(
            subject, SetConfigValue.build(key="some-key", data=123),
        )


class TestBuildModifierFromTargetOverrideEntry(TestCase):
    def test_builds_set_config_value_modifier(self):
        subject = build_modifier_from_target_override_entry("some-key", 123)

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
        config = ConfigFactory()
        modifier = SetConfigValue(key="foo", value="value", help="help")

        modifier(config)

        self.assertEqual(config["settings"]["foo"], {"value": "value", "help": "help"})

    def test_overwrites_existing_value(self):
        config = ConfigFactory(settings={"bar": {"value": "swag", "help": "please help"}})
        modifier = SetConfigValue(key="bar", value=123, help=None)

        modifier(config)

        self.assertEqual(config["settings"]["bar"], {"value": 123, "help": "please help"})
