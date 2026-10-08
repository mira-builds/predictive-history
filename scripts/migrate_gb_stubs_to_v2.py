#!/usr/bin/env python3
"""Migrate stub_routed_to_part GB commentaries to v2 chapter-only SSOT."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from civ_ph.commentary_v2 import SCAFFOLD_VERSION_V2, extract_part_section, markdown_frontmatter  # noqa: E402

GB_STUBS = [
    "gb-03",
    "gb-05",
    "gb-07",
    "gb-08",
    "gb-09",
    "gb-10",
    "gb-11",
    "gb-12",
]

WEAVE_ANCHORS = {
    "gb-03": ("civ-07", "support_ring_optional"),
    "gb-05": ("civ-07", "interwoven"),
    "gb-07": ("civ-07", "interwoven"),
    "gb-08": ("civ-17", "interwoven"),
    "gb-09": ("civ-30", "interwoven"),
    "gb-10": ("civ-41", "interwoven"),
    "gb-11": ("civ-30", "interwoven"),
    "gb-12": ("civ-30", "interwoven"),
}


def parse_field(body: str, label: str) -> str:
    match = re.search(rf"\*\*{re.escape(label)}:\*\*\s*(.+)", body)
    return match.group(1).strip() if match else ""


def parse_claims(body: str, source_id: str) -> list[tuple[str, str, str, str]]:
    rows: list[tuple[str, str, str, str]] = []
    in_table = False
    for line in body.splitlines():
        if "| # | Claim |" in line or "|---|" in line and in_table:
            in_table = True
            continue
        if in_table and line.startswith("|") and "|---" not in line:
            parts = [cell.strip() for cell in line.strip("|").split("|")]
            if len(parts) >= 4 and parts[0].isdigit():
                ref = parts[2].strip("`")
                if ref.startswith("#"):
                    ref = f"{source_id}-transcript.md{ref}"
                elif not ref.endswith(".md"):
                    ref = f"{source_id}-transcript.md#{ref.strip('#')}"
                rows.append((parts[0], parts[1], ref, parts[3]))
            elif len(parts) >= 3 and not parts[0].isdigit():
                break
        elif in_table and not line.startswith("|"):
            if rows:
                break
    return rows


def parse_counter_table(body: str, header: str) -> list[tuple[str, str, str]]:
    pattern = re.compile(
        rf"{re.escape(header)}[\s\S]*?\n\n\| Topic \| Counter-reading \| Strength \|\n\|[-| ]+\n([\s\S]*?)(?:\n\n|\*\*)",
    )
    match = pattern.search(body + "\n\n")
    if not match:
        return []
    rows: list[tuple[str, str, str]] = []
    for line in match.group(1).splitlines():
        if not line.startswith("|"):
            continue
        parts = [cell.strip() for cell in line.strip("|").split("|")]
        if len(parts) == 3 and parts[0] != "Topic":
            rows.append((parts[0], parts[1], parts[2]))
    return rows


def host_commentary_link(anchor_civ: str) -> str:
    return f"../../volume-ii/{anchor_civ}/{anchor_civ}-commentary.md"


def render_v2(
    source_id: str,
    fm: dict[str, str],
    part_body: str,
    anchor_civ: str,
    weave_role: str,
) -> str:
    title = fm.get("title", source_id)
    thesis = parse_field(part_body, "Core thesis")
    arc = parse_field(part_body, "Close-read arc")
    claims = parse_claims(part_body, source_id)
    counters = parse_counter_table(part_body, f"**Counter-readings ({source_id}):**")
    part_links = parse_field(part_body, "Part links")

    header_lines = ["---"]
    skip = {"part_commentary_path", "part_bibliography_path", "commentary_authority"}
    updates = {
        "analysis_depth": "layer2_drafted",
        "scaffold_version": SCAFFOLD_VERSION_V2,
        "commentary_maturity": "l3_falsifiers",
        "migration_source": "extracted_from_part",
        "canonical_weave": f"{weave_role}@{anchor_civ}",
    }
    merged = {**fm, **updates}
    for key, value in merged.items():
        if key in skip:
            continue
        header_lines.append(f"{key}: {value}")
    header_lines.append("---\n")

    l2_rows = []
    for num, claim, ref, conf in claims:
        l2_rows.append(
            f"| {num} | {claim} | `{ref}` | Explicit | {conf} |"
        )
    if not l2_rows:
        l2_rows.append(
            f"| 1 | TBD — extract from Part section | `{source_id}-transcript.md#TBD` | Contextual | Low |"
        )

    l4_rows = []
    for topic, reading, strength in counters:
        l4_rows.append(f"| {topic} | {reading} | {strength} |")
    if not l4_rows:
        l4_rows.append("| TBD | TBD | Low |")

    pred_line = parse_field(part_body, f"{source_id} predictions")
    l3_note = pred_line or "Pending — migrated from Part ledger row"

    body = f"""# Commentary - Great Books

