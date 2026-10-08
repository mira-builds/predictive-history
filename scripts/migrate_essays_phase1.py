#!/usr/bin/env python3
"""Phase 1: move public essay-2026-04-04-world-war-trump..essay-2026-05-16-chinas-third-center-strategy essay packets to repo-root essays/."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_IDS = ["essay-2026-04-04-world-war-trump", "essay-2026-04-18-the-us-iran-war-round-two", "essay-2026-04-25-the-trump-new-deal", "essay-2026-05-01-god-emperor-trump", "essay-2026-05-16-chinas-third-center-strategy"]
LEGACY_PREFIX = "book/volume-vii"
NEW_PREFIX = "essays"


def patch_yaml_part(text: str) -> str:
    text = re.sub(r"^part:\s*world-war\s*$", "part: civilization", text, flags=re.M)
    text = re.sub(r'^part_role:\s*world-war\s*$', "part_role: civilization", text, flags=re.M)
    text = re.sub(r'^part:\s*"world-war"\s*$', 'part: "civilization"', text, flags=re.M)
    text = re.sub(r'^part_role:\s*"world-war"\s*$', 'part_role: "civilization"', text, flags=re.M)
    return text


def patch_paths(text: str, source_id: str) -> str:
    old = f"{LEGACY_PREFIX}/{source_id}"
    new = f"{NEW_PREFIX}/{source_id}"
    return text.replace(old, new)


def legacy_stub(source_id: str, title: str) -> str:
    return f"""# {title} (`{source_id}`)

**Moved.** Canonical essay packet: [`essays/{source_id}/`](../../../essays/{source_id}/README.md).

Legacy provenance path `{LEGACY_PREFIX}/{source_id}/` — do not edit transcript or commentary here.
"""


def rollup_stub(source_id: str, title: str) -> str:
    return f"""# {title}

Staged rollup pointer for `{source_id}`. **Canonical packet:** [`essays/{source_id}/`](../../../../essays/{source_id}/README.md).

During essay recategorization, Substack chapters live at repo-root [`essays/`](../../../../essays/README.md) (`part: civilization`, surface `ph-civ`).
"""


def migrate_chapter(source_id: str) -> None:
    legacy_dir = ROOT / LEGACY_PREFIX / source_id
    target_dir = ROOT / NEW_PREFIX / source_id
    if not legacy_dir.is_dir():
        raise SystemExit(f"missing legacy dir: {legacy_dir}")
    target_dir.parent.mkdir(parents=True, exist_ok=True)
    if target_dir.exists():
        shutil.rmtree(target_dir)
    shutil.move(str(legacy_dir), str(target_dir))

    title = source_id
    for name in ("transcript", "commentary"):
        path = target_dir / f"{source_id}-{name}.md"
        if path.exists():
            text = patch_paths(patch_yaml_part(path.read_text(encoding="utf-8")), source_id)
            path.write_text(text, encoding="utf-8", newline="\n")

    readme = target_dir / "README.md"
    if readme.exists():
        text = readme.read_text(encoding="utf-8")
        text = text.replace("../../../data/cards/", "../../data/cards/")
        readme.write_text(text, encoding="utf-8", newline="\n")
        m = re.search(r"^# (.+)$", text, re.M)
        if m:
            title = m.group(1).strip()

    stub_dir = ROOT / LEGACY_PREFIX / source_id
    stub_dir.mkdir(parents=True, exist_ok=True)
    (stub_dir / "README.md").write_text(legacy_stub(source_id, title), encoding="utf-8", newline="\n")

    rollup = ROOT / "lectures/sub" / source_id / "README.md"
    if rollup.parent.exists() or rollup.parent.parent.exists():
        rollup.parent.mkdir(parents=True, exist_ok=True)
        rollup.write_text(rollup_stub(source_id, title), encoding="utf-8", newline="\n")


def update_cards_jsonl() -> None:
    path = ROOT / "data/cards.jsonl"
    lines = path.read_text(encoding="utf-8").splitlines()
    out = []
    for line in lines:
        if not line.strip():
            continue
        card = json.loads(line)
        sid = card.get("source_id")
        if sid not in SOURCE_IDS:
            out.append(line)
            continue
        card["part"] = "civilization"
        sp = card.setdefault("source_paths", {})
        for key in list(sp):
            if isinstance(sp[key], str):
                sp[key] = patch_paths(sp[key], sid)
        sections = card.get("sections", {})
        if "Return Path" in sections:
            sections["Return Path"] = (
                f"Return through `essays/{sid}/`, the commentary canvas, and "
                f"`essays/{sid}/{sid}-transcript.md`. Legacy `book/volume-vii/` paths are redirects only."
            )
        card["sections"] = sections
        out.append(json.dumps(card, ensure_ascii=False))
    path.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")


def update_card_md(source_id: str) -> None:
    path = ROOT / "data/cards" / f"{source_id}.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    text = patch_yaml_part(text)
    text = re.sub(r"^part:\s*world-war\s*$", "part: civilization", text, flags=re.M)
    text = patch_paths(text, source_id)
    text = text.replace("ph-apo", "ph-civ")
    text = text.replace(
        f"Return through book/volume-vii/{source_id}/",
        f"Return through essays/{source_id}/",
    )
    path.write_text(text, encoding="utf-8", newline="\n")


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
    for sid in SOURCE_IDS:
        migrate_chapter(sid)
        update_card_md(sid)
    update_cards_jsonl()
    sync_index_json()
    print("migrated", ", ".join(SOURCE_IDS), "-> essays/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
