#!/usr/bin/env python3
"""Validate Volume I Part registry against the interwoven spine."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from civ_ph.volume_i_parts import validate_volume_i_parts  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate data/parts/volume-i-parts.json")
    parser.add_argument("--json", action="store_true", help="Reserved for future JSON output")
    parser.add_argument(
        "--skip-doorways",
        action="store_true",
        help="Do not require doorway markdown files on disk",
    )
    parser.add_argument(
        "--skip-chapter-anchors",
        action="store_true",
        help="Do not require chapter_anchors in registry JSON",
    )
    args = parser.parse_args()
    _ = args.json

    errors = validate_volume_i_parts(
        require_doorways=not args.skip_doorways,
        require_chapter_anchors=not args.skip_chapter_anchors,
    )
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print("volume_i_parts: valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
