#!/usr/bin/env python3
"""Apply Title Case section headings + light ASR cleanup to Dialogue Works vi-08 transcript.

    python scripts/patch_dialogue_works_sections_asr.py
    python -m civ_ph.cli index --force
    python -m civ_ph.cli validate
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ID = "interview-2026-03-07-dialogue-works"
TRANSCRIPT_PATH = ROOT / "interviews" / SOURCE_ID / f"{SOURCE_ID}.md"

SECTION_TITLES: list[str] = [
    "Show Open — Nima Welcomes Professor Jiang",
    "World War III — Ground Troops and Strait of Hormuz",
    "Greater Israel — Oil Control and Mossad False Flags",
    "American Empire Decay — Cold War to Iran Blowback",
    "GCC Mirage — British Construct and Regional Collapse",
    "Twelve-Day War — Israeli Media Blackout and Ground Troops",
]

SECTION_ANCHORS: list[str] = [
    "we are in world war iii right now",
    "israel, since its founding in 1948",
    "as you point out, america is desperate",
    "first of all, it's important to understand that these gcc countries",
    "there's a very good reason why there's no footage coming out of israel",
]


def asr_cleanup(text: str) -> str:
    text = text.replace("Professor Dieng", "Professor Jiang")
    text = re.sub(r"\bThe The\b", "The", text)
    text = re.sub(r"\bthe the\b", "the", text, flags=re.I)
    return text


def normalize_for_anchor(s: str) -> str:
    s = s.replace("\u2019", "'").replace("\u2018", "'")
    s = s.replace("\u201c", '"').replace("\u201d", '"')
    s = s.replace("\u2014", "-").replace("\u2013", "-")
    return s.lower()


def find_anchor_pos(flat: str, anchor: str, start: int) -> int:
    hay = normalize_for_anchor(flat)
    needle = normalize_for_anchor(anchor)
    pos = hay.find(needle, start)
    if pos == -1:
        raise ValueError(f"anchor not found: {anchor!r} (from pos {start})")
    return pos


def insert_sections(body: str) -> str:
    flat = asr_cleanup(body)
    positions = [0]
    cursor = 0
    for anchor in SECTION_ANCHORS:
        pos = find_anchor_pos(flat, anchor, cursor)
        positions.append(pos)
        cursor = pos + len(anchor)
    positions.append(len(flat))

    parts: list[str] = []
    for i, heading in enumerate(SECTION_TITLES):
        end = len(flat) if i == len(SECTION_TITLES) - 1 else positions[i + 1]
        chunk = flat[positions[i] : end].strip()
        parts.append(f"### {heading}\n\n{chunk}")
    return "\n\n".join(parts)


def cleanup_dialogue_works_speakers(body: str) -> str:
    body = re.sub(
        r"\n\n\*\*(?:Nima|Jiang Xueqin):\*\*\n\n(### )",
        r"\n\n\1",
        body,
    )
    fixes = [
        (
            r"(### World War III — Ground Troops and Strait of Hormuz\n\n)(We are in World War III)",
            r"\1**Jiang Xueqin:** \2",
        ),
        (
            r"(### Greater Israel — Oil Control and Mossad False Flags\n\n)(Israel, since its founding)",
            r"\1**Jiang Xueqin:** \2",
        ),
        (
            r"(### American Empire Decay — Cold War to Iran Blowback\n\n)(As you point out, America is desperate)",
            r"\1**Jiang Xueqin:** \2",
        ),
        (
            r"(### GCC Mirage — British Construct and Regional Collapse\n\n)(First of all, it's important to understand that these GCC countries)",
            r"\1**Jiang Xueqin:** \2",
        ),
        (
            r"(### Twelve-Day War — Israeli Media Blackout and Ground Troops\n\n)(There's a very good reason why there's no footage coming out of Israel)",
            r"\1**Jiang Xueqin:** \2",
        ),
    ]
    for pattern, repl in fixes:
        body = re.sub(pattern, repl, body, count=1)
    return body


def update_frontmatter(text: str) -> str:
    today = date.today().isoformat()
    text = re.sub(
        r"^transcript_curation:.*$",
        "transcript_curation: curated_sectioned",
        text,
        count=1,
        flags=re.M,
    )
    if "transcript_curation:" not in text.split("---", 2)[1]:
        text = text.replace(
            "transcript_fidelity: exact_body_match\n",
            "transcript_fidelity: exact_body_match\ntranscript_curation: curated_sectioned\n",
            1,
        )
    if "fidelity_reviewed_at:" in text:
        text = re.sub(
            r"^fidelity_reviewed_at:.*$",
            f"fidelity_reviewed_at: {today}",
            text,
            count=1,
            flags=re.M,
        )
    else:
        text = text.replace(
            "source_reviewed_at: 2026-06-25\n",
            f"source_reviewed_at: 2026-06-25\nfidelity_reviewed_at: {today}\n",
            1,
        )
    return text


def main() -> None:
    doc = TRANSCRIPT_PATH.read_text(encoding="utf-8")
    if "## Part I: Full transcript\n" not in doc:
        raise ValueError("missing Part I marker")

    head, body = doc.split("## Part I: Full transcript\n", 1)
    if body.lstrip().startswith("### "):
        raise ValueError("transcript already sectioned")

    head = update_frontmatter(head)
    body = cleanup_dialogue_works_speakers(insert_sections(body.strip()))
    doc = f"{head}## Part I: Full transcript\n\n{body}\n"
    TRANSCRIPT_PATH.write_text(doc, encoding="utf-8", newline="\n")
    print(
        f"wrote {TRANSCRIPT_PATH} "
        f"({len(body.split()):,} words, {len(SECTION_TITLES)} sections)"
    )


if __name__ == "__main__":
    main()
