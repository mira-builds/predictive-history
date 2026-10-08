#!/usr/bin/env python3
"""Batch-update book/volume-i-civilization/parts/ paths after parts migration."""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REPLACEMENTS: list[tuple[str, str]] = [
    ("book/volume-i-civilization/parts/", "docs/routes/volume-i-parts/"),
    ("../../../book/volume-i-civilization/parts/", "../../../docs/routes/volume-i-parts/"),
    ("../../book/volume-i-civilization/parts/", "../../docs/routes/volume-i-parts/"),
    ("../../volume-i-civilization/parts/", "../../../docs/routes/volume-i-parts/"),
    ("book/volume-i-civilization/interwoven-reader/README.md", "docs/archive/two-volume-reader-order-interwoven.md"),
    ("../interwoven-reader/README.md", "../../archive/two-volume-reader-order-interwoven.md"),
    ("book/parts/civilization-to-apocalypse.md", "docs/routes/civilization-to-apocalypse.md"),
    ("book/table-of-contents.md", "docs/archive/two-volume-reader-order.md"),
    ("book/seven-volume-to-two-volume.md", "docs/archive/seven-volume-to-two-volume.md"),
    ("book/provenance/README.md", "docs/archive/book-provenance-index.md"),
]

SCAN_SUFFIXES = {".md", ".json", ".py", ".yaml", ".yml", ".txt"}
SKIP_DIRS = {
    ".git",
    ".codex-tmp",
    "__pycache__",
    "node_modules",
    ".venv",
    "site",
}


def should_scan(path: Path) -> bool:
    if path.suffix.lower() not in SCAN_SUFFIXES:
        return False
    return not any(part in SKIP_DIRS for part in path.parts)


def apply_replacements(text: str) -> tuple[str, int]:
    count = 0
    for old, new in REPLACEMENTS:
        if old in text:
            n = text.count(old)
            text = text.replace(old, new)
            count += n
    return text, count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    total_files = 0
    total_replacements = 0
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or not should_scan(path):
            continue
        if path.name == "migrate_book_parts_paths.py":
            continue
        original = path.read_text(encoding="utf-8")
        updated, count = apply_replacements(original)
        if count:
            total_files += 1
            total_replacements += count
            rel = path.relative_to(ROOT)
            print(f"{rel}: {count}")
            if args.apply:
                path.write_text(updated, encoding="utf-8", newline="\n")

    print(f"files={total_files} replacements={total_replacements} apply={args.apply}")


if __name__ == "__main__":
    main()
