"""Commentary methodology v2 helpers (maturity, validation)."""

from __future__ import annotations

import re
from pathlib import Path

SCAFFOLD_VERSION_V2 = "ph_civ_commentary_canvas_v2"
MATURITY_VALUES = frozenset(
    {
        "scaffold",
        "l2_pinned",
        "l3_falsifiers",
        "l6_drafted",
        "in_review",
        "calibration",
    }
)
V2_LAYER_HEADINGS = [
    "## Layer 3 - Predictions & Falsifiers",
    "## Layer 4 - Counter-Readings",
    "## Layer 5 - Synthesis & Cross-Volume Links",
    "## Layer 6 - Open Issues",
]

LEGACY_DEPTH_TO_MATURITY = {
    "seed": "scaffold",
    "layer2_drafted": "l2_pinned",
    "layer2_slimmed": "l2_pinned",
    "stub_routed_to_part": "scaffold",
}


def markdown_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    return fields


def infer_maturity(text: str, fm: dict[str, str]) -> str:
    explicit = fm.get("commentary_maturity", "")
    if explicit in MATURITY_VALUES:
        return explicit
    depth = fm.get("analysis_depth", "")
    if depth in LEGACY_DEPTH_TO_MATURITY:
        base = LEGACY_DEPTH_TO_MATURITY[depth]
    elif depth == "stub_routed_to_part":
        return "scaffold"
    else:
        base = "scaffold"
    if "## Layer 2" in text and "| Claim |" in text:
        base = "l2_pinned"
    if "## Layer 3" in text and "| Prediction |" in text:
        if "Pending" in text or "Falsifier" in text:
            base = "l3_falsifiers"
    if all(h in text for h in V2_LAYER_HEADINGS) and "## Project Canvas" in text:
        if base in {"l2_pinned", "l3_falsifiers"}:
            base = "l6_drafted"
    if fm.get("commentary_status") == "calibration_seed" or fm.get("source_id") == "civ-01":
        pass
    return base


def commentary_metadata(commentary_path: Path) -> dict:
    text = commentary_path.read_text(encoding="utf-8")
    fm = markdown_frontmatter(text)
    maturity = infer_maturity(text, fm)
    return {
        "commentary_maturity": maturity,
        "scaffold_version": fm.get("scaffold_version", ""),
        "analysis_depth": fm.get("analysis_depth", ""),
        "migration_source": fm.get("migration_source", ""),
        "deprecated_part_routing": bool(fm.get("part_commentary_path") or "Part apparatus" in text),
    }


def validate_v2_pilot(commentary_path: Path, source_id: str) -> list[str]:
    text = commentary_path.read_text(encoding="utf-8")
    fm = markdown_frontmatter(text)
    errors: list[str] = []
    if fm.get("scaffold_version") != SCAFFOLD_VERSION_V2:
        errors.append(f"{source_id} pilot should use {SCAFFOLD_VERSION_V2}")
    if "Part apparatus" in text and "deprecated" not in text.lower().split("Part apparatus")[0][-80:]:
        if "## Part apparatus" in text:
            errors.append(f"{source_id} still has active Part apparatus section")
    if fm.get("part_commentary_path"):
        errors.append(f"{source_id} still has part_commentary_path frontmatter")
    if "## Layer 3" not in text:
        errors.append(f"{source_id} pilot missing Layer 3")
    maturity = fm.get("commentary_maturity") or infer_maturity(text, fm)
    if maturity == "scaffold" and source_id in {"civ-07", "civ-29"}:
        errors.append(f"{source_id} pilot should be at least l2_pinned")
    return errors


def extract_part_section(part_text: str, section_id: str) -> str:
    pattern = re.compile(
        rf"^### {re.escape(section_id)}\s*$([\s\S]*?)(?=^### |\Z)",
        re.MULTILINE,
    )
    match = pattern.search(part_text)
    return match.group(1).strip() if match else ""


