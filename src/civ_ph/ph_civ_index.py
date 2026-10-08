from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from .commentary_v2 import commentary_metadata
from .data import PACKAGE_ROOT, load_cards

INDEX_MD_REL = "docs/predictive-history-index.md"
INDEX_JSON_REL = "docs/predictive-history-index.json"
FINGERPRINT_MARKER = "<!-- predictive-history-index-fingerprint:"
SCHEMA_VERSION = 5
PRIMARY_ARTIFACT = "namespace_catalog"

NAMESPACE_SLICE_PATHS = {
    "lectures": {
        "markdown": "lectures/predictive-history-lecture-index.md",
        "json": "lectures/predictive-history-lecture-index.json",
    },
    "essays": {
        "markdown": "essays/predictive-history-essay-index.md",
        "json": "essays/predictive-history-essay-index.json",
    },
    "interviews": {
        "markdown": "interviews/predictive-history-interview-index.md",
        "json": "interviews/predictive-history-interview-index.json",
    },
}

TWO_VOLUME_DEPRECATED_DOC = "docs/archive/two-volume-ph-civ-apo-deprecated.md"

LEGACY_CHAPTER_INDEX_PATHS = (
    "docs/ph-civ-index.md",
    "data/ph-civ-index.json",
    "docs/source-video-index.md",
    "data/index.json",
    "data/predictive-history-index.json",
    "lectures/predictive-history-lectures-index.md",
    "lectures/predictive-history-lectures-index.json",
    "essays/predictive-history-essays-index.md",
    "essays/predictive-history-essays-index.json",
    "interviews/predictive-history-interviews-index.md",
    "interviews/predictive-history-interviews-index.json",
)

OPERATOR_DOC_GREP_PATHS = (
    "docs",
    "README.md",
    "START-HERE.md",
    "llms.txt",
    "llms-full.txt",
    "data/public-surface-inventory.json",
)

LECTURE_SERIES = frozenset(
    {"civilization", "great-books", "geo-strategy", "game-theory", "secret-history"}
)

LECTURE_SECTIONS: list[tuple[str, str]] = [
    ("civilization", "Civilization"),
    ("great-books", "Great Books"),
    ("geo-strategy", "Geo-Strategy"),
    ("game-theory", "Game Theory"),
    ("secret-history", "Secret History"),
]

PART_ORDER = ("civilization", "world-war", "provenance")

PART_SECTIONS: dict[str, list[tuple[str, str]]] = {
    "civilization": [
        ("civilization", "Civilization"),
        ("great-books", "Great Books"),
        ("game-theory", "Game Theory (Volume I lane)"),
    ],
    "world-war": [
        ("geo-strategy", "Geo-Strategy"),
        ("game-theory", "Game Theory"),
        ("secret-history", "Secret History"),
        ("essays", "Essays"),
    ],
    "provenance": [
        ("interviews", "Interviews"),
    ],
}

PART_META = {
    "civilization": ("ph-civ", "Volume I — Civilization (law discovery)"),
    "world-war": ("ph-apo", "Volume II — Apocalypse (law application)"),
    "provenance": ("provenance", "Provenance (source-family residue)"),
}

PROVENANCE_INTRO = (
    "Provenance packets preserve old seven-volume source-family material (interviews first). "
    "They are cataloged for source review and cross-links from "
    "[`docs/archive/book-provenance-index.md`](../docs/archive/book-provenance-index.md); "
    "they are not foreground Volume I/II law-discovery routes."
)

INTERVIEWS_SLICE_INTRO = (
    "Interview provenance packets (`part: provenance`, `series: interviews`). "
    "Full volume topology and cross-surface routing live in the "
    "[chapter catalog hub](../docs/predictive-history-index.md)."
)


@dataclass(frozen=True)
class NamespaceScope:
    scope: str
    md_rel: str
    json_rel: str
    fingerprint_marker: str
    filter_fn: Callable[[dict], bool]


def _lecture_filter(card: dict) -> bool:
    path = card.get("source_paths", {}).get("source_chapter_path", "")
    return card.get("series") in LECTURE_SERIES and path.startswith("lectures/")


def _essay_filter(card: dict) -> bool:
    return card.get("series") == "essays"


def _interview_filter(card: dict) -> bool:
    return card.get("series") == "interviews"


