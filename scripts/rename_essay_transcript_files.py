#!/usr/bin/env python3
"""Rename essay-*-transcript.md -> essay-NN.md and update references."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", "node_modules"}
OLD_SUFFIX = re.compile(r"(essays/essay-\d{2}/)essay-(\d{2})-transcript\.md")
NEW_PATH = r"\1essay-\2.md"
GLOBAL_OLD = re.compile(r"essay-(\d{2})-transcript\.md")
GLOBAL_NEW = r"essay-\1.md"


def rename_files() -> list[Path]:
    renamed: list[Path] = []
    for old in sorted(ROOT.glob("essays/essay-*/essay-*-transcript.md")):
        source_id = old.stem.replace("-transcript", "")
        new = old.with_name(f"{source_id}.md")
        if new.exists():
            raise SystemExit(f"target exists: {new}")
        old.rename(new)
        renamed.append(new)
    return renamed


def patch_text(text: str) -> str:
    text = OLD_SUFFIX.sub(NEW_PATH, text)
    text = GLOBAL_OLD.sub(GLOBAL_NEW, text)
    return text


def patch_repo() -> int:
    changed = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(p in SKIP_DIRS for p in path.parts):
            continue
        if path.suffix.lower() not in {".md", ".json", ".jsonl", ".py", ".txt", ".yaml", ".yml"}:
            continue
        if path.name == Path(__file__).name:
            continue
        try:
            original = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        updated = patch_text(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    return changed


def main() -> int:
    renamed = rename_files()
    print(f"renamed {len(renamed)} essay body files")
    n = patch_repo()
    print(f"patched {n} reference files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
