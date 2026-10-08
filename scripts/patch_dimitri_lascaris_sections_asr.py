#!/usr/bin/env python3
"""Apply Title Case section headings + light ASR cleanup to Dimitri Lascaris vi-05 transcript.

    python scripts/patch_dimitri_lascaris_sections_asr.py
    python -m civ_ph.cli index --force
    python -m civ_ph.cli validate
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ID = "interview-2026-01-22-dimitri-lascaris"
TRANSCRIPT_PATH = ROOT / "interviews" / SOURCE_ID / f"{SOURCE_ID}.md"

SECTION_TITLES: list[str] = [
    "Show Open — Montreal and Jack Keane Clip",
    "Iran Air Strikes — Soleimani Legacy and 2026 Conflict",
    "Strait of Hormuz — Escalation Ladder and Retaliation",
    "China and Russia — Bolstering Iran Against US Strategy",
    "Davos — Carney Speech and Values-Based Realism",
    "Toxic Canada — Thucydides, Havel, and Asset Strip",
    "Canadian Predicament — Colonization Risks and Love Trump",
    "Beijing Trip — EV Quota, Canola, and Strategic Partnership",
    "Carney Banker Strategy — Breakthrough, BIS, and EV Joint Ventures",
    "Huawei, Interference Narrative, and Close",
]

SECTION_ANCHORS: list[str] = [
    "let me clarify my comments",
    "iran has long warned that if pushed",
    "from the chinese perspective, what trump is really doing",
    "let's turn now to a less violent topic",
    "overall i agree with your sentiment",
    "now let's imagine, professor jiang, that you were asked",
    "well, no. that actually brings us to our next topic",
    "i would say this is a breakthrough",
    "let's talk about another sector — telecommunications",
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


def cleanup_dimitri_lascaris_speakers(body: str) -> str:
    body = re.sub(
        r"\n\n\*\*(?:Dimitri Lascaris|Jiang Xueqin|Jack Keane \(clip\)|Mark Carney \(clip\)):\*\*\n\n(### )",
        r"\n\n\1",
        body,
    )
    ap = r"['\u2019]"
    fixes: list[tuple[str, str, str]] = [
        (
            "Iran Air Strikes — Soleimani Legacy and 2026 Conflict",
            "Jiang Xueqin",
            rf"Let me clarify my comments",
        ),
        (
            "Strait of Hormuz — Escalation Ladder and Retaliation",
            "Dimitri Lascaris",
            rf"Iran has long warned that if pushed",
        ),
        (
            "China and Russia — Bolstering Iran Against US Strategy",
            "Jiang Xueqin",
            rf"From the Chinese perspective, what Trump is really doing",
        ),
        (
            "Davos — Carney Speech and Values-Based Realism",
            "Dimitri Lascaris",
            rf"Let{ap}s turn now to a less violent topic",
        ),
        (
            "Toxic Canada — Thucydides, Havel, and Asset Strip",
            "Jiang Xueqin",
            rf"Overall I agree with your sentiment",
        ),
        (
            "Canadian Predicament — Colonization Risks and Love Trump",
            "Dimitri Lascaris",
            rf"Now let{ap}s imagine, Professor Jiang, that you were asked",
        ),
        (
            "Beijing Trip — EV Quota, Canola, and Strategic Partnership",
            "Dimitri Lascaris",
            rf"Well, no\. That actually brings us to our next topic",
        ),
        (
            "Carney Banker Strategy — Breakthrough, BIS, and EV Joint Ventures",
            "Jiang Xueqin",
            rf"I would say this is a breakthrough",
        ),
        (
            "Huawei, Interference Narrative, and Close",
            "Dimitri Lascaris",
            rf"Let{ap}s talk about another sector — telecommunications",
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
    body = cleanup_dimitri_lascaris_speakers(insert_sections(body.strip()))
    doc = f"{head}## Part I: Full transcript\n\n{body}\n"
    TRANSCRIPT_PATH.write_text(doc, encoding="utf-8", newline="\n")
    print(
        f"wrote {TRANSCRIPT_PATH} "
        f"({len(body.split()):,} words, {len(SECTION_TITLES)} sections)"
    )


if __name__ == "__main__":
    main()
