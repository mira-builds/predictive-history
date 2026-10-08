#!/usr/bin/env python3
"""Sweep repo-relative ph-civ/ph-apo compat path prose after stub tree deletion.

    python scripts/migrate_ph_compat_paths.py --dry-run
    python scripts/migrate_ph_compat_paths.py
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", "node_modules", "runtime", ".codex-tmp"}
SKIP_FILES = {"migrate_ph_compat_paths.py", "relocate_lectures_to_series.py"}
EXTENSIONS = {".md", ".json", ".jsonl", ".yaml", ".yml", ".py", ".txt"}

REPLACEMENTS: list[tuple[str, str]] = [
    (
        "Compat chapter stubs may remain under `ph-civ/chapters/` and `ph-apo/chapters/`.",
        "Legacy `ph-civ/` and `ph-apo/` namespaces are tombstone-only; see "
        "`docs/archive/deprecated-reader-namespaces.md`.",
    ),
    (
        "Legacy `book/volume-*` and `ph-civ`/`ph-apo` chapter paths are compat redirect stubs.",
        "Legacy `book/volume-*` paths are compat redirect stubs; `ph-civ/` and `ph-apo/` are tombstone-only.",
    ),
    (
        "source-bounded chapter bodies under `book/`, `ph-civ/chapters/`, or\n  `ph-apo/chapters/`",
        "source-bounded chapter bodies under root corpora (`lectures/`, `essays/`, `interviews/`)",
    ),
    (
        "Return through the direct ph-apo chapter path, commentary canvas, public card, and lecture transcript.",
        "Return through the lectures packet path, commentary canvas, public card, and lecture transcript.",
    ),
    (
        "This namespace keeps **compat redirect stubs** at `ph-civ/chapters/gt-*` for older public links.",
        "Redirect stubs under `ph-civ/chapters/` were removed; use `lectures/game-theory/gt-*`.",
    ),
    (
        "This namespace keeps **compat redirect stubs** at `ph-apo/chapters/gt-*` for older public links.",
        "Redirect stubs under `ph-apo/chapters/` were removed; use `lectures/game-theory/gt-*`.",
    ),
]


def should_scan(path: Path) -> bool:
    if any(part in SKIP_DIRS for part in path.parts):
        return False
    if path.name in SKIP_FILES:
        return False
    if path.suffix not in EXTENSIONS:
        return False
    if path.parts[0] in {"ph-civ", "ph-apo"} and path.name != "README.md":
        return False
    return True


def rewrite_text(text: str) -> str:
    patched = text
    for old, new in REPLACEMENTS:
        patched = patched.replace(old, new)
    patched = re.sub(
        r"\(\+\s*ph-civ/chapters redirect stubs\)",
        "",
        patched,
    )
    patched = re.sub(
        r"\(\+\s*ph-apo/chapters redirect stubs\)",
        "",
        patched,
    )
    patched = patched.replace(
        "lectures/* · ph-civ/chapters/* · ph-apo/chapters/*",
        "lectures/*",
    )
    return patched


def main() -> int:
    parser = argparse.ArgumentParser(description="Sweep ph-civ/ph-apo compat path prose")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    changed = 0
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or not should_scan(path):
            continue
        text = path.read_text(encoding="utf-8")
        if "ph-civ" not in text and "ph-apo" not in text:
            continue
        patched = rewrite_text(text)
        if patched == text:
            continue
        changed += 1
        rel = path.relative_to(ROOT).as_posix()
        print(f"patch {rel}")
        if not args.dry_run:
            path.write_text(patched, encoding="utf-8", newline="\n")
    print(f"{'would patch' if args.dry_run else 'patched'} {changed} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
