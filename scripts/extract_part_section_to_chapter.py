#!/usr/bin/env python3
"""Extract a Part commentary section for merge into a chapter commentary (v2 migration)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from civ_ph.commentary_v2 import extract_part_section  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("part_commentary", type=Path, help="Path to part-NN-*-commentary.md")
    parser.add_argument("section_id", help="e.g. civ-07, gb-02, sh-17")
    parser.add_argument("--out", type=Path, help="Write extracted markdown to file")
    args = parser.parse_args()

    part_path = args.part_commentary
    if not part_path.is_absolute():
        part_path = ROOT / part_path
    text = part_path.read_text(encoding="utf-8")
    body = extract_part_section(text, args.section_id)
    if not body:
        print(f"ERROR: section ### {args.section_id} not found in {part_path}", file=sys.stderr)
        return 1
    if args.out:
        out = args.out if args.out.is_absolute() else ROOT / args.out
        out.write_text(body + "\n", encoding="utf-8")
        print(f"wrote {out.relative_to(ROOT)}")
    else:
        print(body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
