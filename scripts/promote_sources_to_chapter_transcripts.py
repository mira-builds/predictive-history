#!/usr/bin/env python3
"""Promote lectures/game-theory transcripts into card transcript paths when thin."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from civ_ph.data import PACKAGE_ROOT, load_cards
from civ_ph.ph_civ_index import count_transcript_words, ensure_ph_civ_index

LECTURES_DIR = PACKAGE_ROOT / "lectures/game-theory"
DEFAULT_CAPTURE_DATE = "2026-06-23"


def refresh_capture_date(text: str, capture_date: str) -> str:
    if not text.startswith("---"):
        return text
    end = text.find("\n---\n", 4)
    if end == -1:
        return text
    fm_lines: list[str] = []
    for line in text[4:end].splitlines():
        if line.startswith("source_captured_at:"):
            fm_lines.append(f'source_captured_at: "{capture_date}"')
        else:
            fm_lines.append(line)
    body = text[end + 5 :]
    return "---\n" + "\n".join(fm_lines) + "\n---\n" + body


def promote_file(src: Path, dest: Path, *, capture_date: str) -> int:
    text = refresh_capture_date(src.read_text(encoding="utf-8"), capture_date)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8")
    return count_transcript_words(text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--capture-date", default=DEFAULT_CAPTURE_DATE)
    parser.add_argument("--min-dest-words", type=int, default=1000)
    parser.add_argument("--source-id", action="append", dest="source_ids")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    cards = load_cards()
    if args.source_ids:
        wanted = set(args.source_ids)
        cards = [card for card in cards if card["source_id"] in wanted]

    promoted: list[tuple[str, int, str]] = []
    skipped: list[tuple[str, str]] = []

    for card in cards:
        source_id = card["source_id"]
        rel = card.get("source_paths", {}).get("source_chapter_path", "")
        if not rel:
            skipped.append((source_id, "missing source_chapter_path"))
            continue
        dest = PACKAGE_ROOT / rel
        src = LECTURES_DIR / source_id / f"{source_id}-transcript.md"
        if not src.exists():
            skipped.append((source_id, "missing lecture transcript"))
            continue
        dest_words = (
            count_transcript_words(dest.read_text(encoding="utf-8")) if dest.exists() else 0
        )
        if dest_words >= args.min_dest_words:
            continue
        src_words = count_transcript_words(src.read_text(encoding="utf-8"))
        if src_words < 100:
            skipped.append((source_id, f"thin source ({src_words} words)"))
            continue
        if args.dry_run:
            promoted.append((source_id, src_words, rel))
            continue
        words = promote_file(src, dest, capture_date=args.capture_date)
        promoted.append((source_id, words, rel))

    if not args.dry_run and promoted:
        ensure_ph_civ_index(force=True)

    print(f"promoted: {len(promoted)}")
    for source_id, words, rel in sorted(promoted):
        print(f"  {source_id}: {words} words -> {rel}")
    if skipped:
        print(f"skipped: {len(skipped)}")
        for source_id, reason in sorted(skipped):
            print(f"  {source_id}: {reason}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
