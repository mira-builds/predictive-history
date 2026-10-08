#!/usr/bin/env python3
"""Promote gb-12 transcript from YouTube ASR into volume-v mirror."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VTT = ROOT / "artifacts" / "gb-12-subs.en-orig.vtt"
OUT = ROOT / "book" / "volume-v" / "gb-12" / "gb-12-transcript.md"

SECTIONS: list[tuple[str, str]] = [
    ("opening-paradise-trilogy", "We conclude the Divine Comedy today"),
    ("homer-virgil-dante-arc", "three great poets"),
    ("dante-ends-dark-ages", "Dante will end the Dark Ages"),
    ("inferno-purgatory-paradise", "we've been through Inferno, we've been through Purgatory"),
    ("beatrice-guide-ascent", "Beatrice will be our guide"),
    ("moon-dark-spots", "what are the dark spots on this planet's body"),
    ("spheres-love-imagination", "imagination is what allows us"),
    ("soul-body-duality", "human has two aspects, a soul and a body"),
    ("trinity-vision", "three circles"),
    ("closing-love-moves-stars", "love that moves the sun"),
]

FRONTMATTER = """---
source_id: gb-12
public_slug: great-books-12-dante-in-paradise
title: "Great Books #12: Dante in Paradise"
series: great-books
episode: 12
book_chapter_id: gb-ch12
chapter_id: gb-12
part: I
part_id: part-06-medieval-imagination
part_commentary_path: ../../../docs/routes/volume-i-parts/part-06-medieval-imagination-commentary.md#gb-12
part_bibliography_path: ../../../docs/routes/volume-i-parts/part-06-medieval-imagination-bibliography.md
source_type: video
canonical_url: https://www.youtube.com/watch?v=FspDllFoiDE
video_id: FspDllFoiDE
publication_date: 2026-05-26
source_status: metadata_checked
transcript_status: curated_transcript
annotation_status: drafted
review_status: source_reviewed
source_reviewed_at: 2026-06-09
exported_from_youtube_at: 2026-06-09
fidelity_reviewed_at: 2026-06-09
representation_not_endorsement: true
transcript_fidelity: exact_body_match
transcript_source: youtube_auto_captions
transcript_curation: asr_spot_check_sectioned
corpus_path: ../../../corpus/great-books/gb-12.md
commentary_path: ./gb-12-commentary.md
---

# Part I - Great Books #12: Dante in Paradise

Part I contains the lecture transcript. Source: YouTube auto-captions (`en-orig`), spot-checked and sectioned 2026-06-09 (audio not re-aligned). Part II is kept in the companion commentary file.

## Part I: Full transcript

"""


def vtt_blocks_to_plain(vtt: str) -> str:
    blocks = re.split(r"\n\n+", vtt.replace("\r\n", "\n"))
    parts: list[str] = []
    prev: str | None = None
    for block in blocks:
        if "-->" not in block:
            continue
        lines: list[str] = []
        for ln in block.splitlines():
            s = ln.strip()
            if not s or "-->" in s or s.isdigit() or s.startswith("align:"):
                continue
            if s.startswith("Kind:") or s.startswith("Language:"):
                continue
            s = re.sub(r"<[^>]+>", "", s).strip()
            if s:
                lines.append(s)
        if not lines:
            continue
        best = max(lines, key=len)
        if best != prev:
            parts.append(best)
            prev = best
    return re.sub(r"\s+", " ", " ".join(parts)).strip()


def clean_body(text: str) -> str:
    text = re.sub(r"\[snorts\]\s*", "", text, flags=re.I)
    text = re.sub(r"\[clears throat\]\s*", "", text, flags=re.I)
    text = re.sub(r"\[laughter\]\s*", "", text, flags=re.I)
    text = re.sub(r"\[music\]\s*", "", text, flags=re.I)
    text = re.sub(r">>\s*", "", text)
    text = re.sub(r"&gt;&gt;\s*", "", text)
    text = re.sub(r"&gt;\s*", "", text)
    text = re.sub(r"\bVirtual\b", "Virgil", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def insert_sections(body: str) -> str:
    out: list[str] = []
    pos = 0
    for slug, phrase in SECTIONS:
        idx = body.find(phrase, pos)
        if idx < 0:
            raise ValueError(f"Section phrase not found for {slug}: {phrase[:40]!r}")
        if idx > pos:
            chunk = body[pos:idx].strip()
            if chunk:
                out.append(chunk)
        out.append(f"### {slug}\n")
        pos = idx
    tail = body[pos:].strip()
    if tail:
        out.append(tail)
    return "\n\n".join(out)


def main() -> None:
    if not VTT.is_file():
        raise SystemExit(f"VTT not found: {VTT}")
    raw = VTT.read_text(encoding="utf-8")
    body = clean_body(vtt_blocks_to_plain(raw))
    body = insert_sections(body)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(FRONTMATTER + body + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(body)} chars)")


if __name__ == "__main__":
    main()
