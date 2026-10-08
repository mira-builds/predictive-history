from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = PACKAGE_ROOT / "data"


@lru_cache(maxsize=1)
def load_cards() -> list[dict]:
    cards: list[dict] = []
    with (DATA_ROOT / "cards.jsonl").open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                cards.append(json.loads(line))
    return cards


def get_card(source_id: str) -> dict:
    for card in load_cards():
        if card["source_id"] == source_id:
            return card
    raise KeyError(source_id)


def card_markdown(source_id: str) -> str:
    path = DATA_ROOT / "cards" / f"{source_id}.md"
    if not path.exists():
        raise KeyError(source_id)
    return path.read_text(encoding="utf-8")


@lru_cache(maxsize=1)
def load_patterns() -> list[dict]:
    path = DATA_ROOT / "patterns.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["patterns"]


def get_pattern(pattern_id: str) -> dict:
    for pattern in load_patterns():
        if pattern["pattern_id"] == pattern_id:
            return pattern
    raise KeyError(pattern_id)


def pattern_markdown(pattern_id: str) -> str:
    path = DATA_ROOT / "patterns" / f"{pattern_id}.md"
    if not path.exists():
        raise KeyError(pattern_id)
    return path.read_text(encoding="utf-8")


def patterns_for_source(source_id: str) -> list[dict]:
    return [
        pattern
        for pattern in load_patterns()
        if source_id in pattern.get("source_ids", [])
    ]


def load_spine(spine_id: str = "homer-to-tolstoy") -> dict:
    path = DATA_ROOT / "spines" / f"{spine_id}.json"
    if not path.exists():
        raise KeyError(spine_id)
    return json.loads(path.read_text(encoding="utf-8"))


def load_surfaces() -> dict:
    return json.loads((DATA_ROOT / "surfaces.json").read_text(encoding="utf-8"))


def load_growth_goals() -> dict:
    return json.loads((DATA_ROOT / "growth-goals.json").read_text(encoding="utf-8"))


def load_bilingual_loop() -> dict:
    return json.loads((DATA_ROOT / "bilingual-loop.json").read_text(encoding="utf-8"))


def load_llm_experience() -> dict:
    return json.loads((DATA_ROOT / "llm-experience.json").read_text(encoding="utf-8"))


def load_course_architecture() -> dict:
    data = load_surfaces()
    deprecated = data.get("deprecated", {}).get("two_volume", {})
    return {
        "repo_identity": data["repo_identity"],
        "primary_artifact": data["primary_artifact"],
        "catalog_hub": data.get("catalog_hub", {}),
        "namespace_slices": data.get("namespace_slices", {}),
        "volumes": deprecated.get("volumes", data.get("volumes", {})),
        "bridge_support_nodes": data["bridge_support_nodes"],
        "deprecated_two_volume": deprecated,
    }


def load_choreography() -> list[dict]:
    return json.loads((DATA_ROOT / "routes" / "choreography.json").read_text(encoding="utf-8"))["routes"]


def load_route_seed() -> dict:
    return json.loads((DATA_ROOT / "routes" / "seed.json").read_text(encoding="utf-8"))


def load_first_tour() -> dict:
    return json.loads((DATA_ROOT / "routes" / "first-tour.json").read_text(encoding="utf-8"))


def get_route(source_id: str) -> dict:
    for route in load_choreography():
        if route["source_id"] == source_id:
            return route
    raise KeyError(source_id)
