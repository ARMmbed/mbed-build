#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
from unittest import TestCase, mock

from mbed_build._internal.config.config_modifiers.build_modifiers import (
    build_modifier_from_target_override_entry,
    build_modifier_from_config_entry,
)
from mbed_build._internal.config.config_modifiers.set_target_attribute import InvalidModifierData


class TestBuildModifierFromConfigEntry(TestCase):
    @mock.patch("mbed_build._internal.config.config_modifiers.build_modifiers.set_config_setting.build")
    def test_builds_set_setting_modifier(self, set_config_setting_build):
        key = "foo"
        data = "bar"

        self.assertEqual(build_modifier_from_config_entry(key, data), set_config_setting_build.return_value)
        set_config_setting_build.assert_called_once_with(key, data)


class TestBuildModifierFromTargetOverrideEntry(TestCase):
    @mock.patch("mbed_build._internal.config.config_modifiers.build_modifiers.set_target_attribute.build")
    def test_attempts_to_build_cumulative_modifier(self, set_target_attribute_build):
        key = "foo"
        data = "bar"

        self.assertEqual(build_modifier_from_target_override_entry(key, data), set_target_attribute_build.return_value)
        set_target_attribute_build.assert_called_once_with(key, data)

    @mock.patch("mbed_build._internal.config.config_modifiers.build_modifiers.set_target_attribute.build")
    @mock.patch("mbed_build._internal.config.config_modifiers.build_modifiers.set_config_setting.build")
    def test_returns_setting_modifier_if_building_target_modifier_fails(
        self, set_config_setting_build, set_target_attribute_build
    ):
        set_target_attribute_build.side_effect = InvalidModifierData
        key = "hat"
        data = "boat"

        self.assertEqual(build_modifier_from_target_override_entry(key, data), set_config_setting_build.return_value)
        set_config_setting_build.assert_called_once_with(key, data)

    @mock.patch("mbed_build._internal.config.config_modifiers.build_modifiers.set_target_attribute.build")
    @mock.patch("mbed_build._internal.config.config_modifiers.build_modifiers.set_config_setting.build")
    def test_strips_target_prefix(self, set_config_setting_build, set_target_attribute_build):
        set_target_attribute_build.side_effect = InvalidModifierData
        key = "target.hat"
        data = "boat"

        self.assertEqual(build_modifier_from_target_override_entry(key, data), set_config_setting_build.return_value)
        set_target_attribute_build.assert_called_once_with("hat", data)
        set_config_setting_build.assert_called_once_with("hat", data)
