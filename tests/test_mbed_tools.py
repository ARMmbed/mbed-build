#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
from unittest import TestCase

from mbed_build._internal.mbed_tools.export import export
from mbed_build._internal.mbed_tools.config import config
from mbed_build import mbed_tools


class TestConfig(TestCase):
    def test_aliases_config(self):
        self.assertEqual(mbed_tools.config, config)


class TestExport(TestCase):
    def test_aliases_export(self):
        self.assertEqual(mbed_tools.export, export)
