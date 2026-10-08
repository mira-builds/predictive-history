#!/usr/bin/env python3
"""Migrate essay-NN -> essay-YYYY-MM-DD-{substack_slug} (interview parity).

    python scripts/rename_essays_to_dated_ids.py
    PYTHONPATH=src python -m civ_ph.cli index --force
    PYTHONPATH=src python -m civ_ph.cli validate

Hard cut: legacy essay-NN IDs live only in data/essays/manifest.json crosswalk.
"""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEGACY_RE = re.compile(r"^essay-\d{2}$")
LEGACY_ID_RE = re.compile(r"(?<![0-9])essay-(\d{2})(?![0-9])")
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", "node_modules"}
SKIP_FILES = {
    "rename_essays_to_dated_ids.py",
    "rename_essays_sub_to_essay.py",
}


def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    import yaml

    return yaml.safe_load(parts[1]) or {}


def dated_essay_id(publication_date: str, substack_slug: str) -> str:
    pub = str(publication_date)[:10]
    slug = substack_slug.strip()
    if not pub or not slug:
        raise ValueError(f"missing publication_date or substack_slug for slug={slug!r} date={pub!r}")
    return f"essay-{pub}-{slug}"


def build_mapping() -> dict[str, str]:
    mapping: dict[str, str] = {}
    for essay_dir in sorted(ROOT.glob("essays/essay-*")):
        if not essay_dir.is_dir():
            continue
        old_id = essay_dir.name
        if not LEGACY_RE.match(old_id):
            continue
        md_path = essay_dir / f"{old_id}.md"
        if not md_path.is_file():
            raise SystemExit(f"missing transcript: {md_path}")
        meta = parse_frontmatter(md_path.read_text(encoding="utf-8"))
        pub = str(meta.get("publication_date", ""))[:10]
        slug = str(meta.get("substack_slug", "")).strip()
        if not slug:
            raise SystemExit(f"missing substack_slug in {md_path}")
        new_id = dated_essay_id(pub, slug)
        if new_id in mapping.values():
            raise SystemExit(f"dated id collision: {new_id}")
        mapping[old_id] = new_id
    if len(mapping) != 43:
        raise SystemExit(f"expected 43 legacy essays, found {len(mapping)}")
    return mapping


def build_manifest_entries(mapping: dict[str, str]) -> list[dict]:
    entries: list[dict] = []
    for old_id in sorted(mapping, key=lambda s: int(s.split("-")[1])):
        new_id = mapping[old_id]
        md_path = ROOT / "essays" / old_id / f"{old_id}.md"
        meta = parse_frontmatter(md_path.read_text(encoding="utf-8"))
        num = int(old_id.split("-")[1])
        entry = {
            "legacy_source_id": old_id,
            "source_id": new_id,
            "publication_date": str(meta.get("publication_date", ""))[:10],
            "substack_slug": str(meta.get("substack_slug", "")).strip(),
            "title": meta.get("title", ""),
        }
        if num <= 32:
            entry["workshop_source_id"] = f"es-{num:02d}"
        entries.append(entry)
    return entries


