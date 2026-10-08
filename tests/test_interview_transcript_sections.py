"""Tests for scripts/interview_transcript_sections.py."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from interview_transcript_sections import (  # noqa: E402
    insert_sections,
    normalize_for_anchor,
)


def test_insert_sections_splits_on_anchors_and_last_runs_to_eof():
    body = "Open line. First anchor section one. Second anchor section two tail."
    out = insert_sections(
        body,
        ["Open", "One", "Two"],
        ["first anchor", "second anchor"],
    )
    assert out.startswith("### Open\n\nOpen line.")
    assert "### One\n\nFirst anchor section one." in out
    assert "### Two\n\nSecond anchor section two tail." in out


def test_insert_sections_applies_asr_cleanup_before_split():
    body = "Start. Professor Dieng speaks. Next anchor part."
    out = insert_sections(
        body,
        ["A", "B"],
        ["next anchor"],
        asr_cleanup_fn=lambda t: t.replace("Professor Dieng", "Professor Jiang"),
    )
    assert "Professor Jiang speaks" in out
    assert "Professor Dieng" not in out


def test_normalize_for_anchor_unicode_punctuation():
    assert normalize_for_anchor("Let's — go") == "let's - go"
