from pathlib import Path
from pyfakefs.fake_filesystem_unittest import patchfs
from unittest import TestCase, mock

from mbed_build._internal.mbed_lib import find_mbed_lib_files


class TestFindMbedLibFiles(TestCase):
    @patchfs
    def test_finds_all_mbed_lib_files(self, fs):
        mbed_lib_paths = (
            Path("root", "mbed_lib.json"),
            Path("root", "foo", "mbed_lib.json"),
            Path("root", "foo", "bar", "mbed_lib.json"),
        )
        for path in mbed_lib_paths:
            fs.create_file(path)

        subject = find_mbed_lib_files(Path("root"))

        for path in mbed_lib_paths:
            self.assertIn(path, subject)

    @patchfs
    def test_respects_mbedignore(self, fs):
        mbed_lib_paths = (
            Path("root", "mbed_lib.json"),
            Path("root", "foo", "mbed_lib.json"),
            Path("root", "foo", "bar", "mbed_lib.json"),
        )
        ignored_mbed_lib_paths = (
            Path("root", "foo", "ignored_1", "mbed_lib.json"),
            Path("root", "foo", "ignored_2", "mbed_lib.json"),
        )
        for path in mbed_lib_paths + ignored_mbed_lib_paths:
            fs.create_file(path)

        mbedignore_path = Path("root", "foo", ".mbedignore")
        mbedignore_contents = """
ignored_1/*
ignored_2/mbed_lib.json
"""
        fs.create_file(mbedignore_path, contents=mbedignore_contents)

        subject = find_mbed_lib_files(Path("root"))

        for path in subject:
            self.assertNotIn(path, ignored_mbed_lib_paths, f"{path} should be ignored")
