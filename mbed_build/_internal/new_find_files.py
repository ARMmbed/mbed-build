import os
import collections
from pathlib import Path
import fnmatch

from mbed_targets import get_build_attributes_by_board_type


class MatchFilename:
    def __init__(self, filename):
        self._filename = filename

    def __call__(self, path):
        return path.name == self._filename


class ExcludeUsingTargetLabels:
    def __init__(self, mbed_program_directory, board_type):
        build_attributes = get_build_attributes_by_board_type(board_type, mbed_program_directory)
        self._filters = [
            ExcludeUsingLabels("TARGET", build_attributes.labels),
            ExcludeUsingLabels("FEATURE", build_attributes.features),
            ExcludeUsingLabels("COMPONENT", build_attributes.components),
        ]

    def __call__(self, path):
        return all(f(path) for f in self._filters)


class ExcludeUsingLabels:
    def __init__(self, label_type, allowed_label_values):
        self._label_type = label_type
        self._allowed_labels = set(f"{label_type}_{label_value}" for label_value in allowed_label_values)

    def __call__(self, path):
        labels = set(part for part in path.parts if self._label_type in part)
        return labels.issubset(self._allowed_labels)


class ExcludeMatchingMbedignore:
    def __init__(self, mbedignore_path):
        self._patterns = self._build_mbedignore_patterns(mbedignore_path)

    def __call__(self, path):
        stringified = str(path)
        # all?
        return not any(fnmatch.fnmatch(stringified, pattern) for pattern in self._patterns)


def find_files(desired_filename, program_directory):
    # filters = collections.deque([ExcludeUsingTargetLabels(program_directory, board_type)])

    result = []

    for dirpath, dirnames, filenames in os.walk(program_directory):
        # if ".mbedignore" in filenames:
        #     # Prepend to filters, as .mbedignore should match more paths to filter out
        #     filters.appendleft(ExcludeMatchingMbedignore(Path(dirpath, ".mbedignore")))

        # if not all(f(dirpath) for f in filters):
        #     continue
        for filename in filenames:
            if desired_filename == filename:
                result.append(Path(dirpath, filename))

    return result
