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
            config.options,
            {
                "bool": Option.build("bool", True, source_a).set_value(False, source_b),
                "number": Option.build("number", 1, source_b),
                "string": Option.build("string", "foo", source_a),
            },
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

        self.assertEqual(config.options["bool"].help_text, "A simple bool")

    def test_assembles_metadata_from_sources(self):
        for field in fields(TargetMetadata):
            with self.subTest(f"Assemble {field.name}"):
                source_a = SourceFactory(target_overrides={f"target.{field.name}": ["FOO"]})
                source_b = SourceFactory(target_overrides={f"target.{field.name}_add": ["BAR", "BAZ"]})
                source_c = SourceFactory(target_overrides={f"target.{field.name}_remove": ["BAR"]})

                config = Config.from_sources([source_a, source_b, source_c])

                self.assertEqual(getattr(config.target_metadata, field.name), {"FOO", "BAZ"})


class TestOptionBuild(TestCase):
    def test_builds_option_from_config_data(self):
        source = SourceFactory(name="foo")
        data = {
            "value": 123,
            "help": "some help text",
            "macro_name": "FOO_MACRO",
        }
        option = Option.build(key="target.stack-size", data=data, source=source)

        self.assertEqual(
            option,
            Option(
                key="target.stack-size",
                value=data["value"],
                help_text=data["help"],
                macro_name=data["macro_name"],
                set_by=source.name,
            ),
        )

    def test_generates_macro_name_if_not_in_data(self):
        source = SourceFactory()
        data = {
            "value": 123,
            "help": "some help text",
        }
        option = Option.build(key="update-client.storage-size", data=data, source=source)

        self.assertEqual(option.macro_name, "MBED_CONF_UPDATE_CLIENT_STORAGE_SIZE")
