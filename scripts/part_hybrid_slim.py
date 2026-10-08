#!/usr/bin/env python3
"""Slim chapter commentaries to Layer 0-2 + Part apparatus pointer (--part 01|07|08|09|10)."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOL2 = ROOT / "book" / "volume-ii"
REGISTRY = ROOT / "data" / "parts" / "volume-i-parts.json"

PART_NUMBERS = {
    "01": "part-01-dawn-of-civilization",
    "07": "part-07-world-after-rome",
    "08": "part-08-birth-of-modernity",
    "09": "part-09-age-of-conscience",
    "10": "part-10-rise-of-the-nation-state",
}


def load_part(part_id: str) -> dict:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    for part in data["parts"]:
        if part["part_id"] == part_id:
            return part
    raise KeyError(part_id)


def commentary_slug(part_id: str) -> str:
    return part_id.replace("part-", "part-") + "-commentary.md"


def slim_commentary(cid: str, part_id: str, commentary_path: str, bibliography_path: str) -> None:
    path = VOL2 / cid / f"{cid}-commentary.md"
    if not path.is_file():
        print(f"skip (no commentary): {path.relative_to(ROOT)}")
        return
    text = path.read_text(encoding="utf-8")
    if "## Part apparatus" in text and "## Layer 3" not in text:
        print(f"skip commentary (already slim): {path.relative_to(ROOT)}")
        return
    m = re.search(r"\n## Layer 3\b", text)
    if not m:
        print(f"skip (no Layer 3): {path.relative_to(ROOT)}")
        return
    head = text[: m.start()].rstrip() + "\n"
    comm_base = Path(commentary_path).name
    bib_base = Path(bibliography_path).name
    tail = f"""
---

## Part apparatus

Cross-chapter synthesis, predictions, external counter-readings, and bibliography live in the Part files:

- [Part commentary](../../../docs/routes/volume-i-parts/{comm_base}#{cid})
- [Part bibliography](../../../docs/routes/volume-i-parts/{bib_base})

Layer 0-2 above remain the transcript pin-cite floor for this chapter.

---

## Project Canvas (chapter-local)

### Open Questions

- Cross-chapter claims: verify against Part commentary counter-readings before quotation-grade use.
- Lecture representation_not_endorsement applies to all Layer 2 rows.

### Build Notes

- Phase 2 slim (2026-06-10): Layers 3-6 moved to Part commentary.
"""
    text = head + tail
    if "part_commentary_path:" not in text:
        text = text.replace(
            "scaffold_version: ph_civ_commentary_canvas_v1\n",
            "scaffold_version: ph_civ_commentary_canvas_v1\n"
            f"part_id: {part_id}\n"
            f"part_commentary_path: ../../../docs/routes/volume-i-parts/{comm_base}#{cid}\n"
            f"part_bibliography_path: ../../../docs/routes/volume-i-parts/{bib_base}\n",
            1,
        )
    if "analysis_depth: seed" in text:
        text = text.replace("analysis_depth: seed", "analysis_depth: layer2_slimmed")
    elif "analysis_depth: layer2_drafted" in text:
        text = text.replace("analysis_depth: layer2_drafted", "analysis_depth: layer2_slimmed")
    path.write_text(text, encoding="utf-8")
    print(f"slim commentary: {path.relative_to(ROOT)}")


def patch_readiness(part_number: str, part_id: str) -> None:
    readiness = ROOT / "lectures/parts" / f"PART-{part_number}-HYBRID-READINESS.md"
    if not readiness.is_file():
        return
    text = readiness.read_text(encoding="utf-8")
    if "Phase 2 slim" in text and "**Done**" in text:
        print(f"skip readiness: {readiness.relative_to(ROOT)}")
        return
    if "| Slim `" in text:
        text = re.sub(
            r"\| Slim `[^`]+` \|[^\n]+\|",
            f"| Slim `{part_id}` chapters | **Done** — `scripts/part_hybrid_slim.py --part {part_number}` |",
            text,
            count=1,
        )
    else:
        text += (
            f"\n| Slim `{part_id}` chapters | **Done** — "
            f"`scripts/part_hybrid_slim.py --part {part_number}` (2026-06-10) |\n"
        )
    text = text.replace("plan_status: phase3_complete", "plan_status: phase2_slimmed")
    text = text.replace("Slimming deferred to final pass", "Phase 2 slim **Done** (2026-06-10)")
    readiness.write_text(text, encoding="utf-8")
    print(f"patched readiness: {readiness.relative_to(ROOT)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--part", required=True, help="Part number: 01, 07, 08, 09, 10")
    args = parser.parse_args()
    part_id = PART_NUMBERS.get(args.part)
    if not part_id:
        raise SystemExit(f"unsupported part: {args.part}")
    part = load_part(part_id)
    commentary_path = part.get("commentary_path", "")
    bibliography_path = part.get("bibliography_path", "")
    if not commentary_path or not bibliography_path:
        raise SystemExit(f"{part_id} missing commentary_path/bibliography_path in registry")
    for cid in part["chapters"]:
        slim_commentary(cid, part_id, commentary_path, bibliography_path)
    patch_readiness(args.part, part_id)
    print(f"part_hybrid_slim --part {args.part}: done")


if __name__ == "__main__":
    main()
