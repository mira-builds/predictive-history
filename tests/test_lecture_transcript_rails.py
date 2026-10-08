"""Lecture transcript section rails — baseline ratchet tests."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))


def _audit_counts() -> dict[str, int]:
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / "lecture_section_pass.py"), "audit"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    counts: dict[str, int] = {}
    for line in proc.stdout.splitlines():
        if line.startswith("status:"):
            # status: {'slug': 69, 'flat': 80, ...}
            counts = eval(line.split(":", 1)[1].strip())
    return counts


def test_lecture_rails_strict_title_case():
    counts = _audit_counts()
    assert counts.get("title_case") == 150
    assert sum(counts.values()) == 150


def test_lecture_audit_strict_exit_zero():
    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "lecture_section_pass.py"),
            "audit",
            "--strict",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr


def test_slug_to_title_preserves_github_anchor():
    from lecture_rails_lib import github_heading_anchor, slug_to_title

    slug = "stalin-greatest-man-thesis"
    title = slug_to_title(slug)
    assert title == "Stalin Greatest Man Thesis"
    assert github_heading_anchor(title) == slug


def test_section_boundary_anchors_opening_not_empty():
    from interview_transcript_sections import insert_sections
    from lecture_rails_lib import section_boundary_anchors

    flat = (
        "okay start class recap of prior week today we look at the third force "
        "driving conflict let's look at a map of the region any questions"
    )
    sections = [
        {"title": "Opening"},
        {"title": "Third Force", "anchor": "today we look at the third force"},
        {"title": "Map", "anchor": "let's look at a map"},
        {"title": "Closing Questions"},
    ]
    anchors = section_boundary_anchors(sections, flat)
    body = insert_sections(flat, [s["title"] for s in sections], anchors)
    opening_chunk = body.split("### Third Force", 1)[0]
    assert "okay start class" in opening_chunk
    assert opening_chunk.strip().endswith("week") or "recap" in opening_chunk


def test_pin_cite_verifier_runs():
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / "verify_transcript_pin_cites.py"), "--source-id", "civ-59"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
