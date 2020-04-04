import contextlib
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from typing import Iterable

from mbed_build._internal.new_find_files import find_files


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


class TestFindFiles(TestCase):
    def test_finds_files_by_name(self):
        test_files = [
            Path("file.txt"),
            Path("not_interested.txt"),
            Path("sub_directory", "file.txt"),
            Path("sub_directory", "not_interested.txt"),
        ]
        with create_files(test_files) as program_directory:
            subject = find_files("file.txt", program_directory)

        self.assertEqual(
            subject, [Path(program_directory, "file.txt"), Path(program_directory, "sub_directory", "file.txt")]
        )
