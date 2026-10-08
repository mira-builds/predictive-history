#!/usr/bin/env python3
"""ASR fidelity pass for user-pasted Game Theory transcripts (gt-16, gt-18, gt-27)."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
_PACKAGE_ROOT = _SCRIPTS_DIR.parent
if str(_PACKAGE_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_PACKAGE_ROOT / "src"))

from civ_ph.data import PACKAGE_ROOT
from civ_ph.ph_civ_index import count_transcript_words, ensure_ph_civ_index

LECTURES = PACKAGE_ROOT / "lectures/game-theory"
REVIEW_DATE = "2026-06-23"

SHARED_REPLACEMENTS: list[tuple[str, str]] = [
    ("straits of Hermouth", "Strait of Hormuz"),
    ("straits of Harmuth", "Strait of Hormuz"),
    ("strip of humus", "Strait of Hormuz"),
    ("trip of humus", "Strait of Hormuz"),
    ("close the trip home", "close the Strait of Hormuz"),
    ("close off the shoo", "close off the Strait of Hormuz"),
    ("control the shoo", "control the Strait of Hormuz"),
    ("cross the Homus", "cross the Strait of Hormuz"),
    ("Iran will control the Hummus", "Iran will control the Strait of Hormuz"),
    ("with the tomos they collect", "with the Hormuz toll they collect"),
    ("Peter Hoekstra", "Pete Hegseth"),
    ("this is the second of war Pete Hegseth", "this is Secretary of War Pete Hegseth"),
    ("Karen Levit", "Karoline Leavitt"),
    ("Peter Hexavv", "Pete Hegseth"),
    ("Peter Hav", "Pete Hegseth"),
    ("Scott Besson", "Scott Bessent"),
    ("Black Rockck", "BlackRock"),
    ("Larry Frink", "Larry Fink"),
    ("Donald Rumsfield", "Donald Rumsfeld"),
    ("Tyrron", "Tehran"),
    ("unsectioning", "unsanctioning"),
    ("sessation", "cessation"),
    ("nar in narrow space", "narrative space"),
    ("Mland perspective", "mainland perspective"),
    ("transational capital", "transnational capital"),
    ("rulesbased international order", "rules-based international order"),
    ("def facto", "de facto"),
    ("geogical factor", "geopolitical factor"),
    ("treaty parsley", "Trita Parsi"),
    ("north south quarter", "north-south corridor"),
    ("pray on the weak", "prey on the weak"),
    ("forced by oil from either", "forced to buy oil from either"),
]

GT16_REPLACEMENTS: list[tuple[str, str]] = [
    ("his president's preference", "The president's preference"),
    (
        "Never in history has a modern military Iran had a modern military",
        "Never in history has Iran had a modern military",
    ),
    (
        "they want to not destroy the Iranian leadership, destroy the Iranian economy",
        "they want to destroy the Iranian leadership or destroy the Iranian economy",
    ),
    ("setting army", "standing army"),
    ("prof professional army", "professional army"),
    ("an standing army", "a standing army"),
    ("fair political backlash", "further political backlash"),
    ("polical will", "political will"),
    ("give them rods to politicians", "give bribes to politicians"),
    ("The boy company", "The Boeing company"),
    ("Boeing uh is a very company", "Boeing is a very corrupt company"),
    ("Ioima", "Iwo Jima"),
    ("Jer Ford", "Gerald R. Ford"),
    ("the 04 can't protect", "the Ford can't protect"),
    ("entire world is a gas", "entire world is in uproar"),
    ("AMLAC exists", "Amalek exists"),
    ("AMAC is just like", "Amalek is just like"),
    ("Hezbala members", "Hezbollah members"),
    ("license commanders", "ISIS commanders"),
    ("Issue and event are going to get together", "Israel and Iran are going to get together"),
    ("Issue is happy for the world", "Israel is happy for the world"),
    ("Issue is auditioning to be the new empire", "Israel is auditioning to be the new empire"),
    ("We can use MSA to infiltrate", "We can use Mossad to infiltrate"),
    ("MSAD agent", "Mossad agent"),
    ("they're actually MSAD", "they're actually Mossad"),
    ("MSAD operation", "Mossad operation"),
    ("attricians in Italy", "Etruscans in Italy"),
    ("The Aadian started out as mercenaries for the Samrians", "The Assyrians started out as mercenaries for the Sumerians"),
    ("what the Paka will look like", "what Pax Judaica will look like"),
    ("what tax judic will look like", "what Pax Judaica will look like"),
    ("guess what terrain is also at the epicenter", "guess what Iran is also at the epicenter"),
    ("it has to go through terrain as well", "it has to go through Iran as well"),
    ("GCD proves", "GCC proves"),
    (
        "Israel will ban the GCC in the United States and Israel will work with Iran",
        "Israel will abandon the GCC and the United States and Israel will work with Iran",
    ),
    ("Bahan", "Bahrain"),
    ("And so, it whatso America. We are ready", "And so, unlike America, Israel is ready"),
    ("The answer doesn't even know what it's doing", "The Americans don't even know what they're doing"),
    ("our analysis of H.", "our analysis of hubris."),
    ("steals your money and actually invest it properly", "steals your money rather than invest it properly"),
    ("everything's Donald Trump says is a He doesn't", "Donald Trump doesn't"),
]

GT18_REPLACEMENTS: list[tuple[str, str]] = [
    ("everything's Donald Trump says is a He doesn't", "Donald Trump doesn't"),
    ("He's just a right?", "He's just a fool, right?"),
    ("trans-genderism", "transgenderism"),
]

GT27_REPLACEMENTS: list[tuple[str, str]] = [
    ("President C", "President Xi"),
    ("go over and sect", "go over and select"),
    ("to attend APAC", "to attend APEC"),
    ("hijgemony", "hegemony"),
    ("hedgemanism", "hegemonism"),
    ("hedgemony", "hegemony"),
    ("rulesbased international", "rules-based international"),
    ("more specific than presidency about", "more specific than President Xi about"),
    ("the tent Russia China summer games", "the joint Russia-China summer games"),
    ("comprehensive and inter relationship", "comprehensive and interrelated"),
    ("rules based national order", "rules-based international order"),
    ("China can be the leader and will be a junior partner", "China will be a junior partner"),
    ("Vlamir Putin", "Vladimir Putin"),
    ("straight of Mala", "Strait of Malacca"),
    ("Malaca dilemma", "Malacca dilemma"),
    ("straight of Malaa", "Strait of Malacca"),
    ("close out the straight of Malaa", "close off the Strait of Malacca"),
    ("power cyber barrier 2", "Power of Siberia 2"),
    ("signing anou an agreement", "signing an agreement"),
    ("main pillar of this corporation", "main pillar of this cooperation"),
    ("wester sections on Russia", "western sanctions on Russia"),
    ("didn't have that much in ruining B but now the ruin B accounts", "didn't rely that much on the ruble but now the ruble accounts"),
    ("Barus, Mimer", "Belarus, Myanmar"),
    ("My a civil war, forget about them", "Myanmar civil war, forget about them"),
    ("come to the fence of Russia", "come to the defense of Russia"),
    ("this is Soul.", "this is Seoul."),
    ("how close Soul is to the border", "how close Seoul is to the border"),
    ("remmilitarize", "remilitarize"),
    ("were a vassel to", "were a vassal to"),
    ("Evan says that Russia", "Lavrov says that Russia"),
    ("when the came into power", "when the Bolsheviks came into power"),
    ("FD would come into power", "AfD would come into power"),
    ("USbacked groups", "US-backed groups"),
    (
        "one of the two major battlefronts in World War II. The first is obviously Ukraine",
        "one of the two major battlefronts in World War III. The first is obviously Ukraine",
    ),
    ("issue is key to check it to keeping Russia in check", "Israel is key to checking Russia and keeping Russia in check"),
    ("bread and wood system", "Bretton Woods system"),
    ("bread and woods", "Bretton Woods"),
    ("maintain demanufacturing power", "maintain manufacturing power"),
    ("guaranter of global trade", "guarantor of global trade"),
    ("accommodatize to American society", "acculturate to American society"),
    (
        "Because women be by itself has no value. If you convert B into US dollars",
        "Because the RMB by itself has no value. If you convert RMB into US dollars",
    ),
    ("techn technologically suff sophisticated", "technologically sophisticated"),
    ("surren surrender", "surrender"),
    (
        "So, if you look, if you compare North Korea to South Korea, um, the GDP per person is only $771. Okay, that's it. That's it. Whereas in North Korea, it's over 33,000.",
        "So, if you look, if you compare North Korea to South Korea, um, the GDP per person in North Korea is only $771. Okay, that's it. That's it. Whereas in South Korea, it's over 33,000.",
    ),
    ("hedgemonism are bad", "hegemonism are bad"),
    ("guaranteer of global trade", "guarantor of global trade"),
    ("yang carry trade", "yen carry trade"),
    ("you want union money", "you want yen money"),
    ("the debt $3900 will continue", "the debt $39 trillion will continue"),
    ("America will collapse it in itself", "America will collapse in itself"),
    ("converge to together", "converge together"),
    ("Basically, three money.", "Basically, free money."),
    ("most resol resolutely opposed", "most resolutely opposed"),
    ("transl translation is very bad", "translation is very bad"),
    ("glob. global", "global"),
]

NEW_FRONTMATTER = """---
source_id: "{source_id}"
title: "{title}"
source_series: "Game Theory"
publication_date: "{publication_date}"
source_url: "{source_url}"
video_id: "{video_id}"
transcript_status: "public_transcript"
transcript_fidelity: "exact_body_match"
transcript_source: "user_pasted_public_transcript"
representation_not_endorsement: true
review_status: "source_reviewed"
source_captured_at: "{source_captured_at}"
source_reviewed_at: "{review_date}"
part: "world-war"
part_role: "world-war"
---