def commentary_status_report(cards: list[dict], repo_root: Path) -> dict:
    by_maturity: dict[str, int] = {}
    by_scaffold: dict[str, int] = {}
    by_depth: dict[str, int] = {}
    wave_queue: dict[str, list[str]] = {
        "upgrade_l2_pinned": [],
        "migrate_from_part": [],
        "regen_seed": [],
        "v2_pilot_complete": [],
        "part_apparatus_remaining": [],
    }
    for card in cards:
        source_id = card["source_id"]
        rel = card.get("source_paths", {}).get("commentary_path", "")
        if not rel:
            continue
        path = repo_root / rel
        if not path.exists():
            continue
        meta = commentary_metadata(path)
        text = path.read_text(encoding="utf-8")
        maturity = meta["commentary_maturity"]
        scaffold = meta["scaffold_version"] or "(missing)"
        depth = meta["analysis_depth"] or "(missing)"
        by_maturity[maturity] = by_maturity.get(maturity, 0) + 1
        by_scaffold[scaffold] = by_scaffold.get(scaffold, 0) + 1
        by_depth[depth] = by_depth.get(depth, 0) + 1
        if source_id in {
            "civ-07",
            "civ-22",
            "civ-29",
            "gb-02",
            "gt-24",
            "sh-17",
        } and scaffold == SCAFFOLD_VERSION_V2:
            wave_queue["v2_pilot_complete"].append(source_id)
        elif depth == "stub_routed_to_part" or meta["deprecated_part_routing"]:
            if meta["deprecated_part_routing"]:
                wave_queue["part_apparatus_remaining"].append(source_id)
            if depth == "stub_routed_to_part":
                wave_queue["migrate_from_part"].append(source_id)
        elif depth in {"layer2_drafted", "layer2_slimmed"} and scaffold != SCAFFOLD_VERSION_V2:
            wave_queue["upgrade_l2_pinned"].append(source_id)
        elif depth == "seed" and scaffold != SCAFFOLD_VERSION_V2:
            wave_queue["regen_seed"].append(source_id)
    for key in wave_queue:
        wave_queue[key] = sorted(wave_queue[key])
    return {
        "total": len(cards),
        "by_commentary_maturity": dict(sorted(by_maturity.items())),
        "by_scaffold_version": dict(sorted(by_scaffold.items())),
        "by_analysis_depth": dict(sorted(by_depth.items())),
        "wave_queue": wave_queue,
    }


V2_SCAFFOLD_BODY = """# Commentary - {heading}

The source transcript is `{transcript}`. This commentary uses the v2 multi-layer scaffold (chapter-only SSOT).

## Layer 0 - Metadata & Quick Reference

- Core thesis: TBD — align with transcript after fidelity review.
- Primary focus: TBD
- Confidence in source fidelity: Pending review
- Completeness state: scaffold

---

## Layer 1 - Neutral Summary

TBD — neutral paraphrase of the lecture after transcript review.

---

## Layer 2 - Source-Backed Claims & Concepts

### Major Claims

| # | Claim | Transcript Reference | Strength | Confidence |
|---|-------|---------------------|----------|------------|
| 1 | TBD | `{transcript}#TBD` | Contextual | Low |

---

## Layer 3 - Predictions & Falsifiers

| Prediction | Strength | Falsifier Criteria | Review Date | Current Status | Notes |
|------------|----------|-------------------|-------------|----------------|-------|
| TBD | C | TBD | TBD | Pending | Event-timed rows require review_date when applicable |

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

- Transcript fidelity review pending.
- Scaffold generated by v2 regen tooling.

---

## Project Canvas

### Project Leverage

TBD

### Laws / Patterns Exposed

- TBD

### Volume Role

TBD

### Strategy / Present-Day Application

TBD

### Counter-Readings

TBD

### Open Questions

- TBD

### Build Notes / Future Enhancements

- v2 scaffold regen; expand L0–2 after transcript pin-cite pass.
"""


def render_v2_scaffold_body(source_id: str, title: str, transcript_name: str) -> str:
    heading = title.split(":", 1)[0] if ":" in title else title
    return V2_SCAFFOLD_BODY.format(
        heading=heading,
        transcript=transcript_name,
    )
