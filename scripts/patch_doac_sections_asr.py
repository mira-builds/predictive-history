#!/usr/bin/env python3
"""Apply section titles (Title Case) + light ASR cleanup to DOAC verbatim transcript.

Use after swapping the body of `interviews/interview-2026-05-07-diary-of-a-ceo/
interview-2026-05-07-diary-of-a-ceo.md` with an operator verbatim paste (no `###`
sections). Then regenerate the catalog:

    python scripts/patch_doac_sections_asr.py
    python -m civ_ph.cli index --force
    python -m civ_ph.cli validate

Section map: 14 anchors + Title Case headings (from PH-TRANSCRIPT-EDIT commit c01fe76).
See `interviews/README.md` § DOAC #16 — verbatim swap + section restore.
"""
from __future__ import annotations

import re
import subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ID = "interview-2026-05-07-diary-of-a-ceo"
TITLE = "Interviews #16: Diary of a CEO (Steven Bartlett) — World War 3 Is About To Begin"
TRANSCRIPT_PATH = ROOT / "interviews" / SOURCE_ID / f"{SOURCE_ID}.md"

# slug -> display heading (from c01fe76 section map)
SECTION_TITLES: list[tuple[str, str]] = [
    ("cold-open-predictions-teaser", "Cold Open — Predictions Teaser"),
    ("interview-open-predictions-and-petrodollar", "Interview Open — Predictions and Petrodollar"),
    ("iran-topography-attrition-and-hormuz", "Iran Topography, Attrition, and Hormuz"),
    ("national-defense-strategy-western-hemisphere", "National Defense Strategy — Western Hemisphere"),
    ("war-phases-ground-troops-and-irgc", "War Phases — Ground Troops and IRGC"),
    ("chess-grand-strategies-and-wwiii-players", "Chess Grand Strategies and WWIII Players"),
    ("global-chokepoints-russia-shadow-fleet", "Global Chokepoints — Russia Shadow Fleet"),
    ("timeline-trump-term-limits-and-forever-war", "Timeline — Trump Term Limits and Forever War"),
    ("eight-predictions-trump-third-term-and-ai-state", "Eight Predictions — Trump Third Term and AI State"),
    ("israel-greater-israel-nato-odessa", "Israel — Greater Israel, NATO, and Odessa"),
    ("east-asia-flashpoints-north-korea", "East Asia Flashpoints — North Korea"),
    ("community-hope-bronze-age-collapse", "Community, Hope, and Bronze Age Collapse"),
    ("plato-cave-reality-and-financial-elite", "Plato Cave — Reality and Financial Elite"),
    ("hermetic-philosophy-life-advice-and-closing-tradition", "Hermetic Philosophy, Life Advice, and Closing Tradition"),
]

# Anchor phrases: first ~50 chars of normalized text at section start (from sectioned version)
SECTION_ANCHORS = [
    "in 2024, you made three predictions",
    "there's so much going on in the world at the moment",
    "so, what i want to do now is go to the map",
    "but i want to show you something. okay, it's it's called the national defense strategy",
    "but you said in your prediction that he would lose the war",
    "explain to me how that happens. okay. so, we need to step back",
    "let's look at our present situation, okay? so, what we have so far",
    "so, when do you think this was going to happen?",
    "you've made eight new predictions",
    "so, once america leaves the middle east",
    "but east asia breaks out into conflict",
    "so, what does all of this stuff mean for the average person?",
    "professor, what's the most important thing we haven't talked about",
    "it may happen in everyone's lifetime. it may happen next 5 to 10 years",
]


def load_sectioned_from_git() -> str:
    result = subprocess.run(
        ["git", "show", f"c01fe76:interviews/{SOURCE_ID}/{SOURCE_ID}.md"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    return result.stdout


def extract_body(text: str) -> str:
    if "## Part I: Full transcript\n" not in text:
        raise ValueError("missing Part I marker")
    return text.split("## Part I: Full transcript\n", 1)[1].strip()


def normalize(s: str) -> str:
    s = re.sub(r"\*\*[^*]+:\*\*", "", s)
    s = re.sub(r"^>>\s*", "", s)
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s


def asr_cleanup(text: str) -> str:
    text = text.replace("Professor Dieng.", "Professor Jiang.")
    text = text.replace("Professor Dieng,", "Professor Jiang,")
    text = re.sub(r"\bThe The\b", "The", text)
    text = re.sub(r"\bIt It\b", "It", text)
    text = re.sub(r"\bTrump Trump\b", "Trump", text)
    text = re.sub(r"\bdemystify all of all of\b", "demystify all of", text)
    text = re.sub(r"\bMiddle Middle East\b", "Middle East", text)
    text = re.sub(r"\bof of\b", "of", text)
    text = re.sub(r"\bthe the\b", "the", text, flags=re.I)
    text = re.sub(r"\bhave has\b", "have", text, flags=re.I)
    text = re.sub(r"\bWorld War III\b", "World War III", text)  # normalize spacing
    return text


def find_anchor_pos(flat: str, anchor: str, start: int) -> int:
    pos = flat.lower().find(anchor, start)
    if pos == -1:
        raise ValueError(f"anchor not found: {anchor!r} (from pos {start})")
    return pos


def insert_sections(verbatim: str) -> str:
    flat = verbatim
    # Build char offsets for section splits using anchors
    positions = [0]
    cursor = 0
    for anchor in SECTION_ANCHORS[1:]:
        pos = find_anchor_pos(flat, anchor, cursor)
        positions.append(pos)
        cursor = pos + len(anchor)
    positions.append(len(flat))

    out_parts: list[str] = []
    for i, (slug, heading) in enumerate(SECTION_TITLES):
        chunk = flat[positions[i] : positions[i + 1]].strip()
        out_parts.append(f"### {heading}\n\n{chunk}")
    return "\n\n".join(out_parts)


def build_frontmatter() -> str:
    today = date.today().isoformat()
    return f"""---
source_id: {SOURCE_ID}
title: "{TITLE}"
source_series: "Predictive History Interviews"
publication_date: 2026-05-07
source_url: "https://www.youtube.com/watch?v=BTJGr78-zyw"
canonical_url: "https://www.youtube.com/watch?v=BTJGr78-zyw"
source_kind: youtube_interview
video_id: BTJGr78-zyw
workshop_source_id: ext-doac-01
interviews_episode: 16
ingested_at: "2026-06-25"
transcript_status: curated_transcript
transcript_curation: curated_sectioned
transcript_fidelity: exact_body_match
transcript_source: operator_paste
representation_not_endorsement: true
review_status: source_reviewed
source_reviewed_at: 2026-06-25
fidelity_reviewed_at: {today}
part: provenance
part_role: provenance
series: interviews
---"""


def main() -> None:
    current = TRANSCRIPT_PATH.read_text(encoding="utf-8")
    verbatim = extract_body(current)
    verbatim = asr_cleanup(verbatim)

    # Validate anchors against git sectioned version
    sectioned = load_sectioned_from_git()
    sectioned_body = extract_body(sectioned)
    for slug, _ in SECTION_TITLES:
        if f"### {slug}" not in sectioned_body:
            raise ValueError(f"missing slug in git sectioned: {slug}")

    body = insert_sections(verbatim)
    doc = f"{build_frontmatter()}\n\n# {TITLE}\n\n## Part I: Full transcript\n\n{body}\n"
    TRANSCRIPT_PATH.write_text(doc, encoding="utf-8", newline="\n")
    print(f"wrote {TRANSCRIPT_PATH} ({len(body.split()):,} words, {len(SECTION_TITLES)} sections)")


if __name__ == "__main__":
    main()
