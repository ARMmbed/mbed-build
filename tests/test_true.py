from mbed_build import __version__
from unittest import TestCase


class TestPackage(TestCase):
    def test_version(self):
        self.assertIsNotNone(__version__)