# {title}

## Part I: Full transcript

"""

META = {
    "gt-16": {
        "title": "Game Theory #16: Pax Judaica Rising",
        "publication_date": "2026-03-26",
        "source_url": "https://www.youtube.com/watch?v=0aASxQrJYuo",
        "video_id": "0aASxQrJYuo",
        "dest": "lectures/game-theory/gt-16/gt-16-transcript.md",
    },
    "gt-18": {
        "title": "Game Theory #18: Trump World Order",
        "publication_date": "2026-04-02",
        "source_url": "https://www.youtube.com/watch?v=xrmERlHUqBk",
        "video_id": "xrmERlHUqBk",
        "dest": "lectures/game-theory/gt-18/gt-18-transcript.md",
    },
    "gt-27": {
        "title": "Game Theory #27: Putin Enters the Chat",
        "publication_date": "2026-05-21",
        "source_url": "https://www.youtube.com/watch?v=x83HcLWvHI8",
        "video_id": "x83HcLWvHI8",
        "dest": "lectures/game-theory/gt-27/gt-27-transcript.md",
    },
    "gt-23": {
        "title": "Game Theory #23: The WWIII Chessboard",
        "publication_date": "2026-05-06",
        "source_url": "https://www.youtube.com/watch?v=6aNh6sBpqvQ",
        "video_id": "6aNh6sBpqvQ",
        "dest": "lectures/game-theory/gt-23/gt-23-transcript.md",
    },
    "gt-24": {
        "title": "Game Theory #24: The AI Apocalypse",
        "publication_date": "2026-05-12",
        "source_url": "https://www.youtube.com/watch?v=8nsxuB3Vsts",
        "video_id": "8nsxuB3Vsts",
        "dest": "lectures/game-theory/gt-24/gt-24-transcript.md",
    },
    "gt-25": {
        "title": "Game Theory #25: Trump Visits China",
        "publication_date": "2026-05-14",
        "source_url": "https://www.youtube.com/watch?v=BIl5vJn6ohI",
        "video_id": "BIl5vJn6ohI",
        "dest": "lectures/game-theory/gt-25/gt-25-transcript.md",
    },
    "gt-26": {
        "title": "Game Theory #26: The Holy Empire of AI",
        "publication_date": "2026-05-19",
        "source_url": "https://www.youtube.com/watch?v=RG1clZlrfOo",
        "video_id": "RG1clZlrfOo",
        "dest": "lectures/game-theory/gt-26/gt-26-transcript.md",
    },
}

EXTENDED_PARAGRAPH_IDS = frozenset({"gt-23", "gt-24", "gt-25", "gt-26", "gt-27"})

JOB_REPLACEMENTS = {
    "gt-16": GT16_REPLACEMENTS,
    "gt-18": GT18_REPLACEMENTS,
    "gt-23": [],
    "gt-24": [],
    "gt-25": [],
    "gt-26": [],
    "gt-27": GT27_REPLACEMENTS,
}


def extract_body(text: str) -> str:
    marker = "## Part I: Full transcript"
    idx = text.find(marker)
    if idx == -1:
        raise ValueError("missing transcript marker")
    start = idx + len(marker)
    return text[start:].lstrip("\n").rstrip() + "\n"


def apply_replacements(body: str, extra: list[tuple[str, str]]) -> str:
    for old, new in sorted(SHARED_REPLACEMENTS + extra, key=lambda x: len(x[0]), reverse=True):
        body = body.replace(old, new)
    return body


def add_paragraph_breaks(body: str) -> str:
    body = re.sub(r" >> Okay\.", r"\n\n>> Okay.", body)
    body = re.sub(r"\. All right\.", ".\n\nAll right.", body)
    body = re.sub(
        r"\. Okay\. So (now|let|to first|remember|this is|what|um|we|in um|okay)",
        lambda m: f".\n\nOkay. So {m.group(1)}",
        body,
        flags=re.IGNORECASE,
    )
    body = re.sub(r"\. Okay\. Any questions", ".\n\nOkay. Any questions", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body


def add_paragraph_breaks_gt27(body: str) -> str:
    body = add_paragraph_breaks(body)
    body = re.sub(
        r"(please leave the question behind\.)\n um in the comment",
        r"\1\n\nUm in the comment",
        body,
        flags=re.IGNORECASE,
    )
    body = re.sub(
        r"(talk about Putin in Beijing\.)\n So he came",
        r"\1\n\nSo he came",
        body,
    )
    body = re.sub(
        r"(multipolar world\. Okay\.)\n So um this is a part",
        r"\1\n\nSo um this is a part",
        body,
    )
    body = re.sub(
        r"(Japan\.)\n Putin says the same thing",
        r"\1\n\nPutin says the same thing",
        body,
    )
    body = re.sub(
        r"\. Okay\. (So|But|This|He|Putin|President|Now|First|Second|Third|Yeah|Um|If|What|All|Another|Also|Number)",
        r".\n\nOkay. \1",
        body,
    )
    body = re.sub(r"(\. Okay\?)( So next week)", r"\1\n\n\2", body)
    body = re.sub(r"\? >> ", "?\n\n>> ", body)
    body = re.sub(r"([^>\n]) >> (Wait|Uh|Okay\. So|Yeah\.)", r"\1\n\n>> \2", body)
    body = re.sub(
        r"(sense\? Okay\.)( Any more questions)",
        r"\1\n\n\2",
        body,
    )
    body = re.sub(
        r"(going on\? Okay\.)( How will America)",
        r"\1\n\n\2",
        body,
    )
    body = re.sub(
        r"(host\. Okay\? Clear\?)( All right\. So, next week)",
        r"\1\n\n\2",
        body,
    )
    body = re.sub(r"global\n governance", "global governance", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body


def compose(source_id: str, body: str) -> str:
    meta = META[source_id]
    header = NEW_FRONTMATTER.format(
        source_id=source_id,
        title=meta["title"],
        publication_date=meta["publication_date"],
        source_url=meta["source_url"],
        video_id=meta["video_id"],
        source_captured_at=REVIEW_DATE,
        review_date=REVIEW_DATE,
    )
    return header + body


def process(source_id: str, extra: list[tuple[str, str]]) -> int:
    src_path = LECTURES / source_id / f"{source_id}-transcript.md"
    body = extract_body(src_path.read_text(encoding="utf-8"))
    body = apply_replacements(body, extra)
    if source_id in EXTENDED_PARAGRAPH_IDS:
        body = add_paragraph_breaks_gt27(body)
    else:
        body = add_paragraph_breaks(body)
    text = compose(source_id, body)
    dest = PACKAGE_ROOT / META[source_id]["dest"]
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8")
    return count_transcript_words(text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-id", action="append", dest="source_ids")
    args = parser.parse_args()
    source_ids = args.source_ids or list(JOB_REPLACEMENTS)
    counts: dict[str, int] = {}
    for source_id in source_ids:
        counts[source_id] = process(source_id, JOB_REPLACEMENTS[source_id])
    ensure_ph_civ_index(force=True)
    for source_id, words in counts.items():
        print(f"{source_id}: {words} words -> {META[source_id]['dest']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
