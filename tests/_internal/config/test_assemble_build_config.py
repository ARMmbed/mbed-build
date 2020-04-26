#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
import json
import contextlib
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from mbed_build._internal.config.assemble_build_config import _assemble_config
from mbed_build._internal.config.config import Config
from mbed_build._internal.find_files import find_files
from mbed_build._internal.config.source import Source
from tests._internal.config.factories import SourceFactory


@contextlib.contextmanager
def create_files(files):
    with TemporaryDirectory() as directory:
        for path, json_data in files.items():
            path = Path(directory, path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(json_data))
        yield Path(directory)


class TestConfigAssembly(TestCase):
    def test_assembles_using_all_relevant_files(self):
        mbed_lib_files = {
            Path("TARGET_A", "mbed_lib.json"): {
                "name": "a",
                "config": {"number": 123},
                "target_overrides": {"*": {"target.features_add": ["RED"]}},
            },
            Path("subdir", "FEATURE_RED", "mbed_lib.json"): {
                "name": "red",
                "config": {"bool": False},
                "target_overrides": {
                    "A": {"bool": True, "target.features_add": ["BLUE"], "target.macros_add": ["RED_MACRO"]}
                },
            },
            Path("COMPONENT_LEG", "mbed_lib.json"): {"name": "leg", "config": {"number-of-fingers": 5}},
        }
        unused_mbed_lib_files = {
            Path("subdir", "FEATURE_BROWN", "mbed_lib.json"): {
                "name": "brown",
                "target_overrides": {"*": {"red.bool": "DON'T USE ME"}},
            }
        }

        target_source = SourceFactory(
            cumulative_overrides={
                "target.labels": ["A"],
                "target.components": ["LEG"],
                "target.macros": ["TARGET_MACRO"],
            }
        )

        with create_files({**mbed_lib_files, **unused_mbed_lib_files}) as directory:
            build_config = _assemble_config(target_source, find_files("mbed_lib.json", directory))

            mbed_lib_sources = [Source.from_mbed_lib(Path(directory, file), ["A"]) for file in mbed_lib_files.keys()]
            expected_config = Config.from_sources([target_source] + mbed_lib_sources)

            self.assertEqual(build_config.config, expected_config)
            self.assertEqual(build_config.macros, set(["TARGET_MACRO", "RED_MACRO"]))
