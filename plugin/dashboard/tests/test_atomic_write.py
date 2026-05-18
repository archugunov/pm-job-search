"""Tests for atomic_write — write a file via tempfile + rename."""
from pathlib import Path

from serve import atomic_write


def test_writes_new_file(tmp_path: Path):
    target = tmp_path / "out.txt"
    atomic_write(target, "hello\n")
    assert target.read_text() == "hello\n"


def test_overwrites_existing_file(tmp_path: Path):
    target = tmp_path / "out.txt"
    target.write_text("old\n")
    atomic_write(target, "new\n")
    assert target.read_text() == "new\n"


def test_uses_same_directory_for_tempfile(tmp_path: Path):
    target = tmp_path / "out.txt"
    atomic_write(target, "data\n")
    tmp_files = [p for p in tmp_path.iterdir() if p.name != "out.txt"]
    assert tmp_files == [], f"leftover temp files: {tmp_files}"


def test_creates_parent_directory_if_missing(tmp_path: Path):
    target = tmp_path / "nested" / "out.txt"
    atomic_write(target, "x\n")
    assert target.read_text() == "x\n"
