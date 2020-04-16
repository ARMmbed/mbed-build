from unittest import TestCase, mock

from mbed_build._internal.config.config_modifiers.utils import (
    build_modifier_from_target_override_entry,
    build_modifier_from_config_entry,
)
from mbed_build._internal.config.config_modifiers.cumulative import UnableToBuildCumulativeModifier


class TestBuildModifierFromConfigEntry(TestCase):
    @mock.patch("mbed_build._internal.config.config_modifiers.utils.set_config_setting.build")
    def test_builds_set_setting_modifier(self, set_config_setting_build):
        key = "foo"
        data = "bar"

        self.assertEqual(build_modifier_from_config_entry(key, data), set_config_setting_build.return_value)
        set_config_setting_build.assert_called_once_with(key, data)


class TestBuildModifierFromTargetOverrideEntry(TestCase):
    @mock.patch("mbed_build._internal.config.config_modifiers.utils.cumulative.build")
    def test_attempts_to_build_cumulative_modifier(self, cumulative_build):
        key = "foo"
        data = "bar"

        self.assertEqual(build_modifier_from_target_override_entry(key, data), cumulative_build.return_value)
        cumulative_build.assert_called_once_with(key, data)

    @mock.patch("mbed_build._internal.config.config_modifiers.utils.cumulative.build")
    @mock.patch("mbed_build._internal.config.config_modifiers.utils.set_config_setting.build")
    def test_if_cumulative_modifier_fails_returns_set_setting_modifier(
        self, set_config_setting_build, cumulative_build
    ):
        cumulative_build.side_effect = UnableToBuildCumulativeModifier
        key = "hat"
        data = "boat"

        self.assertEqual(build_modifier_from_target_override_entry(key, data), set_config_setting_build.return_value)
        set_config_setting_build.assert_called_once_with(key, data)
