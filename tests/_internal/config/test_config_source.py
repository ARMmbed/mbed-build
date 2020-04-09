#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
import json
import pathlib
import tempfile
from unittest import TestCase

from mbed_build._internal.config.config_source import ConfigSource


class TestFromFile(TestCase):
    def test_builds_new_config_source_from_json_file(self):
        json_data = {
            "name": "ns-hal-pal",
            "config": {
                "nvm_cfstore": {
                    "help": "Use cfstore as a NVM storage. Else RAM simulation will be used",
                    "value": False,
                },
            },
            "target_overrides": {"*": {"rsa-required": True}},
        }

        with tempfile.NamedTemporaryFile() as fp:
            json_file = pathlib.Path(fp.name)
            json_file.write_text(json.dumps(json_data))

            subject = ConfigSource.from_file(json_file)

        self.assertEqual(
            subject,
            ConfigSource(
                file=json_file,
                name=json_data["name"],
                config=json_data["config"],
                target_overrides=json_data["target_overrides"],
            ),
        )

    def test_gracefully_handles_missing_data(self):
        json_data = {}

        with tempfile.NamedTemporaryFile() as fp:
            json_file = pathlib.Path(fp.name)
            json_file.write_text(json.dumps(json_data))

            subject = ConfigSource.from_file(json_file)

        self.assertEqual(subject, ConfigSource(file=json_file, name=None, config={}, target_overrides={}))
