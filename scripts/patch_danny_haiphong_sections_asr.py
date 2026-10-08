#!/usr/bin/env python3
"""Apply Title Case section headings + light ASR cleanup to Danny Haiphong vi-04 transcript.

    python scripts/patch_danny_haiphong_sections_asr.py
    python -m civ_ph.cli index --force
    python -m civ_ph.cli validate
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ID = "interview-2026-01-18-danny-haiphong"
TRANSCRIPT_PATH = ROOT / "interviews" / SOURCE_ID / f"{SOURCE_ID}.md"

SECTION_TITLES: list[str] = [
    "Show Open — Happy New Year and Iran Flash Point",
    "Iran Chain — Color Revolution, Starlink, and Paused Strikes",
    "Trump Optics — Houthis and American Military Limits",
    "Game Theory War — Propaganda, Bombs, and Dollars vs Iran",
    "Color Revolution Playbook — Overstretch and Carrier Gap",
    "National Security Strategy — China Blockade and 2026 Exhaustion",
]

SECTION_ANCHORS: list[str] = [
    "let's talk about iran and let's look at the chain of events",
    "first of all, trump is first and foremost concerned about optics",
    "let's game theory this war between the united states and iran",
    "it's this classic color revolution playbook where you control the information space",
    "i think first and foremost there's this misinterpretation of what the national security strategy says",
]


def asr_cleanup(text: str) -> str:
    text = text.replace("Professor Dieng", "Professor Jiang")
    text = text.replace("Dawn Roll Doctrine", "Donroe Doctrine")
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


def cleanup_danny_haiphong_speakers(body: str) -> str:
    body = re.sub(
        r"\n\n\*\*(?:DANNY HAIPHONG|JIANG XUEQIN):\*\*\n\n(### )",
        r"\n\n\1",
        body,
    )
    ap = r"['\u2019]"
    fixes = [
        (
            rf"(### Iran Chain — Color Revolution, Starlink, and Paused Strikes\n\n)"
            rf"(?!\*\*JIANG XUEQIN:\*\*)"
            rf"(Let{ap}s talk about Iran)",
            r"\1**JIANG XUEQIN:** \2",
        ),
        (
            rf"(### Trump Optics — Houthis and American Military Limits\n\n)"
            rf"(?!\*\*JIANG XUEQIN:\*\*)"
            rf"(First of all, Trump is first and foremost concerned about optics)",
            r"\1**JIANG XUEQIN:** \2",
        ),
        (
            rf"(### Game Theory War — Propaganda, Bombs, and Dollars vs Iran\n\n)"
            rf"(?!\*\*JIANG XUEQIN:\*\*)"
            rf"(Let{ap}s game theory this war between the United States and Iran)",
            r"\1**JIANG XUEQIN:** \2",
        ),
        (
            rf"(### Color Revolution Playbook — Overstretch and Carrier Gap\n\n)"
            rf"(?!\*\*JIANG XUEQIN:\*\*)"
            rf"(It{ap}s this classic color revolution playbook)",
            r"\1**JIANG XUEQIN:** \2",
        ),
        (
            rf"(### National Security Strategy — China Blockade and 2026 Exhaustion\n\n)"
            rf"(?!\*\*JIANG XUEQIN:\*\*)"
            rf"(I think first and foremost there{ap}s this misinterpretation of what the National Security Strategy says)",
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
    body = cleanup_danny_haiphong_speakers(insert_sections(body.strip()))
    doc = f"{head}## Part I: Full transcript\n\n{body}\n"
    TRANSCRIPT_PATH.write_text(doc, encoding="utf-8", newline="\n")
    print(
        f"wrote {TRANSCRIPT_PATH} "
        f"({len(body.split()):,} words, {len(SECTION_TITLES)} sections)"
    )


if __name__ == "__main__":
    main()
