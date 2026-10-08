#!/usr/bin/env python3
"""Strip Part apparatus steps from chapter READMEs (v2 source-lattice)."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book"

OLD_STEP = re.compile(
    r"4\. Part apparatus[^\n]*\n",
    re.IGNORECASE,
)
NEW_STEP = (
    "4. Chapter commentary — full L0–6 in the companion commentary file "
    "(see docs/methodology/commentary-methodology-v2.md).\n"
)
OLD_LATTICE = re.compile(
    r"Use a source-lattice reading order: README first, transcript second, "
    r"chapter commentary third, Part apparatus fourth, public card fifth, "
    r"and broader interpretation only after those floors are stable\.",
    re.IGNORECASE,
)
NEW_LATTICE = (
    "Use a source-lattice reading order: README first, transcript second, "
    "chapter commentary third (L0–6), public card fourth, and broader "
    "interpretation only after those floors are stable."
)
PART_FILE_LINE = re.compile(
    r"^- \[Part [^\]]+\]\([^)]*parts/[^)]+\)[^\n]*\n",
    re.MULTILINE,
)
THIN_COMMENTARY = re.compile(
    r"\[Commentary canvas \(thin\)\]",
    re.IGNORECASE,
)


def patch_readme(text: str) -> tuple[str, bool]:
    original = text
    if "Part apparatus" in text or "parts/part-" in text:
        text = OLD_STEP.sub(NEW_STEP, text)
        text = OLD_LATTICE.sub(NEW_LATTICE, text)
        text = PART_FILE_LINE.sub("", text)
        text = THIN_COMMENTARY.sub("[Commentary canvas]", text)
        text = text.replace(
            "then use the thin chapter commentary (Layer 0-2 pin-cites), then Part II commentary and bibliography for cross-chapter synthesis.",
            "then use the chapter commentary (L0–6) as the interpretation SSOT.",
        )
        text = text.replace(
            "thin Layer 0-2 pin-cites in the companion commentary file.",
            "full L0–6 commentary in the companion commentary file.",
        )
    return text, text != original


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    changed = 0
    for readme in sorted(BOOK.rglob("README.md")):
        text = readme.read_text(encoding="utf-8")
        if "Part apparatus" not in text and "parts/part-" not in text:
            continue
        new_text, did_change = patch_readme(text)
        if not did_change:
            continue
        changed += 1
        rel = readme.relative_to(ROOT)
        if args.dry_run:
            print(f"would patch {rel}")
        else:
            readme.write_text(new_text, encoding="utf-8")
            print(f"patched {rel}")
    print(f"{'would patch' if args.dry_run else 'patched'} {changed} README files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
