#!/usr/bin/env python3
"""Apply Title Case section headings + light ASR cleanup to Sneako vi-09 transcript.

    python scripts/patch_sneako_sections_asr.py
    python -m civ_ph.cli index --force
    python -m civ_ph.cli validate
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ID = "interview-2026-03-09-sneako"
TRANSCRIPT_PATH = ROOT / "interviews" / SOURCE_ID / f"{SOURCE_ID}.md"

SECTION_TITLES: list[str] = [
    "Show Open — Sneako Callback and Predictive History",
    "Ground Invasion — Proxies, Kurds, and Troop Counts",
    "Protest Death Toll and False-Flag Layer",
    "GCC Strikes, Mirage, and Iranian Diaspora",
    "Empire Decline — Venezuela, Cuba, and Debt Bomb",
    "PBD Setup, Nuclear Discount, and Regional Players",
    "Israel Power, Eschatology, and Kabbalah",
    "Consciousness, Predictions, and Close",
]

SECTION_ANCHORS: list[str] = [
    "this is actually very hard to figure out because the usual strategy is to use proxies",
    "there's a lot of vietnam analogies here. it's extremely unpopular with the youth",
    "the gcc has been hit quite a bit",
    "we saw the same with venezuela. now lindsey graham and trump are talking about cuba",
    "back to patrick bet-david",
    "this goes much deeper into eschatology, chabad lubavitch",
    "what is the real truth? is there one true creator",
]


def remove_misordered_opening(text: str) -> str:
    """Drop caption-order fragment duplicated later in the conversation."""
    start_marker = "**SNEAKO:** If it's true that Israel wants America to lose this war"
    keep_marker = "**SNEAKO:** What are your immediate predictions with this war?"
    start = text.find(start_marker)
    keep = text.find(keep_marker)
    if start != -1 and keep != -1 and start < keep:
        text = text[:start] + text[keep:]
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


def cleanup_sneako_speakers(body: str) -> str:
    body = re.sub(
        r"\n\n\*\*(?:SNEAKO|Professor Jiang):\*\*\n\n(### )",
        r"\n\n\1",
        body,
    )
    fixes = [
        (
            r"(### Ground Invasion — Proxies, Kurds, and Troop Counts\n\n)(This is actually very hard to figure out)",
            r"\1**Professor Jiang:** \2",
        ),
        (
            r"(### Protest Death Toll and False-Flag Layer\n\n)(There's a lot of Vietnam analogies here)",
            r"\1**SNEAKO:** \2",
        ),
        (
            r"(### GCC Strikes, Mirage, and Iranian Diaspora\n\n)(The GCC has been hit quite a bit)",
            r"\1**SNEAKO:** \2",
        ),
        (
            r"(### Empire Decline — Venezuela, Cuba, and Debt Bomb\n\n)(We saw the same with Venezuela)",
            r"\1**SNEAKO:** \2",
        ),
        (
            r"(### PBD Setup, Nuclear Discount, and Regional Players\n\n)(Back to Patrick Bet-David)",
            r"\1**SNEAKO:** \2",
        ),
        (
            r"(### Israel Power, Eschatology, and Kabbalah\n\n)(This goes much deeper into eschatology)",
            r"\1**SNEAKO:** \2",
        ),
        (
            r"(### Consciousness, Predictions, and Close\n\n)(What is the real truth\? Is there one true creator\?)",
            r"\1**SNEAKO:** \2",
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
    body = cleanup_sneako_speakers(insert_sections(body.strip()))
    doc = f"{head}## Part I: Full transcript\n\n{body}\n"
    TRANSCRIPT_PATH.write_text(doc, encoding="utf-8", newline="\n")
    print(
        f"wrote {TRANSCRIPT_PATH} "
        f"({len(body.split()):,} words, {len(SECTION_TITLES)} sections)"
    )


if __name__ == "__main__":
    main()
