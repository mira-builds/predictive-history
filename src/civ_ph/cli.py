from __future__ import annotations

import argparse
import json
import random
import sys
from collections import Counter

from .data import (
    DATA_ROOT,
    card_markdown,
    get_card,
    get_pattern,
    get_route,
    load_bilingual_loop,
    load_cards,
    load_choreography,
    load_course_architecture,
    load_growth_goals,
    load_first_tour,
    load_llm_experience,
    load_patterns,
    load_route_seed,
    load_spine,
    load_surfaces,
    pattern_markdown,
    patterns_for_source,
)
from .commentary_v2 import (
    MATURITY_VALUES,
    SCAFFOLD_VERSION_V2,
    commentary_metadata,
    commentary_status_report,
    infer_maturity,
    validate_v2_pilot,
)
from .ph_civ_index import (
    INDEX_JSON_REL,
    LECTURE_SERIES,
    ensure_all_indexes,
    ensure_ph_civ_index,
    validate_all_indexes,
    validate_no_legacy_chapter_indexes,
    validate_ph_civ_index,
)
from .public_surface_inventory import (
    ensure_public_surface_inventory,
    validate_public_surface_inventory,
)
from .public_surface_triage import (
    ensure_public_surface_triage,
    validate_public_surface_triage,
)
from .volume_i_parts import validate_volume_i_parts
from .reader_namespace_guard import validate_reader_namespace

EXPECTED_SOURCE_REPO = "public-source-capture"  # Neutral metadata marker, not a remote repository.
ALLOWED_CARD_SOURCE_REPOS = frozenset(
    {
        EXPECTED_SOURCE_REPO,
        "operator-supplied-youtube-transcript",
        "mira-builds/predictive-history",
    }
)
GITHUB_TREE_BASE = "https://github.com/mira-builds/predictive-history/tree/main"
GITHUB_BLOB_BASE = "https://github.com/mira-builds/predictive-history/blob/main"

CANONICAL_PUBLIC_ID = "predictive-history"

NAMESPACE_SERIES = {
    "lectures": set(LECTURE_SERIES),
    "essays": {"essays"},
    "interviews": {"interviews"},
}

PROMPT_MODES = {
    "study": "Create a study plan that helps me understand this Predictive History orientation card without treating it as a substitute for the source lecture.",
    "seminar": "Write seminar questions that test the card's framing, pressure points, and limits.",
    "creative": "Generate creative project prompts inspired by this card, preserving the card's limits and avoiding unsupported claims.",
    "counter-reading": "Develop counter-readings and skeptical questions that keep the card grounded in its stated limits.",
}

_surfaces_root = load_surfaces()
SURFACES = _surfaces_root.get("deprecated", {}).get("two_volume", {}).get(
    "surfaces",
    _surfaces_root.get("surfaces", {}),
)

VOLUME_ALIASES = {
    "volume-i": "volume_i",
    "volume-ii": "volume_ii",
    "volume_i": "volume_i",
    "volume_ii": "volume_ii",
}

COMMENTARY_CANVAS_FIELDS = {
    "canvas_status": "open",
    "scaffold_version": "ph_civ_commentary_canvas_v1",
}

ALLOWED_ANALYSIS_DEPTHS = frozenset(
    {"seed", "layer2_slimmed", "layer2_drafted", "stub_routed_to_part"}
)

PILOT_V2_SOURCE_IDS = frozenset({"civ-07", "civ-22", "civ-29", "gb-02", "gt-24", "sh-17"})

COMMENTARY_CANVAS_HEADINGS = [
    "## Project Canvas",
    "### Project Leverage",
    "### Laws / Patterns Exposed",
    "### Volume Role",
    "### Strategy / Present-Day Application",
    "### Counter-Readings",
    "### Open Questions",
    "### Build Notes / Future Enhancements",
]

PUBLIC_BOUNDARY_SCAN_PATHS = [
    "AGENTS.md",
    "README.md",
    "START-HERE.md",
    "llms.txt",
    "llms-full.txt",
    "book",
    "data",
    "docs",
    "lectures",
    "ph-civ",
    "ph-apo",
    "prompts",
    "schemas",
]

PUBLIC_BOUNDARY_SCAN_EXCLUDES = {
    "docs/methodology/strategy-codex-bridge.md",
    "docs/methodology/jiang-analysis-index.md",
    "docs/strategy-codex-bridge.md",
    "docs/jiang-analysis-index.md",
    "docs/catalogs/public-surface-status.md",
    "data/public-surface-inventory.json",
    "data/public-surface-triage.json",
}

PUBLIC_BOUNDARY_FORBIDDEN_MARKERS = [
    "strategy_codex",
    "strategy-codex",
    "Strategy-Codex",
    "transfer_lecture_path",
    "strategy_codex_lecture_path",
    "strategy_codex_analysis_path",
    "strategy_codex_evidence_pack_path",
    "exported_from_strategy_codex_at",
    "raw-input",
    "recursion-gate",
    "self-memory",
    "session-log",
    "C:\\",
    "C:/",
]

ALLOWED_ROUTE_TYPES = {"spine", "paired_close_reading", "application", "coda"}


def warn_deprecated_two_volume_part(part: str) -> None:
    print(
        f"warning: --part {part} is deprecated; use --series, --namespace, or full catalog. "
        "See docs/migrations/PH-SURFACE-RETIREMENT.md",
        file=sys.stderr,
    )


def warn_deprecated_cli_shim(name: str) -> None:
    print(
        f"warning: {name} CLI is deprecated; use predictive-history. "
        "See docs/migrations/PH-SURFACE-RETIREMENT.md",
        file=sys.stderr,
    )


def card_surface(card: dict) -> str:
    if card["part"] == "provenance":
        return "provenance"
    return "ph-civ" if card["part"] == "civilization" else "ph-apo"


def bridge_support_ids() -> set[str]:
    return set(load_course_architecture()["bridge_support_nodes"])


def conceptual_volume_ids(card: dict) -> list[str]:
    if card["part"] == "provenance":
        return []
    volumes: list[str] = []
    if card["part"] == "civilization" or card["source_id"] in bridge_support_ids():
        volumes.append("volume_i")
    if card["part"] == "world-war":
        volumes.append("volume_ii")
    return volumes


def conceptual_bridge_role(card: dict) -> str | None:
    if card["source_id"] in bridge_support_ids():
        return "volume_i_bridge_support"
    return None


def cards_for_volume(volume_id: str) -> list[dict]:
    canonical = VOLUME_ALIASES.get(volume_id)
    if not canonical:
        raise KeyError(volume_id)
    return [card for card in load_cards() if canonical in conceptual_volume_ids(card)]


def markdown_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    return fields


def validate_commentary_canvas(source_id: str, commentary_path) -> list[str]:
    text = commentary_path.read_text(encoding="utf-8").replace("\r\n", "\n")
    frontmatter = markdown_frontmatter(text)
    errors: list[str] = []
    if "commentary_status" not in frontmatter:
        errors.append(f"{source_id} missing commentary_status")
    scaffold = frontmatter.get("scaffold_version", "")
    if scaffold not in {"ph_civ_commentary_canvas_v1", SCAFFOLD_VERSION_V2}:
        errors.append(f"{source_id} invalid scaffold_version: {scaffold}")
    if frontmatter.get("canvas_status") != "open":
        errors.append(f"{source_id} invalid canvas_status: {frontmatter.get('canvas_status')}")
    depth = frontmatter.get("analysis_depth", "")
    if depth not in ALLOWED_ANALYSIS_DEPTHS:
        errors.append(f"{source_id} invalid analysis_depth: {depth}")
    if depth == "stub_routed_to_part":
        return errors
    thin_canvas = (
        "## Project Canvas (chapter-local)" in text
        or depth == "layer2_slimmed"
        or (
            scaffold == SCAFFOLD_VERSION_V2
            and "## Project Canvas (chapter-local)" in text
        )
    )
    if thin_canvas:
        thin_headings = ["## Project Canvas (chapter-local)", "### Open Questions"]
        build_note_headings = ("### Build Notes", "### Build Notes / Future Enhancements")
        for heading in thin_headings:
            if heading not in text:
                errors.append(f"{source_id} missing thin commentary canvas heading: {heading}")
        if not any(marker in text for marker in build_note_headings):
            errors.append(f"{source_id} missing thin commentary canvas heading: ### Build Notes")
        return errors
    for heading in COMMENTARY_CANVAS_HEADINGS:
        if heading not in text:
            errors.append(f"{source_id} missing commentary canvas heading: {heading}")
    return errors


def validate_public_boundary() -> list[str]:
    root = DATA_ROOT.parent
    errors: list[str] = []
    for relative_root in PUBLIC_BOUNDARY_SCAN_PATHS:
        scan_root = root / relative_root
        if not scan_root.exists():
            continue
        paths = [scan_root] if scan_root.is_file() else scan_root.rglob("*")
        for path in paths:
            if not path.is_file():
                continue
            relative_path = path.relative_to(root).as_posix()
            if relative_path in PUBLIC_BOUNDARY_SCAN_EXCLUDES:
                continue
            if path.suffix not in {".json", ".jsonl", ".md", ".py", ".txt", ".yaml", ".yml"}:
                continue
            text = path.read_text(encoding="utf-8")
            for marker in PUBLIC_BOUNDARY_FORBIDDEN_MARKERS:
                if marker in text:
                    errors.append(
                        f"public boundary leak: {relative_path} contains {marker}"
                    )
    return errors


