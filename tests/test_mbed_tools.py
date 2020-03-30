#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
from unittest import TestCase

from mbed_build._internal.mbed_tools.export import export
from mbed_build.mbed_tools import cli


class TestCli(TestCase):
    def test_aliases_export(self):
        self.assertEqual(cli, export)
