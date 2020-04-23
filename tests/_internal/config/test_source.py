#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
import json
import pathlib
import tempfile
from unittest import TestCase, mock

from mbed_build._internal.config.source import Source, _namespace_data, _filter_target_overrides


class TestMbedLibSource(TestCase):
    def test_from_mbed_lib(self):
        with tempfile.TemporaryDirectory() as directory:
            data = {
                "name": "foo",
                "config": {"a-number": 123, "a-bool": {"help": "Simply a boolean", "value": True}},
                "target_overrides": {
                    "*": {"a-number": 456},
                    "NOT_THIS_TARGET": {"a-string": "foo"},
                    "THIS_TARGET": {"a-bool": False},
                },
            }
            file = pathlib.Path(directory, "mbed_lib.json")
            file.write_text(json.dumps(data))

            subject = Source.from_mbed_lib(file, ["THIS_TARGET"])

        self.assertEqual(subject.config, _namespace_data(data["config"], data["name"]))
        self.assertEqual(
            subject.target_overrides,
            _namespace_data(_filter_target_overrides(data["target_overrides"], ["THIS_TARGET"]), data["name"]),
        )

    @mock.patch("mbed_build._internal.config.source.get_target_by_board_type")
    def test_from_target(self, get_target_by_board_type):
        # Warning: Target is a dataclass and dataclasses provide no type safety when mocking
        target = mock.Mock(
            features={"feature_1"},
            components={"component_1"},
            labels={"label_1"},
            config={"foo": "bar", "target.bool": True},
        )
        get_target_by_board_type.return_value = target
        mbed_target = "K66F"
        mbed_program_directory = pathlib.Path("foo")

        subject = Source.from_target(mbed_target, mbed_program_directory)

        self.assertEqual(
            subject,
            Source(
                name=f"mbed_target.Target for {mbed_target}",
                config=_namespace_data(target.config, "target"),
                target_overrides=_namespace_data(
                    {"features": target.features, "components": target.components, "labels": target.labels}, "target"
                ),
            ),
        )


class TestFilterTargetOverrides(TestCase):
    def test_returns_overrides_only_for_given_labels(self):
        subject = _filter_target_overrides(
            {"*": {"number": 123}, "B_TARGET": {"string": "boat"}, "A_TARGET": {"bool": True}}, ["A_TARGET"]
        )

        self.assertEqual(subject, {"number": 123, "bool": True})


class TestNamespaceData(TestCase):
    def test_prefixes_keys_without_namespace(self):
        data = {
            "foo": True,
            "hat.bar": 123,
        }

        self.assertEqual(_namespace_data(data, "my-prefix"), {"my-prefix.foo": True, "hat.bar": 123})
