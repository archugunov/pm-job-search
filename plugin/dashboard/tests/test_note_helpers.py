"""Tests for split_notes / edit_note / delete_note pure helpers."""
from __future__ import annotations

from textwrap import dedent

import pytest

from serve import delete_note, edit_note, split_notes


SAMPLE = dedent("""\
    # Notes — Plaid Senior PM

    ## 2026-05-18 14:30

    First note.

    ## 2026-05-15 09:00

    Second note.
    Multiple lines.
    """)


def test_split_notes_separates_preamble_and_entries():
    preamble, entries = split_notes(SAMPLE)
    assert preamble.startswith("# Notes — Plaid Senior PM")
    assert [h for h, _ in entries] == ["2026-05-18 14:30", "2026-05-15 09:00"]
    assert "First note." in entries[0][1]
    assert "Multiple lines." in entries[1][1]


def test_split_notes_handles_empty_file():
    assert split_notes("") == ("", [])


def test_split_notes_handles_file_with_only_preamble():
    preamble, entries = split_notes("# Notes — X\n")
    assert preamble == "# Notes — X\n"
    assert entries == []


def test_edit_note_replaces_body_keeps_heading():
    out = edit_note(SAMPLE, 0, "2026-05-18 14:30", "Updated first note.")
    assert "Updated first note." in out
    assert "First note." not in out
    # Heading unchanged.
    assert "## 2026-05-18 14:30" in out
    # Other entry untouched.
    assert "Second note." in out


def test_edit_note_rejects_empty_body():
    with pytest.raises(ValueError, match="empty"):
        edit_note(SAMPLE, 0, "2026-05-18 14:30", "   ")


def test_edit_note_rejects_bad_index():
    with pytest.raises(ValueError, match="out of range"):
        edit_note(SAMPLE, 99, "anything", "x")


def test_edit_note_rejects_heading_mismatch():
    with pytest.raises(ValueError, match="heading mismatch"):
        edit_note(SAMPLE, 0, "wrong-heading", "x")


def test_delete_note_removes_section():
    out = delete_note(SAMPLE, 0, "2026-05-18 14:30")
    assert "First note." not in out
    assert "Second note." in out
    assert "## 2026-05-15 09:00" in out
    assert "## 2026-05-18 14:30" not in out


def test_delete_note_rejects_heading_mismatch():
    with pytest.raises(ValueError, match="heading mismatch"):
        delete_note(SAMPLE, 0, "not-the-real-heading")


def test_delete_note_rejects_bad_index():
    with pytest.raises(ValueError, match="out of range"):
        delete_note(SAMPLE, -1, "anything")


def test_edit_then_delete_roundtrip_preserves_structure():
    after_edit = edit_note(SAMPLE, 1, "2026-05-15 09:00", "Replaced body.")
    after_delete = delete_note(after_edit, 0, "2026-05-18 14:30")
    _, entries = split_notes(after_delete)
    assert len(entries) == 1
    assert entries[0][0] == "2026-05-15 09:00"
    assert "Replaced body." in entries[0][1]
