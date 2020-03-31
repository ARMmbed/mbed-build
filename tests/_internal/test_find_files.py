#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
from unittest import TestCase
import pathlib
from pyfakefs.fake_filesystem_unittest import patchfs

from mbed_build._internal.find_files import find_files


class TestFindFiles(TestCase):
    @patchfs
    def test_finds_files_by_name_in_given_root(self, fs):
        files = (
            pathlib.Path("root", "folder_1", "file.txt"),
            pathlib.Path("root", "folder_1", "folder_1_1", "file.txt"),
            pathlib.Path("root", "folder_2", "file.txt"),
        )
        for file in files:
            fs.create_file(file)

        subject = find_files("file.txt", root_dir="root")

        for file in files:
            self.assertIn(file, subject)

    @patchfs
    def test_excludes_files_using_callables(self, fs):
        file = pathlib.Path("root", "folder_1", "file.txt")
        ignored_file_1 = pathlib.Path("root", "ignore_me", "file.txt")
        ignored_file_2 = pathlib.Path("root", "hidden", "file.txt")
        fs.create_file(file)
        fs.create_file(ignored_file_1)
        fs.create_file(ignored_file_2)

        def matches_ignore_me(file):
            return "ignore_me" in str(file)

        def matches_hidden(file):
            return "hidden" in str(file)

        subject = find_files("file.txt", root_dir="root", exclude=[matches_ignore_me, matches_hidden])

        self.assertIn(file, subject)
        self.assertNotIn(ignored_file_1, subject)
        self.assertNotIn(ignored_file_2, subject)
