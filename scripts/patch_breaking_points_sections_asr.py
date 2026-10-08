#!/usr/bin/env python3
"""Apply Title Case section headings + light ASR cleanup to Breaking Points vi-07 transcript.

    python scripts/patch_breaking_points_sections_asr.py
    python -m civ_ph.cli index --force
    python -m civ_ph.cli validate

Section map from PH-TRANSCRIPT-EDIT commit 8c35fd6.
See `interviews/README.md` § Interview section headings.
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ID = "interview-2026-03-02-breaking-points"
TRANSCRIPT_PATH = ROOT / "interviews" / SOURCE_ID / f"{SOURCE_ID}.md"

SECTION_HEADINGS: list[tuple[str, str]] = [
    ("show-open-and-2024-predictions-clip", "Show Open — 2024 Predictions Clip"),
    ("iran-attrition-gcc-and-ai-bubble", "Iran Attrition — GCC and AI Bubble"),
    (
        "munitions-interceptor-math-and-multipolar-shift",
        "Munitions — Interceptor Math and Multipolar Shift",
    ),
    (
        "ground-troops-hegseth-and-gcc-pressure",
        "Ground Troops — Hegseth and GCC Pressure",
    ),
    (
        "saudi-israel-push-and-washington-post-leak",
        "Saudi–Israel Push and Washington Post Leak",
    ),
    (
        "why-trump-struck-hubris-calculus-eschatology",
        "Why Trump Struck — Hubris, Calculus, and Eschatology",
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
    body = apply_section_headings(asr_cleanup(body))
    doc = update_frontmatter_fidelity(head) + "## Part I: Full transcript\n" + body
    TRANSCRIPT_PATH.write_text(doc, encoding="utf-8", newline="\n")
    print(
        f"wrote {TRANSCRIPT_PATH} "
        f"({len(body.split()):,} words, {len(SECTION_HEADINGS)} sections)"
    )


if __name__ == "__main__":
    main()