def write_manifest(mapping: dict[str, str]) -> Path:
    manifest_dir = ROOT / "data" / "essays"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    path = manifest_dir / "manifest.json"
    payload = {
        "schema_version": 1,
        "description": (
            "Pinned public essay IDs. Canonical source_id is essay-YYYY-MM-DD-{substack_slug}; "
            "legacy_source_id essay-NN and workshop es-NN are crosswalk only."
        ),
        "disambiguation": (
            "If two essays share publication_date, append -2 or a title fragment to substack_slug "
            "before assigning source_id."
        ),
        "entries": build_manifest_entries(mapping),
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def replace_ids(text: str, mapping: dict[str, str]) -> str:
    """Replace legacy essay-NN tokens without touching essay-YYYY-MM-DD dated ids."""

    def _sub(match: re.Match[str]) -> str:
        old_id = f"essay-{match.group(1)}"
        return mapping.get(old_id, match.group(0))

    return LEGACY_ID_RE.sub(_sub, text)


def rename_essay_packet(old_id: str, new_id: str) -> None:
    src_dir = ROOT / "essays" / old_id
    dst_dir = ROOT / "essays" / new_id
    if not src_dir.is_dir():
        raise SystemExit(f"missing essay dir: {src_dir}")
    if dst_dir.exists():
        raise SystemExit(f"target already exists: {dst_dir}")

    dst_dir.mkdir(parents=True)
    pair = {old_id: new_id}
    for path in sorted(src_dir.iterdir()):
        if path.name.startswith(f"{old_id}-"):
            new_name = path.name.replace(old_id, new_id, 1)
        elif path.name == f"{old_id}.md":
            new_name = f"{new_id}.md"
        else:
            new_name = path.name
        shutil.move(str(path), str(dst_dir / new_name))

    for path in dst_dir.iterdir():
        if path.is_file() and path.suffix in {".md", ".yaml", ".yml"}:
            path.write_text(
                replace_ids(path.read_text(encoding="utf-8"), pair),
                encoding="utf-8",
                newline="\n",
            )
    src_dir.rmdir()


def rename_card(old_id: str, new_id: str, mapping: dict[str, str]) -> None:
    src = ROOT / "data" / "cards" / f"{old_id}.md"
    dst = ROOT / "data" / "cards" / f"{new_id}.md"
    if not src.is_file():
        raise SystemExit(f"missing card: {src}")
    dst.write_text(replace_ids(src.read_text(encoding="utf-8"), mapping), encoding="utf-8", newline="\n")
    src.unlink()


def rename_legacy_stub(base: Path, old_id: str, new_id: str, mapping: dict[str, str]) -> None:
    src = base / old_id
    dst = base / new_id
    if not src.is_dir():
        return
    if dst.exists():
        shutil.rmtree(dst)
    shutil.move(str(src), str(dst))
    readme = dst / "README.md"
    if readme.is_file():
        readme.write_text(
            replace_ids(readme.read_text(encoding="utf-8"), mapping),
            encoding="utf-8",
            newline="\n",
        )


def update_cards_jsonl(mapping: dict[str, str]) -> None:
    path = ROOT / "data" / "cards.jsonl"
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        card = json.loads(line)
        sid = card.get("source_id", "")
        if sid in mapping:
            card["source_id"] = mapping[sid]
            card = json.loads(replace_ids(json.dumps(card, ensure_ascii=False), mapping))
        out.append(json.dumps(card, ensure_ascii=False))
    path.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")


def patch_tree_text_files(mapping: dict[str, str]) -> None:
    manifest_path = (ROOT / "data" / "essays" / "manifest.json").resolve()
    skip_roots = {
        (ROOT / "essays").resolve(),
        (ROOT / "data" / "cards").resolve(),
        (ROOT / "data" / "cards.jsonl").resolve(),
    }
    for path in ROOT.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if not path.is_file():
            continue
        if path.name in SKIP_FILES:
            continue
        resolved = path.resolve()
        if resolved == manifest_path:
            continue
        if resolved in skip_roots:
            continue
        if resolved.parent.resolve() in skip_roots:
            continue
        if path.suffix not in {".md", ".json", ".jsonl", ".yaml", ".yml", ".py", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8")
        patched = replace_ids(text, mapping)
        if patched != text:
            path.write_text(patched, encoding="utf-8", newline="\n")


def sync_index_json() -> None:
    """Optional: data/index.json is regenerated by `predictive-history index --force`."""
    idx_path = ROOT / "data/index.json"
    if not idx_path.is_file():
        return
    jsonl = [
        json.loads(line)
        for line in (ROOT / "data/cards.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
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
    mapping = build_mapping()
    manifest_path = write_manifest(mapping)
    print(f"wrote {manifest_path} ({len(mapping)} entries)")

    for old_id in sorted(mapping, key=lambda s: int(s.split("-")[1]), reverse=True):
        new_id = mapping[old_id]
        rename_essay_packet(old_id, new_id)
        rename_card(old_id, new_id, {old_id: new_id})
        rename_legacy_stub(ROOT / "book/volume-vii", old_id, new_id, mapping)
        rename_legacy_stub(ROOT / "lectures/sub", old_id, new_id, mapping)

    update_cards_jsonl(mapping)
    patch_tree_text_files(mapping)
    sync_index_json()
    print(f"renamed {len(mapping)} essays essay-NN -> dated source_id")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
