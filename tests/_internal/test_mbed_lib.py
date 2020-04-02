#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
from pathlib import Path
from pyfakefs.fake_filesystem_unittest import patchfs
from unittest import TestCase, mock

from mbed_build._internal.mbed_lib import find_mbed_lib_files, _get_all_target_labels
from mbed_targets import MbedTargetBuildAttributes


class TestFindMbedLibFiles(TestCase):
    @patchfs
    @mock.patch("mbed_build._internal.mbed_lib._get_all_target_labels", return_value={}, autospec=True)
    def test_finds_all_mbed_lib_files(self, _get_all_target_labels, fs):
        mbed_lib_paths = (
            Path("root", "mbed_lib.json"),
            Path("root", "foo", "mbed_lib.json"),
            Path("root", "foo", "bar", "mbed_lib.json"),
        )
        for path in mbed_lib_paths:
            fs.create_file(path)

        subject = find_mbed_lib_files(Path("root"), board_type="K64F")

        for path in mbed_lib_paths:
            self.assertIn(path, subject)

    @patchfs
    @mock.patch("mbed_build._internal.mbed_lib._get_all_target_labels", return_value={}, autospec=True)
    def test_respects_mbedignore(self, _get_all_target_labels, fs):
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

        subject = find_mbed_lib_files(Path("root"), board_type="K66F")

        for path in subject:
            self.assertNotIn(path, ignored_mbed_lib_paths, f"{path} should be ignored")

    @patchfs
    @mock.patch("mbed_build._internal.mbed_lib._get_all_target_labels", return_value={}, autospec=True)
    def test_respects_labelling_rules(self, _get_all_target_labels, fs):
        mbed_program_directory = Path("not_important")
        board_type = "K64F"
        _get_all_target_labels.return_value = {"TARGET": ["FOO", "BAR"]}
        mbed_lib_paths = (
            Path("root", "TARGET_FOO", "mbed_lib.json"),
            Path("root", "TARGET_FOO", "TARGET_BAR", "mbed_lib.json"),
        )
        ignored_mbed_lib_paths = (
            Path("root", "TARGET_IGNORED", "mbed_lib.json"),
            Path("root", "TARGET_FOO", "TARGET_IGNORED", "mbed_lib.json"),
        )
        for path in mbed_lib_paths + ignored_mbed_lib_paths:
            fs.create_file(path)

        subject = find_mbed_lib_files(mbed_program_directory, board_type)

        for path in subject:
            self.assertNotIn(path, ignored_mbed_lib_paths, f"{path} should be ignored")
        _get_all_target_labels.assert_called_once_with(mbed_program_directory, board_type)


class TestGetAllTargetLabels(TestCase):
    @mock.patch("mbed_build._internal.mbed_lib.get_build_attributes_by_board_type", autospec=True)
    def test_returns_labels_extracted_from_build_attributes(self, get_build_attributes_by_board_type):
        build_attributes = mock.Mock(
            MbedTargetBuildAttributes, labels={"TARGET"}, features={"FEATURE"}, components={"COMPONENT"}
        )  # Zero interface safety here, dataclasses don't support spec_set
        get_build_attributes_by_board_type.return_value = build_attributes
        mbed_program_directory = Path("some-path")
        board_type = "A_TYPE"

        subject = _get_all_target_labels(mbed_program_directory, board_type)

        self.assertEqual(
            subject,
            {
                "TARGET": build_attributes.labels,
                "FEATURE": build_attributes.features,
                "COMPONENT": build_attributes.components,
            },
        )
        get_build_attributes_by_board_type.assert_called_once_with(board_type, mbed_program_directory)
