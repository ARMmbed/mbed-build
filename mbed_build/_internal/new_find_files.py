from pathlib import Path
import fnmatch

from typing import Iterable, Tuple


def find_files(filename, directory, allowed_labels):
    filters = [
        ExcludeUsingLabels(label_type, allowed_label_values)
        for label_type, allowed_label_values in allowed_labels.items()
    ]
    return _find_files(filename, directory, filters)


class ExcludeUsingLabels:
    def __init__(self, label_type, allowed_label_values):
        self._label_type = label_type
        self._allowed_labels = set(f"{label_type}_{label_value}" for label_value in allowed_label_values)

    def __call__(self, path):
        labels = set(part for part in path.parts if self._label_type in part)
        return labels.issubset(self._allowed_labels)


class MbedignoreFilter:
    """Filter out given paths based on rules found in .mbedignore files.

    Patterns in .mbedignore use unix shell-style wildcards (fnmatch). It means
    that functionality, although similar is different to that found in
    .gitignore and friends.
    """

    def __init__(self, patterns: Tuple[str]):
        """Initialise the filter attributes.

        Args:
            patterns: List of patterns from .mbedignore to filter against.
        """
        self._patterns = patterns

    @property
    def patterns(self) -> Tuple[str]:
        """Return patterns used for filtering."""
        return self._patterns

    def __call__(self, path: Path) -> bool:
        """Return True if given path doesn't match .mbedignore patterns."""
        stringified = str(path)
        return not any(fnmatch.fnmatch(stringified, pattern) for pattern in self.patterns)

    @classmethod
    def from_file(cls, mbedignore_path: Path) -> "MbedignoreFilter":
        """Return new instance with patterns read from .mbedignore file.

        Constructed patterns are rooted in the directory of .mbedignore file.
        """
        lines = mbedignore_path.read_text().splitlines()
        pattern_lines = (line for line in lines if line.strip() and not line.startswith("#"))
        ignore_root = mbedignore_path.parent
        patterns = tuple(str(ignore_root.joinpath(pattern)) for pattern in pattern_lines)
        return cls(patterns)


def _find_files(filename, directory, filters):
    filters = filters[:]
    result = []

    children = list(directory.iterdir())
    mbedignore = Path(directory, ".mbedignore")
    if mbedignore in children:
        filters.append(MbedignoreFilter.from_file(mbedignore))

    filtered_children = (child for child in children if all(f(child) for f in filters))

    for child in filtered_children:
        if child.is_dir():
            result += _find_files(filename, child, filters)

        if child.is_file() and child.name == filename:
            result.append(child)

    return result
