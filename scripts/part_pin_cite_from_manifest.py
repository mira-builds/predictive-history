#!/usr/bin/env python3
"""Apply pin-cite sections from volume-i-anchors.yaml for one Part or chapter subset."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "pin-cite" / "volume-i-anchors.yaml"

from part_pin_cite_common import patch_transcript, update_chapter_commentary  # noqa: E402

PART_NUMBER_MAP = {
    "01": "part-01-dawn-of-civilization",
    "02": "part-02-hellenic-world",
    "03": "part-03-roman-imperium",
    "04": "part-04-ancient-foundations",
    "05": "part-05-christianity-and-islam",
    "06": "part-06-medieval-imagination",
    "07": "part-07-world-after-rome",
    "08": "part-08-birth-of-modernity",
    "09": "part-09-age-of-conscience",
    "10": "part-10-rise-of-the-nation-state",
}


def load_chapters() -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    data = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    return data.get("chapters", {})


def main() -> int:
    parser = argparse.ArgumentParser(description="Pin-cite from volume-i-anchors.yaml")
    parser.add_argument("--part", help="Part number 01-10")
    parser.add_argument("--chapter", help="Single chapter id e.g. civ-42")
    args = parser.parse_args()

    if not MANIFEST.is_file():
        print(f"missing manifest: {MANIFEST}", file=sys.stderr)
        return 1

    chapters = load_chapters()
    part_id = PART_NUMBER_MAP.get(args.part) if args.part else None

    targets: list[str] = []
    if args.chapter:
        targets = [args.chapter]
    elif part_id:
        targets = sorted(
            cid for cid, entry in chapters.items() if entry.get("part_id") == part_id
        )
    else:
        print("specify --part NN or --chapter civ-NN", file=sys.stderr)
        return 1

    for cid in targets:
        entry = chapters.get(cid)
        if not entry:
            print(f"skip (not in manifest): {cid}")
            continue
        sections = [(row["slug"], row["phrase"]) for row in entry["sections"]]
        claim_refs = entry["claim_refs"]
        patch_transcript(cid, sections, part_id=entry.get("part_id"))
        update_chapter_commentary(cid, claim_refs)

    print(f"part_pin_cite_from_manifest: done ({len(targets)} chapters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
