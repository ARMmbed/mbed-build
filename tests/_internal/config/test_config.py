#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
from unittest import TestCase

from mbed_build._internal.config.config import build_config_from_layers
from mbed_build._internal.config.config_layer import ConfigLayer
from tests._internal.config.factories import ConfigSourceFactory


class TestBuildFromLayers(TestCase):
    def test_assembles_config_from_layers(self):
        source_1 = ConfigSourceFactory(**{"config": {"is-nice": {"help": "Determine if app is nice", "value": True}}})
        source_2 = ConfigSourceFactory(**{"config": {"is-fast": False}})
        layer_1 = ConfigLayer.from_config_source(source_1, ["DOES_NOT_MATTER"])
        layer_2 = ConfigLayer.from_config_source(source_2, ["DOES_NOT_MATTER"])

        subject = build_config_from_layers([layer_1, layer_2])

        self.assertEqual(subject["settings"]["is-nice"]["value"], True)
        self.assertEqual(subject["settings"]["is-nice"]["help"], "Determine if app is nice")
        self.assertEqual(subject["settings"]["is-fast"]["value"], False)

    def test_respects_target_overrides(self):
        source_1 = ConfigSourceFactory(**{"config": {"is-nice": True}})
        source_2 = ConfigSourceFactory(**{"target_overrides": {"*": {"is-nice": False}}})
        source_3 = ConfigSourceFactory(**{"target_overrides": {"NOT_THIS_TARGET": {"is-nice": True}}})
        layer_1 = ConfigLayer.from_config_source(source_1, ["TARGET"])
        layer_2 = ConfigLayer.from_config_source(source_2, ["TARGET"])
        layer_3 = ConfigLayer.from_config_source(source_3, ["TARGET"])

        subject = build_config_from_layers([layer_1, layer_2, layer_3])

        self.assertEqual(subject["settings"]["is-nice"]["value"], False)

    def test_respects_cumulative_overrides(self):
        source_1 = ConfigSourceFactory(
            **{"target_overrides": {"*": {"target.features_add": ["FEATURE_1", "FEATURE_2"]}}}
        )
        source_2 = ConfigSourceFactory(**{"target_overrides": {"*": {"target.features_remove": ["FEATURE_2"]}}})
        source_3 = ConfigSourceFactory(**{"target_overrides": {"K64F": {"target.features_add": ["FEATURE_3"]}}})
        layer_1 = ConfigLayer.from_config_source(source_1, ["K64F"])
        layer_2 = ConfigLayer.from_config_source(source_2, ["K64F"])
        layer_3 = ConfigLayer.from_config_source(source_3, ["K64F"])

        subject = build_config_from_layers([layer_1, layer_2, layer_3])

        self.assertEqual(subject["target"]["features"], set(["FEATURE_1", "FEATURE_3"]))
