#!/usr/bin/env python3
"""Apply Title Case section headings + light ASR cleanup to Glenn Diesen vi-02 transcript.

    python scripts/patch_glenn_diesen_nov_sections_asr.py
    python -m civ_ph.cli index --force
    python -m civ_ph.cli validate
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ID = "interview-2025-11-24-glenn-diesen"
TRANSCRIPT_PATH = ROOT / "interviews" / SOURCE_ID / f"{SOURCE_ID}.md"

SECTION_TITLES: list[str] = [
    "Show Open — Civilizational Rise and Decline",
    "Civilizations Rise — Energy, Openness, and Cohesion",
    "Western Decline — Energy, Openness, and Cohesion",
    "Collapse Theories — Turchin, Piketty, and Spengler",
    "2008 Crisis — Cheap Money and Elite Capture",
    "Roman Populism — Gracchi, Caesar, and Bernie Sanders",
    "Trump — Agency and Burn-Down-the-House",
    "Ukraine — War Over and March to Odessa",
    "Western Closed Society — Yale, Propaganda, and Immigration",
    "US-China — Status Quo and Rapprochement",
    "Russia-China Limits — Kazakhstan and US Balancing",
    "Pax Judea — Close and Predictive History",
]

SECTION_ANCHORS: list[str] = [
    "in my analysis of world history, when civilizations rise",
    "according to this framework, the western world",
    "that's a great point. social cohesion is a huge problem",
    "you bring up a good point about the 2008-2009 great financial crisis",
    "let's look at ancient rome. after the three punic wars",
    "in 2016, the entire world was shocked, bewildered, confused",
    "i think for the past year the war has been over",
    "i went to school at yale and this was like the late",
    "i have a very different take on the us-china rivalry than other analysts",
    "i am not that optimistic about the russia-china relationship",
    "one thing i'm looking very closely at",
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


def cleanup_glenn_diesen_speakers(body: str) -> str:
    body = re.sub(
        r"\n\n\*\*(?:GLENN DIESEN|JIANG XUEQIN):\*\*\n\n(### )",
        r"\n\n\1",
        body,
    )
    fixes = [
        (
            r"(### Civilizations Rise — Energy, Openness, and Cohesion\n\n)(In my analysis of world history, when civilizations rise)",
            r"\1**JIANG XUEQIN:** \2",
        ),
        (
            r"(### Western Decline — Energy, Openness, and Cohesion\n\n)(According to this framework, the Western world)",
            r"\1**JIANG XUEQIN:** \2",
        ),
        (
            r"(### Collapse Theories — Turchin, Piketty, and Spengler\n\n)(That's a great point. Social cohesion)",
            r"\1**JIANG XUEQIN:** \2",
        ),
        (
            r"(### 2008 Crisis — Cheap Money and Elite Capture\n\n)(You bring up a good point about the 2008-2009)",
            r"\1**JIANG XUEQIN:** \2",
        ),
        (
            r"(### Roman Populism — Gracchi, Caesar, and Bernie Sanders\n\n)(Let's look at ancient Rome. After the three Punic Wars)",
            r"\1**JIANG XUEQIN:** \2",
        ),
        (
            r"(### Trump — Agency and Burn-Down-the-House\n\n)(In 2016, the entire world was shocked)",
            r"\1**JIANG XUEQIN:** \2",
        ),
        (
            r"(### Ukraine — War Over and March to Odessa\n\n)(I think for the past year the war has been over)",
            r"\1**JIANG XUEQIN:** \2",
        ),
        (
            r"(### Western Closed Society — Yale, Propaganda, and Immigration\n\n)(I went to school at Yale and this was like the late)",
            r"\1**JIANG XUEQIN:** \2",
        ),
        (
            r"(### US-China — Status Quo and Rapprochement\n\n)(I have a very different take on the US-China rivalry)",
            r"\1**JIANG XUEQIN:** \2",
        ),
        (
            r"(### Russia-China Limits — Kazakhstan and US Balancing\n\n)(I am not that optimistic about the Russia-China relationship)",
            r"\1**JIANG XUEQIN:** \2",
        ),
        (
            r"(### Pax Judea — Close and Predictive History\n\n)(One thing I'm looking very closely at)",
            r"\1**JIANG XUEQIN:** \2",
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
    body = cleanup_glenn_diesen_speakers(insert_sections(body.strip()))
    doc = f"{head}## Part I: Full transcript\n\n{body}\n"
    TRANSCRIPT_PATH.write_text(doc, encoding="utf-8", newline="\n")
    print(
        f"wrote {TRANSCRIPT_PATH} "
        f"({len(body.split()):,} words, {len(SECTION_TITLES)} sections)"
    )


if __name__ == "__main__":
    main()