NAMESPACE_SCOPES: dict[str, NamespaceScope] = {
    "lectures": NamespaceScope(
        scope="lectures",
        md_rel="lectures/predictive-history-lecture-index.md",
        json_rel="lectures/predictive-history-lecture-index.json",
        fingerprint_marker="<!-- predictive-history-lecture-index-fingerprint:",
        filter_fn=_lecture_filter,
    ),
    "essays": NamespaceScope(
        scope="essays",
        md_rel="essays/predictive-history-essay-index.md",
        json_rel="essays/predictive-history-essay-index.json",
        fingerprint_marker="<!-- predictive-history-essay-index-fingerprint:",
        filter_fn=_essay_filter,
    ),
    "interviews": NamespaceScope(
        scope="interviews",
        md_rel="interviews/predictive-history-interview-index.md",
        json_rel="interviews/predictive-history-interview-index.json",
        fingerprint_marker="<!-- predictive-history-interview-index-fingerprint:",
        filter_fn=_interview_filter,
    ),
}


def index_markdown_path(repo_root: Path | None = None) -> Path:
    root = repo_root or PACKAGE_ROOT
    return root / INDEX_MD_REL


def index_json_path(repo_root: Path | None = None) -> Path:
    root = repo_root or PACKAGE_ROOT
    return root / INDEX_JSON_REL


def namespace_markdown_path(scope: str, repo_root: Path | None = None) -> Path:
    root = repo_root or PACKAGE_ROOT
    return root / NAMESPACE_SCOPES[scope].md_rel


def namespace_json_path(scope: str, repo_root: Path | None = None) -> Path:
    root = repo_root or PACKAGE_ROOT
    return root / NAMESPACE_SCOPES[scope].json_rel


def filter_cards_for_scope(scope: str, cards: list[dict]) -> list[dict]:
    filter_fn = NAMESPACE_SCOPES[scope].filter_fn
    return [card for card in cards if filter_fn(card)]


def markdown_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    block = text[4:end]
    fields: dict[str, str] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    return fields


