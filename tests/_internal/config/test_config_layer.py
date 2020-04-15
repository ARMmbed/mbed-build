#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
from unittest import TestCase, mock

from mbed_build._internal.config.config import Config
from mbed_build._internal.config.config_layer import ConfigLayer
from mbed_build._internal.config.config_action import (
    build_action_from_config_entry,
    build_action_from_target_override_entry,
)
from tests._internal.config.factories import ConfigSourceFactory


class TestApply(TestCase):
    def test_applies_all_actions_to_config(self):
        action_1 = mock.Mock()
        action_2 = mock.Mock()
        config = Config()

        subject = ConfigLayer(actions=[action_1, action_2]).apply(config)

        self.assertEqual(subject, action_2.return_value)
        action_1.assert_called_once_with(config)
        action_2.assert_called_once_with(action_1.return_value)


class TestFromConfigSource(TestCase):
    def test_creates_config_layer_with_actions_from_config_source(self):
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
                actions=[
                    build_action_from_config_entry(key="foo", data=True),
                    build_action_from_target_override_entry(key="bar", data=1),
                    build_action_from_target_override_entry(key="baz", data="maybe"),
                ]
            ),
        )
