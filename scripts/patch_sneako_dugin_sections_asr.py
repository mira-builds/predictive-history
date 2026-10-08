#!/usr/bin/env python3
"""Apply Title Case section headings + light ASR cleanup to Sneako–Dugin vi-15 transcript.

    python scripts/patch_sneako_dugin_sections_asr.py
    python -m civ_ph.cli index --force
    python -m civ_ph.cli validate
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ID = "interview-2026-04-13-sneako-dugin"
TRANSCRIPT_PATH = ROOT / "interviews" / SOURCE_ID / f"{SOURCE_ID}.md"

SECTION_TITLES: list[str] = [
    "Show Open — Stream Setup and Eschatology Frame",
    "Dugin on Jiang — Chinese Eschatology Exception",
    "Faith Traditions — Orthodox, Gnostic, and Eschatology Defined",
    "Trump Easter Posts and Western Values Decay",
    "Bank of England and Anglo-Saxon Liberalism",
    "Scofield Bible, Gog and Magog, and Christian Zionism",
    "Zionism in China and Russia",
    "Eurasian Unity and Greater North America",
    "Trump Deep State — Chabad and Convergence of Interests",
    "Chabad in Russia, Putin, Islam, and Epstein",
    "Disagreements, Antichrist, and Closing",
]

SECTION_ANCHORS: list[str] = [
    "okay. do you have major disagreements? and well, first off, how well do you know each other?",
    "absolutely. and well, i have a couple questions for you, alexander",
    "on easter sunday he said praise be to allah",
    "so i think the root of the problem is 1694",
    "that makes me understand your idea and how you can relate traditionalism",
    "there was something really interesting i saw yesterday. i saw these chinese children",
    "but we could not prevent to see behind these events the very alternative scenario",
    "right. so i want to ask the both of you. i'll start with professor jiang",
    "professor dugin, what is the relationship that russia has with chabad lubavitch?",
    "okay. professor jiang, are there any disagreements you have?",
]


def normalize_for_anchor(s: str) -> str:
    s = s.replace("\u2019", "'").replace("\u2018", "'")
    s = s.replace("\u201c", '"').replace("\u201d", '"')
    return s.lower()


def asr_cleanup(text: str) -> str:
    text = re.sub(r"(### Show Open — Stream Setup and Eschatology Frame\n\n)\*\*\n\n", r"\1", text, count=1)
    text = re.sub(r"^\*\*\s*\n\n", "", text, count=1, flags=re.M)
    text = re.sub(r"\n\*\*\s*$", "\n", text)
    text = text.replace(
        "And now Calvinism because it's communism, it's really about fear and anxiety.",
        "And now Calvinism—because it's consumerism—is really about fear and anxiety.",
    )
    text = text.replace("the enlightenment, the sonic revolution marked", "the enlightenment, the scientific revolution marked")
    text = text.replace("we prefer to be abstain civilization", "we prefer to be Asian civilization")
    text = re.sub(r"\bThe The\b", "The", text)
    text = re.sub(r"\bthe the\b", "the", text, flags=re.I)
    return text


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
        cursor = pos + len(normalize_for_anchor(anchor))
    positions.append(len(flat))

    parts: list[str] = []
    for i, heading in enumerate(SECTION_TITLES):
        chunk = flat[positions[i] : positions[i + 1]].strip()
        parts.append(f"### {heading}\n\n{chunk}")
    return "\n\n".join(parts)


def cleanup_orphan_speakers(body: str) -> str:
    body = re.sub(
        r"\n\n\*\*(?:Sneako|Jiang Xueqin|Aleksandr Dugin|Patrick Bet-David|Glenn Diesen):\*\*\n\n(### )",
        r"\n\n\1",
        body,
    )
    body = re.sub(
        r"(### Dugin on Jiang — Chinese Eschatology Exception\n\n)(Okay\. Do you have major)",
        r"\1**Sneako:** \2",
        body,
        count=1,
    )
    body = re.sub(
        r"(### Faith Traditions — Orthodox, Gnostic, and Eschatology Defined\n\n)(Absolutely\. And well, I have a couple)",
        r"\1**Sneako:** \2",
        body,
        count=1,
    )
    body = re.sub(
        r"(### Trump Easter Posts and Western Values Decay\n\n)(On Easter Sunday he said praise be to Allah)",
        r"\1**Sneako:** \2",
        body,
        count=1,
    )
    body = re.sub(
        r"(### Scofield Bible, Gog and Magog, and Christian Zionism\n\n)(That makes me understand your idea)",
        r"\1**Sneako:** \2",
        body,
        count=1,
    )
    body = re.sub(
        r"(### Zionism in China and Russia\n\n)(There was something really interesting)",
        r"\1**Sneako:** \2",
        body,
        count=1,
    )
    body = re.sub(
        r"(very alternative scenario\.)\n\n(### Eurasian Unity)",
        r"\1\n\n\2",
        body,
        count=1,
    )
    body = re.sub(
        r"(### Eurasian Unity and Greater North America\n\n)(So this is an opportunity|Professor Jiang, I don't know)",
        r"\1**Sneako:** \2",
        body,
        count=1,
    )
    body = re.sub(
        r"(opportunity to see if there's some back and forth here between you two\.)\n\n(Professor Jiang, I don't know)",
        r"\1 \2",
        body,
        count=1,
    )
    body = re.sub(
        r"(### Trump Deep State — Chabad and Convergence of Interests\n\n)(Right\. So I want to ask)",
        r"\1**Sneako:** \2",
        body,
        count=1,
    )
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
    body = cleanup_orphan_speakers(insert_sections(body.strip()))
    doc = f"{head}## Part I: Full transcript\n\n{body}\n"
    TRANSCRIPT_PATH.write_text(doc, encoding="utf-8", newline="\n")
    print(
        f"wrote {TRANSCRIPT_PATH} "
        f"({len(body.split()):,} words, {len(SECTION_TITLES)} sections)"
    )


if __name__ == "__main__":
    main()