def visible_cards(surface_scope: str | None = None, include_all: bool = False) -> list[dict]:
    cards = load_cards()
    if include_all or surface_scope is None:
        return cards
    if surface_scope == "ph-civ":
        return [card for card in cards if card["part"] == "civilization"]
    if surface_scope == "ph-apo":
        return [card for card in cards if card["part"] == "world-war"]
    return cards


def route_public_payload(route: dict) -> dict:
    card = get_card(route["source_id"])
    return {
        "source_id": route["source_id"],
        "title": card["title"],
        "surface": route["surface"],
        "part": card["part"],
        "series": card["series"],
        "conceptual_volumes": conceptual_volume_ids(card),
        "bridge_role": conceptual_bridge_role(card),
        "route_type": route["route_type"],
        "caveat": route.get("caveat", ""),
        "what_changes_here": route["what_changes_here"],
        "card": {
            "path": route["card_path"],
            "transcript_path": route["transcript_path"],
            "commentary_path": route["commentary_path"],
        },
        "pressure_echoes": route.get("pressure_echoes", []),
        "civilization_roots": route.get("civilization_roots", []),
    }


def chapter_folder_link_payload(card: dict) -> dict:
    paths = card.get("source_paths", {})
    transcript_path = paths.get("source_chapter_path", "")
    commentary_path = paths.get("commentary_path", "")
    transcript_file = DATA_ROOT.parent / transcript_path
    source_video_url = None
    if transcript_file.exists():
        source_video_url = markdown_frontmatter(
            transcript_file.read_text(encoding="utf-8")
        ).get("source_url")
    folder_path = "/".join(transcript_path.split("/")[:-1])
    is_essay = card.get("series") == "essays"
    if is_essay:
        folder_ready = bool(transcript_path and transcript_file.exists())
        github_folder_url = None
        github_transcript_url = (
            f"{GITHUB_BLOB_BASE}/{transcript_path}" if folder_ready else None
        )
    else:
        folder_ready = bool(
            folder_path
            and folder_path.endswith(f"/{card['source_id']}")
            and commentary_path.startswith(f"{folder_path}/")
            and (DATA_ROOT.parent / folder_path / "README.md").exists()
        )
        github_folder_url = f"{GITHUB_TREE_BASE}/{folder_path}" if folder_ready else None
        github_transcript_url = None
    provisional = card.get("review_status") == "provisional"
    review_note = (
        " The packet is provisional, so use the review status and guardrails before quoting it."
        if provisional
        else ""
    )
    if is_essay:
        share_url = github_transcript_url or "[essay not ready]"
        suggested_llm_prompt = (
            f"Guide me through the {card['source_id']} public essay packet. "
            "Start with the essay body, then use the commentary canvas in commentaries/ "
            "and the orientation card guardrails. Keep provisional claims bounded and "
            "separate source representation from verification."
        )
        suggested_youtube_comment = (
            f"{card['title']} is a useful Predictive History essay for studying civilizational "
            "pattern under pressure.\n\n"
            "Public essay body:\n"
            f"{share_url}\n\n"
            "Paste the link into ChatGPT, Claude, or Grok and ask it to guide you through "
            f"the essay, commentary canvas, and card guardrails.{review_note} "
            "It is part of Predictive History, a public LLM-native reader."
        )
    else:
        suggested_llm_prompt = (
            f"Guide me through the {card['source_id']} chapter folder as a public study packet. "
            "Start with the transcript, then use the commentary canvas and orientation/card "
            "guardrails. Keep provisional claims bounded and separate lecture representation "
            "from verification."
        )
        suggested_youtube_comment = (
            f"{card['title']} is a useful place to study how this lecture turns historical "
            "pattern into strategic pressure.\n\n"
            "There is a public reader packet for following it without losing the thread:\n"
            f"{github_folder_url or '[folder not ready]'}\n\n"
            "Paste the folder link into ChatGPT, Claude, or Grok and ask it to guide you "
            f"through the chapter using the transcript, commentary canvas, and guardrails.{review_note} "
            "It is part of Predictive History, a public LLM-native reader."
        )
    return {
        "source_id": card["source_id"],
        "title": card["title"],
        "surface": card_surface(card),
        "series": card["series"],
        "part": card["part"],
        "review_status": card.get("review_status"),
        "folder_ready": folder_ready,
        "chapter_folder_path": folder_path if folder_ready and not is_essay else None,
        "github_folder_url": github_folder_url,
        "github_transcript_url": github_transcript_url,
        "source_video_url": source_video_url,
        "transcript_path": transcript_path,
        "commentary_path": commentary_path,
        "card_path": f"data/cards/{card['source_id']}.md",
        "suggested_llm_prompt": suggested_llm_prompt,
        "suggested_youtube_comment": suggested_youtube_comment,
    }


def first_tour_payload() -> dict:
    tour = load_first_tour()
    routes_by_id = {route["source_id"]: route for route in load_choreography()}
    stops = []
    for stop in tour["stops"]:
        source_id = stop["source_id"]
        card = get_card(source_id)
        route = routes_by_id[source_id]
        stops.append(
            {
                **stop,
                "title": card["title"],
                "surface": route["surface"],
                "route_type": route["route_type"],
                "caveat": route.get("caveat", ""),
                "what_changes_here": route["what_changes_here"],
                "card_path": route["card_path"],
                "transcript_path": route["transcript_path"],
                "commentary_path": route["commentary_path"],
            }
        )
    return {**tour, "stops": stops}


