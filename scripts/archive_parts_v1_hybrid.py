#!/usr/bin/env python3
"""Copy Volume I Part thick files into docs/archive/parts-v1-hybrid/ (read-only archive)."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTS_DIR = ROOT / "book" / "volume-i-civilization" / "parts"
ARCHIVE_DIR = ROOT / "docs" / "archive" / "parts-v1-hybrid"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not PARTS_DIR.exists():
        print(f"ERROR: missing {PARTS_DIR}", flush=True)
        return 1

    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    patterns = [
        "part-*-commentary.md",
        "part-*-bibliography.md",
        "PART-*-HYBRID*.md",
        "part-*.md",
    ]
    copied = 0
    for pattern in patterns:
        for path in sorted(PARTS_DIR.glob(pattern)):
            if path.name == "README.md":
                continue
            dest = ARCHIVE_DIR / path.name
            if args.dry_run:
                print(f"would copy {path.relative_to(ROOT)} -> {dest.relative_to(ROOT)}")
            else:
                shutil.copy2(path, dest)
                print(f"copied {path.name}")
            copied += 1

    readme_stub = ARCHIVE_DIR / "README.md"
    stub_text = (
        "# Parts v1 hybrid archive\n\n"
        "Frozen copies of Volume I Part apparatus files. "
        "Authority moved to chapter-only commentaries per "
        "[parts-v1-hybrid.md](../parts-v1-hybrid.md).\n"
    )
    if not args.dry_run:
        readme_stub.write_text(stub_text, encoding="utf-8")
    print(f"{'would archive' if args.dry_run else 'archived'} {copied} files under {ARCHIVE_DIR.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
