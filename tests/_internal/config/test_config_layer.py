#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
from unittest import TestCase, mock

from mbed_build._internal.config.config import Config
from mbed_build._internal.config.config_layer import ConfigLayer
from mbed_build._internal.config.config_layer_action import ConfigLayerAction
from tests._internal.config.factories import ConfigSourceFactory


class TestApply(TestCase):
    def test_applies_all_actions_to_config(self):
        action_1 = mock.Mock()
        action_2 = mock.Mock()
        config = Config()

        subject = ConfigLayer(actions=[action_1, action_2]).apply(config)

        self.assertEqual(subject, action_2.apply.return_value)
        action_1.apply.assert_called_once_with(config)
        action_2.apply.assert_called_once_with(action_1.apply.return_value)


class TestFromConfigSource(TestCase):
    def test_creates_config_layer_with_actions_from_config_source(self):
        config_source = ConfigSourceFactory()

        subject = ConfigLayer.from_config_source(config_source)

        actions_from_config = [
            ConfigLayerAction.from_config_entry(name=name, value=value) for name, value in config_source.config.items()
        ]

        actions_from_target_overrides = []
        for target_label, overrides in config_source.target_overrides.items():
            for name, value in overrides.items():
                actions_from_target_overrides.append(
                    ConfigLayerAction.from_target_override_entry(name=name, value=value)
                )

        self.assertEqual(subject, ConfigLayer(actions=(actions_from_config + actions_from_target_overrides)))