def emit_json(data) -> int:
    print(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


def cmd_list(args) -> int:
    cards = visible_cards(getattr(args, "surface_scope", None), getattr(args, "all", False))
    if args.series:
        cards = [card for card in cards if card["series"] == args.series]
    namespace = getattr(args, "namespace", None)
    if namespace:
        allowed = NAMESPACE_SERIES[namespace]
        cards = [card for card in cards if card.get("series") in allowed]
    if args.spine:
        ids = {sid for node in load_spine()["sequence"] for sid in node["source_ids"]}
        cards = [card for card in cards if card["source_id"] in ids]
    rows = [{"source_id": card["source_id"], "title": card["title"], "series": card["series"], "part": card["part"]} for card in cards]
    if args.json:
        return emit_json(rows)
    for row in rows:
        print(f"{row['source_id']}\t{row['series']}\t{row['part']}\t{row['title']}")
    return 0


def cmd_show(args) -> int:
    try:
        card = get_card(args.source_id)
        scope = getattr(args, "surface_scope", None)
        if scope in {"ph-civ", "ph-apo"} and card_surface(card) != scope:
            print(f"{args.source_id} is not available through {scope}", file=sys.stderr)
            return 2
        if args.format == "json":
            return emit_json(card)
        print(card_markdown(args.source_id), end="")
        return 0
    except KeyError:
        print(f"Unknown source_id: {args.source_id}", file=sys.stderr)
        return 2


def cmd_search(args) -> int:
    q = args.query.casefold()
    matches = []
    for card in visible_cards(getattr(args, "surface_scope", None), getattr(args, "all", False)):
        haystack = "\n".join([card["source_id"], card["title"], json.dumps(card["sections"], ensure_ascii=False)]).casefold()
        if q in haystack and (not args.series or card["series"] == args.series):
            namespace = getattr(args, "namespace", None)
            if namespace and card.get("series") not in NAMESPACE_SERIES[namespace]:
                continue
            matches.append({"source_id": card["source_id"], "title": card["title"], "series": card["series"], "part": card["part"]})
    if args.json:
        return emit_json(matches)
    for match in matches:
        print(f"{match['source_id']}\t{match['series']}\t{match['title']}")
    return 0


def cmd_route(args) -> int:
    try:
        route = get_route(args.source_id)
    except KeyError:
        print(f"No public route for source_id: {args.source_id}", file=sys.stderr)
        return 2

    scope = getattr(args, "surface_scope", None)
    if (
        scope in {"ph-civ", "ph-apo"}
        and route["surface"] != scope
        and not (scope == "ph-civ" and route["source_id"] in bridge_support_ids())
    ):
        print(f"{args.source_id} is routed through {route['surface']}, not {scope}", file=sys.stderr)
        return 2
    payload = route_public_payload(route)
    if args.json:
        return emit_json(payload)
    print(f"{payload['source_id']}\t{payload['surface']}\t{payload['title']}")
    print(f"route_type: {payload['route_type']}")
    if payload.get("caveat"):
        print(f"caveat: {payload['caveat']}")
    print(f"what changes here: {payload['what_changes_here']}")
    return 0


def cmd_link(args) -> int:
    try:
        card = get_card(args.source_id)
    except KeyError:
        print(f"Unknown source_id: {args.source_id}", file=sys.stderr)
        return 2
    payload = chapter_folder_link_payload(card)
    if args.json:
        return emit_json(payload)
    if not payload["folder_ready"]:
        print(f"{args.source_id} does not have a dedicated chapter folder yet.", file=sys.stderr)
        return 2
    print(f"{payload['source_id']}\t{payload['title']}")
    if payload.get("source_video_url"):
        print(f"source_video: {payload['source_video_url']}")
    if payload.get("github_transcript_url"):
        print(f"essay: {payload['github_transcript_url']}")
    elif payload.get("github_folder_url"):
        print(f"folder: {payload['github_folder_url']}")
    print(f"review_status: {payload['review_status']}")
    print("")
    print("LLM prompt:")
    print(payload["suggested_llm_prompt"])
    print("")
    print("YouTube comment:")
    print(payload["suggested_youtube_comment"])
    return 0


def cmd_patterns(args) -> int:
    patterns = load_patterns()
    rows = [
        {
            "pattern_id": pattern["pattern_id"],
            "title": pattern["title"],
            "source_ids": pattern["source_ids"],
            "public_status": pattern["public_status"],
        }
        for pattern in patterns
    ]
    if args.json:
        return emit_json(rows)
    for row in rows:
        print(
            f"{row['pattern_id']}\t{row['public_status']}\t"
            f"{','.join(row['source_ids'])}\t{row['title']}"
        )
    return 0


def cmd_pattern(args) -> int:
    try:
        pattern = get_pattern(args.pattern_id)
        if args.format == "json":
            return emit_json(pattern)
        print(pattern_markdown(args.pattern_id), end="")
        return 0
    except KeyError:
        print(f"Unknown pattern_id: {args.pattern_id}", file=sys.stderr)
        return 2


def cmd_bridge(args) -> int:
    try:
        card = get_card(args.source_id)
    except KeyError:
        print(f"Unknown source_id: {args.source_id}", file=sys.stderr)
        return 2
    payload = {
        "source_id": card["source_id"],
        "title": card["title"],
        "patterns": patterns_for_source(card["source_id"]),
    }
    output_format = "json" if args.json else args.format
    if output_format == "json":
        return emit_json(payload)
    print(f"# {payload['source_id']} - {payload['title']}")
    print()
    print("Public bridge patterns:")
    for pattern in payload["patterns"]:
        print(f"- `{pattern['pattern_id']}` - {pattern['title']}")
    if not payload["patterns"]:
        print("- No public bridge patterns currently cite this source.")
    return 0




def cmd_prompt(args) -> int:
    try:
        card = get_card(args.source_id)
    except KeyError:
        print(f"Unknown source_id: {args.source_id}", file=sys.stderr)
        return 2
    print(
        f"{PROMPT_MODES[args.mode]}\n\n"
        f"Source ID: {card['source_id']}\n"
        f"Title: {card['title']}\n"
        f"Placement weight: {card['placement_weight']}\n\n"
        f"Where this sits:\n{card['sections']['Where This Sits']}\n\n"
        f"Limits:\n{card['sections']['Limits of the Frame']}"
    )
    return 0


def cmd_spark(args) -> int:
    try:
        card = get_card(args.source_id)
    except KeyError:
        print(f"Unknown source_id: {args.source_id}", file=sys.stderr)
        return 2
    seeds = [
        "What pattern becomes visible here?",
        "What would change if the lecture's main analogy were weaker?",
        "Which pressure point deserves a diagram?",
        "What should a reader verify before quoting this?",
        "What does this card make easier to return to later?",
        "What object, map, or document would make this lecture legible at a glance?",
    ]
    random.seed(card["source_id"])
    for index, prompt in enumerate(random.sample(seeds, k=min(args.count, len(seeds))), start=1):
        print(f"{index}. {prompt}")
    return 0


def cmd_spine(args) -> int:
    spine = load_spine(args.spine_id)
    if args.json:
        return emit_json(spine)
    print(f"# {spine['title']}\n")
    print(spine["description"])
    if spine.get("guardrail"):
        print("")
        print(f"guardrail: {spine['guardrail']}")
    if spine.get("launch_readiness"):
        print(f"launch_readiness: {spine['launch_readiness']}")
    if spine.get("first_reader_gap"):
        print(f"first_reader_gap: {spine['first_reader_gap']}")
    print("")
    for index, node in enumerate(spine["sequence"], start=1):
        print(f"{index}. {node['author']}: {', '.join(node['source_ids'])}")
        if node.get("note"):
            print(f"   {node['note']}")
    return 0


def cmd_path(args) -> int:
    if args.path_id != "homer-to-tolstoy":
        print(f"Unknown path: {args.path_id}", file=sys.stderr)
        return 2
    return cmd_spine(argparse.Namespace(spine_id=args.path_id, json=args.json))


def cmd_index(args) -> int:
    cards = load_cards()
    if args.check:
        errors = validate_all_indexes(cards)
        if args.json:
            emit_json({"status": "current" if not errors else "stale", "errors": errors})
            return 1 if errors else 0
        if errors:
            for error in errors:
                print(f"error: {error}", file=sys.stderr)
            return 1
        print("status: current")
        return 0

    written = ensure_all_indexes(cards, force=args.force)
    path = DATA_ROOT.parent / "docs" / "predictive-history-index.md"
    json_path = DATA_ROOT.parent / INDEX_JSON_REL
    payload = {
        "status": "written" if written else "unchanged",
        "markdown_path": str(path.relative_to(DATA_ROOT.parent)),
        "json_path": str(json_path.relative_to(DATA_ROOT.parent)),
        "card_count": len(cards),
    }
    if args.json:
        emit_json(payload)
        return 0
    action = "wrote" if written else "unchanged"
    print(f"{action} {payload['markdown_path']} and {payload['json_path']} ({len(cards)} chapters)")
    return 0


def cmd_commentary_status(args) -> int:
    cards = load_cards()
    report = commentary_status_report(cards, DATA_ROOT.parent)
    if args.json:
        emit_json(report)
        return 0
    print(f"total: {report['total']}")
    print("by_commentary_maturity:")
    for key, value in report["by_commentary_maturity"].items():
        print(f"  {key}: {value}")
    print("by_scaffold_version:")
    for key, value in report["by_scaffold_version"].items():
        print(f"  {key}: {value}")
    print("wave_queue:")
    for queue, ids in report["wave_queue"].items():
        print(f"  {queue}: {len(ids)}")
        if args.verbose and ids:
            for source_id in ids:
                print(f"    - {source_id}")
    return 0


def cmd_validate(args) -> int:
    cards = load_cards()
    errors = []
    ids = set()
    required = ["Where This Sits", "Reading Posture", "Historical Pressure Points", "Limits of the Frame", "Return Path"]
    for card in cards:
        source_id = card.get("source_id")
        if not source_id:
            errors.append("card missing source_id")
            continue
        if source_id in ids:
            errors.append(f"duplicate source_id: {source_id}")
        ids.add(source_id)
        for section in required:
            if not card.get("sections", {}).get(section):
                errors.append(f"{source_id} missing section: {section}")
        if card.get("placement_weight") not in {"strong", "medium", "light"}:
            errors.append(f"{source_id} invalid placement_weight: {card.get('placement_weight')}")
        source_repo = card.get("source_snapshot", {}).get("repo")
        if source_repo not in ALLOWED_CARD_SOURCE_REPOS:
            errors.append(f"{source_id} invalid source repo: {source_repo}")
        source_paths = card.get("source_paths", {})
        transcript_path = source_paths.get("source_chapter_path")
        commentary_path = source_paths.get("commentary_path")
        for label, relative_path in [
            ("transcript", transcript_path),
            ("commentary", commentary_path),
        ]:
            if not relative_path:
                errors.append(f"{source_id} missing {label} path")
                continue
            chapter_path = DATA_ROOT.parent / relative_path
            if not chapter_path.exists():
                errors.append(f"{source_id} missing {label} file: {relative_path}")
            elif label == "commentary":
                errors.extend(validate_commentary_canvas(source_id, chapter_path))
        if transcript_path and commentary_path:
            folder_path = "/".join(transcript_path.split("/")[:-1])
            if folder_path.endswith(f"/{source_id}") and commentary_path.startswith(f"{folder_path}/"):
                readme_path = DATA_ROOT.parent / folder_path / "README.md"
                if not readme_path.exists():
                    errors.append(f"{source_id} missing chapter folder README: {folder_path}/README.md")
                else:
                    readme_text = readme_path.read_text(encoding="utf-8")
                    transcript_file = DATA_ROOT.parent / transcript_path
                    source_url = ""
                    if transcript_file.exists():
                        source_url = markdown_frontmatter(
                            transcript_file.read_text(encoding="utf-8")
                        ).get("source_url", "")
                    if source_url and (
                        ("## Source Video" not in readme_text and "## Source" not in readme_text)
                        or source_url not in readme_text
                    ):
                        errors.append(f"{source_id} chapter folder README must surface source URL")
                    for marker in [
                        "public study doorway",
                        "Paste this folder link into ChatGPT, Claude, or Grok",
                        "Commentary canvas",
                    ]:
                        if marker not in readme_text:
                            errors.append(f"{source_id} chapter folder README missing marker: {marker}")
    for metadata_path in [
        DATA_ROOT / "surfaces.json",
        DATA_ROOT / "routes" / "choreography.json",
    ]:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        source_repo = metadata.get("source_snapshot", {}).get("repo")
        if source_repo != EXPECTED_SOURCE_REPO:
            errors.append(f"{metadata_path.relative_to(DATA_ROOT)} invalid source repo: {source_repo}")
    choreography = load_choreography()
    route_ids = [route.get("source_id") for route in choreography]
    if len(choreography) != 10:
        errors.append(f"choreography route count must be 10: {len(choreography)}")
    if len(set(route_ids)) != len(route_ids):
        errors.append("choreography route IDs must be unique")
    for route in choreography:
        source_id = route.get("source_id")
        route_type = route.get("route_type")
        if route_type not in ALLOWED_ROUTE_TYPES:
            errors.append(f"{source_id} invalid route_type: {route_type}")
        if not route.get("caveat"):
            errors.append(f"{source_id} missing route caveat")
    route_seed = load_route_seed()
    seed_route_ids = route_seed.get("route_ids", [])
    if route_seed.get("seed_id") != "ten_route_spine_seed":
        errors.append("route seed must be ten_route_spine_seed")
    if seed_route_ids != route_ids:
        errors.append("route seed IDs must match choreography route IDs in order")
    first_tour = load_first_tour()
    if first_tour.get("tour_id") != "first_tour_ten_route_spine":
        errors.append("first tour must use first_tour_ten_route_spine")
    if first_tour.get("mode") != "first_tour":
        errors.append("first tour must use first_tour mode")
    if first_tour.get("seed_id") != route_seed.get("seed_id"):
        errors.append("first tour seed_id must match route seed")
    if first_tour.get("opening_route") != "civ-07":
        errors.append("first tour must open at civ-07")
    if first_tour.get("opening_path") != "homer-to-tolstoy":
        errors.append("first tour must open Homer-to-Tolstoy")
    tour_stop_ids = [stop.get("source_id") for stop in first_tour.get("stops", [])]
    if tour_stop_ids != seed_route_ids:
        errors.append("first tour stops must match route seed order")
    phase_ids = [source_id for phase in first_tour.get("phases", []) for source_id in phase.get("route_ids", [])]
    if phase_ids != seed_route_ids:
        errors.append("first tour phases must cover route seed in order")
    if "civ-07" not in first_tour.get("continue_prompt", ""):
        errors.append("first tour continue prompt must open civ-07")
    first_tour_doc = DATA_ROOT.parent / "docs" / "onboarding" / "first-tour.md"
    if not first_tour_doc.exists():
        errors.append("docs/onboarding/first-tour.md must exist")
    else:
        first_tour_text = first_tour_doc.read_text(encoding="utf-8")
        for marker in [
            "First-Tour Response Shape",
            "First tour, stop 1: civ-07",
            "Continue to civ-17",
            "namespace catalog hub",
        ]:
            if marker not in first_tour_text:
                errors.append(f"docs/onboarding/first-tour.md missing marker: {marker}")
    llm_experience = load_llm_experience()
    if not (DATA_ROOT.parent / "START-HERE.md").exists():
        errors.append("START-HERE.md must exist as the LLM bootloader")
    if llm_experience.get("start_here") != "START-HERE.md":
        errors.append("llm-experience.json must point to START-HERE.md")
    full_context = llm_experience.get("full_context", {})
    if full_context.get("path") != "llms-full.txt":
        errors.append("llm-experience.json must point to llms-full.txt")
    full_context_path = DATA_ROOT.parent / "llms-full.txt"
    if not full_context_path.exists():
        errors.append("llms-full.txt must exist as the full LLM context packet")
    if llm_experience.get("primary_artifact") != "namespace_catalog":
        errors.append("llm-experience.json invalid primary_artifact")
    first_response = llm_experience.get("first_response_contract", {})
    if first_response.get("default_mode") != "first_tour":
        errors.append("llm-experience first response must default to first_tour")
    if "generic repository summary" not in first_response.get("anti_pattern", ""):
        errors.append("llm-experience must forbid summary-only pasted-URL responses")
    if first_response.get("required_opening_files") != [
        "START-HERE.md",
        "llms.txt",
        "llms-full.txt",
    ]:
        errors.append("llm-experience first response must cite all opening files")
    if first_response.get("opening_route") != "civ-07":
        errors.append("llm-experience first response must open at civ-07")
    if first_response.get("opening_path") != "homer-to-tolstoy":
        errors.append("llm-experience first response must open Homer-to-Tolstoy")
    if not any("Choose one:" in line for line in first_response.get("template", [])):
        errors.append("llm-experience first response template must offer reader choices")
    llm_first_tour = llm_experience.get("first_tour", {})
    if llm_first_tour.get("path") != "data/routes/first-tour.json":
        errors.append("llm-experience first_tour must point to data/routes/first-tour.json")
    if llm_first_tour.get("reader_doc") != "docs/onboarding/first-tour.md":
        errors.append("llm-experience first_tour must point to docs/onboarding/first-tour.md")
    if llm_first_tour.get("opening_route") != "civ-07":
        errors.append("llm-experience first_tour must open at civ-07")
    chapter_folder_links = llm_experience.get("chapter_folder_links", {})
    if chapter_folder_links.get("reader_doc") != "docs/onboarding/chapter-folder-links.md":
        errors.append("llm-experience chapter_folder_links must point to docs/onboarding/chapter-folder-links.md")
    if chapter_folder_links.get("default_mode") != "study":
        errors.append("llm-experience chapter_folder_links must default to study")
    if "predictive-history link" not in chapter_folder_links.get("cli", ""):
        errors.append("llm-experience chapter_folder_links must expose predictive-history link")
    chapter_catalog = llm_experience.get("chapter_catalog", {})
    if chapter_catalog.get("json_path") != "docs/predictive-history-index.json":
        errors.append("llm-experience chapter_catalog must point to docs/predictive-history-index.json")
    if chapter_catalog.get("markdown_path") != "docs/predictive-history-index.md":
        errors.append("llm-experience chapter_catalog must point to docs/predictive-history-index.md")
    if chapter_catalog.get("not_replacement_for") != "first_tour":
        errors.append("llm-experience chapter_catalog must not replace first_tour")
    if "predictive-history index" not in chapter_catalog.get("cli", ""):
        errors.append("llm-experience chapter_catalog must expose predictive-history index")
    catalog_json = DATA_ROOT.parent / "docs" / "predictive-history-index.json"
    if not catalog_json.exists():
        errors.append("docs/predictive-history-index.json must exist as the chapter catalog")
    else:
        catalog_payload = json.loads(catalog_json.read_text(encoding="utf-8"))
        if catalog_payload.get("card_count") != len(cards):
            errors.append("docs/predictive-history-index.json card_count must match cards.jsonl")
        if len(catalog_payload.get("chapters", [])) != len(cards):
            errors.append("docs/predictive-history-index.json chapters must match cards.jsonl")
        if catalog_payload.get("primary_artifact") != "namespace_catalog":
            errors.append("docs/predictive-history-index.json must declare namespace_catalog primary_artifact")
        if not catalog_payload.get("by_series"):
            errors.append("docs/predictive-history-index.json must include by_series aggregation")
        if not catalog_payload.get("by_surface"):
            errors.append("docs/predictive-history-index.json must retain deprecated by_surface mirror")
    catalog_md = DATA_ROOT.parent / "docs" / "predictive-history-index.md"
    if not catalog_md.exists():
        errors.append("docs/predictive-history-index.md must exist as the chapter catalog")
    else:
        catalog_md_text = catalog_md.read_text(encoding="utf-8")
        for marker in [
            "Predictive History Chapter Index",
            "Namespace slice indexes",
            "Deprecated reader frame",
            "## Full alphabetical index",
            "predictive-history-index.json",
        ]:
            if marker not in catalog_md_text:
                errors.append(f"docs/predictive-history-index.md missing marker: {marker}")
    unfolding_map = llm_experience.get("unfolding_map", [])
    for required_path in ["docs/predictive-history-index.json", "docs/predictive-history-index.md"]:
        if required_path not in unfolding_map:
            errors.append(f"llm-experience unfolding_map must include {required_path}")
    study_mode = next((mode for mode in llm_experience.get("modes", []) if mode.get("mode") == "study"), {})
    if "docs/predictive-history-index.json" not in study_mode.get("start_files", []):
        errors.append("llm-experience study mode must start from docs/predictive-history-index.json")
    catalog_mode = next((mode for mode in llm_experience.get("modes", []) if mode.get("mode") == "catalog"), None)
    if catalog_mode is None:
        errors.append("llm-experience must define catalog mode")
    elif catalog_mode.get("start_files") != ["docs/predictive-history-index.json", "docs/predictive-history-index.md"]:
        errors.append("llm-experience catalog mode must start from chapter index files")
    full_context_text = full_context_path.read_text(encoding="utf-8") if full_context_path.exists() else ""
    if full_context_path.exists():
        for marker in [
            "full one-shot LLM context packet",
            "First Response Contract",
            "Do not stop at a generic repository summary",
            "Default mode: `first_tour`",
            "Homer to Tolstoy is the literary spine route",
            "namespace catalog hub",
            "docs/predictive-history-index.json",
            "Chapter Catalog",
        ]:
            if marker not in full_context_text:
                errors.append(f"llms-full.txt missing marker: {marker}")
    chapter_folder_doc = DATA_ROOT.parent / "docs" / "onboarding" / "chapter-folder-links.md"
    if not chapter_folder_doc.exists():
        errors.append("docs/onboarding/chapter-folder-links.md must exist")
    else:
        chapter_folder_text = chapter_folder_doc.read_text(encoding="utf-8")
        for marker in [
            "chapter-folder URL",
            "YouTube comment",
            "paste the folder link into ChatGPT, Claude, or Grok",
            "not a replacement for `first_tour`",
        ]:
            if marker not in chapter_folder_text:
                errors.append(f"docs/onboarding/chapter-folder-links.md missing marker: {marker}")
    errors.extend(validate_no_legacy_chapter_indexes(repo_root=DATA_ROOT.parent))
    bilingual = load_bilingual_loop()
    if bilingual.get("loop_id") != "english_chinese_civilizational_bridge":
        errors.append("bilingual-loop.json invalid loop_id")
    if bilingual.get("bridge_id") != "trilingual_civilizational_bridge":
        errors.append("bilingual-loop.json invalid bridge_id")
    if bilingual.get("language_scope") != "trilingual":
        errors.append("bilingual-loop.json must be trilingual")
    if bilingual.get("posture") != "civilizational_bridge":
        errors.append("bilingual-loop.json invalid posture")
    if bilingual.get("status") != "ambition_metadata":
        errors.append("bilingual-loop.json invalid status")
    if bilingual.get("canonical_source") != CANONICAL_PUBLIC_ID:
        errors.append("bilingual-loop.json must name predictive-history as canonical_source")
    canonical_surface = bilingual.get("canonical_language_surface", {})
    if canonical_surface.get("surface") != CANONICAL_PUBLIC_ID or canonical_surface.get("locale") != "en":
        errors.append("bilingual-loop.json must name English predictive-history as the canonical language surface")
    if bilingual.get("downstream_mirrors") != ["ph-civ-zh", "ph-civ-ru"]:
        errors.append("bilingual-loop.json downstream_mirrors must list ph-civ-zh then ph-civ-ru")
    downstream_language_surfaces = bilingual.get("downstream_language_surfaces", [])
    downstream_pairs = [(item.get("surface"), item.get("locale"), item.get("role")) for item in downstream_language_surfaces]
    if downstream_pairs != [
        ("ph-civ-zh", "zh", "downstream_localization_mirror"),
        ("ph-civ-ru", "ru", "downstream_localization_mirror"),
    ]:
        errors.append("bilingual-loop.json downstream_language_surfaces must define zh and ru downstream mirrors")
    authority_model = bilingual.get("authority_model", "")
    if "downstream localization mirrors" not in authority_model or CANONICAL_PUBLIC_ID not in authority_model:
        errors.append("bilingual-loop.json must state localization mirrors are downstream of predictive-history")
    if bilingual.get("primary_wedge") != "homer_to_tolstoy_read_from_china":
        errors.append("bilingual-loop.json invalid primary_wedge")
    bilingual_guardrails = "\n".join(bilingual.get("guardrails", []))
    for marker in ["not propaganda", "not anti-Western", "not a translation dump"]:
        if marker not in bilingual_guardrails:
            errors.append(f"bilingual-loop.json missing guardrail: {marker}")
    future_zh = bilingual.get("future_zh_wedge", {})
    if future_zh.get("upstream_source") != CANONICAL_PUBLIC_ID:
        errors.append("bilingual-loop.json future_zh_wedge must be downstream of predictive-history")
    if future_zh.get("dependency_role") != "downstream_localization_mirror":
        errors.append("bilingual-loop.json future_zh_wedge must use downstream mirror dependency role")
    future_steps = future_zh.get("first_steps", [])
    if future_steps != ["canonical glossary", "Chinese bootloader", "Chinese first-tour metadata"]:
        errors.append("bilingual-loop.json future_zh_wedge must start with glossary, bootloader, first-tour metadata")
    if "149 source chapters" not in future_zh.get("defer", ""):
        errors.append("bilingual-loop.json future_zh_wedge must defer transcript translation")
    future_ru = bilingual.get("future_ru_wedge", {})
    if future_ru.get("upstream_source") != CANONICAL_PUBLIC_ID:
        errors.append("bilingual-loop.json future_ru_wedge must be downstream of predictive-history")
    if future_ru.get("dependency_role") != "downstream_localization_mirror":
        errors.append("bilingual-loop.json future_ru_wedge must use downstream mirror dependency role")
    if future_ru.get("future_surface") != "ph-civ-ru":
        errors.append("bilingual-loop.json future_ru_wedge must reserve ph-civ-ru")
    if future_ru.get("status") != "roadmap_candidate":
        errors.append("bilingual-loop.json future_ru_wedge must be a roadmap candidate")
    if future_ru.get("first_steps", []) != ["Russian glossary", "Russian bootloader", "Russian first-tour metadata"]:
        errors.append("bilingual-loop.json future_ru_wedge must start with Russian glossary, bootloader, first-tour metadata")
    ru_guardrails = "\n".join(future_ru.get("guardrails", []))
    for marker in ["not Russian-state apologetics", "not anti-Ukrainian", "not live war analysis", "not a translation dump"]:
        if marker not in ru_guardrails:
            errors.append(f"bilingual-loop.json future_ru_wedge missing guardrail: {marker}")
    if "149 source chapters" not in future_ru.get("defer", "") or "localization commands" not in future_ru.get("defer", ""):
        errors.append("bilingual-loop.json future_ru_wedge must defer transcript translation and commands")
    roadmap = bilingual.get("localization_roadmap", [])
    roadmap_surfaces = [item.get("future_surface") for item in roadmap]
    if roadmap_surfaces != ["ph-civ-zh", "ph-civ-ru"]:
        errors.append("bilingual-loop.json localization_roadmap must list ph-civ-zh then ph-civ-ru")
    for item in roadmap:
        if item.get("upstream_source") != CANONICAL_PUBLIC_ID or item.get("dependency_role") != "downstream_localization_mirror":
            errors.append("bilingual-loop.json localization_roadmap entries must be downstream of predictive-history")
    llm_bilingual = llm_experience.get("bilingual_bridge", {})
    if llm_bilingual.get("path") != "data/bilingual-loop.json":
        errors.append("llm-experience bilingual_bridge must point to data/bilingual-loop.json")
    if llm_bilingual.get("reader_doc") != "docs/localization/bilingual-civilizational-bridge.md":
        errors.append("llm-experience bilingual_bridge must point to docs/localization/bilingual-civilizational-bridge.md")
    if llm_bilingual.get("bridge_id") != "trilingual_civilizational_bridge":
        errors.append("llm-experience bilingual_bridge must expose the trilingual bridge ID")
    if llm_bilingual.get("language_scope") != "trilingual":
        errors.append("llm-experience bilingual_bridge must expose trilingual scope")
    if llm_bilingual.get("localization_roadmap") != ["ph-civ-zh", "ph-civ-ru"]:
        errors.append("llm-experience bilingual_bridge must expose ph-civ-zh and ph-civ-ru roadmap")
    if llm_bilingual.get("canonical_source") != CANONICAL_PUBLIC_ID:
        errors.append("llm-experience bilingual_bridge must keep predictive-history as canonical source")
    if "downstream mirrors" not in llm_bilingual.get("authority_model", ""):
        errors.append("llm-experience bilingual_bridge must state localization mirrors are downstream")
    bilingual_doc = DATA_ROOT.parent / "docs" / "localization" / "bilingual-civilizational-bridge.md"
    if not bilingual_doc.exists():
        errors.append("docs/localization/bilingual-civilizational-bridge.md must exist")
    else:
        bilingual_doc_text = bilingual_doc.read_text(encoding="utf-8")
        for marker in [
            "Homer to Tolstoy, read from China.",
            "Trilingual Civilizational Bridge",
            "`predictive-history` / English / canonical public artifact",
            "paired mirrors",
            "not propaganda",
            "not a translation dump",
            "not anti-Western",
            "Volume I literary spine",
            "ph-civ-ru",
            "Russian glossary",
            "not live war analysis",
            "downstream of `predictive-history`",
            "not become sibling authorities",
        ]:
            if marker not in bilingual_doc_text:
                errors.append(f"docs/localization/bilingual-civilizational-bridge.md missing marker: {marker}")
    if llm_experience.get("first_seed", {}).get("route_ids") != seed_route_ids:
        errors.append("llm-experience route IDs must match route seed")
    llm_slices = llm_experience.get("namespace_slices", {})
    for slice_key in ("lectures", "essays", "interviews"):
        if slice_key not in llm_slices:
            errors.append(f"llm-experience namespace_slices missing {slice_key}")
    catalog_hub = llm_experience.get("catalog_hub", {})
    if catalog_hub.get("json") != "docs/predictive-history-index.json":
        errors.append("llm-experience catalog_hub must point to docs/predictive-history-index.json")
    deprecated_artifacts = llm_experience.get("deprecated_artifacts", {})
    if deprecated_artifacts.get("two_volume_ph_civ", {}).get("archive_doc") != (
        "docs/archive/two-volume-ph-civ-apo-deprecated.md"
    ):
        errors.append("llm-experience must document deprecated two_volume_ph_civ archive doc")
    guardrails = "\n".join(llm_experience.get("guardrails", []))
    for marker in [
        "Homer to Tolstoy",
        "Anna Karenina coda",
    ]:
        if marker not in guardrails:
            errors.append(f"llm-experience missing guardrail: {marker}")
    provisional_gt_ids = {f"gt-{index}" for index in range(23, 27)}
    cards_by_id = {card["source_id"]: card for card in cards}
    missing_provisional_gt = provisional_gt_ids - set(cards_by_id)
    for source_id in sorted(missing_provisional_gt):
        errors.append(f"{source_id} must exist as a provisional Game Theory chapter")
    for source_id in sorted(provisional_gt_ids & set(cards_by_id)):
        if cards_by_id[source_id].get("review_status") != "provisional":
            errors.append(f"{source_id} must remain provisional")
        if source_id in set(seed_route_ids):
            errors.append(f"{source_id} must not be promoted into routes before review")
    sh16_route = next((route for route in choreography if route.get("source_id") == "sh-16"), None)
    if not sh16_route:
        errors.append("choreography must include sh-16")
    else:
        if sh16_route.get("surface") != "ph-apo":
            errors.append("sh-16 route must remain on ph-apo")
        if sh16_route.get("route_type") != "coda":
            errors.append("sh-16 route must use coda route_type")
        caveat = sh16_route.get("caveat", "")
        if "Anna Karenina coda" not in caveat or "not a dedicated Tolstoy lecture" not in caveat:
            errors.append("sh-16 route must preserve the Tolstoy caveat")
    architecture = load_course_architecture()
    if architecture.get("repo_identity") != "predictive-history":
        errors.append("surfaces.json invalid repo_identity")
    if architecture.get("primary_artifact") != "namespace_catalog":
        errors.append("surfaces.json invalid primary_artifact")
    if architecture.get("volumes", {}).get("volume_i", {}).get("surface") != "ph-civ":
        errors.append("volume_i must route through ph-civ")
    if architecture.get("volumes", {}).get("volume_i", {}).get("role") != "law_discovery":
        errors.append("volume_i must use law_discovery role")
    if architecture.get("volumes", {}).get("volume_ii", {}).get("surface") != "ph-apo":
        errors.append("volume_ii must route through ph-apo")
    if architecture.get("volumes", {}).get("volume_ii", {}).get("role") != "law_application":
        errors.append("volume_ii must use law_application role")
    if architecture.get("bridge_support_nodes") != ["sh-11", "sh-16", "sh-17", "sh-18"]:
        errors.append("bridge_support_nodes invariant changed")
    literary_spine = load_spine("homer-to-tolstoy")
    if literary_spine.get("launch_readiness") != "defined_not_launch_ready":
        errors.append("homer-to-tolstoy spine must preserve launch readiness tension")
    if "first public reader" not in literary_spine.get("first_reader_gap", ""):
        errors.append("homer-to-tolstoy spine must name the first-reader gap")
    growth_goals = load_growth_goals()
    policy = growth_goals.get("agent_goal_policy", {})
    if growth_goals.get("goal_system") != "ph_civ_public_growth":
        errors.append("growth-goals.json invalid goal_system")
    if policy.get("must_translate_outcome_to_machinery") is not True:
        errors.append("growth goals must translate outcome goals into machinery")
    required_outputs = {
        "README and public contract explain the namespace catalog hub within one screen",
        "analytics plan defines what counts as a view across GitHub, web, video, social, and document surfaces",
        "distribution calendar converts the target into weekly and monthly milestones",
    }
    campaigns = growth_goals.get("campaigns", [])
    if not campaigns:
        errors.append("growth-goals.json must define at least one campaign")
    for campaign in campaigns:
        if "source-disciplined educational trust" not in campaign.get("unresolved_tension", ""):
            errors.append(f"{campaign.get('campaign_id')} must preserve the growth-vs-trust tension")
        if campaign.get("success_requires_external_audience_behavior") is not True:
            errors.append(f"{campaign.get('campaign_id')} must mark external audience dependency")
        wedge = campaign.get("first_live_wedge", {})
        if wedge.get("wedge_id") != "launch_volume_i_spine":
            errors.append(f"{campaign.get('campaign_id')} must name the first live publishing wedge")
        if wedge.get("launch_readiness") != "defined_not_launch_ready":
            errors.append(f"{campaign.get('campaign_id')} must distinguish defined wedge from launch readiness")
        if "without claiming views have already been earned" not in wedge.get("done_when", ""):
            errors.append(f"{campaign.get('campaign_id')} must forbid fake reach completion")
        outputs = set(campaign.get("measurable_agent_outputs", []))
        if not required_outputs <= outputs:
            errors.append(f"{campaign.get('campaign_id')} missing measurable growth outputs")
    errors.extend(validate_patterns(load_patterns(), cards))
    errors.extend(validate_public_boundary())
    weave_registry = DATA_ROOT / "weave" / "volume-i-companions.json"
    if not weave_registry.exists():
        errors.append("data/weave/volume-i-companions.json must exist")
    spine_tour_path = DATA_ROOT / "routes" / "volume-i-spine-tour.json"
    if not spine_tour_path.exists():
        errors.append("data/routes/volume-i-spine-tour.json must exist")
    else:
        spine_tour = json.loads(spine_tour_path.read_text(encoding="utf-8"))
        if spine_tour.get("tour_id") != "volume_i_spine_tour":
            errors.append("volume-i-spine-tour must use tour_id volume_i_spine_tour")
        if len(spine_tour.get("stops", [])) != 10:
            errors.append("volume-i-spine-tour must have 10 stops")
    deprecated_parts = DATA_ROOT / "parts" / "volume-i-parts.deprecated.json"
    if not deprecated_parts.exists():
        errors.append("data/parts/volume-i-parts.deprecated.json must exist for link redirects")
    llm_spine = llm_experience.get("spine_tour", {})
    if llm_spine.get("path") != "data/routes/volume-i-spine-tour.json":
        errors.append("llm-experience spine_tour must point to data/routes/volume-i-spine-tour.json")
    if llm_spine.get("registry") != "data/weave/volume-i-companions.json":
        errors.append("llm-experience spine_tour must point to data/weave/volume-i-companions.json")
    spine_mode = next(
        (mode for mode in llm_experience.get("modes", []) if mode.get("mode") == "spine_tour"),
        None,
    )
    if spine_mode is None:
        errors.append("llm-experience must define spine_tour mode")
    elif not any(
        "volume-i-spine-tour.json" in path for path in spine_mode.get("start_files", [])
    ):
        errors.append("llm-experience spine_tour mode must start from volume-i-spine-tour.json")
    cards_by_id = {card["source_id"]: card for card in cards}
    for pilot_id in sorted(PILOT_V2_SOURCE_IDS):
        card = cards_by_id.get(pilot_id)
        if not card:
            errors.append(f"v2 pilot missing card: {pilot_id}")
            continue
        commentary_rel = card.get("source_paths", {}).get("commentary_path", "")
        commentary_path = DATA_ROOT.parent / commentary_rel
        if commentary_path.exists():
            errors.extend(validate_v2_pilot(commentary_path, pilot_id))
        else:
            errors.append(f"v2 pilot missing commentary file: {pilot_id}")
    errors.extend(validate_volume_i_parts(require_doorways=True, require_chapter_anchors=True))
    errors.extend(validate_reader_namespace())
    ensure_all_indexes(cards)
    errors.extend(validate_all_indexes(cards))
    errors.extend(validate_no_legacy_chapter_indexes(repo_root=DATA_ROOT.parent))
    if getattr(args, "surfaces", False) or getattr(args, "surface_inventory", False):
        if getattr(args, "check", False):
            errors.extend(validate_public_surface_inventory(cards))
        else:
            ensure_public_surface_inventory(cards)
            errors.extend(validate_public_surface_inventory(cards))
    if getattr(args, "surfaces", False) or getattr(args, "surface_triage", False):
        if getattr(args, "check", False):
            errors.extend(validate_public_surface_triage(cards))
        else:
            ensure_public_surface_triage(cards)
            errors.extend(validate_public_surface_triage(cards))
    series = Counter(card["series"] for card in cards)
    result = {"status": "valid" if not errors else "invalid", "card_count": len(cards), "series_counts": dict(sorted(series.items())), "errors": errors}
    if args.json:
        emit_json(result)
        return 1 if errors else 0
    print(f"status: {result['status']}")
    print(f"card_count: {len(cards)}")
    for key, value in result["series_counts"].items():
        print(f"{key}: {value}")
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


def validate_patterns(patterns: list[dict], cards: list[dict]) -> list[str]:
    errors: list[str] = []
    pattern_ids: set[str] = set()
    source_ids = {card["source_id"] for card in cards}
    required = {
        "pattern_id",
        "title",
        "summary",
        "strategy_use",
        "source_ids",
        "tags",
        "limits",
        "public_status",
    }
    allowed_status = {"seed", "in_review", "stable"}
    for pattern in patterns:
        pattern_id = pattern.get("pattern_id")
        if not pattern_id:
            errors.append("pattern missing pattern_id")
            continue
        if pattern_id in pattern_ids:
            errors.append(f"duplicate pattern_id: {pattern_id}")
        pattern_ids.add(pattern_id)
        for field in sorted(required):
            if field not in pattern or pattern.get(field) in ("", [], None):
                errors.append(f"{pattern_id} missing field: {field}")
        status = pattern.get("public_status")
        if status not in allowed_status:
            errors.append(f"{pattern_id} invalid public_status: {status}")
        for source_id in pattern.get("source_ids", []):
            if source_id not in source_ids:
                errors.append(f"{pattern_id} unknown source_id: {source_id}")
    return errors


def cmd_surface_inventory(args) -> int:
    cards = load_cards()
    if args.check:
        errors = validate_public_surface_inventory(cards)
        if args.json:
            emit_json({"status": "current" if not errors else "stale", "errors": errors})
            return 1 if errors else 0
        if errors:
            for error in errors:
                print(f"error: {error}", file=sys.stderr)
            return 1
        print("status: current")
        return 0
    json_path, md_path, written = ensure_public_surface_inventory(cards, force=args.force)
    payload = {
        "status": "written" if written else "unchanged",
        "json_path": str(json_path.relative_to(DATA_ROOT.parent)),
        "markdown_path": str(md_path.relative_to(DATA_ROOT.parent)),
    }
    if args.json:
        emit_json(payload)
        return 0
    action = "wrote" if written else "unchanged"
    print(f"{action} {payload['json_path']} and {payload['markdown_path']}")
    return 0


def cmd_surface_triage(args) -> int:
    cards = load_cards()
    if args.check:
        errors = validate_public_surface_triage(cards)
        if args.json:
            emit_json({"status": "current" if not errors else "stale", "errors": errors})
            return 1 if errors else 0
        if errors:
            for error in errors:
                print(f"error: {error}", file=sys.stderr)
            return 1
        print("status: current")
        return 0
    json_path, md_path, written = ensure_public_surface_triage(cards, force=args.force)
    from .public_surface_triage import build_triage_payload

    triage = build_triage_payload(cards, DATA_ROOT.parent)
    if args.json:
        emit_json(
            {
                "status": "written" if written else "unchanged",
                "json_path": str(json_path.relative_to(DATA_ROOT.parent)),
                "markdown_path": str(md_path.relative_to(DATA_ROOT.parent)),
                "bucket_counts": triage["bucket_counts"],
                "buckets": triage["buckets"] if args.verbose else {},
            }
        )
        return 0
    action = "wrote" if written else "unchanged"
    print(
        f"{action} {json_path.relative_to(DATA_ROOT.parent)} "
        f"and {md_path.relative_to(DATA_ROOT.parent)}"
    )
    for bucket, count in triage["bucket_counts"].items():
        if count:
            print(f"  {bucket}: {count}")
            if args.verbose:
                for source_id in triage["buckets"].get(bucket, []):
                    print(f"    - {source_id}")
    return 0


def cmd_surface(args) -> int:
    if args.surface is None:
        print(
            "Use `predictive-history status` for the namespace catalog hub. "
            "Retired two-volume surfaces: docs/migrations/PH-SURFACE-RETIREMENT.md"
        )
        return 0
    if args.surface in {"ph-civ", "ph-apo"}:
        print(
            f"error: surface {args.surface} is retired; use predictive-history status or the namespace catalog hub. "
            "See docs/migrations/PH-SURFACE-RETIREMENT.md",
            file=sys.stderr,
        )
        return 2
    surface = SURFACES[args.surface]
    if args.json:
        return emit_json({"surface": args.surface, **surface})
    print(f"{args.surface}: {surface['title']}")
    print(f"status: {surface['status']}")
    print(surface["description"])
    return 0


def cmd_status(args) -> int:
    architecture = load_course_architecture()
    cards = load_cards()
    commentary = commentary_status_report(cards, DATA_ROOT.parent)
    from .public_surface_triage import build_triage_payload

    triage = build_triage_payload(cards, DATA_ROOT.parent)
    inv_stale = bool(validate_public_surface_inventory(cards))
    tri_stale = bool(validate_public_surface_triage(cards))
    if args.json:
        return emit_json(
            {
                "repo_identity": architecture["repo_identity"],
                "primary_artifact": architecture["primary_artifact"],
                "volumes": architecture["volumes"],
                "surfaces": SURFACES,
                "unique_card_count": len(cards),
                "commentary_maturity": commentary["by_commentary_maturity"],
                "commentary_wave_queue": {
                    k: len(v) for k, v in commentary["wave_queue"].items()
                },
                "surface_triage_counts": triage["bucket_counts"],
                "surface_inventory_stale": inv_stale,
                "surface_triage_stale": tri_stale,
            }
        )
    print(f"predictive-history: namespace catalog hub ({len(load_cards())} public chapters)")
    print(f"primary_artifact: {architecture['primary_artifact']}")
    hub = architecture.get("catalog_hub", {})
    if hub:
        print(f"catalog_hub: {hub.get('markdown')} · {hub.get('json')}")
    slices = architecture.get("namespace_slices", {})
    for slice_key, paths in slices.items():
        print(f"  {slice_key}: {paths.get('markdown')}")
    print(
        "deprecated two-volume: "
        f"{architecture['volumes']['volume_i']['surface']} / "
        f"{architecture['volumes']['volume_ii']['surface']}"
    )
    print(f"unique_card_count: {len(cards)}")
    print("commentary_maturity:")
    for key, value in commentary["by_commentary_maturity"].items():
        print(f"  {key}: {value}")
    print("surface_triage:")
    for bucket, count in triage["bucket_counts"].items():
        if count:
            print(f"  {bucket}: {count}")
    print(f"surface_inventory_stale: {inv_stale}")
    print(f"surface_triage_stale: {tri_stale}")
    return 0


def volume_payload(volume_id: str, include_cards: bool = False) -> dict:
    canonical = VOLUME_ALIASES[volume_id]
    architecture = load_course_architecture()
    volume = architecture["volumes"][canonical]
    cards = cards_for_volume(canonical)
    payload = {
        "volume_id": canonical,
        "surface": volume["surface"],
        "title": volume["title"],
        "role": volume["role"],
        "description": volume["description"],
        "card_count": len(cards),
        "bridge_support_nodes": architecture["bridge_support_nodes"]
        if canonical == "volume_i"
        else [],
    }
    if include_cards:
        payload["cards"] = [
            {
                "source_id": card["source_id"],
                "title": card["title"],
                "series": card["series"],
                "part": card["part"],
                "bridge_role": conceptual_bridge_role(card),
            }
            for card in cards
        ]
    return payload


def cmd_volumes(args) -> int:
    architecture = load_course_architecture()
    payload = {
        "repo_identity": architecture["repo_identity"],
        "primary_artifact": architecture["primary_artifact"],
        "volumes": {
            "volume_i": volume_payload("volume_i"),
            "volume_ii": volume_payload("volume_ii"),
        },
        "unique_card_count": len(load_cards()),
    }
    if args.json:
        return emit_json(payload)
    for volume in payload["volumes"].values():
        print(f"{volume['volume_id']}\t{volume['surface']}\t{volume['role']}\t{volume['card_count']}")
    print(f"unique_card_count\t{payload['unique_card_count']}")
    return 0


def cmd_volume(args) -> int:
    try:
        payload = volume_payload(args.volume_id, include_cards=True)
    except KeyError:
        print(f"Unknown volume: {args.volume_id}", file=sys.stderr)
        return 2
    if args.json:
        return emit_json(payload)
    print(f"# {payload['title']} ({payload['volume_id']})")
    print(f"surface: {payload['surface']}")
    print(f"role: {payload['role']}")
    print(f"card_count: {payload['card_count']}")
    for card in payload["cards"]:
        bridge = f"\t{card['bridge_role']}" if card["bridge_role"] else ""
        print(f"{card['source_id']}\t{card['series']}\t{card['title']}{bridge}")
    return 0


def cmd_growth(args) -> int:
    growth_goals = load_growth_goals()
    if args.json:
        return emit_json(growth_goals)
    print("Predictive History public growth")
    print(growth_goals["principle"])
    print("")
    print("Agent goal rule:")
    print(f"- {growth_goals['agent_goal_policy']['forbidden_completion_claim']}")
    print("- Translate reach ambitions into repo quality, assets, cadence, metrics, and human-approved distribution.")
    print("")
    for campaign in growth_goals["campaigns"]:
        print(f"{campaign['campaign_id']}: {campaign['title']}")
        print(f"status: {campaign['status']}")
        print(f"target: {campaign['target_count']} {campaign['target_metric']} by {campaign['target_date']}")
        print(f"tension: {campaign['unresolved_tension']}")
        print(f"agent work: {campaign['agent_executable_translation']}")
        wedge = campaign.get("first_live_wedge")
        if wedge:
            print(f"first wedge: {wedge['wedge_id']} - {wedge['title']}")
            print(f"readiness: {wedge['launch_readiness']}")
    return 0


def cmd_bilingual(args) -> int:
    bilingual = load_bilingual_loop()
    if args.json:
        return emit_json(bilingual)
    print(f"{bilingual['bridge_id']}: {bilingual['posture']}")
    print(f"legacy_loop_id: {bilingual['loop_id']}")
    print(f"language_scope: {bilingual['language_scope']}")
    print(f"status: {bilingual['status']}")
    print(f"canonical_source: {bilingual['canonical_source']}")
    print(f"primary_wedge: {bilingual['primary_wedge']}")
    print(f"downstream_mirrors: {', '.join(bilingual['downstream_mirrors'])}")
    print("")
    print(f"English hook: {bilingual['english_hook']}")
    print(f"Chinese hook: {bilingual['chinese_hook']}")
    print("")
    print("Guardrails:")
    for guardrail in bilingual["guardrails"]:
        print(f"- {guardrail}")
    print("")
    future = bilingual["future_zh_wedge"]
    print("future_zh_wedge:")
    print(f"- status: {future['status']}")
    print(f"- first_steps: {', '.join(future['first_steps'])}")
    print(f"- defer: {future['defer']}")
    ru_future = bilingual.get("future_ru_wedge")
    if ru_future:
        print()
        print("future_ru_wedge:")
        print(f"- future_surface: {ru_future['future_surface']}")
        print(f"- status: {ru_future['status']}")
        print(f"- primary_wedge: {ru_future['primary_wedge']}")
        print(f"- first_steps: {', '.join(ru_future['first_steps'])}")
        print(f"- defer: {ru_future['defer']}")
    return 0


def cmd_trilingual(args) -> int:
    return cmd_bilingual(args)


def cmd_start(args) -> int:
    experience = load_llm_experience()
    if args.json:
        return emit_json(experience)
    print("predictive-history: LLM-native namespace catalog bootloader")
    print(f"github_url: {experience['github_url']}")
    print(f"start_here: {experience['start_here']}")
    if experience.get("full_context"):
        print(f"full_context: {experience['full_context']['path']}")
    if experience.get("first_response_contract"):
        print(f"default_mode: {experience['first_response_contract']['default_mode']}")
        print(f"opening_path: {experience['first_response_contract']['opening_path']}")
    print(f"primary_artifact: {experience['primary_artifact']}")
    catalog_hub = experience.get("catalog_hub", {})
    if catalog_hub:
        print(f"catalog_hub: {catalog_hub.get('markdown')}")
    print("namespace_slices:")
    for key, paths in experience.get("namespace_slices", {}).items():
        print(f"- {key}: {paths.get('markdown')}")
    deprecated = experience.get("deprecated_artifacts", {}).get("two_volume_ph_civ", {})
    if deprecated:
        print(f"deprecated_two_volume: {deprecated.get('archive_doc')}")
    print("first_seed:")
    print(f"- {experience['first_seed']['seed_id']}: {', '.join(experience['first_seed']['route_ids'])}")
    if experience.get("first_tour"):
        print(f"first_tour: {experience['first_tour']['path']}")
    if experience.get("bilingual_bridge"):
        print(f"bilingual_bridge: {experience['bilingual_bridge']['path']}")
    if experience.get("chapter_folder_links"):
        print(f"chapter_folder_links: {experience['chapter_folder_links']['reader_doc']}")
    print("modes:")
    for mode in experience["modes"]:
        print(f"- {mode['mode']}: {mode['instruction']}")
    print("guardrails:")
    for guardrail in experience["guardrails"]:
        print(f"- {guardrail}")
    return 0


def cmd_tour(args) -> int:
    payload = first_tour_payload()
    if args.json:
        return emit_json(payload)
    print(f"# {payload['tour_id']}")
    print(f"mode: {payload['mode']}")
    print(f"opening_path: {payload['opening_path']}")
    print(f"opening_route: {payload['opening_route']}")
    print("")
    print(payload["reader_promise"])
    print("")
    print("Phases:")
    for phase in payload["phases"]:
        print(f"- {phase['title']}: {', '.join(phase['route_ids'])}")
        print(f"  {phase['function']}")
    print("")
    print("Stops:")
    for index, stop in enumerate(payload["stops"], start=1):
        print(f"{index}. {stop['source_id']} - {stop['title']} [{stop['route_type']}]")
        print(f"   question: {stop['reader_question']}")
        print(f"   next: {stop['next_action']}")
    print("")
    print("Opening move:")
    print(payload["continue_prompt"])
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="predictive-history",
        description="Provider-neutral Predictive History study cards and prompts.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("list", help="List cards.")
    p.add_argument("--series", choices=["civilization", "great-books", "geo-strategy", "game-theory", "secret-history"])
    p.add_argument("--spine", action="store_true", help="Limit to Homer-to-Tolstoy spine cards.")
    p.add_argument(
        "--namespace",
        choices=sorted(NAMESPACE_SERIES),
        help="Filter by corpus namespace (lectures, essays, interviews).",
    )
    p.add_argument("--all", action="store_true", help="Include cards outside the current public surface.")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("show", help="Show one card.")
    p.add_argument("source_id")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("search", help="Search cards.")
    p.add_argument("query")
    p.add_argument("--series", choices=["civilization", "great-books", "geo-strategy", "game-theory", "secret-history"])
    p.add_argument(
        "--namespace",
        choices=sorted(NAMESPACE_SERIES),
        help="Filter by corpus namespace (lectures, essays, interviews).",
    )
    p.add_argument("--all", action="store_true", help="Include cards outside the current public surface.")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("route", help="Show the public choreography route for one source ID.")
    p.add_argument("source_id")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_route)

    p = sub.add_parser("link", help="Render a paste-ready public chapter-folder link packet.")
    p.add_argument("source_id")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_link)

    p = sub.add_parser("patterns", help="List downstream strategy-facing public pattern IDs.")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_patterns)

    p = sub.add_parser("pattern", help="Show one public pattern card.")
    p.add_argument("pattern_id")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.set_defaults(func=cmd_pattern)

    p = sub.add_parser("bridge", help="Show public patterns attached to one source ID.")
    p.add_argument("source_id")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_bridge)

    p = sub.add_parser("prompt", help="Render a provider-neutral prompt template for one card.")
    p.add_argument("source_id")
    p.add_argument("--mode", choices=sorted(PROMPT_MODES), default="study")
    p.set_defaults(func=cmd_prompt)

    p = sub.add_parser("spark", help="Generate deterministic study sparks for one card.")
    p.add_argument("source_id")
    p.add_argument("--count", type=int, default=3)
    p.set_defaults(func=cmd_spark)

    p = sub.add_parser("spine", help="Show a spine.")
    p.add_argument("spine_id", nargs="?", default="homer-to-tolstoy")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_spine)

    p = sub.add_parser("path", help="Show a named path.")
    p.add_argument("path_id")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_path)

    p = sub.add_parser("validate", help="Validate packaged cards.")
    p.add_argument("--json", action="store_true")
    p.add_argument(
        "--surfaces",
        action="store_true",
        help="Also check or refresh public surface inventory and triage JSON.",
    )
    p.add_argument("--surface-inventory", action="store_true", help="Include surface inventory only.")
    p.add_argument("--surface-triage", action="store_true", help="Include surface triage only.")
    p.add_argument(
        "--check",
        action="store_true",
        help="With --surfaces*, fail if inventory/triage fingerprints are stale (no regen).",
    )
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("commentary-status", help="Commentary maturity histogram and rebuild wave queue.")
    p.add_argument("--json", action="store_true")
    p.add_argument("--verbose", action="store_true", help="List source IDs in each wave queue.")
    p.set_defaults(func=cmd_commentary_status)

    p = sub.add_parser("index", help="Generate or verify docs/predictive-history-index.md.")
    p.add_argument("--check", action="store_true", help="Fail if the index is stale without rewriting.")
    p.add_argument("--force", action="store_true", help="Rewrite the index even when fingerprint matches.")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_index)

    p = sub.add_parser("surface-inventory", help="Generate or verify public surface inventory.")
    p.add_argument("--check", action="store_true", help="Fail if inventory is stale without rewriting.")
    p.add_argument("--force", action="store_true", help="Rewrite even when fingerprint matches.")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_surface_inventory)

    p = sub.add_parser("surface-triage", help="Generate or verify per-chapter surface triage buckets.")
    p.add_argument("--check", action="store_true", help="Fail if triage is stale without rewriting.")
    p.add_argument("--force", action="store_true", help="Rewrite even when fingerprint matches.")
    p.add_argument("--json", action="store_true")
    p.add_argument("--verbose", action="store_true", help="List source IDs per bucket.")
    p.set_defaults(func=cmd_surface_triage)

    p = sub.add_parser("status", help="Show the current public surface status.")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("start", help="Show the LLM-native start-here bootloader.")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_start)

    p = sub.add_parser("tour", help="Show the first-tour route experience.")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_tour)

    p = sub.add_parser("volumes", help="Show the deprecated two-volume architecture metadata.")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_volumes)

    p = sub.add_parser("volume", help="Show cards for one conceptual volume.")
    p.add_argument("volume_id", choices=sorted(VOLUME_ALIASES))
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_volume)

    p = sub.add_parser("growth", help="Show public-growth goals and agent-executable translation rules.")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_growth)

    p = sub.add_parser("trilingual", help="Show the trilingual civilizational bridge ambition.")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_trilingual)

    p = sub.add_parser("bilingual", help="Compatibility alias for the trilingual bridge roadmap.")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_bilingual)

    p = sub.add_parser("surface", help="Show public surface metadata.")
    p.add_argument("surface", choices=sorted(SURFACES), nargs="?")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_surface)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    args.surface_scope = None
    return args.func(args)





if __name__ == "__main__":
    raise SystemExit(main())
