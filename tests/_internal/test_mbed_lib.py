#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
from pathlib import Path
from unittest import TestCase, mock

from mbed_build._internal.mbed_lib import find_mbed_lib_files, _exclude_using_target_labels
from mbed_targets import MbedTargetBuildAttributes


class TestFindMbedLibFiles(TestCase):
    @mock.patch("mbed_build._internal.mbed_lib.find_files", autospec=True)
    @mock.patch("mbed_build._internal.mbed_lib.exclude_using_mbedignore", autospec=True)
    @mock.patch("mbed_build._internal.mbed_lib._exclude_using_target_labels", autospec=True)
    def test_filters_mbed_lib_json_paths_using_exclusion_rules(
        self, _exclude_using_target_labels, exclude_using_mbedignore, find_files
    ):
        mbed_program_directory = Path("some-program")
        board_type = "K64F"

        subject = find_mbed_lib_files(mbed_program_directory, board_type)

        self.assertEqual(subject, _exclude_using_target_labels.return_value)
        find_files.assert_called_once_with("mbed_lib.json", mbed_program_directory)
        exclude_using_mbedignore.assert_called_once_with(mbed_program_directory, find_files.return_value)
        _exclude_using_target_labels.assert_called_once_with(
            mbed_program_directory, board_type, exclude_using_mbedignore.return_value
        )


class TestExcludeUsingTargetLabels(TestCase):
    @mock.patch("mbed_build._internal.mbed_lib.get_build_attributes_by_board_type", autospec=True)
    @mock.patch("mbed_build._internal.mbed_lib.exclude_using_labels", autospec=True)
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

        subject = _exclude_using_target_labels(mbed_program_directory, board_type, paths)

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
