#!/usr/bin/env python3
"""Apply Title Case section headings + light ASR cleanup to Glenn Diesen vi-14 transcript.

    python scripts/patch_glenn_diesen_april_sections_asr.py
    python -m civ_ph.cli index --force
    python -m civ_ph.cli validate
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ID = "interview-2026-04-13-glenn-diesen"
TRANSCRIPT_PATH = ROOT / "interviews" / SOURCE_ID / f"{SOURCE_ID}.md"

SECTION_TITLES: list[str] = [
    "Show Open — Petrodollar and Piracy",
    "War Escalation and Islamabad Talks",
    "Trump Business Logic and China Leverage",
    "Naval Blockade — Malacca and Countermeasures",
    "Deep State, Prodi, and Military as Pirate Force",
    "Empire Extractivism and Great Power Response",
    "Perpetual War, BRI, and Ground Troops",
    "Tehran Siege and NATO Shadow War",
]

SECTION_ANCHORS: list[str] = [
    "so what do they need to achieve then in this war?",
    "let me try to figure out how donald trump thinks because he's a businessman",
    "the naval blockade. this is a strange conception",
    "romano prodi, the former prime minister of italy",
    "what's interesting with trump though, there's some consistency here",
    "so how will the great powers respond then?",
    "i often think about the current situation. it resembles a little bit like before world war i",
]


def asr_cleanup(text: str) -> str:
    text = text.replace("interceptive missiles", "interceptor missiles")
    text = text.replace(
        "more than the law of Belt and Road infrastructure",
        "more bombing of Belt and Road infrastructure",
    )
    text = re.sub(
        r"\*\*Glenn Diesen:\*\* Let me try to figure out how Donald Trump thinks",
        "**Jiang Xueqin:** Let me try to figure out how Donald Trump thinks",
        text,
        count=1,
    )
    text = re.sub(r"\bThe The\b", "The", text)
    text = re.sub(r"\bthe the\b", "the", text, flags=re.I)
    return text


def normalize_for_anchor(s: str) -> str:
    s = s.replace("\u2019", "'").replace("\u2018", "'")
    s = s.replace("\u201c", '"').replace("\u201d", '"')
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


def cleanup_glenn_speakers(body: str) -> str:
    body = re.sub(
        r"\n\n\*\*(?:Glenn Diesen|Jiang Xueqin):\*\*\n\n(### )",
        r"\n\n\1",
        body,
    )
    fixes = [
        (r"(### War Escalation and Islamabad Talks\n\n)(So what do they need)", r"\1**Glenn Diesen:** \2"),
        (r"(### Trump Business Logic and China Leverage\n\n)(Let me try)", r"\1**Jiang Xueqin:** \2"),
        (r"(### Naval Blockade — Malacca and Countermeasures\n\n)(The naval blockade)", r"\1**Glenn Diesen:** \2"),
        (r"(### Deep State, Prodi, and Military as Pirate Force\n\n)(Romano Prodi)", r"\1**Glenn Diesen:** \2"),
        (r"(### Empire Extractivism and Great Power Response\n\n)(What's interesting with Trump)", r"\1**Glenn Diesen:** \2"),
        (r"(### Perpetual War, BRI, and Ground Troops\n\n)(So how will the great powers)", r"\1**Glenn Diesen:** \2"),
        (r"(### Tehran Siege and NATO Shadow War\n\n)(I often think about the current situation)", r"\1**Glenn Diesen:** \2"),
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
    body = cleanup_glenn_speakers(insert_sections(body.strip()))
    doc = f"{head}## Part I: Full transcript\n\n{body}\n"
    TRANSCRIPT_PATH.write_text(doc, encoding="utf-8", newline="\n")
    print(
        f"wrote {TRANSCRIPT_PATH} "
        f"({len(body.split()):,} words, {len(SECTION_TITLES)} sections)"
    )


if __name__ == "__main__":
    main()
