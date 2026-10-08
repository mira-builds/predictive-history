#!/usr/bin/env python3
"""Apply Title Case section headings + light ASR cleanup to Tucker Carlson vi-11 transcript.

    python scripts/patch_tucker_sections_asr.py
    python -m civ_ph.cli index --force
    python -m civ_ph.cli validate

Section map from PH-TRANSCRIPT-EDIT commit d475974.
See `interviews/README.md` § Interview section headings.
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ID = "interview-2026-03-20-tucker-carlson"
TITLE = "Interviews #11: Tucker Carlson — Iran War, Energy, and Global Order"
TRANSCRIPT_PATH = ROOT / "interviews" / SOURCE_ID / f"{SOURCE_ID}.md"

SECTION_HEADINGS: list[tuple[str, str]] = [
    ("iran-attrition-and-global-stakes", "Iran Attrition and Global Stakes"),
    ("us-off-ramp-petrodollar-and-china", "US Off-Ramp — Petrodollar and China"),
    ("three-trends-under-energy-shock", "Three Trends Under Energy Shock"),
    ("east-asia-japan-korea-and-southeast-asia", "East Asia — Japan, Korea, and Southeast Asia"),
    ("regional-horizons-gcc-iran-israel", "Regional Horizons — GCC, Iran, and Israel"),
    ("us-military-eschatology-and-trump", "US Military Eschatology and Trump"),
    (
        "north-america-europe-and-western-civ-closing",
        "North America, Europe, and Western Civilization Closing",
    ),
]


def asr_cleanup(text: str) -> str:
    text = text.replace("Professor Dieng.", "Professor Jiang.")
    text = text.replace("Professor Dieng,", "Professor Jiang,")
    text = re.sub(r"\bThe The\b", "The", text)
    text = re.sub(r"\bIt It\b", "It", text)
    text = re.sub(r"\bthe the\b", "the", text, flags=re.I)
    text = re.sub(r"\bof of\b", "of", text)
    return text


def apply_section_headings(body: str) -> str:
    out = body
    for slug, heading in SECTION_HEADINGS:
        old = f"### {slug}"
        new = f"### {heading}"
        if old not in out and new in out:
            continue
        if old not in out:
            raise ValueError(f"missing section slug: {slug}")
        out = out.replace(old, new, 1)
    return out


def update_frontmatter_fidelity(text: str) -> str:
    today = date.today().isoformat()
    if "fidelity_reviewed_at:" in text:
        text = re.sub(
            r"^fidelity_reviewed_at:.*$",
            f'fidelity_reviewed_at: {today}',
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
    body = apply_section_headings(asr_cleanup(body))
    doc = update_frontmatter_fidelity(head) + "## Part I: Full transcript\n" + body
    TRANSCRIPT_PATH.write_text(doc, encoding="utf-8", newline="\n")
    print(
        f"wrote {TRANSCRIPT_PATH} "
        f"({len(body.split()):,} words, {len(SECTION_HEADINGS)} sections)"
    )


if __name__ == "__main__":
    main()
