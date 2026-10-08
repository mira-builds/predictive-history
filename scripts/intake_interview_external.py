#!/usr/bin/env python3
"""Intake one external interview (operator paste / no workshop vi-* row)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Reuse packet builders from phase-1 workshop intake.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from intake_interviews_phase1 import (  # noqa: E402
    INGESTED_AT,
    MANIFEST_PATH,
    PH_CIV,
    build_card_jsonl,
    build_card_md,
    build_commentary,
    build_readme,
    build_transcript,
    ensure_ph_civ_index,
    merge_cards_jsonl,
)


def read_operator_body(path: Path) -> str:
    """Read an operator paste and remove only the known YouTube transcript wrapper."""
    body = path.read_text(encoding="utf-8").strip()
    lines = body.splitlines()
    if len(lines) >= 3 and lines[0].strip().endswith(" - YouTube"):
        transcript_marker = next(
            (index for index, line in enumerate(lines[:5]) if line.strip() == "Transcripts:"),
            None,
        )
        if transcript_marker is not None:
            return "\n".join(lines[transcript_marker + 1 :]).strip()
    return body


def mark_operator_paste_transcript(transcript: str) -> str:
    """Replace workshop-promotion review claims with truthful intake metadata."""
    return (
        transcript.replace("transcript_status: curated_transcript", "transcript_status: operator_paste")
        .replace(
            "transcript_fidelity: exact_body_match\ntranscript_source: workshop_promotion",
            "transcript_fidelity: exact_body_match\ntranscript_source: operator_paste\ntranscript_curation: unsectioned",
        )
        .replace("review_status: source_reviewed", "review_status: in_review")
        .replace(f"source_reviewed_at: {INGESTED_AT}\n", "")
    )


def mark_operator_paste_commentary(commentary: str) -> str:
    return commentary.replace("review_status: source_reviewed", "review_status: in_review").replace(
        f"source_reviewed_at: {INGESTED_AT}\n", ""
    )


def append_manifest(row: dict) -> None:
    payload = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    entries = payload["entries"]
    if any(e["source_id"] == row["source_id"] for e in entries):
        raise SystemExit(f"manifest already has source_id: {row['source_id']}")
    entries.append(row)
    payload["entries"] = entries
    MANIFEST_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def intake_external(
    *,
    source_id: str,
    title: str,
    publication_date: str,
    url: str,
    video_id: str,
    workshop_source_id: str,
    interviews_episode: int,
    body: str,
    thesis: str,
    terms: str,
    claims: str,
) -> str:
    target = PH_CIV / "interviews" / source_id
    target.mkdir(parents=True, exist_ok=True)

    (target / f"{source_id}.md").write_text(
        mark_operator_paste_transcript(build_transcript(
            source_id,
            title,
            publication_date=publication_date,
            url=url,
            video_id=video_id,
            workshop_source_id=workshop_source_id,
            interviews_episode=interviews_episode,
            body=body,
        )),
        encoding="utf-8",
        newline="\n",
    )
    (target / f"{source_id}-commentary.md").write_text(
        mark_operator_paste_commentary(build_commentary(
            source_id,
            title,
            thesis=thesis,
            terms=terms,
            claims=claims,
            workshop_source_id=workshop_source_id,
        )),
        encoding="utf-8",
        newline="\n",
    )
    (target / "README.md").write_text(build_readme(source_id, title, url), encoding="utf-8", newline="\n")

    card_md = PH_CIV / "data" / "cards" / f"{source_id}.md"
    card_md.write_text(build_card_md(source_id, title, workshop_source_id), encoding="utf-8", newline="\n")
    return source_id


def main() -> int:
    parser = argparse.ArgumentParser(description="Intake external interview packet")
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--publication-date", required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument("--video-id", required=True)
    parser.add_argument("--workshop-source-id", default="ext-doac-01")
    parser.add_argument("--interviews-episode", type=int, required=True)
    parser.add_argument("--body-file", type=Path, required=True)
    parser.add_argument("--thesis-file", type=Path, default=None)
    parser.add_argument("--skip-manifest", action="store_true")
    args = parser.parse_args()

    body = read_operator_body(args.body_file)
    thesis = terms = claims = ""
    if args.thesis_file and args.thesis_file.exists():
        thesis = args.thesis_file.read_text(encoding="utf-8").strip()

    if not args.skip_manifest:
        append_manifest(
            {
                "workshop_source_id": args.workshop_source_id,
                "source_id": args.source_id,
                "publication_date": args.publication_date,
                "video_id": args.video_id,
                "interviews_episode": args.interviews_episode,
                "title": args.title,
                "intake_mode": "operator_paste",
            }
        )

    source_id = intake_external(
        source_id=args.source_id,
        title=args.title,
        publication_date=args.publication_date,
        url=args.url,
        video_id=args.video_id,
        workshop_source_id=args.workshop_source_id,
        interviews_episode=args.interviews_episode,
        body=body,
        thesis=thesis,
        terms=terms,
        claims=claims,
    )
    card = build_card_jsonl(
        source_id,
        args.title,
        args.publication_date,
        args.workshop_source_id,
    )
    card["source_snapshot"] = {
        "commit": "operator-paste",
        "path": f"data/cards/{source_id}.md",
        "repo": "mira-builds/predictive-history",
    }
    merge_cards_jsonl([card])
    ensure_ph_civ_index()
    print(f"intake complete: {source_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