def markdown_body(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[end + 5 :]
    return text


def count_transcript_words(text: str) -> int:
    body = markdown_body(text)
    return len(re.findall(r"\b[\w']+\b", body, flags=re.UNICODE))


def transcript_word_count(card: dict, repo_root: Path) -> int:
    transcript_rel = card.get("source_paths", {}).get("source_chapter_path", "")
    if not transcript_rel:
        return 0
    transcript_path = repo_root / transcript_rel
    if not transcript_path.exists():
        return 0
    return count_transcript_words(transcript_path.read_text(encoding="utf-8"))


def source_url_from_path(transcript_rel: str, repo_root: Path) -> str:
    if not transcript_rel:
        return ""
    transcript_path = repo_root / transcript_rel
    if not transcript_path.exists():
        return ""
    frontmatter = markdown_frontmatter(transcript_path.read_text(encoding="utf-8"))
    return frontmatter.get("source_url", "") or frontmatter.get("canonical_url", "")


def source_video_url(card: dict, repo_root: Path) -> str:
    transcript_rel = card.get("source_paths", {}).get("source_chapter_path", "")
    return source_url_from_path(transcript_rel, repo_root)


def chapter_folder_rel(card: dict, repo_root: Path) -> str:
    transcript_rel = card.get("source_paths", {}).get("source_chapter_path", "")
    commentary_rel = card.get("source_paths", {}).get("commentary_path", "")
    if not transcript_rel or not commentary_rel:
        return ""
    folder = "/".join(transcript_rel.split("/")[:-1])
    if not folder.endswith(f"/{card['source_id']}"):
        return ""
    if not commentary_rel.startswith(f"{folder}/"):
        return ""
    readme = repo_root / folder / "README.md"
    return folder if readme.exists() else ""


def chapter_entry(card: dict, repo_root: Path) -> dict:
    paths = card.get("source_paths", {})
    transcript = paths.get("source_chapter_path", "")
    commentary = paths.get("commentary_path", "")
    folder = chapter_folder_rel(card, repo_root)
    surface, volume_label = PART_META[card["part"]]
    entry = {
        "source_id": card["source_id"],
        "title": card["title"],
        "part": card["part"],
        "surface": surface,
        "volume_label": volume_label,
        "series": card["series"],
        "review_status": card.get("review_status", ""),
        "placement_weight": card.get("placement_weight", ""),
        "paths": {
            "transcript": transcript,
            "commentary": commentary,
        },
        "transcript_word_count": transcript_word_count(card, repo_root),
    }
    if card.get("publication_date"):
        entry["publication_date"] = card["publication_date"]
    if folder:
        entry["paths"]["folder"] = folder
        entry["paths"]["folder_readme"] = f"{folder}/README.md"
    video = source_video_url(card, repo_root)
    if video:
        entry["source_video_url"] = video
    commentary_path = repo_root / commentary if commentary else None
    if commentary_path and commentary_path.exists():
        meta = commentary_metadata(commentary_path)
        entry["commentary_maturity"] = meta["commentary_maturity"]
        entry["scaffold_version"] = meta["scaffold_version"]
        if meta["migration_source"]:
            entry["migration_source"] = meta["migration_source"]
        entry["deprecated_part_routing"] = meta["deprecated_part_routing"]
    return entry


def sort_cards_for_table(cards: list[dict], *, part: str | None = None) -> list[dict]:
    effective_part = part or (cards[0]["part"] if cards else "")
    if effective_part == "provenance":
        return sorted(cards, key=lambda row: (row.get("publication_date", ""), row["source_id"]))
    return sorted(cards, key=lambda row: row["source_id"])


def sort_essays_for_table(cards: list[dict]) -> list[dict]:
    return sorted(cards, key=lambda row: (row.get("publication_date", ""), row["source_id"]))


def build_by_series(chapters: list[dict]) -> dict[str, dict]:
    by_series: dict[str, dict] = {}
    for entry in chapters:
        series = entry["series"]
        bucket = by_series.setdefault(
            series,
            {"chapter_count": 0, "transcript_word_total": 0},
        )
        bucket["chapter_count"] += 1
        bucket["transcript_word_total"] += entry.get("transcript_word_count", 0)
    return dict(sorted(by_series.items()))


def build_by_surface(chapters: list[dict]) -> dict[str, dict]:
    by_surface: dict[str, dict] = {}
    for part in PART_ORDER:
        surface, volume_label = PART_META[part]
        surface_chapters = [entry for entry in chapters if entry["surface"] == surface]
        series_counts: dict[str, int] = {}
        for entry in surface_chapters:
            series_counts[entry["series"]] = series_counts.get(entry["series"], 0) + 1
        by_surface[surface] = {
            "part": part,
            "volume_label": volume_label,
            "chapter_count": len(surface_chapters),
            "series_counts": dict(sorted(series_counts.items())),
            "transcript_word_total": sum(
                entry.get("transcript_word_count", 0) for entry in surface_chapters
            ),
        }
    return by_surface


def namespace_slice_counts(cards: list[dict]) -> dict[str, int]:
    return {
        scope: len(filter_cards_for_scope(scope, cards))
        for scope in NAMESPACE_SCOPES
    }


def render_index_payload(cards: list[dict], repo_root: Path) -> dict:
    chapters = [
        chapter_entry(card, repo_root)
        for card in sorted(cards, key=lambda row: row["source_id"])
    ]
    by_surface = build_by_surface(chapters)
    by_series = build_by_series(chapters)
    slice_counts = namespace_slice_counts(cards)

    fingerprint = index_payload_fingerprint(chapters)
    transcript_word_total = sum(entry.get("transcript_word_count", 0) for entry in chapters)
    return {
        "schema_version": SCHEMA_VERSION,
        "primary_artifact": PRIMARY_ARTIFACT,
        "fingerprint": fingerprint,
        "card_count": len(cards),
        "transcript_word_total": transcript_word_total,
        "ssot": "data/cards.jsonl",
        "markdown_index": INDEX_MD_REL,
        "catalog_hub": {
            "markdown": INDEX_MD_REL,
            "json": INDEX_JSON_REL,
        },
        "namespace_slices": {
            scope: {
                **NAMESPACE_SLICE_PATHS[scope],
                "card_count": slice_counts[scope],
            }
            for scope in NAMESPACE_SLICE_PATHS
        },
        "deprecated": {
            "two_volume": {
                "primary_artifact": "two_volume_ph_civ",
                "archive_doc": TWO_VOLUME_DEPRECATED_DOC,
                "surfaces": {
                    PART_META[part][0]: {"part": part, "label": PART_META[part][1]}
                    for part in PART_ORDER
                },
                "series_order": {
                    part: [{"series": series, "label": label} for series, label in sections]
                    for part, sections in PART_SECTIONS.items()
                },
            }
        },
        "by_series": by_series,
        "by_surface": by_surface,
        "chapters": chapters,
    }


def render_namespace_payload(scope: str, cards: list[dict], repo_root: Path) -> dict:
    config = NAMESPACE_SCOPES[scope]
    filtered = filter_cards_for_scope(scope, cards)
    chapters = [
        chapter_entry(card, repo_root)
        for card in sorted(filtered, key=lambda row: row["source_id"])
    ]
    fingerprint = index_payload_fingerprint(chapters)
    transcript_word_total = sum(entry.get("transcript_word_count", 0) for entry in chapters)
    return {
        "schema_version": SCHEMA_VERSION,
        "scope": config.scope,
        "fingerprint": fingerprint,
        "card_count": len(filtered),
        "transcript_word_total": transcript_word_total,
        "ssot": "data/cards.jsonl",
        "markdown_index": config.md_rel,
        "hub_index": INDEX_MD_REL,
        "chapters": chapters,
    }


def index_payload_fingerprint(chapters: list[dict]) -> str:
    blob = json.dumps(chapters, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    digest = hashlib.sha256(blob.encode("utf-8")).hexdigest()
    return digest[:16]


def md_link(label: str, rel: str, *, link_prefix: str = "../") -> str:
    if not rel:
        return ""
    if link_prefix:
        return f"[{label}]({link_prefix}{rel})"
    return f"[{label}]({rel})"


def render_table(
    cards: list[dict],
    repo_root: Path,
    *,
    part: str | None = None,
    link_prefix: str = "../",
) -> list[str]:
    header = "| Source ID | Title | Review | Words | Transcript | Commentary | Folder | Video |"
    sep = "| --- | --- | --- | ---: | --- | --- | --- | --- |"
    rows = [header, sep]
    for card in sort_cards_for_table(cards, part=part):
        entry = chapter_entry(card, repo_root)
        paths = entry["paths"]
        transcript = paths.get("transcript", "")
        commentary = paths.get("commentary", "")
        folder = paths.get("folder", "")
        video = entry.get("source_video_url", "")
        words = entry.get("transcript_word_count", 0)
        rows.append(
            "| "
            + " | ".join(
                [
                    f"`{entry['source_id']}`",
                    entry["title"].replace("|", "\\|"),
                    f"`{entry['review_status']}`",
                    f"{words:,}" if words else "—",
                    md_link("transcript", transcript, link_prefix=link_prefix) if transcript else "",
                    md_link("commentary", commentary, link_prefix=link_prefix) if commentary else "",
                    md_link("folder", paths.get("folder_readme", ""), link_prefix=link_prefix) if folder else "",
                    f"[video]({video})" if video else "",
                ]
            )
            + " |"
        )
    return rows


def render_essays_table(cards: list[dict], repo_root: Path) -> list[str]:
    header = "| Source ID | Title | Date | Words | Essay | Commentary | Substack |"
    sep = "| --- | --- | --- | ---: | --- | --- | --- |"
    rows = [header, sep]
    for card in sort_essays_for_table(cards):
        entry = chapter_entry(card, repo_root)
        paths = entry["paths"]
        transcript = paths.get("transcript", "")
        commentary = paths.get("commentary", "")
        substack = entry.get("source_video_url", "")
        words = entry.get("transcript_word_count", 0)
        rows.append(
            "| "
            + " | ".join(
                [
                    f"`{entry['source_id']}`",
                    entry["title"].replace("|", "\\|"),
                    card.get("publication_date", ""),
                    f"{words:,}" if words else "—",
                    md_link("essay", transcript, link_prefix="") if transcript else "",
                    md_link("commentary", commentary, link_prefix="../") if commentary else "",
                    f"[substack]({substack})" if substack else "",
                ]
            )
            + " |"
        )
    return rows


def render_hub_slice_section(cards: list[dict]) -> list[str]:
    lecture_count = len(filter_cards_for_scope("lectures", cards))
    essay_count = len(filter_cards_for_scope("essays", cards))
    interview_count = len(filter_cards_for_scope("interviews", cards))
    return [
        "## Namespace slice indexes",
        "",
        "Namespace catalogs beside each corpus (lectures, essays, interviews). "
        "This page remains the full cross-surface hub.",
        "",
        "| Slice | Markdown | JSON | Cards |",
        "| --- | --- | --- | ---: |",
        (
            f"| Lectures | "
            f"[lectures index](../lectures/predictive-history-lecture-index.md) | "
            f"[json](../lectures/predictive-history-lecture-index.json) | {lecture_count} |"
        ),
        (
            f"| Essays | "
            f"[essays index](../essays/predictive-history-essay-index.md) | "
            f"[json](../essays/predictive-history-essay-index.json) | {essay_count} |"
        ),
        (
            f"| Interviews | "
            f"[interviews index](../interviews/predictive-history-interview-index.md) | "
            f"[json](../interviews/predictive-history-interview-index.json) | {interview_count} |"
        ),
        "",
    ]


def render_index_body(cards: list[dict], repo_root: Path) -> str:
    lecture_cards = filter_cards_for_scope("lectures", cards)
    by_lecture_series: dict[str, list[dict]] = {}
    for card in lecture_cards:
        by_lecture_series.setdefault(card["series"], []).append(card)

    essay_count = len(filter_cards_for_scope("essays", cards))
    interview_count = len(filter_cards_for_scope("interviews", cards))

    lines = [
        "# Predictive History Chapter Index",
        "",
        "Canonical catalog of every public Predictive History chapter in this repository "
        "(lectures, Substack essays, and provenance interviews).",
        "",
        f"- **Primary artifact:** `{PRIMARY_ARTIFACT}` (namespace hub + slice indexes)",
        f"- **Card count:** {len(cards)}",
        f"- **Transcript words (total):** {sum(transcript_word_count(card, repo_root) for card in cards):,}",
        (
            f"- **SSOT:** [`data/cards.jsonl`](../data/cards.jsonl) · "
            f"[`predictive-history-index.json`](predictive-history-index.json)"
        ),
        "- **Regenerate:** `predictive-history index` · `python scripts/generate_ph_civ_index.py` · auto-sync during `predictive-history validate` and publish",
        "",
        "YouTube and Substack source URLs appear in catalog tables and in "
        "[`predictive-history-index.json`](predictive-history-index.json) (`source_video_url`). "
        "**Words** counts transcript body text only (YAML frontmatter excluded).",
        "",
    ]
    lines.extend(render_hub_slice_section(cards))
    lines.extend(
        [
            "## Deprecated reader frame",
            "",
            "The **two-volume ph-civ / ph-apo** model (Volume I Civilization / Volume II Apocalypse) "
            "is deprecated for onboarding. Legacy `part` and route `surface` metadata remain on cards for compatibility. "
            f"See [`two-volume deprecation archive`](archive/two-volume-ph-civ-apo-deprecated.md).",
            "",
            "Bridge support nodes (`sh-11`, `sh-16`, `sh-17`, `sh-18`) still carry cross-part routing in routes and cards.",
            "",
        ]
    )

    for series_key, series_label in LECTURE_SECTIONS:
        series_cards = by_lecture_series.get(series_key, [])
        if not series_cards:
            continue
        lines.extend(
            [
                f"## {series_label}",
                "",
                f"**Series:** `{series_key}` · **Chapters:** {len(series_cards)}",
                "",
            ]
        )
        lines.extend(render_table(series_cards, repo_root, link_prefix="../"))
        lines.append("")

    lines.extend(
        [
            "## Essays",
            "",
            f"**Substack essays:** {essay_count} — full catalog: "
            f"[`essays/predictive-history-essay-index.md`](../essays/predictive-history-essay-index.md) · "
            f"[json](../essays/predictive-history-essay-index.json)",
            "",
            "## Interviews / provenance",
            "",
            f"**Interview provenance:** {interview_count} — full catalog: "
            f"[`interviews/predictive-history-interview-index.md`](../interviews/predictive-history-interview-index.md) · "
            f"[json](../interviews/predictive-history-interview-index.json)",
            "",
            PROVENANCE_INTRO,
            "",
        ]
    )

    lines.append("## Full alphabetical index")
    lines.append("")
    lines.extend(render_table(cards, repo_root))
    lines.append("")
    return lines


def render_lectures_index_body(cards: list[dict], repo_root: Path) -> list[str]:
    filtered = filter_cards_for_scope("lectures", cards)
    by_series: dict[str, list[dict]] = {}
    for card in filtered:
        by_series.setdefault(card["series"], []).append(card)

    lines = [
        "# Predictive History Lectures Index",
        "",
        "Catalog of lecture chapter packets under `lectures/` (video-sourced transcripts).",
        "",
        f"- **Card count:** {len(filtered)}",
        f"- **SSOT:** [`data/cards.jsonl`](../data/cards.jsonl) · "
        f"[`predictive-history-lecture-index.json`](predictive-history-lecture-index.json)",
        f"- **Full hub:** [`docs/predictive-history-index.md`](../docs/predictive-history-index.md)",
        "- **Regenerate:** `predictive-history index` · `python scripts/generate_ph_civ_index.py`",
        "",
    ]
    for series_key, series_label in LECTURE_SECTIONS:
        series_cards = by_series.get(series_key, [])
        if not series_cards:
            continue
        lines.extend(
            [
                f"## {series_label}",
                "",
                f"**Series:** `{series_key}` · **Chapters:** {len(series_cards)}",
                "",
            ]
        )
        lines.extend(render_table(series_cards, repo_root, link_prefix=""))
        lines.append("")
    return lines


def render_essays_index_body(cards: list[dict], repo_root: Path) -> list[str]:
    filtered = filter_cards_for_scope("essays", cards)
    lines = [
        "# Predictive History Essays Index",
        "",
        "Catalog of Substack essay bodies under `essays/` (flat files).",
        "",
        f"- **Card count:** {len(filtered)}",
        f"- **SSOT:** [`data/cards.jsonl`](../data/cards.jsonl) · "
        f"[`data/essays/manifest.json`](../data/essays/manifest.json)",
        f"- **Machine catalog:** [`predictive-history-essay-index.json`](predictive-history-essay-index.json)",
        f"- **Full hub:** [`docs/predictive-history-index.md`](../docs/predictive-history-index.md)",
        "- **Regenerate:** `predictive-history index` · `python scripts/generate_ph_civ_index.py`",
        "",
        "## Essays by publication date",
        "",
    ]
    lines.extend(render_essays_table(filtered, repo_root))
    lines.append("")
    return lines


def render_interviews_index_body(cards: list[dict], repo_root: Path) -> list[str]:
    filtered = filter_cards_for_scope("interviews", cards)
    lines = [
        "# Predictive History Interviews Index",
        "",
        "Catalog of interview provenance packets under `interviews/`.",
        "",
        f"- **Card count:** {len(filtered)}",
        f"- **SSOT:** [`data/cards.jsonl`](../data/cards.jsonl) · "
        f"[`data/interviews/manifest.json`](../data/interviews/manifest.json)",
        f"- **Machine catalog:** [`predictive-history-interview-index.json`](predictive-history-interview-index.json)",
        f"- **Full hub:** [`docs/predictive-history-index.md`](../docs/predictive-history-index.md)",
        "- **Regenerate:** `predictive-history index` · `python scripts/generate_ph_civ_index.py`",
        "",
        INTERVIEWS_SLICE_INTRO,
        "",
        "## Interviews by upload date",
        "",
    ]
    lines.extend(render_table(filtered, repo_root, part="provenance", link_prefix=""))
    lines.append("")
    return lines


def render_namespace_body(scope: str, cards: list[dict], repo_root: Path) -> list[str]:
    if scope == "lectures":
        return render_lectures_index_body(cards, repo_root)
    if scope == "essays":
        return render_essays_index_body(cards, repo_root)
    if scope == "interviews":
        return render_interviews_index_body(cards, repo_root)
    raise ValueError(f"unknown namespace scope: {scope}")


def render_index_markdown(cards: list[dict], repo_root: Path, *, fingerprint: str) -> str:
    body = "\n".join(render_index_body(cards, repo_root))
    return f"{FINGERPRINT_MARKER} {fingerprint} -->\n{body}"


def render_namespace_markdown(
    scope: str,
    cards: list[dict],
    repo_root: Path,
    *,
    fingerprint: str,
) -> str:
    config = NAMESPACE_SCOPES[scope]
    body = "\n".join(render_namespace_body(scope, cards, repo_root))
    return f"{config.fingerprint_marker} {fingerprint} -->\n{body}"


def render_index_json(cards: list[dict], repo_root: Path) -> str:
    payload = render_index_payload(cards, repo_root)
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def render_namespace_json(scope: str, cards: list[dict], repo_root: Path) -> str:
    payload = render_namespace_payload(scope, cards, repo_root)
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def _fingerprint_pattern(marker: str) -> re.Pattern[str]:
    return re.compile(re.escape(marker) + r" ([0-9a-f]+) -->")


def read_index_fingerprint(path: Path, *, marker: str | None = None) -> str | None:
    if not path.exists():
        return None
    if path.suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        value = data.get("fingerprint")
        return value if isinstance(value, str) else None
    first_line = path.read_text(encoding="utf-8").splitlines()[0:1]
    if not first_line:
        return None
    fingerprint_marker = marker or FINGERPRINT_MARKER
    match = _fingerprint_pattern(fingerprint_marker).match(first_line[0])
    return match.group(1) if match else None


def expected_index_fingerprint(cards: list[dict], repo_root: Path) -> str:
    chapters = [
        chapter_entry(card, repo_root)
        for card in sorted(cards, key=lambda row: row["source_id"])
    ]
    return index_payload_fingerprint(chapters)


def expected_namespace_fingerprint(scope: str, cards: list[dict], repo_root: Path) -> str:
    filtered = filter_cards_for_scope(scope, cards)
    chapters = [
        chapter_entry(card, repo_root)
        for card in sorted(filtered, key=lambda row: row["source_id"])
    ]
    return index_payload_fingerprint(chapters)


def ensure_ph_civ_index(
    cards: list[dict] | None = None,
    *,
    repo_root: Path | None = None,
    force: bool = False,
) -> tuple[Path, Path, bool]:
    root = repo_root or PACKAGE_ROOT
    cards = cards if cards is not None else load_cards()
    md_path = index_markdown_path(root)
    json_path = index_json_path(root)
    fingerprint = expected_index_fingerprint(cards, root)
    if not force and md_path.exists() and json_path.exists():
        if (
            read_index_fingerprint(md_path) == fingerprint
            and read_index_fingerprint(json_path) == fingerprint
        ):
            return md_path, json_path, False

    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(render_index_markdown(cards, root, fingerprint=fingerprint), encoding="utf-8")
    json_path.write_text(render_index_json(cards, root), encoding="utf-8")
    return md_path, json_path, True


def ensure_namespace_index(
    scope: str,
    cards: list[dict] | None = None,
    *,
    repo_root: Path | None = None,
    force: bool = False,
) -> tuple[Path, Path, bool]:
    root = repo_root or PACKAGE_ROOT
    cards = cards if cards is not None else load_cards()
    config = NAMESPACE_SCOPES[scope]
    md_path = namespace_markdown_path(scope, root)
    json_path = namespace_json_path(scope, root)
    fingerprint = expected_namespace_fingerprint(scope, cards, root)
    if not force and md_path.exists() and json_path.exists():
        if (
            read_index_fingerprint(md_path, marker=config.fingerprint_marker) == fingerprint
            and read_index_fingerprint(json_path) == fingerprint
        ):
            return md_path, json_path, False

    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(
        render_namespace_markdown(scope, cards, root, fingerprint=fingerprint),
        encoding="utf-8",
    )
    json_path.write_text(render_namespace_json(scope, cards, root), encoding="utf-8")
    return md_path, json_path, True


def ensure_lectures_index(
    cards: list[dict] | None = None,
    *,
    repo_root: Path | None = None,
    force: bool = False,
) -> tuple[Path, Path, bool]:
    return ensure_namespace_index("lectures", cards, repo_root=repo_root, force=force)


def ensure_essays_index(
    cards: list[dict] | None = None,
    *,
    repo_root: Path | None = None,
    force: bool = False,
) -> tuple[Path, Path, bool]:
    return ensure_namespace_index("essays", cards, repo_root=repo_root, force=force)


def ensure_interviews_index(
    cards: list[dict] | None = None,
    *,
    repo_root: Path | None = None,
    force: bool = False,
) -> tuple[Path, Path, bool]:
    return ensure_namespace_index("interviews", cards, repo_root=repo_root, force=force)


def ensure_all_indexes(
    cards: list[dict] | None = None,
    *,
    repo_root: Path | None = None,
    force: bool = False,
) -> bool:
    cards = cards if cards is not None else load_cards()
    written = False
    for ensure_fn in (
        ensure_ph_civ_index,
        ensure_lectures_index,
        ensure_essays_index,
        ensure_interviews_index,
    ):
        _, _, changed = ensure_fn(cards, repo_root=repo_root, force=force)
        written = written or changed
    return written


def validate_ph_civ_index(cards: list[dict] | None = None, *, repo_root: Path | None = None) -> list[str]:
    root = repo_root or PACKAGE_ROOT
    cards = cards if cards is not None else load_cards()
    md_path = index_markdown_path(root)
    json_path = index_json_path(root)
    expected_fp = expected_index_fingerprint(cards, root)
    errors: list[str] = []

    if not md_path.exists():
        errors.append(f"missing chapter index: {INDEX_MD_REL}")
    elif read_index_fingerprint(md_path) != expected_fp:
        errors.append(
            f"stale chapter index: {INDEX_MD_REL} (run `predictive-history index` or `predictive-history validate` to refresh)"
        )

    if not json_path.exists():
        errors.append(f"missing chapter index: {INDEX_JSON_REL}")
    else:
        json_fp = read_index_fingerprint(json_path)
        if json_fp != expected_fp:
            errors.append(
                f"stale chapter index: {INDEX_JSON_REL} (run `predictive-history index` or `predictive-history validate` to refresh)"
            )
        payload = json.loads(json_path.read_text(encoding="utf-8"))
        if payload.get("card_count") != len(cards):
            errors.append(f"chapter index card_count mismatch in {INDEX_JSON_REL}")

    md_fp = read_index_fingerprint(md_path) if md_path.exists() else None
    json_fp = read_index_fingerprint(json_path) if json_path.exists() else None
    if md_fp and json_fp and md_fp != json_fp:
        errors.append("chapter index fingerprint mismatch between markdown and JSON exports")

    return errors


def validate_namespace_index(
    scope: str,
    cards: list[dict] | None = None,
    *,
    repo_root: Path | None = None,
) -> list[str]:
    root = repo_root or PACKAGE_ROOT
    cards = cards if cards is not None else load_cards()
    config = NAMESPACE_SCOPES[scope]
    md_path = namespace_markdown_path(scope, root)
    json_path = namespace_json_path(scope, root)
    expected_fp = expected_namespace_fingerprint(scope, cards, root)
    expected_count = len(filter_cards_for_scope(scope, cards))
    errors: list[str] = []

    if not md_path.exists():
        errors.append(f"missing namespace index: {config.md_rel}")
    elif read_index_fingerprint(md_path, marker=config.fingerprint_marker) != expected_fp:
        errors.append(
            f"stale namespace index: {config.md_rel} (run `predictive-history index` or `predictive-history validate` to refresh)"
        )

    if not json_path.exists():
        errors.append(f"missing namespace index: {config.json_rel}")
    else:
        json_fp = read_index_fingerprint(json_path)
        if json_fp != expected_fp:
            errors.append(
                f"stale namespace index: {config.json_rel} (run `predictive-history index` or `predictive-history validate` to refresh)"
            )
        payload = json.loads(json_path.read_text(encoding="utf-8"))
        if payload.get("card_count") != expected_count:
            errors.append(f"namespace index card_count mismatch in {config.json_rel}")
        if payload.get("scope") != scope:
            errors.append(f"namespace index scope mismatch in {config.json_rel}")
        if payload.get("hub_index") != INDEX_MD_REL:
            errors.append(f"namespace index hub_index mismatch in {config.json_rel}")

    md_fp = (
        read_index_fingerprint(md_path, marker=config.fingerprint_marker) if md_path.exists() else None
    )
    json_fp = read_index_fingerprint(json_path) if json_path.exists() else None
    if md_fp and json_fp and md_fp != json_fp:
        errors.append(f"namespace index fingerprint mismatch for {scope}")

    return errors


def validate_lectures_index(cards: list[dict] | None = None, *, repo_root: Path | None = None) -> list[str]:
    return validate_namespace_index("lectures", cards, repo_root=repo_root)


def validate_essays_index(cards: list[dict] | None = None, *, repo_root: Path | None = None) -> list[str]:
    return validate_namespace_index("essays", cards, repo_root=repo_root)


def validate_interviews_index(cards: list[dict] | None = None, *, repo_root: Path | None = None) -> list[str]:
    return validate_namespace_index("interviews", cards, repo_root=repo_root)


def validate_all_indexes(cards: list[dict] | None = None, *, repo_root: Path | None = None) -> list[str]:
    cards = cards if cards is not None else load_cards()
    errors: list[str] = []
    errors.extend(validate_ph_civ_index(cards, repo_root=repo_root))
    for scope in NAMESPACE_SCOPES:
        errors.extend(validate_namespace_index(scope, cards, repo_root=repo_root))
    return errors


def validate_no_legacy_chapter_indexes(*, repo_root: Path | None = None) -> list[str]:
    root = repo_root or PACKAGE_ROOT
    errors: list[str] = []
    for rel in LEGACY_CHAPTER_INDEX_PATHS:
        if (root / rel).exists():
            errors.append(f"legacy chapter index must be removed: {rel}")

    forbidden = "ph-civ-index"
    for rel in OPERATOR_DOC_GREP_PATHS:
        path = root / rel
        if not path.exists():
            continue
        if path.is_dir():
            for doc in path.rglob("*"):
                if doc.suffix not in {".md", ".txt", ".json"}:
                    continue
                if doc.is_file() and forbidden in doc.read_text(encoding="utf-8"):
                    errors.append(f"operator doc must not reference {forbidden}: {doc.relative_to(root)}")
        elif forbidden in path.read_text(encoding="utf-8"):
            errors.append(f"operator doc must not reference {forbidden}: {rel}")
    return errors
