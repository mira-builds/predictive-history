#!/usr/bin/env python3
"""Apply Title Case section headings + light ASR cleanup to Glenn Diesen vi-03 transcript.

    python scripts/patch_glenn_diesen_jan_sections_asr.py
    python -m civ_ph.cli index --force
    python -m civ_ph.cli validate
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ID = "interview-2026-01-05-glenn-diesen"
TRANSCRIPT_PATH = ROOT / "interviews" / SOURCE_ID / f"{SOURCE_ID}.md"

SECTION_TITLES: list[str] = [
    "Show Open — 2026 and Prediction Method",
    "Game Theory — April Visit and Petrodollar Strategy",
    "Coercion vs Trust — US-China Codependency",
    "US Crisis — AI Bubble, Silver, and Civil War",
    "China Strategy — Exports, Japan, and Malacca",
    "Europe — Militarize Despite No Path to Victory",
    "European Elite — WWI Irrationality and Media Bubble",
    "Trump vs Europe — NATO Odessa and Immigration",
    "US Transactional Empire — Abandon Europe",
    "Venezuela Raid — Empire Decline and Trump World",
    "Iran, April Grand Bargain, and 2026 Close",
]

SECTION_ANCHORS: list[str] = [
    "i use game theory. i basically see geopolitics as a game",
    "but it looks like this can go both ways",
    "america has some major weaknesses, and you're right that it's possible",
    "the greatest strength and the greatest vulnerability of the united states is the us dollar",
    "the future is obvious. europe is going to militarize against russia",
    "the leadership of europe, the european elite, they live in their own reality",
    "the reality is that trump hates europe",
    "the united states is now transactional",
    "what we're seeing is an acceleration of the demise of the american empire",
    "trump was elected and the israelis helped to elect trump",
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
            r"(### Game Theory — April Visit and Petrodollar Strategy\n\n)(I use game theory)",
            r"\1**JIANG XUEQIN:** \2",
        ),
        (
            r"(### Coercion vs Trust — US-China Codependency\n\n)(But it looks like this can go both ways)",
            r"\1**GLENN DIESEN:** \2",
        ),
        (
            r"(### US Crisis — AI Bubble, Silver, and Civil War\n\n)(America has some major weaknesses)",
            r"\1**JIANG XUEQIN:** \2",
        ),
        (
            r"(### China Strategy — Exports, Japan, and Malacca\n\n)(The greatest strength and the greatest vulnerability of the United States is the US dollar)",
            r"\1**JIANG XUEQIN:** \2",
        ),
        (
            r"(### Europe — Militarize Despite No Path to Victory\n\n)(The future is obvious. Europe is going to militarize)",
            r"\1**JIANG XUEQIN:** \2",
        ),
        (
            r"(### European Elite — WWI Irrationality and Media Bubble\n\n)(The leadership of Europe, the European elite)",
            r"\1**JIANG XUEQIN:** \2",
        ),
        (
            r"(### Trump vs Europe — NATO Odessa and Immigration\n\n)(The reality is that Trump hates Europe)",
            r"\1**JIANG XUEQIN:** \2",
        ),
        (
            r"(### US Transactional Empire — Abandon Europe\n\n)(The United States is now transactional)",
            r"\1**JIANG XUEQIN:** \2",
        ),
        (
            r"(### Venezuela Raid — Empire Decline and Trump World\n\n)(What we're seeing is an acceleration of the demise of the American empire)",
            r"\1**JIANG XUEQIN:** \2",
        ),
        (
            r"(### Iran, April Grand Bargain, and 2026 Close\n\n)(Trump was elected and the Israelis helped to elect Trump)",
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
