#!/usr/bin/env python3
"""Generate data/weave/volume-i-companions.json from volume-i-parts.json."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTS_PATH = ROOT / "data" / "parts" / "volume-i-parts.json"
OUT_PATH = ROOT / "data" / "weave" / "volume-i-companions.json"
DEPRECATED_PATH = ROOT / "data" / "parts" / "volume-i-parts.deprecated.json"


def main() -> int:
    parts_data = json.loads(PARTS_PATH.read_text(encoding="utf-8"))
    by_civ_host: dict = {}
    by_companion: dict = {}

    for part in parts_data.get("parts", []):
        for entry in part.get("great_books_weave", []):
            civ = entry["anchor_civ"]
            gb = entry["gb_id"]
            by_civ_host.setdefault(civ, {"great_books": [], "secret_history": [], "corridor_touchpoints": []})
            by_civ_host[civ]["great_books"].append(
                {"gb_id": gb, "role": entry.get("role", "interwoven"), "note": entry.get("note")}
            )
            by_companion[gb] = {
                "anchor_civ": civ,
                "kind": "great-books",
                "role": entry.get("role", "interwoven"),
            }
        for entry in part.get("secret_history_companions", []):
            civ = entry["anchor_civ"]
            sh = entry["sh_id"]
            by_civ_host.setdefault(civ, {"great_books": [], "secret_history": [], "corridor_touchpoints": []})
            by_civ_host[civ]["secret_history"].append(
                {"sh_id": sh, "role": entry.get("role", "companion")}
            )
            by_companion[sh] = {
                "anchor_civ": civ,
                "kind": "secret-history",
                "role": entry.get("role", "companion"),
            }
        for corridor in part.get("corridor_touchpoints", []):
            if isinstance(corridor, dict):
                civ = corridor.get("anchor_civ") or part.get("spine_start")
            else:
                civ = part.get("spine_start")
            by_civ_host.setdefault(civ, {"great_books": [], "secret_history": [], "corridor_touchpoints": []})
            by_civ_host[civ]["corridor_touchpoints"].append(corridor)

    payload = {
        "schema_version": 1,
        "generated_from": "data/parts/volume-i-parts.json",
        "spine_ssot": parts_data.get("spine_ssot", "docs/archive/two-volume-reader-order-interwoven.md"),
        "deprecated_parts_registry": "data/parts/volume-i-parts.deprecated.json",
        "by_civ_host": dict(sorted(by_civ_host.items())),
        "by_companion": dict(sorted(by_companion.items())),
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    deprecated = dict(parts_data)
    deprecated["deprecated"] = True
    deprecated["successor"] = "data/weave/volume-i-companions.json"
    DEPRECATED_PATH.write_text(json.dumps(deprecated, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT_PATH.relative_to(ROOT)}")
    print(f"wrote {DEPRECATED_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
