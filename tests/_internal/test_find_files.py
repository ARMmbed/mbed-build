#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
from unittest import TestCase
import pathlib
from pyfakefs.fake_filesystem_unittest import patchfs

from mbed_build._internal.find_files import find_files, exclude_listed_in_mbedignore


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


class TestExcludeListedInMbedignore(TestCase):
    @patchfs
    def test_returns_true_for_files_matching_mbedignore(self, fs):
        mbedignore_contents = """
*.py
hidden.txt

*/test/*
*/stubs/*
stubs/*
"""
        fs.create_file("project/.mbedignore", contents=mbedignore_contents)

        subject = exclude_listed_in_mbedignore(pathlib.Path("project/.mbedignore"))

        ignored_paths = (
            "project/nested/test/file.doc",
            "project/nested/stubs/file.xls",
            "project/stubs/file.xls",
            "project/hidden.txt",
            "project/file.py",
        )

        not_ignored_paths = (
            "outside_of_project/hidden.txt",
            "foo.py",
            "project/test/foo.html",
        )

        for path in ignored_paths:
            self.assertTrue(subject(pathlib.Path(path)), f"{path} should be ignored")

        for path in not_ignored_paths:
            self.assertFalse(subject(pathlib.Path(path)), f"{path} should not be ignored")
