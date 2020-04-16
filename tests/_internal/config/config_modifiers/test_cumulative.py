#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
from unittest import TestCase

from mbed_build._internal.config.config_modifiers.cumulative import (
    AppendToConfig,
    CUMULATIVE_OVERRIDES,
    RemoveFromConfig,
    UnableToBuildCumulativeModifier,
    build,
)
from tests._internal.config.factories import ConfigFactory


class TestBuild(TestCase):
    def test_builds_append_value_modifier_for_cumulative_overrides(self):
        for override in CUMULATIVE_OVERRIDES:
            with self.subTest('builds append value modifier for "{override}" override'):
                subject = build(f"target.{override}_add", ["FOO"])

                self.assertEqual(subject, AppendToConfig(key=override, value=["FOO"]))

    def test_builds_remove_value_modifier(self):
        for override in CUMULATIVE_OVERRIDES:
            with self.subTest('builds remove value modifier for "{override}" override'):
                subject = build(f"target.{override}_remove", ["BAR"])

                self.assertEqual(subject, RemoveFromConfig(key=override, value=["BAR"]))

    def test_raises_given_invalid_key(self):
        with self.assertRaises(UnableToBuildCumulativeModifier):
            build("definitely-not-a-cumulative-override", data=None)


class TestAppendValue(TestCase):
    def test_appends_to_existing_value(self):
        config = ConfigFactory(features=set(["SWAG"]))
        modifier = AppendToConfig(key="features", value=["BAR"])

        modifier(config)

        self.assertEqual(config["features"], set(["SWAG", "BAR"]))


class TestRemoveValue(TestCase):
    def test_removes_existing_values(self):
        config = ConfigFactory(features=set(["FOO", "BAR", "BAZ"]))
        modifier = RemoveFromConfig(key="features", value=["FOO", "BAR"])

        modifier(config)

        self.assertEqual(config["features"], set(["BAZ"]))
