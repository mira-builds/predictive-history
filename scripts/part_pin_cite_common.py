#!/usr/bin/env python3
"""Shared pin-cite helpers: transcript sectioning and L2 ref refresh."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOL2 = ROOT / "book" / "volume-ii"

PART_COMMENTARY_FILES: dict[str, str] = {
    "part-07-world-after-rome": "part-07-world-after-rome-commentary.md",
    "part-08-birth-of-modernity": "part-08-birth-of-modernity-commentary.md",
    "part-09-age-of-conscience": "part-09-age-of-conscience-commentary.md",
    "part-10-rise-of-the-nation-state": "part-10-rise-of-the-nation-state-commentary.md",
    "part-01-dawn-of-civilization": "part-01-dawn-of-civilization-commentary.md",
}


def part_paths(part_id: str, chapter_id: str) -> tuple[str, str]:
    comm_path = (
        f"../../../docs/routes/volume-i-parts/"
        f"{PART_COMMENTARY_FILES[part_id]}#{chapter_id}"
    )
    bib_path = f"../../../docs/routes/volume-i-parts/{part_id}-bibliography.md"
    return comm_path, bib_path


def split_transcript_body(body: str, sections: list[tuple[str, str]]) -> str:
    body = re.sub(r"\s+", " ", body).strip() + "\n"
    lower = body.lower()
    markers: list[tuple[int, str]] = []
    search_from = 0
    for slug, phrase in sections:
        idx = lower.find(phrase.lower(), search_from)
        if idx < 0:
            raise ValueError(f"Anchor not found: {slug!r} -> {phrase[:60]!r}...")
        markers.append((idx, slug))
        search_from = idx + 1
    markers.sort(key=lambda x: x[0])
    out: list[str] = []
    pos = 0
    for idx, slug in markers:
        if idx > pos:
            chunk = body[pos:idx].rstrip()
            if chunk:
                out.append(chunk)
        out.append(f"\n\n### {slug}\n\n")
        pos = idx
    out.append(body[pos:])
    return "".join(out).strip() + "\n"


def patch_transcript(
    chapter_id: str,
    sections: list[tuple[str, str]],
    *,
    part_id: str | None = None,
) -> None:
    path = VOL2 / chapter_id / f"{chapter_id}-transcript.md"
    text = path.read_text(encoding="utf-8")
    first_slug = sections[0][0]
    if f"### {first_slug}" in text:
        print(f"skip transcript (already sectioned): {path.relative_to(ROOT)}")
        return
    marker = "## Part I: Full transcript\n\n"
    if marker not in text:
        raise ValueError(f"Missing transcript marker in {path}")
    head, rest = text.split(marker, 1)
    body = rest.strip() + "\n"
    patched = split_transcript_body(body, sections)
    if "transcript_curation:" not in head:
        head = head.replace(
            "transcript_fidelity: exact_body_match\n",
            "transcript_fidelity: exact_body_match\n"
            "transcript_curation: curated_sectioned\n"
            "pin_cite_reviewed_at: 2026-06-09\n",
        )
    if part_id and "part_id:" not in head and part_id in PART_COMMENTARY_FILES:
        comm_path, bib_path = part_paths(part_id, chapter_id)
        head = head.replace(
            "part: I\n",
            f"part: I\npart_id: {part_id}\n"
            f"part_commentary_path: {comm_path}\n"
            f"part_bibliography_path: {bib_path}\n",
        )
    path.write_text(head + marker + patched, encoding="utf-8")
    print(f"patched transcript: {path.relative_to(ROOT)}")


def update_chapter_commentary(chapter_id: str, claim_refs: list[str]) -> None:
    path = VOL2 / chapter_id / f"{chapter_id}-commentary.md"
    text = path.read_text(encoding="utf-8")
    for i, anchor in enumerate(claim_refs, start=1):
        new_ref = f"`{chapter_id}-transcript.md{anchor}`"
        if new_ref in text:
            continue
        for old in (":32", ":29", ":31"):
            pattern = rf"(\| {i} \|[^\n]+\| )`?{chapter_id}-transcript\.md{old}`?"
            text, n = re.subn(pattern, rf"\1{new_ref}", text, count=1)
            if n:
                break
        else:
            pattern2 = rf"(\| {i} \|[^\n]+\| )TBD pin-cite"
            text, n2 = re.subn(pattern2, rf"\1{new_ref}", text, count=1)
            if n2 == 0 and new_ref not in text:
                raise ValueError(f"Row {i} not updated in {path}")
    if "analysis_depth: seed" in text:
        text = text.replace("analysis_depth: seed", "analysis_depth: layer2_drafted")
    path.write_text(text, encoding="utf-8")
    print(f"patched commentary: {path.relative_to(ROOT)}")
