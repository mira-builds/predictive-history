#!/usr/bin/env python3
"""Validate pin-cite manifest against transcript ### rails and phrase uniqueness."""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "pin-cite" / "volume-i-anchors.yaml"
VOL2 = ROOT / "book" / "volume-ii"


def load_manifest() -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required: pip install pyyaml")
    data = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    return data.get("chapters", {})


def transcript_body(chapter_id: str) -> str:
    path = VOL2 / chapter_id / f"{chapter_id}-transcript.md"
    text = path.read_text(encoding="utf-8")
    marker = "## Part I: Full transcript\n\n"
    if marker not in text:
        raise ValueError(f"Missing transcript marker: {path}")
    return text.split(marker, 1)[1]


def validate_chapter(chapter_id: str, entry: dict) -> list[str]:
    errors: list[str] = []
    path = VOL2 / chapter_id / f"{chapter_id}-transcript.md"
    if not path.is_file():
        return [f"missing transcript: {path.relative_to(ROOT)}"]
    full = path.read_text(encoding="utf-8")
    body = transcript_body(chapter_id)
    flat = re.sub(r"\s+", " ", body)
    lower = flat.lower()

    sections = entry.get("sections", [])
    claim_refs = entry.get("claim_refs", [])
    slugs = [row["slug"] for row in sections]

    for slug in slugs:
        if f"### {slug}" not in full:
            errors.append(f"{chapter_id}: missing ### {slug} in transcript")

    search_from = 0
    for row in sections:
        slug = row["slug"]
        phrase = row["phrase"]
        idx = lower.find(phrase.lower(), search_from)
        if idx < 0:
            errors.append(f"{chapter_id}: phrase not found for {slug}: {phrase[:50]!r}")
        else:
            search_from = idx + 1

    for ref in claim_refs:
        slug = ref.lstrip("#")
        if slug not in slugs:
            errors.append(f"{chapter_id}: claim_ref {ref} not in sections slugs")

    comm = VOL2 / chapter_id / f"{chapter_id}-commentary.md"
    if comm.is_file():
        comm_text = comm.read_text(encoding="utf-8")
        for ref in claim_refs:
            needle = f"{chapter_id}-transcript.md{ref}"
            if needle not in comm_text:
                errors.append(f"{chapter_id}: commentary missing ref {needle}")

    return errors


def main() -> int:
    if not MANIFEST.is_file():
        print(f"missing manifest: {MANIFEST.relative_to(ROOT)}", file=sys.stderr)
        return 1
    chapters = load_manifest()
    all_errors: list[str] = []
    for chapter_id in sorted(chapters):
        all_errors.extend(validate_chapter(chapter_id, chapters[chapter_id]))
    if all_errors:
        for err in all_errors:
            print(err, file=sys.stderr)
        print(f"validate_pin_cite: {len(all_errors)} error(s)", file=sys.stderr)
        return 1
    print(f"validate_pin_cite: ok ({len(chapters)} chapters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
