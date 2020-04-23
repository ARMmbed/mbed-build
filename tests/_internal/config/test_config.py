#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
from unittest import TestCase

from dataclasses import fields
from mbed_build._internal.config.config import Config, Option, TargetMetadata
from tests._internal.config.factories import SourceFactory


class TestConfigFromSources(TestCase):
    def test_builds_config_from_sources(self):
        source_a = SourceFactory(config={"bool": True, "string": "foo"})
        source_b = SourceFactory(config={"number": 1}, target_overrides={"bool": False})

        config = Config.from_sources([source_a, source_b])

        self.assertEqual(
            config.options, {"bool": Option.build(False), "number": Option.build(1), "string": Option.build("foo")},
        )

    def test_raises_when_trying_to_override_unset_option(self):
        source_a = SourceFactory(config={"bool": True})
        source_b = SourceFactory(target_overrides={"string": "hello"})

        with self.assertRaises(ValueError):
            Config.from_sources([source_a, source_b])

    def test_keeps_old_option_data(self):
        source_a = SourceFactory(config={"bool": {"help": "A simple bool", "value": True}})
        source_b = SourceFactory(target_overrides={"bool": False})

        config = Config.from_sources([source_a, source_b])

        self.assertEqual(config.options, {"bool": Option.build({"help": "A simple bool", "value": False})})

    def test_assembles_metadata_from_sources(self):
        for field in fields(TargetMetadata):
            with self.subTest(f"Assemble {field.name}"):
                source_a = SourceFactory(target_overrides={f"target.{field.name}": ["FOO"]})
                source_b = SourceFactory(target_overrides={f"target.{field.name}_add": ["BAR", "BAZ"]})
                source_c = SourceFactory(target_overrides={f"target.{field.name}_remove": ["BAR"]})

                config = Config.from_sources([source_a, source_b, source_c])

                self.assertEqual(getattr(config.target_metadata, field.name), {"FOO", "BAZ"})
