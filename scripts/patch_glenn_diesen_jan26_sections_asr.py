#!/usr/bin/env python3
"""Apply Title Case section headings + light ASR cleanup to Glenn Diesen vi-06 transcript.

    python scripts/patch_glenn_diesen_jan26_sections_asr.py
    python -m civ_ph.cli index --force
    python -m civ_ph.cli validate
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ID = "interview-2026-01-26-glenn-diesen"
TRANSCRIPT_PATH = ROOT / "interviews" / SOURCE_ID / f"{SOURCE_ID}.md"

SECTION_TITLES: list[str] = [
    "Show Open — China Rise and Great Power Wars",
    "Carney Davos — BRICS Framework vs American Empire",
    "US Hegemon — Hard Tools, Vassals, and Rivals",
    "Fake Consensus — Davos Club, Inequality, and Trump",
    "NATO Instrument — Divide and Rule vs Trump Reshape",
    "Trump World Order — Minneapolis, ICE, and Messiah",
    "Europe Decline — Biden Vacuum and Caesar Pattern",
    "Meritocracy Lie — Yale Bubble and Rorty Prediction",
    "Order Breakdown — No Replacement and 1930s Parallel",
    "East Asia Limits — Kennan Skew and Demographic Crisis",
    "Modernity Crisis — Durkheim, Spirituality, and Solzhenitsyn",
    "Iran — Regime Change, Color Revolution, and Persian Resilience",
    "Empire Hubris — Mafia State, Canada Annex, and Close",
]

SECTION_ANCHORS: list[str] = [
    "let's go to mark carney's speech at the world economic forum",
    "since 1945, though, this system of consensus and multilateralism",
    "for the longest time the american empire was able to maintain the illusion",
    "what you said about the fake consensus is interesting",
    "trump's ultimate ambition is to create a trump world order",
    "on the other hand, though, when i read the national security strategy",
    "why are there such terrible leaders at the moment",
    "what are we looking at then",
    "it reminds me of what kennan wrote in his policy planning staff memorandum",
    "the divisions between the countries are quite interesting",
    "as a last question: if the us would like to restore its dominance",
    "when an empire declines, the defining characteristic is hubris",
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


def cleanup_glenn_diesen_jan26_speakers(body: str) -> str:
    body = re.sub(
        r"\n\n\*\*(?:GLENN DIESEN|JIANG XUEQIN):\*\*\n\n(### )",
        r"\n\n\1",
        body,
    )
    ap = r"['\u2019]"
    fixes: list[tuple[str, str, str]] = [
        (
            "Carney Davos — BRICS Framework vs American Empire",
            "JIANG XUEQIN",
            rf"Let{ap}s go to Mark Carney{ap}s speech at the World Economic Forum",
        ),
        (
            "US Hegemon — Hard Tools, Vassals, and Rivals",
            "GLENN DIESEN",
            rf"Since 1945, though, this system of consensus and multilateralism",
        ),
        (
            "Fake Consensus — Davos Club, Inequality, and Trump",
            "JIANG XUEQIN",
            rf"For the longest time the American Empire was able to maintain the illusion",
        ),
        (
            "NATO Instrument — Divide and Rule vs Trump Reshape",
            "GLENN DIESEN",
            rf"What you said about the fake consensus is interesting",
        ),
        (
            "Trump World Order — Minneapolis, ICE, and Messiah",
            "JIANG XUEQIN",
            rf"Trump{ap}s ultimate ambition is to create a Trump world order",
        ),
        (
            "Europe Decline — Biden Vacuum and Caesar Pattern",
            "GLENN DIESEN",
            rf"On the other hand, though, when I read the National Security Strategy",
        ),
        (
            "Meritocracy Lie — Yale Bubble and Rorty Prediction",
            "GLENN DIESEN",
            rf"Why are there such terrible leaders at the moment",
        ),
        (
            "Order Breakdown — No Replacement and 1930s Parallel",
            "GLENN DIESEN",
            rf"What are we looking at then",
        ),
        (
            "East Asia Limits — Kennan Skew and Demographic Crisis",
            "GLENN DIESEN",
            rf"It reminds me of what Kennan wrote in his Policy Planning Staff memorandum",
        ),
        (
            "Modernity Crisis — Durkheim, Spirituality, and Solzhenitsyn",
            "GLENN DIESEN",
            rf"The divisions between the countries are quite interesting",
        ),
        (
            "Iran — Regime Change, Color Revolution, and Persian Resilience",
            "GLENN DIESEN",
            rf"As a last question: if the US would like to restore its dominance",
        ),
        (
            "Empire Hubris — Mafia State, Canada Annex, and Close",
            "JIANG XUEQIN",
            rf"When an empire declines, the defining characteristic is hubris",
        ),
    ]
    for section, speaker, opener in fixes:
        pattern = (
            rf"(### {re.escape(section)}\n\n)"
            rf"(?!\*\*{re.escape(speaker)}:\*\*)"
            rf"({opener})"
        )
        body = re.sub(pattern, rf"\1**{speaker}:** \2", body, count=1)
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
    body = cleanup_glenn_diesen_jan26_speakers(insert_sections(body.strip()))
    doc = f"{head}## Part I: Full transcript\n\n{body}\n"
    TRANSCRIPT_PATH.write_text(doc, encoding="utf-8", newline="\n")
    print(
        f"wrote {TRANSCRIPT_PATH} "
        f"({len(body.split()):,} words, {len(SECTION_TITLES)} sections)"
    )


if __name__ == "__main__":
    main()
