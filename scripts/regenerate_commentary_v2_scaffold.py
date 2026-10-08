#!/usr/bin/env python3
"""Regenerate or upgrade chapter commentaries to v2 scaffold (tiered waves)."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from civ_ph.commentary_v2 import (  # noqa: E402
    SCAFFOLD_VERSION_V2,
    markdown_frontmatter,
    render_v2_scaffold_body,
)
from civ_ph.data import load_cards  # noqa: E402

WAVE_SERIES = {
    "civ": {"civilization"},
    "gb": {"great-books"},
    "gt": {"game-theory"},
    "apo": {"geo-strategy", "game-theory", "secret-history", "essays"},
    "seed": None,
}


def merge_frontmatter(existing: str, updates: dict[str, str]) -> str:
    if not existing.startswith("---\n"):
        lines = ["---"]
        for key, value in updates.items():
            lines.append(f'{key}: {value}')
        lines.append("---\n")
        return "\n".join(lines)
    end = existing.find("\n---\n", 4)
    body = existing[end + 5 :] if end != -1 else ""
    fm = markdown_frontmatter(existing)
    fm.update(updates)
    lines = ["---"]
    for key, value in fm.items():
        if key in updates or key in {
            "source_id",
            "title",
            "commentary_status",
            "canvas_status",
            "analysis_depth",
            "representation_not_endorsement",
        }:
            lines.append(f"{key}: {value}")
    for key, value in fm.items():
        if key not in {line.split(":")[0] for line in lines[1:]}:
            lines.append(f"{key}: {value}")
    lines.append("---\n")
    return "\n".join(lines) + body


def strip_part_apparatus(text: str) -> str:
    text = re.sub(
        r"\n## Part apparatus[\s\S]*?(?=\n## Project Canvas|\Z)",
        "\n",
        text,
    )
    return text


def upgrade_in_place(path: Path, card: dict, wipe: bool) -> bool:
    title = card.get("title", path.stem)
    source_id = card["source_id"]
    transcript_name = f"{source_id}-transcript.md"
    existing = path.read_text(encoding="utf-8")
    fm = markdown_frontmatter(existing)
    updates = {
        "scaffold_version": SCAFFOLD_VERSION_V2,
        "commentary_maturity": fm.get("commentary_maturity") or "scaffold",
        "migration_source": "regen" if wipe else "upgrade",
    }
    if wipe:
        header = merge_frontmatter(existing, {**fm, **updates})
        body = render_v2_scaffold_body(source_id, title, transcript_name)
        path.write_text(header + body, encoding="utf-8")
        return True
    if fm.get("scaffold_version") == SCAFFOLD_VERSION_V2 and "## Layer 3" in existing:
        return False
    body = existing.split("---", 2)[-1] if existing.startswith("---") else existing
    if "## Part apparatus" in body:
        body = strip_part_apparatus(body)
    if "## Layer 3" not in body and "## Layer 2" in body:
        insert = """

---

## Layer 3 - Predictions & Falsifiers

| Prediction | Strength | Falsifier Criteria | Review Date | Current Status | Notes |
|------------|----------|-------------------|-------------|----------------|-------|
| TBD | C | TBD | TBD | Pending | Upgrade wave — populate from Part extract or lecture |

---

## Layer 4 - Counter-Readings

| Topic | Counter-reading | Strength |
|-------|-----------------|----------|
| TBD | TBD | Low |

---

## Layer 5 - Synthesis & Cross-Volume Links

| pattern_id | How this chapter supports or limits it |
|------------|----------------------------------------|
| TBD | TBD |

---

## Layer 6 - Open Issues

- v2 upgrade wave; remove Part-only claims after extract pass.

"""
        anchor = "## Project Canvas"
        body = body.replace(anchor, insert + "\n" + anchor, 1) if anchor in body else body.rstrip() + insert
    merged_fm = {**fm, **updates}
    merged_fm.pop("part_commentary_path", None)
    merged_fm.pop("part_bibliography_path", None)
    path.write_text(merge_frontmatter(existing, merged_fm) + body, encoding="utf-8")
    return True


def card_matches_wave(card: dict, wave: str) -> bool:
    if wave == "seed":
        return card.get("source_paths", {}) and True
    series = card.get("series", "")
    allowed = WAVE_SERIES.get(wave)
    if allowed is None:
        return False
    return series in allowed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-id", action="append", help="Single chapter (repeatable)")
    parser.add_argument(
        "--wave",
        choices=["civ", "gb", "gt", "apo", "seed"],
        help="Tiered rebuild wave by series",
    )
    parser.add_argument("--wipe-seed", action="store_true", help="Full regen for seed-depth chapters")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not args.source_id and not args.wave:
        parser.error("provide --source-id and/or --wave")

    cards = load_cards()
    by_id = {c["source_id"]: c for c in cards}
    targets: list[dict] = []
    if args.source_id:
        for sid in args.source_id:
            if sid not in by_id:
                print(f"ERROR: unknown source_id {sid}", file=sys.stderr)
                return 1
            targets.append(by_id[sid])
    if args.wave:
        for card in cards:
            if card in targets:
                continue
            if args.wave == "seed":
                rel = card["source_paths"]["commentary_path"]
                text = (ROOT / rel).read_text(encoding="utf-8")
                fm = markdown_frontmatter(text)
                if fm.get("analysis_depth") == "seed" and fm.get("scaffold_version") != SCAFFOLD_VERSION_V2:
                    targets.append(card)
            elif card_matches_wave(card, args.wave):
                rel = card["source_paths"]["commentary_path"]
                path = ROOT / rel
                if path.exists():
                    fm = markdown_frontmatter(path.read_text(encoding="utf-8"))
                    if fm.get("scaffold_version") != SCAFFOLD_VERSION_V2:
                        targets.append(card)

    touched = 0
    for card in sorted(targets, key=lambda row: row["source_id"]):
        rel = card["source_paths"]["commentary_path"]
        path = ROOT / rel
        wipe = args.wipe_seed or markdown_frontmatter(
            path.read_text(encoding="utf-8")
        ).get("analysis_depth") == "seed"
        if args.dry_run:
            print(f"would upgrade {card['source_id']} ({rel}) wipe={wipe}")
            touched += 1
            continue
        if upgrade_in_place(path, card, wipe=wipe):
            print(f"upgraded {card['source_id']}")
            touched += 1
    print(f"{'would touch' if args.dry_run else 'touched'} {touched} chapters")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
