#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
from unittest import TestCase

from mbed_build._internal.config.config_modifiers.set_target_attribute import (
    AppendToTargetAttribute,
    ACCUMULATING_OVERRIDES,
    RemoveFromTargetAttribute,
    OverwriteTargetAttribute,
    InvalidModifierData,
    build,
)
from tests._internal.config.factories import ConfigFactory


class TestBuild(TestCase):
    def test_builds_append_modifier(self):
        for override in ACCUMULATING_OVERRIDES:
            with self.subTest('builds append value modifier for "{override}" override'):
                subject = build(f"{override}_add", ["FOO"])

                self.assertEqual(subject, AppendToTargetAttribute(key=override, value=["FOO"]))

    def test_builds_remove_modifier(self):
        for override in ACCUMULATING_OVERRIDES:
            with self.subTest('builds remove value modifier for "{override}" override'):
                subject = build(f"{override}_remove", ["BAR"])

                self.assertEqual(subject, RemoveFromTargetAttribute(key=override, value=["BAR"]))

    def test_builds_override_modifier(self):
        for override in ACCUMULATING_OVERRIDES:
            with self.subTest('builds override value modifier for "{override}" override'):
                subject = build(f"{override}", ["BAR"])

                self.assertEqual(subject, OverwriteTargetAttribute(key=override, value=["BAR"]))

    def test_raises_given_invalid_key(self):
        with self.assertRaises(InvalidModifierData):
            build("definitely-not-a-cumulative-override", data=None)


class TestAppendToTargetAttribute(TestCase):
    def test_appends_to_existing_value(self):
        config = ConfigFactory(target={"features": set(["SWAG"])})
        modifier = AppendToTargetAttribute(key="features", value=["BAR"])

        modifier(config)

        self.assertEqual(config["target"]["features"], set(["SWAG", "BAR"]))


class TestRemoveFromTargetAttribute(TestCase):
    def test_removes_existing_values(self):
        config = ConfigFactory(target={"features": set(["FOO", "BAR", "BAZ"])})
        modifier = RemoveFromTargetAttribute(key="features", value=["FOO", "BAR"])

        modifier(config)

        self.assertEqual(config["target"]["features"], set(["BAZ"]))
