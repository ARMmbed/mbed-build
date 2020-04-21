#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
from unittest import TestCase, mock

from mbed_build._internal.config.config_layer import ConfigLayer
from mbed_build._internal.config.config_modifiers import (
    build_modifier_from_config_entry,
    build_modifier_from_target_override_entry,
)
from tests._internal.config.factories import ConfigSourceFactory, ConfigFactory


class TestApply(TestCase):
    def test_applies_all_modifiers_to_config(self):
        modifier_1 = mock.Mock()
        modifier_2 = mock.Mock()
        config = ConfigFactory()
        config_layer = ConfigLayer(modifiers=[modifier_1, modifier_2], config_source=ConfigSourceFactory())

        subject = config_layer.apply(config)

        self.assertEqual(subject, modifier_2.return_value)
        modifier_1.assert_called_once_with(config)
        modifier_2.assert_called_once_with(modifier_1.return_value)


class TestFromConfigSource(TestCase):
    def test_creates_config_layer_modifiers_from_config_source(self):
        config_source = ConfigSourceFactory(
            config={"foo": True},
            target_overrides={
                "*": {"bar": 1},
                "TARGET": {"baz": "maybe"},
                "NOT_THIS_TARGET": {"xyz": "should not be included"},
            },
        )

        subject = ConfigLayer.from_config_source(config_source, ["TARGET"])

        self.assertEqual(
            subject,
            ConfigLayer(
                config_source=config_source,
                modifiers=[
                    build_modifier_from_config_entry(key="foo", data=True),
                    build_modifier_from_target_override_entry(key="bar", data=1),
                    build_modifier_from_target_override_entry(key="baz", data="maybe"),
                ],
            ),
        )
