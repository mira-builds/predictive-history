"""Public surface triage — per-chapter curator readiness buckets."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

from .commentary_v2 import SCAFFOLD_VERSION_V2, commentary_metadata
from .data import PACKAGE_ROOT, load_cards, load_choreography
from .ph_civ_index import markdown_frontmatter

TRIAGE_JSON_REL = "data/public-surface-triage.json"
TRIAGE_MD_REL = "runtime/artifacts/public-surface-triage.md"
FINGERPRINT_MARKER = "<!-- public-surface-triage-fingerprint:"
SCHEMA_VERSION = 1
MD_LIST_CAP = 25

MATURITY_RANK = {
    "scaffold": 0,
    "l2_pinned": 1,
    "l3_falsifiers": 2,
    "l6_drafted": 3,
    "in_review": 4,
    "calibration": 5,
}

BUCKET_ORDER = [
    "PUBLIC_READY",
    "OPEN_CANVAS",
    "REVIEW_WITH_CURATOR",
    "PROVISIONAL",
    "NEEDS_ROUTE_REVIEW",
    "NEEDS_SOURCE_FLOOR",
    "NEEDS_CARD_LIMITS",
    "NEEDS_COMMENTARY_REVIEW",
    "STUB_ROUTED",
    "UNASSIGNED",
]

REQUIRED_CARD_SECTIONS = [
    "Where This Sits",
    "Reading Posture",
    "Historical Pressure Points",
    "Limits of the Frame",
    "Return Path",
]

README_MARKERS = [
    "public study doorway",
    "Paste this folder link into ChatGPT, Claude, or Grok",
    "Commentary canvas",
]


def triage_json_path(repo_root: Path | None = None) -> Path:
    return (repo_root or PACKAGE_ROOT) / TRIAGE_JSON_REL


def triage_md_path(repo_root: Path | None = None) -> Path:
    return (repo_root or PACKAGE_ROOT) / TRIAGE_MD_REL


def choreography_source_ids() -> set[str]:
    return {route["source_id"] for route in load_choreography()}


def commentary_has_placeholder(text: str) -> bool:
    return text.count("TBD") >= 5 or "Pending review" in text


def readme_markers_ok(card: dict, repo_root: Path) -> bool:
    paths = card.get("source_paths", {})
    transcript_path = paths.get("source_chapter_path", "")
    commentary_path = paths.get("commentary_path", "")
    if not transcript_path or not commentary_path:
        return False
    folder_path = "/".join(transcript_path.split("/")[:-1])
    if not folder_path.endswith(f"/{card['source_id']}"):
        return True
    if not commentary_path.startswith(f"{folder_path}/"):
        return False
    readme_path = repo_root / folder_path / "README.md"
    if not readme_path.exists():
        return False
    readme_text = readme_path.read_text(encoding="utf-8")
    for marker in README_MARKERS:
        if marker not in readme_text:
            return False
    return True


def missing_source_floor(card: dict, repo_root: Path, meta: dict, text: str) -> bool:
    paths = card.get("source_paths", {})
    transcript_rel = paths.get("source_chapter_path", "")
    if not transcript_rel:
        return True
    if not (repo_root / transcript_rel).exists():
        return True
    depth = meta.get("analysis_depth", "")
    if depth == "layer2_drafted" and card["series"] == "civilization":
        if "## Layer 2" not in text or "| Claim |" not in text:
            return True
    return False


def needs_commentary_review(meta: dict, text: str) -> bool:
    scaffold = meta.get("scaffold_version", "")
    if meta.get("deprecated_part_routing"):
        return True
    if "## Part apparatus" in text:
        return True
    if scaffold == "ph_civ_commentary_canvas_v1":
        return True
    if meta.get("analysis_depth") == "stub_routed_to_part":
        return False
    return False


def assign_chapter_bucket(
    card: dict,
    repo_root: Path,
    *,
    commentary_errors: list[str] | None = None,
) -> str:
    from .cli import validate_commentary_canvas

    source_id = card["source_id"]
    paths = card.get("source_paths", {})
    commentary_rel = paths.get("commentary_path", "")
    review_status = card.get("review_status", "")
    commentary_path = repo_root / commentary_rel if commentary_rel else None
    meta: dict = {}
    text = ""
    if commentary_path and commentary_path.exists():
        meta = commentary_metadata(commentary_path)
        text = commentary_path.read_text(encoding="utf-8")
    errors = commentary_errors
    if errors is None and commentary_path and commentary_path.exists():
        errors = validate_commentary_canvas(source_id, commentary_path)
    else:
        errors = errors or []

    if meta.get("analysis_depth") == "stub_routed_to_part":
        return "STUB_ROUTED"
    if needs_commentary_review(meta, text):
        return "NEEDS_COMMENTARY_REVIEW"
    if review_status == "provisional" and source_id in choreography_source_ids():
        return "NEEDS_ROUTE_REVIEW"
    if review_status == "provisional":
        return "PROVISIONAL"
    if review_status == "in_review" and commentary_has_placeholder(text):
        return "REVIEW_WITH_CURATOR"
    maturity = meta.get("commentary_maturity", "scaffold")
    maturity_rank = MATURITY_RANK.get(maturity, 0)
    canvas_open = "canvas_status" not in markdown_frontmatter(text) or markdown_frontmatter(text).get(
        "canvas_status"
    ) == "open"
    if (
        review_status not in {"provisional", "in_review"}
        and maturity_rank >= MATURITY_RANK["l3_falsifiers"]
        and not errors
        and readme_markers_ok(card, repo_root)
    ):
        return "PUBLIC_READY"
    if canvas_open and (
        maturity == "scaffold"
        or meta.get("analysis_depth") in {"seed", ""}
        or maturity_rank < MATURITY_RANK["l3_falsifiers"]
    ):
        return "OPEN_CANVAS"
    if missing_source_floor(card, repo_root, meta, text):
        return "NEEDS_SOURCE_FLOOR"
    for section in REQUIRED_CARD_SECTIONS:
        if not card.get("sections", {}).get(section):
            return "NEEDS_CARD_LIMITS"
    return "UNASSIGNED"


def build_triage_payload(cards: list[dict], repo_root: Path) -> dict:
    generated_at = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    buckets: dict[str, list[str]] = {name: [] for name in BUCKET_ORDER}
    chapters: list[dict] = []
    for card in sorted(cards, key=lambda c: c["source_id"]):
        bucket = assign_chapter_bucket(card, repo_root)
        buckets.setdefault(bucket, []).append(card["source_id"])
        chapters.append(
            {
                "source_id": card["source_id"],
                "bucket": bucket,
                "review_status": card.get("review_status", ""),
                "part": card["part"],
                "series": card["series"],
            }
        )
    for key in buckets:
        buckets[key] = sorted(buckets[key])
    bucket_counts = {k: len(v) for k, v in buckets.items()}
    stable = {
        "schema_version": SCHEMA_VERSION,
        "card_count": len(cards),
        "bucket_counts": bucket_counts,
        "buckets": buckets,
        "chapters": chapters,
    }
    fingerprint = hashlib.sha256(
        json.dumps(stable, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()
    ).hexdigest()[:16]
    return {
        **stable,
        "fingerprint": fingerprint,
        "generated_at": generated_at,
        "markdown_summary": TRIAGE_MD_REL,
        "inventory_json": "data/public-surface-inventory.json",
    }


def render_triage_markdown(payload: dict) -> str:
    fp = payload["fingerprint"]
    lines = [
        f"{FINGERPRINT_MARKER} {fp} -->",
        "# Public surface triage",
        "",
        f"- **Chapters:** {payload['card_count']}",
        f"- **Generated:** {payload['generated_at']}",
        f"- **Machine SSOT:** [`{TRIAGE_JSON_REL}`](../../{TRIAGE_JSON_REL})",
        f"- **Regenerate:** `predictive-history surface-triage`",
        "",
        "Vocabulary: [public-surface-status.md](../../docs/catalogs/public-surface-status.md).",
        "Rebuild wave queue: `predictive-history commentary-status`.",
        "",
        "## Bucket counts",
        "",
        "| Bucket | Count |",
        "| --- | --- |",
    ]
    for bucket in BUCKET_ORDER:
        count = payload["bucket_counts"].get(bucket, 0)
        if count:
            lines.append(f"| `{bucket}` | {count} |")
    lines.append("")
    for bucket in BUCKET_ORDER:
        ids = payload["buckets"].get(bucket, [])
        if not ids:
            continue
        lines.extend([f"## {bucket}", ""])
        shown = ids[:MD_LIST_CAP]
        for source_id in shown:
            lines.append(f"- `{source_id}`")
        if len(ids) > MD_LIST_CAP:
            lines.append(f"- … and {len(ids) - MD_LIST_CAP} more (see JSON)")
        lines.append("")
    return "\n".join(lines)


def ensure_public_surface_triage(
    cards: list[dict] | None = None,
    *,
    repo_root: Path | None = None,
    force: bool = False,
) -> tuple[Path, Path, bool]:
    root = repo_root or PACKAGE_ROOT
    cards = cards if cards is not None else load_cards()
    json_path = triage_json_path(root)
    md_path = triage_md_path(root)
    payload = build_triage_payload(cards, root)
    if not force and json_path.exists() and md_path.exists():
        stored = json.loads(json_path.read_text(encoding="utf-8"))
        if stored.get("fingerprint") == payload["fingerprint"]:
            return json_path, md_path, False
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(render_triage_markdown(payload), encoding="utf-8")
    return json_path, md_path, True


def validate_public_surface_triage(
    cards: list[dict] | None = None, *, repo_root: Path | None = None
) -> list[str]:
    root = repo_root or PACKAGE_ROOT
    cards = cards if cards is not None else load_cards()
    json_path = triage_json_path(root)
    md_path = triage_md_path(root)
    errors: list[str] = []
    if not json_path.exists():
        errors.append(f"missing triage: {TRIAGE_JSON_REL}")
        return errors
    stored = json.loads(json_path.read_text(encoding="utf-8"))
    current = build_triage_payload(cards, root)
    if stored.get("fingerprint") != current["fingerprint"]:
        errors.append(
            f"stale triage: {TRIAGE_JSON_REL} (run `predictive-history surface-triage` to refresh)"
        )
    if not md_path.exists():
        errors.append(f"missing triage summary: {TRIAGE_MD_REL}")
    elif not md_path.read_text(encoding="utf-8").startswith(
        f"{FINGERPRINT_MARKER} {stored.get('fingerprint')}"
    ):
        errors.append(f"stale triage summary: {TRIAGE_MD_REL}")
    return errors
