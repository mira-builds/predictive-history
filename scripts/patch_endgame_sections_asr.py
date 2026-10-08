#!/usr/bin/env python3
"""Apply Title Case section headings + light ASR cleanup to Endgame vi-10 transcript.

    python scripts/patch_endgame_sections_asr.py
    python -m civ_ph.cli index --force
    python -m civ_ph.cli validate

Re-sections the existing three-block transcript (Trailer / Promo / Captions monolith)
into curated Title Case rails. See `interviews/README.md` § Interview section headings.
"""
from __future__ import annotations

import re
from pathlib import Path

import sys

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from interview_transcript_sections import (  # noqa: E402
    PART_I_MARKER,
    common_asr_cleanup,
    insert_sections,
    update_fidelity_reviewed_at,
    update_sectioned_frontmatter,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ID = "interview-2026-03-16-endgame"
TRANSCRIPT_PATH = ROOT / "interviews" / SOURCE_ID / f"{SOURCE_ID}.md"

SECTION_TITLES: list[str] = [
    "Trailer — Consciousness (Clip)",
    "Channel Promo and Introduction",
    "Early Life — Toronto Immigrant Upbringing and Yale Acceptance",
    "Yale Essay — Feynman, Poetry, and Skull and Bones",
    "Journalistic Disillusion — Depression and Jimmy Dore",
    "Journalism Future — AI Matrix vs Truth-Seeking",
    "Rules-Based Order — Empire Hubris, 2008, and Trump",
    "US Civil War — Trump, Elections, and Narrative Control",
    "Consciousness — Plato, Wealth, Technomarxism, and Transhumanism",
    "Board of Peace — Trump World and De-industrialization Trends",
    "Middle East War — Empire, Chaos, and 2024 Predictions",
    "Eschatology — Epstein, Secret Societies, and End Times",
    "War Expansion — Al-Aqsa, Greater Israel, and Nuclear Ladder",
    "GCC Economics — Hormuz, Water, and Regional Collapse",
    "Gog and Magog — China Outside Eschatology",
    "Civil War Manufacturing — ICE, Minnesota, and Attention",
    "Education — Great Books, You Matter, and Free Will",
    "Closing — Trump-Xi Meeting and Third Term",
]

SECTION_ANCHORS: list[str] = [
    "hi friends, it's a pleasure to tell you that my book",
    "yeah, i want to start out with how you grew up",
    "talk about the essay that you wrote",
    "i had given up on journalism. now i switched to the internet",
    "journalism is going to have to get normalized",
    "next big topic i want to switch over to is really the",
    "let's look at the united states. trump, does trump really care about venezuela",
    "talk talk about how AI is going to replace fiat and how AI is going to be able to create the illusion of God",
    "called the board of peace. what what's your take on this",
    "segue to the third big point, uh which is what's going on in the middle east",
    "did did you have all this in mind in 2024, early 2024",
    "the third thing, and this is really important, is eschatological",
    "what's the likelihood this is likely to get nuclear",
    "draw the picture in terms of the economic",
    "well, how does china look look at all this",
    "what's the likelihood for for for a civil war",
    "contemporary education ought to be like going forward",
]


def flatten_part_i_body(body: str) -> str:
    """Strip existing ### headings and the one-line caption disclaimer."""
    lines: list[str] = []
    for line in body.splitlines():
        if line.startswith("### "):
            continue
        if line.strip().startswith("_YouTube captions do not separate"):
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def asr_cleanup(text: str) -> str:
    text = common_asr_cleanup(
        text,
        replacements={
            "techno Marxarxism": "technomarxism",
            "Jang Suin": "Jiang Xueqin",
            "Jang Suin.": "Jiang Xueqin.",
            "graten and endover": "Groton and Andover",
            "Exiter": "Exeter",
            "Skone and Bones": "Skull and Bones",
            "Scrum and Bones": "Skull and Bones",
            "Scrum Bones": "Skull Bones",
            "Skill and Bones": "Skull and Bones",
            "Yo had accepted me": "Yale had accepted me",
            "food and admissions officer": "through to an admissions officer",
            "Richard Fineman": "Richard Feynman",
            "Richard Feman": "Richard Feynman",
            "Ter Carson": "Tucker Carlson",
            "Taro Carlson": "Tucker Carlson",
            "Turo Carlson": "Tucker Carlson",
            "walter gate to lean": "Walter Kirn said we",
            "Kasam Salmani": "Qassem Soleimani",
            "Greta Fernberg": "Greta Thunberg",
            "Jimmy Kimmo": "Jimmy Kimmel",
            "the ass battalion": "the Azov battalion",
            "dingoism": "jingoism",
            "middle-ass societies": "Middle East societies",
            "border of peace": "Board of Peace",
            "the border of peace": "the Board of Peace",
            "uniolarity": "unipolarity",
            "multiparity": "multipolarity",
            "transnationalize": "transnationalize",
            "esquetological": "eschatological",
            "esquetology": "eschatology",
            "Epson Island": "Epstein Island",
            "Epson Files": "Epstein files",
            "Msad": "Mossad",
            "Alexic moss": "Al-Aqsa mosque",
            "Actic moss": "Al-Aqsa mosque",
            "alexic moss": "Al-Aqsa mosque",
            "actic moss": "Al-Aqsa mosque",
            "Chachi BT": "ChatGPT",
            "Chachi has": "ChatGPT has",
            "Lex Wer": "Lex Wexner",
            "s Alman": "Sam Altman",
            "Professor Dang": "Professor Jiang",
            "Mr. Dang": "Mr. Jiang",
            "Maldi visited": "Modi visited",
            "packa.": "Pax Judaica.",
            "Pax Judea": "Pax Judaica",
            "pack Judea": "Pax Judaica",
            "tax um Judeica": "Pax Judaica",
            "Gamok": "Gog and Magog",
            "Gaga Magog": "Gog and Magog",
            "GA mal": "Gog and Magog",
            "bollocks": "Baloch",
            "bolakis": "Baloch",
            "Rain Good shooting": "Renee Good shooting",
            "preient": "prescient",
            "Chachi just kind": "ChatGPT just kind",
            "Jang,": "Jiang,",
            "confirmed that I' had been accepted": "confirmed that I'd been accepted",
        },
    )
    text = re.sub(r"### Trailer - ", "### Trailer — ", text)
    return text


def cleanup_endgame_speakers(body: str) -> str:
    """Pass-2 Host/Jiang labels for caption-merged paragraphs (sample sections)."""
    body = asr_cleanup(body)

    body = re.sub(
        r"\n\n\*\*Host \(Endgame\):\*\*\n\n(?=### )",
        "\n\n",
        body,
    )

    body = re.sub(
        r"(### Channel Promo and Introduction\n\n)(Hi friends, it's a pleasure)",
        r"\1**Host (Endgame):** \2",
        body,
        count=1,
    )

    body = re.sub(
        r"(### Early Life —[^\n]+\n\n)(Yeah, I want to start out with how you grew up\.)",
        r"\1**Host (Endgame):** \2",
        body,
        count=1,
    )

    body = re.sub(
        r"(### Yale Essay —[^\n]+\n\n)(Talk about the essay that you wrote\.)",
        r"\1**Host (Endgame):** \2",
        body,
        count=1,
    )
    body = re.sub(
        r"(\*\*Host \(Endgame\):\*\* Talk about the essay that you wrote\.\n\n)(Uh when I was a high school student)",
        r"\1**Jiang Xueqin:** \2",
        body,
        count=1,
    )
    body = re.sub(
        r"(\*\*Host \(Endgame\):\*\* Um, after one year, did you know anything about English lit or English poetry or you just it\nwas random\?) (Yeah, I know\.)",
        r"\1\n\n**Jiang Xueqin:** \2",
        body,
        count=1,
    )
    body = re.sub(
        r"(was random\?\n\n\*\*Jiang Xueqin:\*\* Yeah, I know\. I mean, I um I mean it was a it was a standard Toronto public school)",
        r"was random?\n\n**Jiang Xueqin:** Yeah, I know. I mean, I um I mean it was a it was a standard Toronto public school",
        body,
        count=1,
    )
    body = re.sub(
        r"(\n\n)(Did did you ever have any curiosity with respect to the Russian stuff or the Chinese stuff\ntoki\? )(Right\. So yeah\. Right\. So again you receive)",
        r"\1**Host (Endgame):** \2\n\n**Jiang Xueqin:** \3",
        body,
        count=1,
    )
    body = re.sub(
        r"(\n\n)(Because I would have thought that, you know, you you've you've talked quite a bit about how\nclass structures are shaped by ideology and, you know, how Marxism, socialism, communism,\ncapitalism\.)",
        r"\1**Host (Endgame):** \2",
        body,
        count=1,
    )
    body = re.sub(
        r"(capitalism\.\n\n)(I mean a lot of the stuff would have you know been shaped by a lot of the readings that came\nout of Russia)",
        r"\1**Jiang Xueqin:** \2",
        body,
        count=1,
    )
    body = re.sub(
        r"(\n\n)(Did did you get a sense at that time that that was sort of like a the way for anybody to get\npowerful, get rich or whatever\.)",
        r"\1**Host (Endgame):** \2",
        body,
        count=1,
    )
    body = re.sub(
        r"(leadership or authority, right\? So again, I was very naive when I\nwas at Yale\.)",
        r"leadership or authority, right?\n\n**Jiang Xueqin:** So again, I was very naive when I was at Yale.",
        body,
        count=1,
    )

    body = re.sub(
        r"(that's what's happening)( talk talk about how AI is going to replace fiat)",
        r"\1\n\n**Host (Endgame):** Talk talk about how AI is going to replace fiat",
        body,
        count=1,
    )
    body = re.sub(
        r"(\*\*Host \(Endgame\):\*\* Talk talk about how AI is going to replace fiat and how AI\nis going to be able to create the illusion of God and how AI is going to be able create the\nillusion of the antichrist and all that which we've been talking quite a bit\.\n\n)"
        r"(Okay\. All right\. So, this is a really uh good question, but but I I need to go slowly so\nthat um I want to make sure I'm make myself clear\. Okay\. All right\. Right\. So, the key idea\nis)\n\n"
        r"### Consciousness — Plato, Wealth, Technomarxism, and Transhumanism\n\n"
        r"(Plato's allegory of the cave\.)",
        r"\1### Consciousness — Plato, Wealth, Technomarxism, and Transhumanism\n\n**Jiang Xueqin:** \2 \3",
        body,
        count=1,
    )
    body = re.sub(
        r"(So, the key idea is)\n\n### Consciousness — Plato, Wealth, Technomarxism, and Transhumanism\n\n(Plato's allegory of the cave\.)",
        r"\1 \2",
        body,
        count=1,
    )

    return body


def apply_speaker_pass2(head: str, body: str) -> tuple[str, str]:
    head = update_fidelity_reviewed_at(head)
    return head, cleanup_endgame_speakers(body)


def main() -> None:
    doc = TRANSCRIPT_PATH.read_text(encoding="utf-8")
    if PART_I_MARKER not in doc:
        raise ValueError("missing Part I marker")

    head, body = doc.split(PART_I_MARKER, 1)
    body = body.strip()

    if body.startswith("### ") and "transcript_curation: curated_sectioned" in head:
        head, body = apply_speaker_pass2(head, body)
        doc = f"{head}{PART_I_MARKER}\n\n{body}\n"
        TRANSCRIPT_PATH.write_text(doc, encoding="utf-8", newline="\n")
        print(
            f"speaker pass 2: {TRANSCRIPT_PATH} "
            f"({len(body.split()):,} words, pass-2 Host/Jiang sample sections)"
        )
        return

    flat = flatten_part_i_body(body)
    head = update_sectioned_frontmatter(head)
    if "transcript_curation: curated_sectioned" not in head:
        raise ValueError("expected curated_sectioned in frontmatter")

    body = insert_sections(
        flat,
        SECTION_TITLES,
        SECTION_ANCHORS,
        asr_cleanup_fn=asr_cleanup,
    )
    body = cleanup_endgame_speakers(body)

    doc = f"{head}{PART_I_MARKER}\n\n{body}\n"
    TRANSCRIPT_PATH.write_text(doc, encoding="utf-8", newline="\n")
    print(
        f"wrote {TRANSCRIPT_PATH} "
        f"({len(body.split()):,} words, {len(SECTION_TITLES)} sections)"
    )


if __name__ == "__main__":
    main()
