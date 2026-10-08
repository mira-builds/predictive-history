#!/usr/bin/env python3
"""Apply pin-cite for Part IX (civ-51..53) via volume-i-anchors.yaml manifest."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READINESS = ROOT / "docs/routes/volume-i-parts/PART-09-HYBRID-READINESS.md"
MANIFEST_SCRIPT = ROOT / "scripts/part_pin_cite_from_manifest.py"


def update_readiness() -> None:
    if not READINESS.is_file():
        return
    text = READINESS.read_text(encoding="utf-8")
    replacements = [
        (
            "plan_status: phase0_inventory",
            "plan_status: phase3_complete",
        ),
        (
            "**Pin-cite debt:** **Open**",
            "**Pin-cite debt:** **Cleared** (2026-06-10)",
        ),
    ]
    for old, new in replacements:
        if old in text:
            text = text.replace(old, new)
    READINESS.write_text(text, encoding="utf-8")
    print(f"patched: {READINESS.relative_to(ROOT)}")


def main() -> int:
    result = subprocess.run(
        [sys.executable, str(MANIFEST_SCRIPT), "--part", "09"],
        cwd=ROOT,
        check=False,
    )
    if result.returncode == 0:
        update_readiness()
        print("part_ix_pin_cite_prep: done")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
