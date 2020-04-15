#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
from unittest import TestCase

from mbed_build._internal.config.config import Config
from mbed_build._internal.config.config_layer import ConfigLayer

from tests._internal.config.factories import ConfigSourceFactory


class TestFromLayers(TestCase):
    def test_assembles_config_from_layers(self):
        source_1 = ConfigSourceFactory(**{"config": {"is-nice": {"help": "Determine if app is nice", "value": True}}})
        source_2 = ConfigSourceFactory(**{"config": {"is-fast": True}, "target_overrides": {"*": {"is-nice": False}}})
        source_3 = ConfigSourceFactory(**{"target_overrides": {"NOT_THIS_TARGET": {"is-nice": True}}})
        layer_1 = ConfigLayer.from_config_source(source_1, ["TARGET"])
        layer_2 = ConfigLayer.from_config_source(source_2, ["TARGET"])
        layer_3 = ConfigLayer.from_config_source(source_3, ["TARGET"])

        subject = Config.from_layers([layer_1, layer_2, layer_3])

        expected_config = Config(
            settings={"is-nice": {"help": "Determine if app is nice", "value": False}, "is-fast": {"value": True}},
        )
        self.assertEqual(subject, expected_config)
