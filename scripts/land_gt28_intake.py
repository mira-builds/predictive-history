#!/usr/bin/env python3
"""One-shot ph-civ intake for gt-28 from statecraft source-archive capture."""

from __future__ import annotations

import json
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = (
    ROOT.parent.parent
    / "source-archive/statecraft/2026-05-26/source-game-theory-28-predictive-history-2026-05-26.md"
)

SOURCE_ID = "gt-28"
TITLE = "Game Theory #28: Predictive History"
PUB_DATE = "2026-05-26"
SOURCE_URL = "https://www.youtube.com/watch?v=dja6dkCfngE"
VIDEO_ID = "dja6dkCfngE"
CAPTURED = "2026-06-24"

TRANSCRIPT_FM = f"""---
source_id: "{SOURCE_ID}"
title: "{TITLE}"
source_series: "Game Theory"
publication_date: "{PUB_DATE}"
source_url: "{SOURCE_URL}"
video_id: "{VIDEO_ID}"
transcript_status: "public_transcript"
transcript_fidelity: "exact_body_match"
transcript_source: "user_pasted_public_transcript"
representation_not_endorsement: true
review_status: "provisional"
source_captured_at: "{CAPTURED}"
part: "world-war"
part_role: "world-war"
---

# {TITLE}

## Part I: Full transcript

"""


def extract_body(archive_path: Path) -> str:
    text = archive_path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise SystemExit(f"expected YAML frontmatter in {archive_path}")
    end = text.find("\n---", 3)
    if end == -1:
        raise SystemExit("missing closing frontmatter")
    body = text[end + 4 :].lstrip("\n")
    if body.startswith(f"# {TITLE}"):
        body = body.split("\n", 1)[1].lstrip("\n")
    return body.strip() + "\n"


def write_transcript_pair(body: str) -> None:
    payload = TRANSCRIPT_FM + body
    paths = [
        ROOT / "lectures/game-theory/gt-28/gt-28-transcript.md",
        ROOT / "lectures/game-theory/gt-28/gt-28-transcript.md",
    ]
    for path in paths:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload, encoding="utf-8", newline="\n")


def write_commentary() -> None:
    path = ROOT / "lectures/game-theory/gt-28/gt-28-commentary.md"
    path.write_text(
        textwrap.dedent(
            f"""\
            ---
            source_id: "{SOURCE_ID}"
            title: "{TITLE}"
            source_series: "Game Theory"
            publication_date: "{PUB_DATE}"
            source_chapter_path: "lectures/game-theory/gt-28/gt-28-transcript.md"
            source_corpus_path: "lectures/game-theory/gt-28/gt-28-transcript.md"
            commentary_status: "provisional"
            review_status: "provisional"
            annotation_status: "seeded"
            template_family: "world-war-strategic-commentary"
            part: "world-war"
            part_role: "world-war"
            representation_not_endorsement: true
            canvas_status: open
            analysis_depth: seed
            scaffold_version: ph_civ_commentary_canvas_v1
            ---

            # {TITLE}

            ## Core Strategic Thesis

            The lecture argues that geopolitics, eschatology, and imperial decline are not competing explanations for the US-Iran war but convergent frameworks that predict similar outcomes — and that beneath all three lies a struggle over consciousness, money, and the emerging AI god.

            ## Neutral Lecture Summary

            This commentary canvas is a source-first placeholder for `{SOURCE_ID}`. It is meant to help a reader follow the semester-review argument without treating the transcript or analysis as final.

            ## Actors, Systems, And Stakes

            - the US, Iran, Russia, China, and Israel as the lecture's primary state actors
            - Levant crossroads history as the allegorical seed of shared eschatological scripts
            - secret societies, occult traditions, Kabbalah, and Hermetic philosophy as coordination metaphors
            - transnational capital (money) versus AI as competing systems of imagination capture

            ## Claims, Forecasts, And Falsifiers

            - Identify which claims are structural metaphor versus falsifiable forecast.
            - Separate lecture-local eschatological narrative from verifiable geopolitical mechanism.
            - Revisit after transcript fidelity and source review are complete.

            ## Evidence Limits And Date Sensitivity

            This chapter is date-sensitive and provisional. Verify event timing, religious-historical claims, economic statistics, and named institutional assertions against primary sources before quotation-grade use.

            ## Counter-Readings

            A conventional reading may treat the three-framework convergence as rhetorical synthesis rather than proof of unified causation, and may reject literal secret-society or occult drivers in favor of institutional incentive analysis.

            ## Open Issues For Review

            - Verify the transcript against the public video.
            - Check proper nouns, quotations, statistics, and institutional names.
            - Decide which blocks are pedagogical metaphor, which are falsifiable forecasts, and which require external theological or historical review.

            ---

            ## Project Canvas

            ### Layer 0 — Source floor

            - Transcript: `lectures/game-theory/gt-28/gt-28-transcript.md`
            - Canonical capture: `lectures/game-theory/gt-28/gt-28-transcript.md`

            ### Layer 1 — Lecture spine (seed)

            1. Three reasons for US-Iran war: geopolitics, eschatology, imperial decline
            2. Eschatology as condensed Levant geopolitics (Messiah / antichrist pattern)
            3. Occult, secret societies, and sexual-metaphor eschatological mobilization
            4. Plato's cave: money god versus AI god

            ### Layer 2 — Pin-cite targets (pending)

            - _Unpinned — run pin-cite pass after fidelity review_

            ### Layer 3 — Falsifiers (pending)

            - _Ungraded — add after Layer 2 pin-cite pass_

            ### Layer 4–6 — Reserved

            Open canvas. Do not treat seed scaffolding as final analysis.
            """
        ),
        encoding="utf-8",
        newline="\n",
    )