The source transcript is `{source_id}-transcript.md`. This commentary uses the v2 multi-layer scaffold (chapter-only SSOT).

## Layer 0 - Metadata & Quick Reference

- Core thesis: {thesis or "TBD"}
- Primary focus: migrated from Part apparatus § {source_id}
- Confidence in source fidelity: High for transcript body where pin-cited; lecture overlays marked in L4
- Template version: v2 GB migration
- Completeness state: in-review

---

## Layer 1 - Neutral Summary

{arc or "TBD — neutral summary from transcript after review."}

---

## Layer 2 - Source-Backed Claims & Concepts

### Major Claims

| # | Claim | Transcript Reference | Strength | Confidence |
|---|-------|---------------------|----------|------------|
{chr(10).join(l2_rows)}

---

## Layer 3 - Predictions & Falsifiers

| Prediction | Strength | Falsifier Criteria | Review Date | Current Status | Notes |
|------------|----------|-------------------|-------------|----------------|-------|
| {l3_note} | SI | Part ledger falsifier or scholarly counter-evidence | 2027-06-01 | Pending | Migrated from Part § {source_id} |

---

## Layer 4 - Counter-Readings

| Topic | Counter-reading | Strength |
|-------|-----------------|----------|
{chr(10).join(l4_rows)}

---

## Layer 5 - Synthesis & Cross-Volume Links

| pattern_id | How this chapter supports or limits it |
|------------|----------------------------------------|
| TBD | Calibrate after host chapter weave review |

**Weave host:** [`{anchor_civ}`]({host_commentary_link(anchor_civ)}) — `{weave_role}` @ this anchor.

**Part links (migration note):** {part_links or "see weave registry"}

---

## Layer 6 - Open Issues

- Part v1 section migrated; verify no unique claims remain only in archived Part files.
- Expand L3 rows from Part prediction ledger where folded summaries need unpacking.

---

## Project Canvas (chapter-local)

### Open Questions

- Which claims need external bibliography before quotation-grade use?

### Build Notes

- Migrated from Part extract via `migrate_gb_stubs_to_v2.py`; authority now chapter-only.
"""
    return "\n".join(header_lines) + body


def migrate_one(source_id: str, dry_run: bool) -> bool:
    commentary_path = ROOT / "book" / "volume-v" / source_id / f"{source_id}-commentary.md"
    if not commentary_path.exists():
        print(f"ERROR: missing {commentary_path}", file=sys.stderr)
        return False
    text = commentary_path.read_text(encoding="utf-8")
    fm = markdown_frontmatter(text)
    if fm.get("analysis_depth") != "stub_routed_to_part":
        print(f"skip {source_id}: not stub_routed_to_part")
        return False
    part_rel = fm.get("part_commentary_path", "")
    if "#" in part_rel:
        part_file, section_id = part_rel.split("#", 1)
    else:
        part_file, section_id = part_rel, source_id
    part_path = (commentary_path.parent / part_file).resolve()
    if not part_path.exists():
        print(f"ERROR: missing part file {part_path}", file=sys.stderr)
        return False
    part_body = extract_part_section(part_path.read_text(encoding="utf-8"), section_id)
    if not part_body:
        print(f"ERROR: section ### {section_id} not found in {part_path}", file=sys.stderr)
        return False
    anchor_civ, weave_role = WEAVE_ANCHORS[source_id]
    out = render_v2(source_id, fm, part_body, anchor_civ, weave_role)
    if dry_run:
        print(f"would write {commentary_path.relative_to(ROOT)} ({len(out)} bytes)")
        return True
    commentary_path.write_text(out, encoding="utf-8")
    print(f"wrote {commentary_path.relative_to(ROOT)}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-id", action="append")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    targets = args.source_id or GB_STUBS
    ok = 0
    for sid in targets:
        if migrate_one(sid, args.dry_run):
            ok += 1
    print(f"{'would migrate' if args.dry_run else 'migrated'} {ok}/{len(targets)}")
    return 0 if ok == len(targets) else 1


if __name__ == "__main__":
    raise SystemExit(main())
