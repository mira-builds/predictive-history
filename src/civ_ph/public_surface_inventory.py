"""Public surface inventory — machine catalog of Predictive History surfaces."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

from .data import PACKAGE_ROOT, load_cards
from .ph_civ_index import chapter_entry, index_json_path

INVENTORY_JSON_REL = "data/public-surface-inventory.json"
INVENTORY_MD_REL = "runtime/artifacts/public-surface-inventory.md"
FINGERPRINT_MARKER = "<!-- public-surface-inventory-fingerprint:"
SCHEMA_VERSION = 1

VALIDATION_COVERAGE_MAP = {
    "llm_bootloader": "validate:llm-experience",
    "first_tour": "validate:first-tour",
    "choreography": "validate:choreography",
    "predictive_history_index": "validate:predictive-history-index",
    "cards": "validate:cards",
    "patterns": "validate:patterns",
    "public_boundary": "validate:public-boundary",
    "volume_i_parts_deprecated": "validate:volume-i-parts-deprecated",
    "commentary_canvas": "validate:commentary-canvas",
    "manual": "manual",
    "aggregate": "docs/predictive-history-index.json",
}


def inventory_json_path(repo_root: Path | None = None) -> Path:
    root = repo_root or PACKAGE_ROOT
    return root / INVENTORY_JSON_REL


def inventory_md_path(repo_root: Path | None = None) -> Path:
    root = repo_root or PACKAGE_ROOT
    return root / INVENTORY_MD_REL


def _row(
    *,
    surface: str,
    path: str,
    surface_class: str,
    status: str,
    authority_level: str = "public",
    reader_mode: str = "any",
    source_floor: str = "n/a",
    generated_or_hand_authored: str = "hand",
    regeneration_command: str = "",
    public_ready: bool = True,
    validation_coverage: str = "manual",
    notes: str = "",
) -> dict:
    return {
        "surface": surface,
        "path": path,
        "surface_class": surface_class,
        "status": status,
        "authority_level": authority_level,
        "reader_mode": reader_mode,
        "source_floor": source_floor,
        "generated_or_hand_authored": generated_or_hand_authored,
        "regeneration_command": regeneration_command,
        "public_ready": public_ready,
        "validation_coverage": VALIDATION_COVERAGE_MAP.get(validation_coverage, validation_coverage),
        "notes": notes,
    }


def static_surface_rows() -> list[dict]:
    return [
        _row(
            surface="start_here",
            path="START-HERE.md",
            surface_class="bootloader",
            status="canonical",
            reader_mode="first_tour",
            source_floor="orientation",
            validation_coverage="llm_bootloader",
            notes="LLM paste URL entry; pairs with llm-experience.json",
        ),
        _row(
            surface="agents_guardrails",
            path="AGENTS.md",
            surface_class="bootloader",
            status="canonical",
            reader_mode="agent",
            validation_coverage="public_boundary",
        ),
        _row(
            surface="llms_txt",
            path="llms.txt",
            surface_class="llm_context",
            status="active",
            reader_mode="agent",
            validation_coverage="llm_bootloader",
        ),
        _row(
            surface="llms_full",
            path="llms-full.txt",
            surface_class="llm_context",
            status="active",
            reader_mode="agent",
            validation_coverage="llm_bootloader",
        ),
        _row(
            surface="llm_experience",
            path="data/llm-experience.json",
            surface_class="llm_context",
            status="active",
            reader_mode="first_tour",
            generated_or_hand_authored="hand",
            validation_coverage="llm_bootloader",
            regeneration_command="predictive-history validate",
        ),
        _row(
            surface="predictive_history_index",
            path="docs/predictive-history-index.json",
            surface_class="chapter_catalog",
            status="generated",
            generated_or_hand_authored="generated",
            regeneration_command="predictive-history index",
            validation_coverage="predictive_history_index",
            notes="Human mirror: docs/predictive-history-index.md",
        ),
        _row(
            surface="cards_dataset",
            path="data/cards.jsonl",
            surface_class="card_dataset",
            status="active",
            source_floor="card",
            validation_coverage="cards",
        ),
        _row(
            surface="patterns_dataset",
            path="data/patterns.json",
            surface_class="pattern_dataset",
            status="active",
            validation_coverage="patterns",
        ),
        _row(
            surface="choreography_routes",
            path="data/routes/choreography.json",
            surface_class="route_dataset",
            status="active",
            reader_mode="first_tour",
            validation_coverage="choreography",
        ),
        _row(
            surface="route_seed",
            path="data/routes/seed.json",
            surface_class="route_dataset",
            status="active",
            validation_coverage="choreography",
        ),
        _row(
            surface="first_tour",
            path="data/routes/first-tour.json",
            surface_class="route_dataset",
            status="active",
            reader_mode="first_tour",
            validation_coverage="first_tour",
            notes="Doctrine mirror: docs/onboarding/first-tour.md",
        ),
        _row(
            surface="spine_tour",
            path="data/routes/volume-i-spine-tour.json",
            surface_class="route_dataset",
            status="active",
            reader_mode="study",
        ),
        _row(
            surface="source_lattice",
            path="docs/methodology/source-lattice.md",
            surface_class="doctrine_doc",
            status="canonical",
            source_floor="law",
            validation_coverage="manual",
        ),
        _row(
            surface="commentary_methodology_v2",
            path="docs/methodology/commentary-methodology-v2.md",
            surface_class="doctrine_doc",
            status="canonical",
            validation_coverage="commentary_canvas",
        ),
        _row(
            surface="public_repo_contract",
            path="docs/contracts/public-repo-contract.md",
            surface_class="doctrine_doc",
            status="canonical",
        ),
        _row(
            surface="public_surface_status",
            path="docs/catalogs/public-surface-status.md",
            surface_class="doctrine_doc",
            status="active",
            public_ready=True,
            notes="Surface readiness vocabulary SSOT",
        ),
        _row(
            surface="growth_goals",
            path="data/growth-goals.json",
            surface_class="growth_surface",
            status="active",
            public_ready=False,
            notes="Ambitions ≠ launch readiness",
        ),
        _row(
            surface="parts_v1_hybrid_archive",
            path="docs/archive/parts-v1-hybrid.md",
            surface_class="archive_retired",
            status="deprecated",
            public_ready=False,
            validation_coverage="volume_i_parts_deprecated",
        ),
        _row(
            surface="volume_i_parts_deprecated_json",
            path="data/parts/volume-i-parts.deprecated.json",
            surface_class="archive_retired",
            status="deprecated",
            public_ready=False,
        ),
        _row(
            surface="strategy_codex_bridge",
            path="docs/methodology/strategy-codex-bridge.md",
            surface_class="bridge",
            status="active",
            notes="Publisher staging-mirror boundary; names private workshop explicitly",
        ),
        _row(
            surface="public_surface_inventory",
            path=INVENTORY_JSON_REL,
            surface_class="schema_prompt",
            status="generated",
            generated_or_hand_authored="generated",
            regeneration_command="predictive-history surface-inventory",
            validation_coverage="manual",
        ),
        _row(
            surface="public_surface_triage",
            path="data/public-surface-triage.json",
            surface_class="schema_prompt",
            status="generated",
            generated_or_hand_authored="generated",
            regeneration_command="predictive-history surface-triage",
            validation_coverage="manual",
        ),
    ]


def aggregate_chapter_rows(cards: list[dict], repo_root: Path) -> list[dict]:
    by_surface: dict[str, int] = {"ph-civ": 0, "ph-apo": 0}
    folder_count = 0
    for card in cards:
        entry = chapter_entry(card, repo_root)
        by_surface[entry["surface"]] = by_surface.get(entry["surface"], 0) + 1
        if entry.get("paths", {}).get("folder"):
            folder_count += 1
    return [
        _row(
            surface="transcript_commentary_chapters",
            path="(per docs/predictive-history-index.json chapters[].paths)",
            surface_class="transcript",
            status="canonical",
            source_floor="transcript",
            validation_coverage="aggregate",
            notes=f"{len(cards)} chapters with transcript + commentary paths",
        ),
        _row(
            surface="chapter_folders",
            path="lectures/*",
            surface_class="chapter_folder",
            status="active",
            reader_mode="study",
            validation_coverage="cards",
            notes=f"{folder_count} folder-backed study doorways; full list in predictive-history-index.json",
        ),
        _row(
            surface="ph_civ_volume_i_chapters",
            path="lectures/* ",
            surface_class="chapter_folder",
            status="active",
            notes=f"ph-civ surface count: {by_surface.get('ph-civ', 0)}",
            validation_coverage="aggregate",
        ),
        _row(
            surface="ph_apo_volume_ii_chapters",
            path="lectures/* ",
            surface_class="chapter_folder",
            status="active",
            notes=f"ph-apo surface count: {by_surface.get('ph-apo', 0)}",
            validation_coverage="aggregate",
        ),
    ]


def build_inventory_rows(cards: list[dict], repo_root: Path, *, last_checked: str) -> list[dict]:
    rows = static_surface_rows() + aggregate_chapter_rows(cards, repo_root)
    for row in rows:
        row["last_checked"] = last_checked
        rel = row["path"]
        if rel.startswith("(") or rel.endswith("*"):
            continue
        if not (repo_root / rel).exists():
            row["notes"] = (row.get("notes", "") + " [path missing at generation]").strip()
    return sorted(rows, key=lambda r: (r["surface_class"], r["surface"]))


def rows_fingerprint(rows: list[dict]) -> str:
    stable = [{k: v for k, v in row.items() if k != "last_checked"} for row in rows]
    blob = json.dumps(stable, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]


def render_inventory_payload(cards: list[dict], repo_root: Path) -> dict:
    last_checked = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    rows = build_inventory_rows(cards, repo_root, last_checked=last_checked)
    fingerprint = rows_fingerprint(rows)
    index_path = index_json_path(repo_root)
    return {
        "schema_version": SCHEMA_VERSION,
        "fingerprint": fingerprint,
        "generated_at": last_checked,
        "card_count": len(cards),
        "chapter_catalog": "docs/predictive-history-index.json",
        "markdown_summary": INVENTORY_MD_REL,
        "surface_count": len(rows),
        "surfaces": rows,
    }


def render_inventory_markdown(payload: dict) -> str:
    fp = payload["fingerprint"]
    lines = [
        f"{FINGERPRINT_MARKER} {fp} -->",
        "# Public surface inventory",
        "",
        f"- **Surfaces:** {payload['surface_count']}",
        f"- **Generated:** {payload['generated_at']}",
        f"- **Machine SSOT:** [`{INVENTORY_JSON_REL}`](../../{INVENTORY_JSON_REL})",
        f"- **Regenerate:** `predictive-history surface-inventory`",
        "",
        "Per-surface status vocabulary: [public-surface-status.md](../../docs/catalogs/public-surface-status.md).",
        "",
        "| Surface | Class | Status | Path | Validation |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in payload["surfaces"]:
        path_cell = row["path"].replace("|", "\\|")
        if len(path_cell) > 60:
            path_cell = path_cell[:57] + "…"
        lines.append(
            f"| `{row['surface']}` | {row['surface_class']} | {row['status']} | {path_cell} | {row['validation_coverage']} |"
        )
    lines.append("")
    return "\n".join(lines)


def read_stored_fingerprint(repo_root: Path) -> str | None:
    json_path = inventory_json_path(repo_root)
    if not json_path.exists():
        return None
    data = json.loads(json_path.read_text(encoding="utf-8"))
    value = data.get("fingerprint")
    return value if isinstance(value, str) else None


def expected_fingerprint(cards: list[dict], repo_root: Path) -> str:
    rows = build_inventory_rows(
        cards,
        repo_root,
        last_checked=datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    return rows_fingerprint(rows)


def ensure_public_surface_inventory(
    cards: list[dict] | None = None,
    *,
    repo_root: Path | None = None,
    force: bool = False,
) -> tuple[Path, Path, bool]:
    root = repo_root or PACKAGE_ROOT
    cards = cards if cards is not None else load_cards()
    json_path = inventory_json_path(root)
    md_path = inventory_md_path(root)
    payload = render_inventory_payload(cards, root)
    if not force and json_path.exists() and md_path.exists():
        stored = json.loads(json_path.read_text(encoding="utf-8"))
        if stored.get("fingerprint") == payload["fingerprint"]:
            return json_path, md_path, False
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(render_inventory_markdown(payload), encoding="utf-8")
    return json_path, md_path, True


def validate_public_surface_inventory(
    cards: list[dict] | None = None, *, repo_root: Path | None = None
) -> list[str]:
    root = repo_root or PACKAGE_ROOT
    cards = cards if cards is not None else load_cards()
    json_path = inventory_json_path(root)
    md_path = inventory_md_path(root)
    errors: list[str] = []
    if not json_path.exists():
        errors.append(f"missing inventory: {INVENTORY_JSON_REL}")
        return errors
    stored = json.loads(json_path.read_text(encoding="utf-8"))
    current_fp = rows_fingerprint(
        build_inventory_rows(
            cards,
            root,
            last_checked=datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
    )
    if stored.get("fingerprint") != current_fp:
        errors.append(
            f"stale inventory: {INVENTORY_JSON_REL} (run `predictive-history surface-inventory` to refresh)"
        )
    if not md_path.exists():
        errors.append(f"missing inventory summary: {INVENTORY_MD_REL}")
    elif not md_path.read_text(encoding="utf-8").startswith(f"{FINGERPRINT_MARKER} {stored.get('fingerprint')}"):
        errors.append(f"stale inventory summary: {INVENTORY_MD_REL}")
    return errors
