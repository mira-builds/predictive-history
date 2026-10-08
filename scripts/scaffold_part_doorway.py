#!/usr/bin/env python3
"""Scaffold Volume I Part doorway markdown from volume-i-parts.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from civ_ph.volume_i_parts import chapter_titles_from_spine, load_volume_i_parts_registry  # noqa: E402

CORRIDOR_PATHS = {
    "homer-to-tolstoy": "../../../data/corridors/homer-to-tolstoy.md",
    "homer-to-tolstoy-support-ring": "../../../data/corridors/homer-to-tolstoy-support-ring.md",
    "homer-to-tolstoy-source-lattice": "../../../data/corridors/homer-to-tolstoy-source-lattice.md",
    "homer-to-dante": "../../../data/corridors/homer-to-dante.md",
    "plato-to-hegel": "../../../data/corridors/plato-to-hegel.md",
    "civilization-to-apocalypse": "../../docs/routes/civilization-to-apocalypse.md",
}


def _distinction_block(part: dict) -> str:
    part_id = part["part_id"]
    if part_id == "part-06-medieval-imagination":
        return (
            "**What this Part is:** The **inner** medieval slice — Dante, Great Books weave, "
            "and post-classical Roman **imagination** (oceanic currents, Byzantium, Holy Roman fiction).\n\n"
            "**What this Part is not:** Viking, steppe, and church **world orders** — those open in "
            "[Part VII — The World After Rome](part-07-world-after-rome.md) at `civ-35`.\n\n"
            "**Corridor:** Homer-to-Dante **opens** here; the corridor **returns** to Dante at `civ-41` in Part VII.\n"
        )
    if part_id == "part-07-world-after-rome":
        return (
            "**What this Part is:** The **world after Rome** — Viking, Islamic, Mongol, Chinese twilight, "
            "and church–empire orders on Rome's plural afterlife.\n\n"
            "**What this Part is not:** The opening Dante / GB block (`civ-29`–`30`) — that lives in "
            "[Part VI — The Medieval Imagination](part-06-medieval-imagination.md).\n\n"
            "**Corridor:** Dante **returns** at `civ-41` (*Dante's Quiet Revolution*); this closes the "
            "Homer-to-Dante segment before [Part VIII — The Birth of Modernity](part-08-birth-of-modernity.md).\n"
        )
    if part_id == "part-03-roman-imperium":
        return (
            "**Why this order:** Rome (`civ-14`–`17`) appears **before** the ancient-worlds floor in "
            "interwoven order — imperial machinery and Virgil before Egypt, Mesopotamia, and parallel "
            "grammars in Part IV.\n"
        )
    if part_id == "part-04-ancient-foundations":
        return (
            "**Why this order:** This Part is the ancient-worlds **floor** (`civ-18`–`23`) placed **after** "
            "Rome in the spine — parallel grammars beside Greece/Rome, not a prelude to them.\n"
        )
    return ""


def _companion_weave(part: dict) -> str:
    lines: list[str] = []
    for row in part.get("great_books_weave", []):
        gb_id = row["gb_id"]
        anchor = row["anchor_civ"]
        role = row.get("role", "interwoven")
        note = row.get("note", "")
        suffix = f" — {note}" if note else ""
        lines.append(
            f"- `{gb_id}` @ `{anchor}` ({role}) — "
            f"[{gb_id}](../great-books-evidence/{gb_id}/README.md){suffix}"
        )
    for row in part.get("secret_history_companions", []):
        sh_id = row["sh_id"]
        anchor = row["anchor_civ"]
        role = row.get("role", "support")
        lines.append(
            f"- `{sh_id}` @ `{anchor}` ({role}) — "
            f"[{sh_id}](../secret-history-support/{sh_id}/README.md)"
        )
    return "\n".join(lines) if lines else "_No interwoven companions in this Part._"


def _corridor_links(part: dict) -> str:
    touchpoints = part.get("corridor_touchpoints", [])
    if not touchpoints:
        return "_No corridor touchpoints in this Part._"
    lines = []
    for name in touchpoints:
        rel = CORRIDOR_PATHS.get(name, f"../../../data/corridors/{name}.md")
        lines.append(f"- [{name}]({rel})")
    return "\n".join(lines)


def _nav_links(part: dict, by_id: dict[str, dict]) -> tuple[str, str]:
    prev_line = "_Start of Volume I._"
    prev_id = part.get("previous_part_id")
    if prev_id and prev_id in by_id:
        prev = by_id[prev_id]
        prev_line = (
            f"**Previous:** [{prev['display_title']}]({Path(prev['doorway_path']).name})"
        )
    next_line = "_End of Volume I._"
    next_id = part.get("next_part_id")
    if next_id and next_id in by_id:
        nxt = by_id[next_id]
        next_line = f"**Next:** [{nxt['display_title']}]({Path(nxt['doorway_path']).name})"
    elif part.get("exit_hook"):
        next_line = f"**Exit:** {part['exit_hook']}"
    return prev_line, next_line


def render_doorway(part: dict, titles: dict[str, str], by_id: dict[str, dict]) -> str:
    subtitle = part.get("part_distinction_subtitle")
    header = f"# {part['display_title']}"
    if subtitle:
        header += f"\n\n*{subtitle}*"

    anchor_rows = []
    for civ_id in part.get("chapters", []):
        lecture = titles.get(civ_id, "")
        anchor_rows.append(f"| `{civ_id}` | {lecture} |")

    distinction = _distinction_block(part)
    distinction_section = f"\n## Distinction\n\n{distinction}" if distinction else ""

    prev_link, next_link = _nav_links(part, by_id)

    return f"""{header}

*This Part is a **spine slice** of Volume I — Civilization. It follows [interwoven-reader](../../archive/two-volume-reader-order-interwoven.md) order; it is not a pure historical period box.*
{distinction_section}
## Law-discovery question

{part['law_discovery_question']}

## Chapter anchors

| Chapter | Lecture |
|---------|---------|
{chr(10).join(anchor_rows)}

## Companion weave

{_companion_weave(part)}

## Corridor cross-links

{_corridor_links(part)}

## Navigation

- {prev_link}
- {next_link}
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--part-id", help="Scaffold one part only")
    parser.add_argument(
        "--update-registry-anchors",
        action="store_true",
        help="Write chapter_anchors arrays back into volume-i-parts.json",
    )
    args = parser.parse_args()

    registry = load_volume_i_parts_registry()
    titles = chapter_titles_from_spine()
    parts = registry["parts"]
    by_id = {part["part_id"]: part for part in parts}

    targets = parts
    if args.part_id:
        targets = [by_id[args.part_id]]

    for part in targets:
        doorway_path = ROOT / part["doorway_path"]
        doorway_path.parent.mkdir(parents=True, exist_ok=True)
        doorway_path.write_text(render_doorway(part, titles, by_id), encoding="utf-8")
        print(f"wrote {doorway_path.relative_to(ROOT)}")

        if args.update_registry_anchors:
            part["chapter_anchors"] = [
                f"{civ_id} {titles.get(civ_id, '')}".strip() for civ_id in part["chapters"]
            ]

    if args.update_registry_anchors:
        registry_path = ROOT / "data" / "parts" / "volume-i-parts.json"
        registry_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
        print(f"updated {registry_path.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
