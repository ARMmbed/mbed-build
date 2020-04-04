import os
from pathlib import Path
import fnmatch


def find_files(desired_filename, directory, allowed_labels):
    filters = [
        ExcludeUsingLabels(label_type, allowed_label_values)
        for label_type, allowed_label_values in allowed_labels.items()
    ]
    return _find_files(desired_filename, directory, filters)


def _find_files(desired_filename, directory, filters):
    filters = filters[:]
    result = []

    children = list(directory.iterdir())
    mbedignore = Path(directory, ".mbedignore")
    if mbedignore in children:
        filters.append(ExcludeMatchingMbedignore.from_file(mbedignore))

    filtered_children = (child for child in children if all(f(child) for f in filters))

    for child in filtered_children:
        if child.is_dir():
            result += _find_files(desired_filename, child, filters)

        if child.is_file() and child.name == desired_filename:
            result.append(child)

    return result


class ExcludeUsingLabels:
    def __init__(self, label_type, allowed_label_values):
        self._label_type = label_type
        self._allowed_labels = set(f"{label_type}_{label_value}" for label_value in allowed_label_values)

    def __call__(self, path):
        labels = set(part for part in path.parts if self._label_type in part)
        return labels.issubset(self._allowed_labels)


class ExcludeMatchingMbedignore:
    def __init__(self, patterns):
        self._patterns = patterns

    def __call__(self, path):
        stringified = str(path)
        return not any(fnmatch.fnmatch(stringified, pattern) for pattern in self._patterns)

    @classmethod
    def from_file(cls, mbedignore_path):
        lines = mbedignore_path.read_text().splitlines()
        pattern_lines = (line for line in lines if line.strip() and not line.startswith("#"))
        ignore_root = mbedignore_path.parent
        patterns = tuple(str(ignore_root.joinpath(pattern)) for pattern in pattern_lines)
        return cls(patterns)
