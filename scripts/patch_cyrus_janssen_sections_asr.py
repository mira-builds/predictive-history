#!/usr/bin/env python3
"""Apply Title Case section headings + light ASR cleanup to Cyrus Janssen vi-01 transcript.

    python scripts/patch_cyrus_janssen_sections_asr.py
    python -m civ_ph.cli index --force
    python -m civ_ph.cli validate
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ID = "interview-2025-10-30-cyrus-janssen"
TRANSCRIPT_PATH = ROOT / "interviews" / SOURCE_ID / f"{SOURCE_ID}.md"

SECTION_TITLES: list[str] = [
    "Show Open — Cyrus Welcomes Professor Jiang",
    "Game Theory — Predicting Geopolitics",
    "Middle East — Trade, Oil, Eschatology, and Hamas",
    "Russia-Ukraine — NATO Provocation and Mafia Empire",
    "Ukraine Finished — Casualties and Partition",
    "NATO Expansion — Three Facts and Domino Theory",
    "Sunk Cost — Odessa as Final Battle",
    "US-China — Trade War, Rapprochement, and People-to-People",
    "Taiwan — Why Invasion Is Idiotic",
    "Flash Points, Geophysical Risk, and Close",
]

SECTION_ANCHORS: list[str] = [
    "i see geopolitics as a game among different players",
    "trump is known for overstatement",
    "according to game theory, russia had no choice but to invade ukraine",
    "ukraine has no future. ukraine is finished as a nation",
    "listen to the facts. the first fact is that when the soviet union fell",
    "i think most military analysts actually say the war is lost",
    "america is behaving like a mafia state",
    "from a game theory perspective, it would be idiotic to go invade taiwan",
    "in the short term the geopolitical conflicts are an issue",
]


def remove_misordered_opening(text: str) -> str:
    """Drop caption-order clip duplicated in the main interview."""
    start_marker = "**Cyrus Janssen:** I see geopolitics as a game among different players"
    keep_marker = "This is Professor Jiang Xueqin, one of the fastest growing geopolitical YouTubers"
    start = text.find(start_marker)
    keep = text.find(keep_marker)
    if start != -1 and keep != -1 and start < keep:
        text = text[:start] + "**Cyrus Janssen:** " + text[keep:]
    return text


def asr_cleanup(text: str) -> str:
    text = remove_misordered_opening(text)
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


def cleanup_cyrus_janssen_speakers(body: str) -> str:
    body = re.sub(
        r"\n\n\*\*(?:Cyrus Janssen|Professor Jiang Xueqin):\*\*\n\n(### )",
        r"\n\n\1",
        body,
    )
    fixes = [
        (
            r"(### Game Theory — Predicting Geopolitics\n\n)(I see geopolitics as a game among different players)",
            r"\1**Professor Jiang Xueqin:** \2",
        ),
        (
            r"(### Middle East — Trade, Oil, Eschatology, and Hamas\n\n)(Trump is known for overstatement)",
            r"\1**Professor Jiang Xueqin:** \2",
        ),
        (
            r"(### Russia-Ukraine — NATO Provocation and Mafia Empire\n\n)(According to game theory, Russia had no choice)",
            r"\1**Professor Jiang Xueqin:** \2",
        ),
        (
            r"(### Ukraine Finished — Casualties and Partition\n\n)(Ukraine has no future)",
            r"\1**Professor Jiang Xueqin:** \2",
        ),
        (
            r"(### NATO Expansion — Three Facts and Domino Theory\n\n)(Listen to the facts)",
            r"\1**Professor Jiang Xueqin:** \2",
        ),
        (
            r"(### Sunk Cost — Odessa as Final Battle\n\n)(I think most military analysts actually say the war is lost)",
            r"\1**Professor Jiang Xueqin:** \2",
        ),
        (
            r"(### US-China — Trade War, Rapprochement, and People-to-People\n\n)(America is behaving like a mafia state)",
            r"\1**Professor Jiang Xueqin:** \2",
        ),
        (
            r"(### Taiwan — Why Invasion Is Idiotic\n\n)(From a game theory perspective, it would be idiotic to go invade Taiwan)",
            r"\1**Professor Jiang Xueqin:** \2",
        ),
        (
            r"(### Flash Points, Geophysical Risk, and Close\n\n)(In the short term the geopolitical conflicts are an issue)",
            r"\1**Professor Jiang Xueqin:** \2",
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
    body = cleanup_cyrus_janssen_speakers(insert_sections(body.strip()))
    doc = f"{head}## Part I: Full transcript\n\n{body}\n"
    TRANSCRIPT_PATH.write_text(doc, encoding="utf-8", newline="\n")
    print(
        f"wrote {TRANSCRIPT_PATH} "
        f"({len(body.split()):,} words, {len(SECTION_TITLES)} sections)"
    )


if __name__ == "__main__":
    main()
