#!/usr/bin/env python3
"""Apply Title Case section headings + light ASR cleanup to Jay Shapiro vi-12 transcript.

    python scripts/patch_jay_shapiro_sections_asr.py
    python -m civ_ph.cli index --force
    python -m civ_ph.cli validate
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ID = "interview-2026-04-01-jay-shapiro"
TRANSCRIPT_PATH = ROOT / "interviews" / SOURCE_ID / f"{SOURCE_ID}.md"

SECTION_TITLES: list[str] = [
    "Show Intro — Jay Opens on Professor Xiang",
    "Personal Path — Village, Yale, and China Return",
    "Professor Xiang Moniker and Prediction Record",
    "Secret Societies, Freemasons, and Eschatology",
    "Myth vs Truth — Monsters, Holocaust, and 9/11",
    "Holocaust Evidence Gap and Birthright Israel",
    "Masada Myth and Zionist Propaganda",
    "Eschatology, 9/11, Epstein, and Transnational Elite",
    "Religion Matters — Doctrine, Hamas, and Al-Aqsa",
    "Kabbalah, Jacob-Esau, and End-Times Fanaticism",
    "Truth-Seeking, Consequences, and the Tightrope",
    "Myth Collapse, Free Debate, and Hopeful Close",
    "Show Outro — Dead Sea Scrolls and Professor Xiang Phenomenon",
]

SECTION_ANCHORS: list[str] = [
    "so my background is um i was born in 1976",
    "so, let's let's set the record straight",
    "i completely sympathize and a year ago i would have",
    "monsters don't exist, right?",
    "i'm not saying the holocaust didn't happen. it must have happened",
    "did you do the hike and the sunrise?",
    "okay. um, so i think that eschatology is interesting for my work",
    "i probably like you absolutely think the doctrines matter",
    "there are um certain jews who believe that actually the real founder",
    "yeah. no, that's a really good question. and this is something that i've struggled",
    "i go to a time in the 1990s when open free debate was a core liberal value",
    "so, i obviously love that conversation. i have some final thoughts here",
]


def remove_misordered_opening(text: str) -> str:
    """Drop caption-order fragment duplicated later in the conversation."""
    start_marker = "**Jay Shapiro:** That day also uh is when a blood moon"
    intro_marker = "I just need to know that Lummit Podcast J Shapiro here."
    start = text.find(start_marker)
    intro = text.find(intro_marker)
    if start != -1 and intro != -1 and start < intro:
        tail = text[intro + len(intro_marker) :].lstrip()
        text = (
            text[:start]
            + "**Jay Shapiro:** Luminary Podcast — Jay Shapiro here. "
            + tail
        )
    return text


def asr_cleanup(text: str) -> str:
    text = remove_misordered_opening(text)
    replacements = [
        ("Lummit Podcast J Shapiro here", "Luminary Podcast — Jay Shapiro here"),
        ("Professor Dang", "Professor Jiang"),
        ("Professor Dieng", "Professor Jiang"),
        ("rever the number 33", "revere the number 33"),
        ("Alaska mosque", "Al-Aqsa mosque"),
        ("Alakamas", "Al-Aqsa"),
        ("strip of hummus", "Strait of Hormuz"),
        ("Kmeni", "Khamenei"),
        ("Porum", "Purim"),
        ("G bands", "JD Vance"),
        ("Isaac Azimov", "Isaac Asimov"),
        ("aven flu", "avian flu"),
        ("truth seeeking", "truth-seeking"),
        ("esquetologies", "eschatologies"),
        ("Msada", "Masada"),
        ("Mada story", "Masada story"),
        ("qwame and Kruma", "Kwame Nkrumah"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    text = re.sub(r"\bThe The\b", "The", text)
    text = re.sub(r"\bthe the\b", "the", text, flags=re.I)
    text = re.sub(r"\bMiddle East, Middle East\b", "Middle East", text)
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


def cleanup_jay_shapiro_speakers(body: str) -> str:
    body = re.sub(
        r"\n\n\*\*(?:Jay Shapiro|Jiang Xueqin):\*\*\n\n(### )",
        r"\n\n\1",
        body,
    )
    fixes = [
        (
            r"(### Personal Path — Village, Yale, and China Return\n\n)(So my background)",
            r"\1**Jiang Xueqin:** \2",
        ),
        (
            r"(### Professor Xiang Moniker and Prediction Record\n\n)(So, let's let's set the record straight)",
            r"\1**Jiang Xueqin:** \2",
        ),
        (
            r"\*\*Jay Shapiro:\*\* Um, I also expected the war start maybe in 2027",
            "**Jiang Xueqin:** Um, I also expected the war start maybe in 2027",
        ),
        (
            r"(### Secret Societies, Freemasons, and Eschatology\n\n)(I completely sympathize)",
            r"\1**Jiang Xueqin:** \2",
        ),
        (
            r"(### Myth vs Truth — Monsters, Holocaust, and 9/11\n\n)(So I I grew up a little my background)",
            r"\1**Jay Shapiro:** \2",
        ),
        (
            r"(### Holocaust Evidence Gap and Birthright Israel\n\n)(I'm not saying the Holocaust didn't happen)",
            r"\1**Jiang Xueqin:** \2",
        ),
        (
            r"(### Masada Myth and Zionist Propaganda\n\n)(Did you do the hike and the sunrise\?)",
            r"\1**Jiang Xueqin:** \2",
        ),
        (
            r"(### Eschatology, 9/11, Epstein, and Transnational Elite\n\n)(Okay\. Um, so I think that eschatology is interesting)",
            r"\1**Jiang Xueqin:** \2",
        ),
        (
            r"\*\*Jiang Xueqin:\*\* Yeah\. No, that that was good\. if I could respond to it because",
            "**Jay Shapiro:** Yeah. No, that that was good. if I could respond to it because",
        ),
        (
            r"\*\*Jay Shapiro:\*\* right\? So, um I'm still grappling with secret societies",
            "**Jiang Xueqin:** right? So, um I'm still grappling with secret societies",
        ),
        (
            r"(### Religion Matters — Doctrine, Hamas, and Al-Aqsa\n\n)(I probably like you absolutely think the doctrines matter)",
            r"\1**Jay Shapiro:** \2",
        ),
        (
            r"(### Kabbalah, Jacob-Esau, and End-Times Fanaticism\n\n)(there are um certain Jews who believe)",
            r"\1**Jiang Xueqin:** \2",
        ),
        (
            r"\*\*Jay Shapiro:\*\* and and and and so for these cabalists, that's what they think like what salvation is\.",
            "**Jiang Xueqin:** and and and and so for these cabalists, that's what they think like what salvation is.",
        ),
        (
            r"(### Truth-Seeking, Consequences, and the Tightrope\n\n)(Yeah\. No, that's a really good question\.)",
            r"\1**Jiang Xueqin:** \2",
        ),
        (
            r"\*\*Jay Shapiro:\*\* uh um you know your birds being sick it's not a huge problem\. So, um, and then I started to work in study abroad education",
            "**Jiang Xueqin:** uh um you know your birds being sick it's not a huge problem. So, um, and then I started to work in study abroad education",
        ),
        (
            r"\*\*Jay Shapiro:\*\* you have to speak the truth and and and and and so that might be naive but but but I but but that's a principle why I live by\.",
            "**Jiang Xueqin:** you have to speak the truth and and and and and so that might be naive but but but I but but that's a principle why I live by.",
        ),
        (
            r"(### Myth Collapse, Free Debate, and Hopeful Close\n\n)(I go to a time in the 1990s when open free debate)",
            r"\1**Jiang Xueqin:** \2",
        ),
        (
            r"(### Show Outro — Dead Sea Scrolls and Professor Xiang Phenomenon\n\n)(So, I obviously love that conversation)",
            r"\1**Jay Shapiro:** \2",
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
    body = cleanup_jay_shapiro_speakers(insert_sections(body.strip()))
    doc = f"{head}## Part I: Full transcript\n\n{body}\n"
    TRANSCRIPT_PATH.write_text(doc, encoding="utf-8", newline="\n")
    print(
        f"wrote {TRANSCRIPT_PATH} "
        f"({len(body.split()):,} words, {len(SECTION_TITLES)} sections)"
    )


if __name__ == "__main__":
    main()