def write_orientation() -> None:
    path = ROOT / "lectures/game-theory/gt-28/gt-28-orientation.yaml"
    path.write_text(
        textwrap.dedent(
            f"""\
            source_id: {SOURCE_ID}
            placement_weight: strong
            part: world-war
            part_role: world-war
            where_this_sits: |
              This Game Theory chapter is the semester-review synthesis before the final examination: it unifies geopolitics, eschatology, and imperial decline, then descends through Levant history, occult coordination metaphors, and Plato's cave (money versus AI).
            reading_posture: |
              Read it with strict representation boundaries. The packet should help a reader follow a capstone classroom framework without treating metaphysical, occult, or conspiracy metaphors as verified institutional fact.
            historical_pressure_points:
              - US-Iran war as the semester's central diagnostic case
              - convergent geopolitical, eschatological, and imperial-decline frames
              - reserve-currency stress, elite overproduction, and outward projection of civil conflict
              - money versus AI as competing imagination-capture systems
            limits_of_the_frame: |
              This packet is provisional and high-caution. Transcript fidelity, religious-historical claims, occult metaphors, economic statistics, and named institutional assertions require close review before quotation-grade use.
            return_path: |
              Return through the transcript, commentary canvas, public card, and the direct `ph-apo` chapter namespace. Do not promote this chapter into public routes until review is complete.
            """
        ),
        encoding="utf-8",
        newline="\n",
    )


def write_readme() -> None:
    path = ROOT / "lectures/game-theory/gt-28/README.md"
    path.write_text(
        textwrap.dedent(
            f"""\
            # {TITLE}

            This chapter folder is a public study doorway for `{SOURCE_ID}`. This folder is provisional: transcript fidelity and claims review are still visible work.

            ## Start Here

            Use this folder when someone shares the GitHub chapter link in a YouTube comment or an LLM chat. Start with the transcript, then use the commentary canvas and orientation card to keep the reading bounded.

            ## Source-Lattice Reading Order

            Treat this chapter folder as a small source-lattice:

            1. `Doorway` - this README tells you what the packet is and what limits apply.
            2. `Primary source floor` - read the transcript and public source capture first.
            3. `Secondary support` - use the commentary canvas, orientation payload, and public card only after the source floor is open.
            4. `Widened interpretation` - draw comparisons or broader claims only after keeping the review status in view.


            ## Source Video

            - YouTube: {SOURCE_URL}

            ## Canonical Source Capture

            - [Public source capture](../../../lectures/game-theory/gt-28/gt-28-transcript.md)

            ## Files

            - [Transcript](gt-28-transcript.md)
            - [Commentary canvas](gt-28-commentary.md)
            - [Orientation payload](gt-28-orientation.yaml)
            - [Public card](../../../data/cards/gt-28.md)

            ## Review Status

            `provisional`. Do not treat provisional transcript text, named claims, quotations, or current-event predictions as final until review is complete.

            ## LLM Prompt

            Paste this folder link into ChatGPT, Claude, or Grok and ask:

            > Guide me through this chapter folder as a public study packet. Start with the transcript, then use the commentary canvas and orientation/card guardrails. Keep provisional claims bounded and separate lecture representation from verification.
            >
            > Use a source-lattice reading order: README first, transcript and source capture second, commentary/orientation/card third, and broader interpretation only after the source floor is stable.

            ## Guardrails

            This folder represents the public lecture material and companion study apparatus. It is not a private note dump, not an endorsement layer, and not a substitute for source review.
            """
        ),
        encoding="utf-8",
        newline="\n",
    )


