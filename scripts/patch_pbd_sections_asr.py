#!/usr/bin/env python3
"""Apply Title Case section headings + light ASR cleanup to PBD vi-13 transcript.

    python scripts/patch_pbd_sections_asr.py
    python -m civ_ph.cli index --force
    python -m civ_ph.cli validate
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ID = "interview-2026-04-07-patrick-bet-david"
TRANSCRIPT_PATH = ROOT / "interviews" / SOURCE_ID / f"{SOURCE_ID}.md"

SECTION_TITLES: list[str] = [
    "Show Open — Predictions and Hubris",
    "Trump Truth Social — Escalation and Scenarios",
    "IRGC, Off-Ramp, and Four-Power Diplomacy",
    "NATO, Globalists, and Post-War Iran Extremism",
    "China — Population, Demographics, and Lie Flat",
    "Jack Ma, Jimmy Lai, and Bureaucrat Culture",
    "Biography — Yale, PBS Arrest, and Why China",
    "Gray Zone, Monitoring, and Iran Youth Dreams",
    "COVID Narrative, Free Speech, and Surveillance State",
    "Soft Power, Muslims, Red Lines, and Closing",
]

SECTION_ANCHORS: list[str] = [
    "now, let me go to the tweet of what president trump posted",
    "yeah, tulsi — i think there was another name as well",
    "a lot of people agree with you on that. a lot of people agree with you. but here's the problem",
    "let me ask you a couple other questions about china since you're in beijing right now",
    "let me ask another question in regards to the lie flat. i'm going more on the business side with jack ma",
    "what do you like about each country? because you chose to go back to china",
    "do you feel safe for yourself in china long term?",
    "let's talk about covid. covid is the time when i started talking about politics",
    "last question here with muslims and what is the position that xi jinping",
]


def asr_cleanup(text: str) -> str:
    text = text.replace("Osager and Crystal", "Saagar and Crystal")
    text = text.replace("Osager", "Saagar")
    text = re.sub(
        r"(?m)^The best case scenario is that the Americans",
        "**Jiang Xueqin:** The best case scenario is that the Americans",
        text,
        count=1,
    )
    text = text.replace("cow sheet type", "odds-sheet type")
    text = re.sub(r"\bThe The\b", "The", text)
    text = re.sub(r"\bthe the\b", "the", text, flags=re.I)
    text = re.sub(r"\bof of\b", "of", text)
    return text


def find_anchor_pos(flat: str, anchor: str, start: int) -> int:
    pos = flat.lower().find(anchor, start)
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
        chunk = flat[positions[i] : positions[i + 1]].strip()
        parts.append(f"### {heading}\n\n{chunk}")
    return "\n\n".join(parts)


def update_frontmatter(text: str) -> str:
    today = date.today().isoformat()
    text = re.sub(
        r"^transcript_curation:.*$",
        "transcript_curation: curated_sectioned",
        text,
        count=1,
        flags=re.M,
    )
    if "fidelity_reviewed_at:" in text:
        text = re.sub(
            r"^fidelity_reviewed_at:.*$",
            f"fidelity_reviewed_at: {today}",
            text,
            count=1,
            flags=re.M,
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
    body = insert_sections(body.strip())
    doc = f"{head}## Part I: Full transcript\n\n{body}\n"
    TRANSCRIPT_PATH.write_text(doc, encoding="utf-8", newline="\n")
    print(
        f"wrote {TRANSCRIPT_PATH} "
        f"({len(body.split()):,} words, {len(SECTION_TITLES)} sections)"
    )


if __name__ == "__main__":
    main()
