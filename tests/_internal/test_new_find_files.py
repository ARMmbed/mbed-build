import contextlib
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from typing import Iterable

from mbed_build._internal.new_find_files import list_files, ExcludeMatchingMbedignore


@contextlib.contextmanager
def create_files(files: Iterable[Path]):
    with TemporaryDirectory() as temp_directory:
        temp_directory = Path(temp_directory)
        for file in files:
            file_path = temp_directory / file
            file_directory = file_path.parent
            if not file_directory.exists():
                file_directory.mkdir(parents=True)
            file_path.touch()
        yield Path(temp_directory)


class TestListFiles(TestCase):
    def test_finds_files_by_name(self):
        matching_paths = [
            Path("file.txt"),
            Path("sub_directory", "file.txt"),
        ]
        excluded_paths = [
            Path("not_interested.txt"),
            Path("sub_directory", "not_interested.txt"),
        ]

        with create_files(matching_paths + excluded_paths) as program_directory:
            subject = list_files("file.txt", program_directory)

        self.assertEqual(len(subject), len(matching_paths))
        for path in matching_paths:
            self.assertIn(Path(program_directory, path), subject)

    def test_respects_mbedignore(self):
        matching_paths = [
            Path("file.txt"),
        ]
        excluded_paths = [
            Path("foo", "file.txt"),
            Path("bar", "file.txt"),
        ]
        with create_files(matching_paths + excluded_paths) as program_directory:
            Path(program_directory, ".mbedignore").write_text("foo/*")
            Path(program_directory, "bar", ".mbedignore").write_text("*")

            subject = list_files("file.txt", program_directory)

        self.assertEqual(len(subject), len(matching_paths))
        for path in matching_paths:
            self.assertIn(Path(program_directory, path), subject)


class TestExcludeUsingMbedignore(TestCase):
    def test_matches_files_by_name(self):
        subject = ExcludeMatchingMbedignore(("*.py",))

        self.assertFalse(subject("file.py"))
        self.assertFalse(subject("nested/file.py"))
        self.assertTrue(subject("file.txt"))

    def test_matches_wildcards(self):
        subject = ExcludeMatchingMbedignore(("*/test/*",))

        self.assertFalse(subject("foo/test/bar.txt"))
        self.assertFalse(subject("bar/test/other/file.py"))
        self.assertTrue(subject("file.txt"))

    def test_from_file(self):
        # TODO:
        pass
