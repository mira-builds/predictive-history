#!/usr/bin/env python3
"""Rename essay source_ids and paths: sub-01..sub-37 -> essay-01..essay-37."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPPING = {f"sub-{n:02d}": f"essay-{n:02d}" for n in range(1, 38)}
OLD_IDS = sorted(MAPPING, key=lambda s: int(s.split("-")[1]), reverse=True)


def replace_ids(text: str) -> str:
    for old, new in ((o, MAPPING[o]) for o in OLD_IDS):
        text = text.replace(old, new)
    return text


def rename_essay_packet(old_id: str, new_id: str) -> None:
    src_dir = ROOT / "essays" / old_id
    dst_dir = ROOT / "essays" / new_id
    if not src_dir.is_dir():
        raise SystemExit(f"missing essay dir: {src_dir}")
    if dst_dir.exists():
        raise SystemExit(f"target already exists: {dst_dir}")

    dst_dir.mkdir(parents=True)
    for path in sorted(src_dir.iterdir()):
        if path.name.startswith(f"{old_id}-"):
            new_name = path.name.replace(old_id, new_id, 1)
        else:
            new_name = path.name
        shutil.move(str(path), str(dst_dir / new_name))

    for path in dst_dir.iterdir():
        if path.is_file() and path.suffix in {".md", ".yaml", ".yml"}:
            path.write_text(replace_ids(path.read_text(encoding="utf-8")), encoding="utf-8", newline="\n")

    src_dir.rmdir()


def rename_card(old_id: str, new_id: str) -> None:
    src = ROOT / "data" / "cards" / f"{old_id}.md"
    dst = ROOT / "data" / "cards" / f"{new_id}.md"
    if not src.is_file():
        raise SystemExit(f"missing card: {src}")
    dst.write_text(replace_ids(src.read_text(encoding="utf-8")), encoding="utf-8", newline="\n")
    src.unlink()


def rename_legacy_stub(base: Path, old_id: str, new_id: str) -> None:
    src = base / old_id
    dst = base / new_id
    if not src.is_dir():
        return
    if dst.exists():
        shutil.rmtree(dst)
    shutil.move(str(src), str(dst))
    readme = dst / "README.md"
    if readme.is_file():
        readme.write_text(replace_ids(readme.read_text(encoding="utf-8")), encoding="utf-8", newline="\n")


def update_cards_jsonl() -> None:
    path = ROOT / "data" / "cards.jsonl"
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        card = json.loads(line)
        sid = card.get("source_id", "")
        if sid in MAPPING:
            card = json.loads(replace_ids(json.dumps(card, ensure_ascii=False)))
        out.append(json.dumps(card, ensure_ascii=False))
    path.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")


def patch_tree_text_files() -> None:
    skip_dirs = {".git", "__pycache__", ".pytest_cache"}
    skip_files = {"rename_essays_sub_to_essay.py"}
    for path in ROOT.rglob("*"):
        if any(part in skip_dirs for part in path.parts):
            continue
        if not path.is_file():
            continue
        if path.name in skip_files:
            continue
        if path.suffix not in {".md", ".json", ".jsonl", ".yaml", ".yml", ".py", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8")
        patched = replace_ids(text)
        if patched != text:
            path.write_text(patched, encoding="utf-8", newline="\n")


def sync_index_json() -> None:
    jsonl = [
        json.loads(line)
        for line in (ROOT / "data/cards.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    idx_path = ROOT / "data/index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    review = {c["source_id"]: c.get("review_status", "in_review") for c in idx.get("cards", [])}
    idx["cards"] = [
        {
            "part": c["part"],
            "path": f"data/cards/{c['source_id']}.md",
            "placement_weight": c.get("placement_weight", "strong"),
            "review_status": review.get(c["source_id"], c.get("review_status", "in_review")),
            "series": c["series"],
            "source_id": c["source_id"],
            "title": c["title"],
        }
        for c in jsonl
    ]
    idx["card_count"] = len(jsonl)
    idx_path.write_text(json.dumps(idx, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    for old_id in sorted(MAPPING, key=lambda s: int(s.split("-")[1])):
        new_id = MAPPING[old_id]
        rename_essay_packet(old_id, new_id)
        rename_card(old_id, new_id)
        rename_legacy_stub(ROOT / "book/volume-vii", old_id, new_id)
        rename_legacy_stub(ROOT / "lectures/sub", old_id, new_id)

    update_cards_jsonl()
    patch_tree_text_files()
    sync_index_json()
    print("renamed", len(MAPPING), "essays sub-* -> essay-*")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
