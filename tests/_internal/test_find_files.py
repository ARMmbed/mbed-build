#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
from unittest import TestCase, mock
from pathlib import Path
from pyfakefs.fake_filesystem_unittest import patchfs
from mbed_targets import MbedTargetBuildAttributes

from mbed_build._internal.find_files import (
    find_files,
    exclude_legacy_directories,
    exclude_using_mbedignore,
    exclude_using_target_labels,
    exclude_using_labels,
)


class TestFindFiles(TestCase):
    @patchfs
    def test_finds_files_by_name_in_given_root(self, fs):
        files = [
            Path("root", "folder_1", "file.txt"),
            Path("root", "folder_1", "folder_1_1", "file.txt"),
            Path("root", "folder_2", "file.txt"),
        ]
        for file in files:
            fs.create_file(file)

        subject = find_files("file.txt", directory=Path("root"))

        self.assertEqual(list(subject), files)


class TestExcludeUsingMbedignore(TestCase):
    @patchfs
    def test_excludes_files_ignored_by_mbedignore(self, fs):
        project_path = Path("project")
        fs.create_file(
            project_path.joinpath(".mbedignore"),
            contents="""
*.py
hidden.txt

*/test/*
*/stubs/*
stubs/*
""",
        )
        fs.create_file(project_path.joinpath("isolated", ".mbedignore"), contents="*")

        paths = [
            Path("foo.py"),
            Path("project", "test", "foo.html"),
        ]

        excluded_paths = [
            Path("project", "nested", "test", "file.doc"),
            Path("project", "nested", "stubs", "file.xls"),
            Path("project", "stubs", "file.xls"),
            Path("project", "hidden.txt"),
            Path("project", "file.py"),
            Path("project", "isolated", "file.c"),
        ]

        subject = exclude_using_mbedignore(project_path, paths + excluded_paths)

        self.assertEqual(list(subject), paths)


class TestExcludeLegacyDirectories(TestCase):
    def test_excludes_known_legacy_directories(self):
        paths = [
            Path("mbed-os", "subdir", "some_file.c"),
        ]

        ignored_paths = [
            Path("mbed-os", "TESTS", "some_file.c"),
            Path("mbed-os", "TEST_APPS", "some_file.c"),
        ]

        subject = exclude_legacy_directories(paths + ignored_paths)

        self.assertEqual(list(subject), paths)


class TestExcludeUsingTargetLabels(TestCase):
    @mock.patch("mbed_build._internal.find_files.get_build_attributes_by_board_type", autospec=True)
    @mock.patch("mbed_build._internal.find_files.exclude_using_labels", autospec=True)
    def test_excludes_paths_using_target_labels(self, exclude_using_labels, get_build_attributes_by_board_type):
        build_attributes = mock.Mock(
            MbedTargetBuildAttributes, labels={"TARGET"}, features={"FEATURE"}, components={"COMPONENT"}
        )  # Zero interface safety here, dataclasses don't support spec_set
        get_build_attributes_by_board_type.return_value = build_attributes
        after_target_filtering = [Path("filtered_using_targets")]
        after_feature_filtering = [Path("filtered_using_features")]
        after_component_filtering = [Path("filtered_using_components")]
        exclude_using_labels.side_effect = [after_target_filtering, after_feature_filtering, after_component_filtering]
        mbed_program_directory = Path("some-path")
        board_type = "A_TYPE"
        paths = [Path("mbed_lib.json")]

        subject = exclude_using_target_labels(mbed_program_directory, board_type, paths)

        self.assertEqual(subject, after_component_filtering)
        get_build_attributes_by_board_type.assert_called_once_with(board_type, mbed_program_directory)
        self.assertEqual(
            exclude_using_labels.mock_calls,
            [
                mock.call("TARGET", build_attributes.labels, paths),
                mock.call("FEATURE", build_attributes.features, after_target_filtering),
                mock.call("COMPONENT", build_attributes.components, after_feature_filtering),
            ],
        )


class TestExcludeUsingLabels(TestCase):
    def test_excludes_files_not_matching_label(self):
        paths = [
            Path("mbed-os", "TARGET_BAR", "some_file.c"),
            Path("mbed-os", "COMPONENT_X", "header.h"),
            Path("mbed-os", "COMPONENT_X", "TARGET_BAZ", "some_file.c"),
            Path("README.md"),
        ]

        excluded_paths = [
            Path("mbed-os", "TARGET_FOO", "some_file.c"),
            Path("mbed-os", "TARGET_FOO", "nested", "other_file.c"),
            Path("mbed-os", "TARGET_BAR", "TARGET_FOO", "other_file.c"),
        ]

        subject = exclude_using_labels(
            label_type="TARGET", allowed_label_values={"BAR", "BAZ"}, paths=(paths + excluded_paths)
        )

        self.assertEqual(list(subject), paths)
