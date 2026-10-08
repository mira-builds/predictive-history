#!/usr/bin/env python3
"""Phase 1 study-edition enrichments (pilot: civ-07)."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any

PHASE1_CHAPTER = "civ-07"
PHASE1_SEMINAR_SLUGS = frozenset(
    {"homer-poet-for-people", "iliad-empathy", "greece-china-contrast"}
)
CONTRAST_SLUG = "greece-china-contrast"

GREECE_MARKERS = re.compile(
    r"\b(greece|greek|homer|plato|thucydides|phoenician|alphabet|polis|iliad)\b",
    re.I,
)
CHINA_MARKERS = re.compile(
    r"\b(china|chinese|confucian|scholar.?official|classical chinese|censorship|merchant|farmer)\b",
    re.I,
)


def load_json(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def default_claim_aid(claim: dict[str, str], section_body: str) -> dict[str, Any]:
    text = claim["claim"]
    thesis = text if len(text) <= 120 else text[:117].rstrip() + "…"
    snippet = " ".join(section_body.split())[:140]
    notices = [
        f"Lecture passage (excerpt): {snippet}…" if snippet else "Open the linked passage.",
        "Check whether the claim wording matches this section before quoting.",
    ]
    return {"thesis": thesis, "notices": notices}


def load_claim_aids(
    root: Path, source_id: str, claims: list[dict], sections_by_slug: dict[str, str]
) -> dict[str, dict[str, Any]]:
    path = root / "site" / "_data" / "generated" / f"{source_id}-claims.json"
    data = load_json(path) or {}
    aids: dict[str, dict[str, Any]] = {}
    for claim in claims:
        key = str(claim["n"])
        if key in data:
            aids[key] = data[key]
        else:
            aids[key] = default_claim_aid(claim, sections_by_slug.get(claim["anchor"], ""))
    return aids


def load_seminar_aids(root: Path, source_id: str) -> dict[str, dict[str, Any]]:
    path = root / "site" / "_data" / "generated" / f"{source_id}-seminar.json"
    data = load_json(path) or {}
    fallback = {
        "prompts": [
            "What in this section is doing the most work for the lecture's argument?",
            "What would you need to verify outside this passage?",
        ],
        "pressure": "Where might the lecture overstate or compress history here?",
    }
    return {slug: data.get(slug, fallback) for slug in PHASE1_SEMINAR_SLUGS}


def heuristic_contrast_split(body: str) -> dict[str, Any]:
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", " ".join(body.split())) if s.strip()]
    left: list[str] = []
    right: list[str] = []
    for sentence in sentences:
        g = len(GREECE_MARKERS.findall(sentence))
        c = len(CHINA_MARKERS.findall(sentence))
        if c > g:
            right.append(sentence)
        else:
            left.append(sentence)
    if not left or not right:
        mid = max(1, len(sentences) // 2)
        left = [" ".join(sentences[:mid])]
        right = [" ".join(sentences[mid:])]
    return {
        "slug": CONTRAST_SLUG,
        "divider": "Structural contrast · lecture representation",
        "left_label": "Greece",
        "right_label": "China",
        "left_paragraphs": left,
        "right_paragraphs": right,
    }


def load_contrast_split(root: Path, source_id: str, section_body: str) -> dict[str, Any]:
    path = root / "site" / "_data" / "overrides" / f"{source_id}-contrast.json"
    override = load_json(path)
    if override:
        return override
    return heuristic_contrast_split(section_body)


def enrich_bundle(root: Path, bundle: dict[str, Any]) -> dict[str, Any]:
    if bundle.get("source_id") != PHASE1_CHAPTER:
        return bundle
    sections_by_slug = {row["slug"]: row["body"] for row in bundle["sections"]}  # type: ignore[index]
    contrast_body = sections_by_slug.get(CONTRAST_SLUG, "")
    bundle["phase1"] = {
        "claim_aids": load_claim_aids(root, PHASE1_CHAPTER, bundle["claims"], sections_by_slug),  # type: ignore[arg-type]
        "seminar": load_seminar_aids(root, PHASE1_CHAPTER),
        "contrast_split": load_contrast_split(root, PHASE1_CHAPTER, contrast_body),
        "seminar_slugs": sorted(PHASE1_SEMINAR_SLUGS),
    }
    return bundle


def render_seminar_strip(slug: str, seminar: dict[str, Any]) -> str:
    prompts = seminar.get("prompts") or []
    pressure = seminar.get("pressure", "")
    prompt_items = "".join(f"<li>{html.escape(p)}</li>" for p in prompts)
    return (
        f'<details class="seminar-strip" data-slug="{html.escape(slug)}">'
        f"<summary>Seminar</summary>"
        f'<ul class="seminar-prompts">{prompt_items}</ul>'
        f'<p class="seminar-pressure"><strong>Pressure:</strong> {html.escape(pressure)}</p>'
        f'<p class="gen-ai-footer">Generated study aid · not new evidence · verify in transcript.</p>'
        f"</details>"
    )


def render_contrast_floor(section: dict[str, Any], contrast: dict[str, Any], seminar_html: str) -> str:
    slug = html.escape(section["slug"])
    label = html.escape(section["label"])
    nums = section.get("claim_numbers") or []
    markers = "".join(
        f'<button type="button" class="claim-marker" data-claim="{n}">[{n}]</button>'
        for n in nums
    )
    left_items = "".join(
        f"<p>{html.escape(p)}</p>" for p in contrast.get("left_paragraphs") or []
    )
    right_items = "".join(
        f"<p>{html.escape(p)}</p>" for p in contrast.get("right_paragraphs") or []
    )
    divider = html.escape(str(contrast.get("divider", "Structural contrast")))
    left_label = html.escape(str(contrast.get("left_label", "Greece")))
    right_label = html.escape(str(contrast.get("right_label", "China")))
    return (
        f'<section class="transcript-section contrast-section" id="{slug}" data-slug="{slug}">'
        f'<header class="section-head"><h3>{label}</h3>{markers}</header>'
        f'<div class="contrast-split" role="group" aria-label="{divider}">'
        f'<p class="contrast-divider">{divider}</p>'
        f'<div class="contrast-columns">'
        f'<div class="contrast-col contrast-greece"><h4>{left_label}</h4>{left_items}</div>'
        f'<div class="contrast-col contrast-china"><h4>{right_label}</h4>{right_items}</div>'
        f"</div></div>{seminar_html}</section>"
    )


def render_floor_section(section: dict[str, Any], phase1: dict[str, Any] | None) -> str:
    slug = section["slug"]
    seminar_html = ""
    if phase1 and slug in PHASE1_SEMINAR_SLUGS:
        seminar_html = render_seminar_strip(slug, phase1["seminar"].get(slug, {}))
    if phase1 and slug == CONTRAST_SLUG:
        return render_contrast_floor(section, phase1["contrast_split"], seminar_html)
    slug_esc = html.escape(slug)
    body = html.escape(section["body"])
    label = html.escape(section["label"])
    nums = section.get("claim_numbers") or []
    markers = "".join(
        f'<button type="button" class="claim-marker" data-claim="{n}">[{n}]</button>'
        for n in nums
    )
    return (
        f'<section class="transcript-section" id="{slug_esc}" data-slug="{slug_esc}">'
        f'<header class="section-head"><h3>{label}</h3>{markers}</header>'
        f"<p>{body}</p>{seminar_html}</section>"
    )


def render_notes_phase1(claim_items: list[str], phase1: dict[str, Any]) -> str:
    morph = (
        '<div id="claim-morph-view" class="claim-morph-view hidden" aria-live="polite">'
        '<button type="button" class="claim-morph-back" id="claim-morph-all">← View all claims</button>'
        '<article class="claim-morph-card">'
        '<p class="claim-morph-title"><span id="claim-morph-n"></span></p>'
        '<p class="claim-morph-thesis" id="claim-morph-thesis"></p>'
        '<ul class="claim-morph-notices" id="claim-morph-notices"></ul>'
        '<p class="claim-morph-meta" id="claim-morph-meta"></p>'
        '<button type="button" class="claim-jump" id="claim-morph-passage">↗ Return to passage</button>'
        '<p class="gen-ai-footer">Generated study aid · not new evidence · verify in transcript.</p>'
        "</article></div>"
    )
    aids_json = html.escape(json.dumps(phase1["claim_aids"], ensure_ascii=False))
    return (
        f'{morph}<div id="claims-list-view" class="claims-list">{"".join(claim_items)}</div>'
        f'<script id="phase1-claim-aids" type="application/json">{aids_json}</script>'
    )
