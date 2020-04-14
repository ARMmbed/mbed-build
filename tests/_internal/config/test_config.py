#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
from unittest import TestCase
import tempfile
import pathlib
import json


from mbed_build._internal.config.config import Config
from mbed_build._internal.config.config_layer import ConfigLayer
from mbed_build._internal.config.config_source import ConfigSource


class TestFromLayers(TestCase):
    def test_assembles_config_from_layers(self):
        with tempfile.TemporaryDirectory() as directory:
            config_data_1 = {"config": {"is-nice": {"help": "Determine if app is nice", "value": True}}}
            source_json_1 = pathlib.Path(directory, "source_1.json")
            source_json_1.write_text(json.dumps(config_data_1))
            source_1 = ConfigSource.from_file(source_json_1)

            config_data_2 = {"config": {"is-fast": True}, "target_overrides": {"*": {"is-nice": False}}}
            source_json_2 = pathlib.Path(directory, "source_2.json")
            source_json_2.write_text(json.dumps(config_data_2))
            source_2 = ConfigSource.from_file(source_json_2)

            config_data_3 = {"target_overrides": {"NOT_THIS_TARGET": {"is-nice": True}}}
            source_json_3 = pathlib.Path(directory, "source_3.json")
            source_json_3.write_text(json.dumps(config_data_3))
            source_3 = ConfigSource.from_file(source_json_3)

        layer_1 = ConfigLayer.from_config_source(source_1, ["TARGET"])
        layer_2 = ConfigLayer.from_config_source(source_2, ["TARGET"])
        layer_3 = ConfigLayer.from_config_source(source_3, ["TARGET"])

        subject = Config.from_layers([layer_1, layer_2, layer_3])
        expected_config = Config(
            settings={"is-nice": {"help": "Determine if app is nice", "value": False}, "is-fast": {"value": True}},
        )

        self.assertEqual(subject, expected_config)
