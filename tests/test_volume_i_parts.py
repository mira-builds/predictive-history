from civ_ph.volume_i_parts import (
    chapter_titles_from_spine,
    load_volume_i_parts_registry,
    parse_interwoven_spine,
    validate_volume_i_parts,
)


def test_volume_i_parts_registry_valid():
    errors = validate_volume_i_parts(require_doorways=True, require_chapter_anchors=True)
    assert errors == []


def test_interwoven_spine_covers_sixty_civ_chapters():
    civ_ids = [entry["entry_id"] for entry in parse_interwoven_spine() if entry["kind"] == "civ"]
    assert civ_ids == [f"civ-{n:02d}" for n in range(1, 61)]


def test_part_ii_forward_chain_anchors():
    registry = load_volume_i_parts_registry()
    part_ii = next(part for part in registry["parts"] if part["part_id"] == "part-02-hellenic-world")
    assert part_ii["spine_start"] == "civ-07"
    titles = chapter_titles_from_spine()
    anchors = part_ii["chapter_anchors"][:3]
    assert anchors[0] == f"civ-07 {titles['civ-07']}"
    assert anchors[1] == f"civ-08 {titles['civ-08']}"
    assert anchors[2] == f"civ-09 {titles['civ-09']}"
    assert "Homer" in anchors[0]
    assert part_ii["law_discovery_question"].startswith("How does epic")


def test_part_boundary_tour_aligns_with_registry():
    import json
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    tour = json.loads((root / "data" / "routes" / "part-boundary-tour.json").read_text(encoding="utf-8"))
    registry = load_volume_i_parts_registry()
    assert len(tour["stops"]) == 10
    for stop, part in zip(tour["stops"], registry["parts"], strict=True):
        assert stop["part_id"] == part["part_id"]
        assert stop["route_id"] == part["spine_start"]
