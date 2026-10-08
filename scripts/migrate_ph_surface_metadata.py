#!/usr/bin/env python3
"""Migrate ph-civ/ph-apo surface metadata to predictive-history identity.

    python scripts/migrate_ph_surface_metadata.py --dry-run
    python scripts/migrate_ph_surface_metadata.py
    PYTHONPATH=src python -m civ_ph.cli index --force
    PYTHONPATH=src python -m civ_ph.cli validate
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CARD_MD_REPLACEMENTS: list[tuple[str, str]] = [
    (
        " sits on the ph-civ essays surface (`part: civilization`).",
        " sits in the public essays namespace (`part: civilization`, legacy two-volume metadata).",
    ),
    (
        " carries the public `ph-civ` essay lane into",
        " carries the public essays namespace into",
    ),
    (
        " extends the public `ph-civ` essay lane into",
        " extends the public essays namespace into",
    ),
    (
        " continues the first public `ph-civ` essay arc at",
        " continues the first public essays arc at",
    ),
    (
        " belongs to the first public `ph-civ` essay arc where",
        " belongs to the first public essays arc where",
    ),
    (
        "This chapter belongs in Volume I because",
        "This chapter belongs in the civilization series (legacy Volume I metadata) because",
    ),
    (
        "This chapter belongs in Volume II because",
        "This chapter belongs in the world-war part metadata (legacy Volume II framing) because",
    ),
]


def migrate_cards_jsonl(*, dry_run: bool) -> int:
    path = ROOT / "data" / "cards.jsonl"
    lines_out: list[str] = []
    changed = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        card = json.loads(line)
        corpus = card.get("derived_corpus")
        if corpus == "ph-civ":
            card["derived_corpus"] = "predictive-history"
            changed += 1
        lines_out.append(json.dumps(card, ensure_ascii=False))
    if changed and not dry_run:
        path.write_text("\n".join(lines_out) + "\n", encoding="utf-8", newline="\n")
    return changed


def migrate_card_markdown(*, dry_run: bool) -> int:
    changed = 0
    cards_dir = ROOT / "data" / "cards"
    for path in sorted(cards_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        patched = text
        for old, new in CARD_MD_REPLACEMENTS:
            patched = patched.replace(old, new)
        if patched != text:
            changed += 1
            if not dry_run:
                path.write_text(patched, encoding="utf-8", newline="\n")
    return changed


def _replace_upstream_ph_civ(obj: object) -> object:
    if isinstance(obj, dict):
        out = {}
        for key, value in obj.items():
            if key in {"canonical_source", "upstream_source"} and value == "ph-civ":
                out[key] = "predictive-history"
            elif key == "surface" and value == "ph-civ" and "locale" not in obj:
                out[key] = "predictive-history"
            else:
                out[key] = _replace_upstream_ph_civ(value)
        return out
    if isinstance(obj, list):
        return [_replace_upstream_ph_civ(item) for item in obj]
    if isinstance(obj, str):
        return (
            obj.replace("canonical English ph-civ", "canonical English predictive-history")
            .replace("canonical `ph-civ`", "canonical `predictive-history`")
            .replace("downstream of `ph-civ`", "downstream of `predictive-history`")
            .replace("downstream of ph-civ", "downstream of predictive-history")
            .replace("upstream public artifact and source of truth; ph-civ-zh", "upstream public artifact; ph-civ-zh")
            .replace("ph-civ is the upstream public artifact and source of truth", "predictive-history is the upstream public artifact and source of truth")
            .replace("ph-civ is an LLM-native trilingual", "predictive-history is an LLM-native trilingual")
            .replace("ph-civ-ru commands", "predictive-history localization commands")
        )
    return obj


def migrate_bilingual_loop(*, dry_run: bool) -> bool:
    path = ROOT / "data" / "bilingual-loop.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    original = json.dumps(payload, sort_keys=True)
    payload["canonical_source"] = "predictive-history"
    canonical_surface = payload.get("canonical_language_surface", {})
    if canonical_surface.get("surface") == "ph-civ":
        canonical_surface["surface"] = "predictive-history"
    for key in ("future_zh_wedge", "future_ru_wedge"):
        wedge = payload.get(key, {})
        if wedge.get("upstream_source") == "ph-civ":
            wedge["upstream_source"] = "predictive-history"
    for item in payload.get("localization_roadmap", []):
        if item.get("upstream_source") == "ph-civ":
            item["upstream_source"] = "predictive-history"
    authority = payload.get("authority_model", "")
    payload["authority_model"] = (
        authority.replace("ph-civ is the upstream public artifact and source of truth", "predictive-history is the upstream public artifact and source of truth")
        .replace("ph-civ is the upstream public artifact", "predictive-history is the upstream public artifact and source of truth")
        .replace("from ph-civ.", "from predictive-history.")
        .replace("status from ph-civ", "status from predictive-history")
    )
    defer = payload.get("future_ru_wedge", {}).get("defer", "")
    if "ph-civ-ru commands" in defer:
        payload["future_ru_wedge"]["defer"] = defer.replace(
            "ph-civ-ru commands",
            "predictive-history localization commands",
        )
    payload["identity"] = payload.get("identity", "").replace(
        "ph-civ is an LLM-native",
        "predictive-history is an LLM-native",
    )
    public_copy = payload.get("public_copy", {})
    if isinstance(public_copy, dict):
        public_copy["long"] = public_copy.get("long", "").replace(
            "canonical English ph-civ",
            "canonical English predictive-history",
        )
    patched = json.dumps(payload, sort_keys=True)
    if original == patched:
        return False
    if not dry_run:
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    return True


def migrate_llm_experience(*, dry_run: bool) -> bool:
    path = ROOT / "data" / "llm-experience.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    patched = _replace_upstream_ph_civ(payload)
    links = patched.get("chapter_folder_links", {})
    if links.get("cli") == "ph-civ link <source_id>":
        links["cli"] = "predictive-history link <source_id>"
    catalog = patched.get("chapter_catalog", {})
    if "ph-civ index" in catalog.get("cli", ""):
        catalog["cli"] = "predictive-history index"
        catalog["instruction"] = re.sub(
            r"CLI name remains ph-civ index for compatibility\.?",
            "Use predictive-history index for the namespace catalog.",
            catalog.get("instruction", ""),
        )
    bridge = patched.get("bilingual_bridge", {})
    if bridge.get("canonical_source") == "ph-civ":
        bridge["canonical_source"] = "predictive-history"
    if "ph-civ-zh and ph-civ-ru are downstream mirrors of canonical ph-civ" in bridge.get("authority_model", ""):
        bridge["authority_model"] = bridge["authority_model"].replace(
            "canonical ph-civ",
            "canonical predictive-history",
        )
    if payload == patched:
        return False
    if not dry_run:
        path.write_text(json.dumps(patched, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Migrate ph surface metadata to predictive-history")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    jsonl_n = migrate_cards_jsonl(dry_run=args.dry_run)
    md_n = migrate_card_markdown(dry_run=args.dry_run)
    bilingual = migrate_bilingual_loop(dry_run=args.dry_run)
    llm = migrate_llm_experience(dry_run=args.dry_run)
    print(
        f"cards.jsonl derived_corpus rows: {jsonl_n}; "
        f"cards/*.md: {md_n}; "
        f"bilingual-loop: {bilingual}; "
        f"llm-experience: {llm}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
