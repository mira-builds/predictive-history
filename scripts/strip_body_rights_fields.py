#!/usr/bin/env python3
"""Remove transcript body-rights YAML from chapter frontmatter and site JSON."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

STATUS_REPLACEMENTS = {
    "curated_transcript_pending_rights_review": "curated_transcript",
    "public_transcript_pending_rights_review": "public_transcript",
}

BODY_RIGHTS_LINE = re.compile(
    r"^rights_(?:review(?:ed_at)?|note)\s*:.*(?:\n|$)", re.MULTILINE
)

SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", "node_modules"}


def normalize_transcript_status(value: str) -> str:
    return STATUS_REPLACEMENTS.get(value, value)


def strip_markdown_frontmatter(text: str) -> tuple[str, bool]:
    if not text.startswith("---\n"):
        return text, False
    end = text.find("\n---\n", 4)
    if end == -1:
        return text, False
    fm = text[4:end]
    body = text[end + 5 :]
    original_fm = fm
    fm = BODY_RIGHTS_LINE.sub("", fm)
    for old, new in STATUS_REPLACEMENTS.items():
        fm = fm.replace(old, new)
    if fm == original_fm:
        return text, False
    fm = fm.rstrip("\n") + "\n"
    return f"---\n{fm}---\n{body}", True


def strip_json_transcript_status(path: Path) -> bool:
    data = json.loads(path.read_text(encoding="utf-8"))
    status = data.get("transcript_status")
    if not isinstance(status, str):
        return False
    new_status = normalize_transcript_status(status)
    if new_status == status and "rights_review" not in data and "rights_note" not in data:
        return False
    data.pop("rights_review", None)
    data.pop("rights_reviewed_at", None)
    data.pop("rights_note", None)
    if new_status != status:
        data["transcript_status"] = new_status
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return True


def strip_text_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".json" and path.parent.name == "chapters":
        return strip_json_transcript_status(path)
    new_text, changed = strip_markdown_frontmatter(text)
    if not changed:
        original = text
        for old, new in STATUS_REPLACEMENTS.items():
            text = text.replace(old, new)
        text = BODY_RIGHTS_LINE.sub("", text)
        changed = text != original
        new_text = text
    if changed:
        path.write_text(new_text, encoding="utf-8")
    return changed


def main() -> int:
    changed = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix not in {".md", ".json"}:
            continue
        if path.name.endswith("-media.yaml") or path.suffix == ".yaml":
            continue
        if path.suffix == ".json" and "site/_data/chapters" not in path.as_posix():
            continue
        if strip_text_file(path):
            changed += 1
            print(path.relative_to(ROOT))
    print(f"updated {changed} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
