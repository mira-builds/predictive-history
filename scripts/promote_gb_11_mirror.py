#!/usr/bin/env python3
"""Promote gb-11 transcript from strategy-codex source-archive into volume-v mirror."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = (
    ROOT.parents[3]
    / "source-archive"
    / "statecraft"
    / "2026-05-26"
    / "source-gb-11-dantes-revolution-2026-05-26.md"
)
OUT = ROOT / "book" / "volume-v" / "gb-11" / "gb-11-transcript.md"

SECTIONS: list[tuple[str, str]] = [
    ("opening-purgatory-series", "So, we have a two-part lecture series"),
    ("augustine-virgil-human-nature", "And this will become the basis of the Catholic Church"),
    ("dante-intuition-rebuttal", "So, what Dante's going to do is he's going to assert"),
    ("purgatory-structure", "But the moment you enter purgatory"),
    ("envy-terrace-sharing", "And his reply, \"He knows the harm"),
    ("indras-net-love-fractal", "So, when we need to visualize this, it's with something called Indra's net"),
    ("virgil-love-reason-free-will", "Reason is the capacity to restrain our emotions by obeying authority"),
    ("purgatory-will-penance", "The issue is not that God has not forgiven us"),
    ("statius-paradox", "On Earth my name is still remembered, Statius"),
    ("virgil-disappears-beatrice", "Virgil, the gentlest father"),
]

FRONTMATTER = """---
source_id: gb-11
public_slug: great-books-11-dantes-revolution
title: "Great Books #11: Dante's Revolution"
series: great-books
episode: 11
book_chapter_id: gb-ch11
chapter_id: gb-11
part: I
part_id: part-06-medieval-imagination
part_commentary_path: ../../../docs/routes/volume-i-parts/part-06-medieval-imagination-commentary.md#gb-11
part_bibliography_path: ../../../docs/routes/volume-i-parts/part-06-medieval-imagination-bibliography.md
source_type: video
canonical_url: https://www.youtube.com/watch?v=otyUpKhpTYM
video_id: otyUpKhpTYM
publication_date: 2026-05-26
source_status: metadata_checked
transcript_status: curated_transcript
annotation_status: drafted
review_status: source_reviewed
source_reviewed_at: 2026-06-09
public_imported_at: 2026-06-09
promoted_from: strategy-codex/source-archive/statecraft/2026-05-26/source-gb-11-dantes-revolution-2026-05-26.md
representation_not_endorsement: true
transcript_fidelity: exact_body_match
transcript_source: operator_paste_capture
transcript_curation: archive_promotion_sectioned
corpus_path: ../../../corpus/great-books/gb-11.md
commentary_path: ./gb-11-commentary.md
---

# Part I - Great Books #11: Dante's Revolution

Part I contains the lecture transcript promoted from strategy-codex source archive (operator paste, 2026-05-26). Part II is kept in the companion commentary file.

## Part I: Full transcript

"""


def clean_body(text: str) -> str:
    text = re.sub(r"^# Great Books.*\n\n", "", text, count=1)
    text = re.sub(r"\[snorts\]\s*", "", text, flags=re.I)
    text = re.sub(r"\[clears throat\]\s*", "", text, flags=re.I)
    text = re.sub(r"\[laughter\]\s*", "", text, flags=re.I)
    text = re.sub(r"\[music\]\s*", "", text, flags=re.I)
    text = re.sub(r">>\s*", "", text)
    text = re.sub(r"\bVirtual\b", "Virgil", text)
    text = re.sub(r"\bSatius\b", "Statius", text)
    text = re.sub(r"\bOKAY\?\s*HE DID NOT", "Okay? He did not", text)
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
    if not ARCHIVE.is_file():
        raise SystemExit(f"Archive not found: {ARCHIVE}")
    raw = ARCHIVE.read_text(encoding="utf-8")
    if raw.startswith("---"):
        end = raw.find("\n---", 3)
        raw = raw[end + 4 :].lstrip() if end >= 0 else raw
    body = clean_body(raw)
    body = insert_sections(body)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(FRONTMATTER + body + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