def write_card_md() -> None:
    path = ROOT / "data/cards/gt-28.md"
    path.write_text(
        textwrap.dedent(
            f"""\
            ---
            source_id: "{SOURCE_ID}"
            title: "{TITLE}"
            series: "game-theory"
            part: "world-war"
            placement_weight: "strong"
            review_status: "provisional"
            ---

            # {TITLE}

            ## Where This Sits

            This Game Theory chapter is the semester-review synthesis before the final examination: it merges geopolitics, eschatology, and imperial decline into one predictive-history framework, then moves through Levant allegory, occult coordination metaphors, and Plato's cave (money versus AI).

            ## Reading Posture

            Read it with strict representation boundaries. The lecture moves between classroom recap, religious-historical narrative, occult metaphor, and monetary-AI civil-war diagnosis; the packet keeps those layers separate.

            ## Historical Pressure Points

            - US-Iran war as the semester's central case study
            - convergent geopolitical, eschatological, and imperial-decline explanations
            - Levant crossroads history and shared messianic scripts
            - money versus AI as competing systems of imagination capture

            ## Limits of the Frame

            This packet is provisional and high-caution. Transcript fidelity, religious-historical claims, occult metaphors, economic statistics, and named institutional assertions require close review.

            ## Return Path

            Return through `lectures/game-theory/gt-28/`, the commentary canvas, and the lecture transcript under `lectures/`. This card is a provisional doorway, not a launch claim.
            """
        ),
        encoding="utf-8",
        newline="\n",
    )


def card_jsonl_entry() -> dict:
    return {
        "part": "world-war",
        "placement_weight": "strong",
        "review_status": "provisional",
        "sections": {
            "Historical Pressure Points": (
                "- US-Iran war as the semester's central case study\n"
                "- convergent geopolitical, eschatological, and imperial-decline explanations\n"
                "- Levant crossroads history and shared messianic scripts\n"
                "- money versus AI as competing systems of imagination capture"
            ),
            "Limits of the Frame": (
                "This packet is provisional and high-caution. Transcript fidelity, "
                "religious-historical claims, occult metaphors, economic statistics, "
                "and named institutional assertions require close review."
            ),
            "Reading Posture": (
                "Read it with strict representation boundaries. The lecture moves between "
                "classroom recap, religious-historical narrative, occult metaphor, and "
                "monetary-AI civil-war diagnosis; the packet keeps those layers separate."
            ),
            "Return Path": (
                "Return through `lectures/game-theory/gt-28/`, the commentary canvas, and "
                "the lecture transcript under `lectures/`. This card is a provisional "
                "doorway, not a launch claim."
            ),
            "Where This Sits": (
                "This Game Theory chapter is the semester-review synthesis before the final "
                "examination: it merges geopolitics, eschatology, and imperial decline into "
                "one predictive-history framework, then moves through Levant allegory, occult "
                "coordination metaphors, and Plato's cave (money versus AI)."
            ),
        },
        "series": "game-theory",
        "source_id": SOURCE_ID,
        "source_paths": {
            "commentary_path": "lectures/game-theory/gt-28/gt-28-commentary.md",
            "orientation_payload_path": "lectures/game-theory/gt-28/gt-28-orientation.yaml",
            "source_chapter_path": "lectures/game-theory/gt-28/gt-28-transcript.md",
            "source_corpus_path": "lectures/game-theory/gt-28/gt-28-transcript.md",
        },
        "source_snapshot": {"commit": "", "path": "data/cards/gt-28.md", "repo": "public-source-capture"},
        "title": TITLE,
    }


def insert_cards_jsonl(entry: dict) -> None:
    path = ROOT / "data/cards.jsonl"
    lines = path.read_text(encoding="utf-8").splitlines()
    if any(f'"source_id": "{SOURCE_ID}"' in line for line in lines):
        return
    out: list[str] = []
    inserted = False
    for line in lines:
        out.append(line)
        if not inserted and '"source_id": "gt-27"' in line:
            out.append(json.dumps(entry, ensure_ascii=False))
            inserted = True
    if not inserted:
        raise SystemExit("gt-27 anchor not found in cards.jsonl")
    path.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")


def insert_index_json() -> None:
    path = ROOT / "data/index.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    cards = data.get("cards", [])
    if any(card.get("source_id") == SOURCE_ID for card in cards):
        data["card_count"] = len(cards)
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
        return
    new_card = {
        "part": "world-war",
        "path": "data/cards/gt-28.md",
        "placement_weight": "strong",
        "review_status": "provisional",
        "series": "game-theory",
        "source_id": SOURCE_ID,
        "title": TITLE,
    }
    out: list[dict] = []
    inserted = False
    for card in cards:
        out.append(card)
        if not inserted and card.get("source_id") == "gt-27":
            out.append(new_card)
            inserted = True
    if not inserted:
        raise SystemExit("gt-27 anchor not found in index.json")
    data["cards"] = out
    data["card_count"] = len(out)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    if not ARCHIVE.exists():
        raise SystemExit(f"missing archive capture: {ARCHIVE}")
    body = extract_body(ARCHIVE)
    write_transcript_pair(body)
    write_commentary()
    write_orientation()
    write_readme()
    write_card_md()
    insert_cards_jsonl(card_jsonl_entry())
    insert_index_json()
    print(f"landed {SOURCE_ID}: {len(body.split())} transcript words")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
