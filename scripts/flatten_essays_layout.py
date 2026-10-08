#!/usr/bin/env python3
"""Flatten essays/ subfolders; move commentary canvases to commentaries/.

    python scripts/flatten_essays_layout.py
    PYTHONPATH=src python -m civ_ph.cli index --force
    PYTHONPATH=src python -m civ_ph.cli validate
"""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ESSAY_DIR_RE = re.compile(r"^essay-\d{4}-\d{2}-\d{2}-")
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", "node_modules"}
SKIP_FILES = {"flatten_essays_layout.py"}


def load_essay_source_ids() -> list[str]:
    manifest = ROOT / "data" / "essays" / "manifest.json"
    if manifest.is_file():
        data = json.loads(manifest.read_text(encoding="utf-8"))
        return [e["source_id"] for e in data.get("entries", [])]
    ids = []
    for path in sorted(ROOT.glob("essays/essay-*")):
        if path.is_dir() and ESSAY_DIR_RE.match(path.name):
            ids.append(path.name)
    return ids


def essay_paths(source_id: str) -> tuple[str, str, str, str]:
    old_body = f"essays/{source_id}/{source_id}.md"
    new_body = f"essays/{source_id}.md"
    old_comm = f"essays/{source_id}/{source_id}-commentary.md"
    new_comm = f"commentaries/{source_id}-commentary.md"
    return old_body, new_body, old_comm, new_comm


def rewrite_essay_paths(text: str, source_ids: list[str]) -> str:
    for sid in sorted(source_ids, key=len, reverse=True):
        old_body, new_body, old_comm, new_comm = essay_paths(sid)
        text = text.replace(old_comm, new_comm)
        text = text.replace(old_body, new_body)
        text = text.replace(f"essays/{sid}/README.md", new_body)
        text = text.replace(f"essays/{sid}/", f"essays/{sid}.md")  # trailing folder refs
        text = text.replace(f"`essays/{sid}`", f"`essays/{sid}.md`")
    return text


def write_commentaries_readme() -> None:
    path = ROOT / "commentaries" / "README.md"
    if path.is_file():
        return
    path.write_text(
        """# Commentaries

**Essay commentary canvases** for the Predictive History public corpus.

Repo path: **`commentaries/`** at the repository root (sibling to [`essays/`](../essays/README.md), [`interviews/`](../interviews/README.md), [`lectures/`](../lectures/README.md)).

## Scope (this pass)

- **Essays only:** `commentaries/essay-YYYY-MM-DD-{slug}-commentary.md` pairs with flat [`essays/essay-YYYY-MM-DD-{slug}.md`](../essays/README.md).
- **Lectures / interviews** keep commentary beside their chapter folders under `book/` and `interviews/`.

## Path template

| File | Role |
| --- | --- |
| `commentaries/{source_id}-commentary.md` | Open commentary canvas |
| [`essays/{source_id}.md`](../essays/) | Verbatim essay body |
| [`data/cards/{source_id}.md`](../data/cards/) | Public orientation card |

Registry: [`data/cards.jsonl`](../data/cards.jsonl) · catalog: [`docs/predictive-history-index.md`](../docs/predictive-history-index.md).
""",
        encoding="utf-8",
        newline="\n",
    )


def flatten_packet(source_id: str) -> None:
    src_dir = ROOT / "essays" / source_id
    if not src_dir.is_dir():
        return
    body_src = src_dir / f"{source_id}.md"
    comm_src = src_dir / f"{source_id}-commentary.md"
    body_dst = ROOT / "essays" / f"{source_id}.md"
    comm_dst = ROOT / "commentaries" / f"{source_id}-commentary.md"
    if not body_src.is_file():
        raise SystemExit(f"missing essay body: {body_src}")
    if not comm_src.is_file():
        raise SystemExit(f"missing commentary: {comm_src}")
    if body_dst.exists() or comm_dst.exists():
        raise SystemExit(f"flat target already exists: {body_dst} or {comm_dst}")
    shutil.move(str(body_src), str(body_dst))
    shutil.move(str(comm_src), str(comm_dst))
    readme = src_dir / "README.md"
    if readme.is_file():
        readme.unlink()
    src_dir.rmdir()


def update_cards_jsonl(source_ids: list[str]) -> None:
    path = ROOT / "data" / "cards.jsonl"
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        card = json.loads(line)
        if card.get("series") == "essays":
            card = json.loads(rewrite_essay_paths(json.dumps(card, ensure_ascii=False), source_ids))
        out.append(json.dumps(card, ensure_ascii=False))
    path.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")


def patch_tree(source_ids: list[str]) -> None:
    skip_roots = {
        (ROOT / "essays" / "README.md").resolve(),
        (ROOT / "commentaries" / "README.md").resolve(),
    }
    for path in ROOT.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if not path.is_file():
            continue
        if path.name in SKIP_FILES:
            continue
        if path.resolve() in skip_roots:
            continue
        if path.suffix not in {".md", ".json", ".jsonl", ".yaml", ".yml", ".py", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8")
        if not any(f"essays/{sid}/" in text or f"essays/{sid}/{sid}" in text for sid in source_ids):
            continue
        patched = rewrite_essay_paths(text, source_ids)
        if patched != text:
            path.write_text(patched, encoding="utf-8", newline="\n")


def main() -> int:
    source_ids = load_essay_source_ids()
    if len(source_ids) != 43:
        raise SystemExit(f"expected 43 essay source_ids, found {len(source_ids)}")
    (ROOT / "commentaries").mkdir(exist_ok=True)
    write_commentaries_readme()
    moved = 0
    for source_id in source_ids:
        src_dir = ROOT / "essays" / source_id
        if src_dir.is_dir():
            flatten_packet(source_id)
            moved += 1
    if moved == 0:
        print("no essay subfolders to flatten (already flat?)")
    else:
        print(f"flattened {moved} essay packets")
    update_cards_jsonl(source_ids)
    patch_tree(source_ids)
    remaining = sum(1 for p in ROOT.glob("essays/essay-*") if p.is_dir() and ESSAY_DIR_RE.match(p.name))
    if remaining:
        raise SystemExit(f"{remaining} essay subfolders remain")
    print("path rewrite complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
