"""Tests for public surface inventory and triage."""

from __future__ import annotations

import json
from pathlib import Path

from civ_ph.cli import main
from civ_ph.data import load_cards
from civ_ph.public_surface_inventory import (
    INVENTORY_JSON_REL,
    build_inventory_rows,
    ensure_public_surface_inventory,
    rows_fingerprint,
    static_surface_rows,
    validate_public_surface_inventory,
)
from civ_ph.public_surface_triage import (
    assign_chapter_bucket,
    build_triage_payload,
    ensure_public_surface_triage,
    validate_public_surface_triage,
)

ROOT = Path(__file__).resolve().parents[1]


def test_static_inventory_includes_bootloader_surfaces():
    surfaces = {row["surface"] for row in static_surface_rows()}
    assert "start_here" in surfaces
    assert "llm_experience" in surfaces


def test_inventory_rows_fingerprint_stable_without_last_checked():
    cards = load_cards()
    rows_a = build_inventory_rows(cards, ROOT, last_checked="2026-01-01T00:00:00Z")
    rows_b = build_inventory_rows(cards, ROOT, last_checked="2026-02-01T00:00:00Z")
    assert rows_fingerprint(rows_a) == rows_fingerprint(rows_b)


def test_ensure_inventory_writes_json_with_start_here_path():
    cards = load_cards()
    json_path, _, _ = ensure_public_surface_inventory(cards, repo_root=ROOT, force=True)
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    paths = [row["path"] for row in payload["surfaces"]]
    assert "START-HERE.md" in paths
    assert "data/llm-experience.json" in paths
    assert payload["fingerprint"]
    assert not validate_public_surface_inventory(cards, repo_root=ROOT)


def test_triage_payload_covers_all_cards():
    cards = load_cards()
    payload = build_triage_payload(cards, ROOT)
    assert payload["card_count"] == len(cards)
    assert len(payload["chapters"]) == len(cards)
    assert sum(payload["bucket_counts"].values()) == len(cards)


def test_choreography_provisional_is_needs_route_review():
    cards = {c["source_id"]: c for c in load_cards()}
    card = cards["gt-24"]
    assert card.get("review_status") == "provisional"
    from civ_ph.data import load_choreography

    choreo_ids = {r["source_id"] for r in load_choreography()}
    if "gt-24" in choreo_ids:
        bucket = assign_chapter_bucket(card, ROOT)
        assert bucket == "NEEDS_ROUTE_REVIEW"
    else:
        bucket = assign_chapter_bucket(card, ROOT)
        assert bucket in {"PROVISIONAL", "NEEDS_COMMENTARY_REVIEW", "OPEN_CANVAS"}


def test_ensure_triage_round_trip():
    cards = load_cards()
    json_path, md_path, _ = ensure_public_surface_triage(cards, repo_root=ROOT, force=True)
    assert json_path.exists()
    assert md_path.exists()
    assert not validate_public_surface_triage(cards, repo_root=ROOT)


def test_cli_surface_inventory_check_passes_after_regen(capsys):
    cards = load_cards()
    ensure_public_surface_inventory(cards, repo_root=ROOT, force=True)
    code = main(["surface-inventory", "--check"])
    assert code == 0


def test_cli_validate_surfaces_check(capsys):
    ensure_public_surface_inventory(load_cards(), repo_root=ROOT, force=True)
    ensure_public_surface_triage(load_cards(), repo_root=ROOT, force=True)
    code = main(["validate", "--surfaces", "--check"])
    assert code == 0


def test_inventory_json_rel_matches_constant():
    assert (ROOT / INVENTORY_JSON_REL).exists()
