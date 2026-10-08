#!/usr/bin/env python3
"""Phase 2: intake workshop Substack essays es-01..es-32 -> public dated essay IDs."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

import yaml

PH_CIV = Path(__file__).resolve().parents[1]
WORKSHOP = PH_CIV.parent.parent / "codex" / "predictive-history"
SOURCES_YAML = WORKSHOP / "metadata" / "sources.yaml"
SKIP_ES_NUMBERS = {33, 34, 35}  # already public as essay-2026-04-04-world-war-trump..essay-2026-04-25-the-trump-new-deal
MAX_ES = 32
INGESTED_AT = date.today().isoformat()

COMMENTARY_CANVAS = """---

## Project Canvas

### Project Leverage

- What this chapter can unlock for the broader ph-civ project:
- How this chapter can support reader navigation, teaching, writing, product design, or strategic synthesis:
- What should become easier after this chapter is developed:

### Laws / Patterns Exposed

- Candidate law or pattern:
- Supporting transcript evidence to extract later:
- Related public pattern IDs or future pattern candidates:

### Volume Role

- Conceptual volume role:
- Relationship to Volume I law discovery or Volume II law application:
- Bridge/support role, if any:

### Strategy / Present-Day Application

- Possible present-day analogy or strategic use:
- Evidence needed before using the analogy operationally:
- Risks of overextension:

### Counter-Readings

- Strongest alternative explanation:
- External sources or schools of thought to consult:
- What would weaken the chapter's current framing:

### Open Questions

- Questions for close rereading:
- Questions for external verification:
- Questions for cross-volume comparison:

### Build Notes / Future Enhancements

- Next concrete enhancement pass:
- Needed links, manifests, or pattern entries:
- Completion blockers:
"""


def load_essay_manifest() -> list[dict]:
    data = yaml.safe_load(SOURCES_YAML.read_text(encoding="utf-8"))
    rows = [s for s in data["sources"] if str(s.get("source_id", "")).startswith("es-")]
    rows.sort(key=lambda s: int(s["source_id"].split("-")[1]))
    out = []
    for row in rows:
        num = int(row["source_id"].split("-")[1])
        if num > MAX_ES or num in SKIP_ES_NUMBERS:
            continue
        out.append(row)
    return out


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta = yaml.safe_load(parts[1]) or {}
    body = parts[2].lstrip("\n")
    return meta, body


def slug_from_url(url: str) -> str:
    path = urlparse(url).path.rstrip("/")
    return path.split("/")[-1] if path else ""


def dated_essay_id(publication_date: str, substack_slug: str) -> str:
    pub = str(publication_date)[:10]
    slug = substack_slug.strip()
    if not pub or not slug:
        raise ValueError(f"missing publication_date or substack_slug: date={pub!r} slug={slug!r}")
    return f"essay-{pub}-{slug}"


def load_public_manifest_ids() -> set[str]:
    path = PH_CIV / "data" / "essays" / "manifest.json"
    if not path.is_file():
        return set()
    data = json.loads(path.read_text(encoding="utf-8"))
    return {e["source_id"] for e in data.get("entries", [])}


def assert_unique_dated_id(source_id: str, existing: set[str]) -> None:
    if source_id in existing:
        raise SystemExit(f"dated essay source_id collision: {source_id}")


def extract_essay_body(workshop_text: str) -> str:
    _, body = parse_frontmatter(workshop_text)
    if "## Essay body" in body:
        return body.split("## Essay body", 1)[1].strip()
    if "## Part I: Full transcript" in body:
        return body.split("## Part I: Full transcript", 1)[1].strip()
    lines = body.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    return "\n".join(lines).strip()


def escape_yaml(value: str) -> str:
    if not value:
        return '""'
    if any(ch in value for ch in ':"\\#\n') or value.startswith((" ", "-", "?")):
        return json.dumps(value, ensure_ascii=False)
    return value


def build_transcript(source_id: str, meta: dict, workshop_meta: dict, body: str) -> str:
    title = meta["title"]
    pub = str(meta.get("publication_date", ""))[:10]
    url = meta["canonical_url"]
    slug = workshop_meta.get("substack_slug") or slug_from_url(url)
    essays_volume = workshop_meta.get("essays_volume", 7)
    deck = workshop_meta.get("deck", "")
    paid = workshop_meta.get("paid", True)
    fm = f"""---
source_id: {source_id}
title: {escape_yaml(title)}
source_series: "Predictive History Essays"
publication_date: {pub}
source_url: {escape_yaml(url)}
source_kind: substack_essay
essays_volume: {essays_volume}
substack_slug: {slug}
canonical_url: {escape_yaml(url)}
deck: {escape_yaml(str(deck))}
paid: {str(paid).lower()}
ingested_at: "{INGESTED_AT}"
transcript_status: curated_transcript
transcript_fidelity: exact_body_match
transcript_source: workshop_promotion
representation_not_endorsement: true
review_status: source_reviewed
source_reviewed_at: {INGESTED_AT}
part: civilization
part_role: civilization
---

# {title}

## Part I: Full transcript

{body}
"""
    return fm


def build_commentary(source_id: str, title: str) -> str:
    return f"""---
source_id: {source_id}
title: {escape_yaml(title)}
source_series: "Predictive History Essays"
source_chapter_path: essays/{source_id}.md
source_corpus_path: corpus/essays/{source_id}.md
commentary_status: in-review
review_status: source_reviewed
annotation_status: drafted
source_reviewed_at: {INGESTED_AT}
template_family: civilization-essay-commentary
part: civilization
part_role: civilization
representation_not_endorsement: true
canvas_status: open
analysis_depth: seed
scaffold_version: ph_civ_commentary_canvas_v1
---

# {title}

## Core Strategic Thesis

`{source_id}` is a public essay packet on the ph-civ essays surface. The working thesis is that the essay should be read as an interpretive argument within the Predictive History civilizational frame, not as settled proof or operational guidance.

## Neutral Lecture Summary

Seed summary pending close reread. Use the transcript for exact wording before quoting or teaching from this packet.

## Actors, Systems, And Stakes

- **Primary actors:** To be extracted on commentary pass
- **System pressure:** To be extracted on commentary pass
- **Decision field:** Separate descriptive claims, interpretive frames, and forecasts.
- **Reader task:** Keep representation distinct from verification.

## Claims, Forecasts, And Falsifiers

- Treat predictive or motive-attribution claims as provisional until externally reviewed.
- Add dated falsifiers during the next commentary enhancement pass.

## Evidence Limits And Date Sensitivity

This commentary is a seed canvas, not final analysis. Current-event claims and strategic predictions require external review before reuse as operational guidance.

## Counter-Readings

- Alternative explanations should be added during the next commentary pass.

## Open Issues For Review

- Mark which claims are descriptive, interpretive, predictive, and theatrical.
- Add external chronology where the essay cites current events.
- Link related essays in the same arc when commentary matures.

{COMMENTARY_CANVAS}
"""


def build_readme(source_id: str, title: str, url: str) -> str:
    return f"""# {title}

This chapter folder is a public study doorway for `{source_id}`.

## Start Here

Use this folder when someone shares the GitHub chapter link in a YouTube comment or an LLM chat. Start with the essay, then use the commentary canvas and orientation card to keep the reading bounded.

## Source-Lattice Reading Order

Treat this chapter folder as a small source-lattice:

1. `Doorway` - this README tells you what the packet is and what limits apply.
2. `Primary source floor` - read the essay and public source capture first.
3. `Secondary support` - use the commentary canvas, orientation payload, and public card only after the source floor is open.
4. `Widened interpretation` - draw comparisons or broader claims only after keeping the review status in view.

## Source

- Substack: {url}

## Files

- [Essay]({source_id}.md)
- [Commentary canvas]({source_id}-commentary.md)
- [Public card](../../data/cards/{source_id}.md)

## Review Status

`in_review`. Do not treat provisional essay text, named claims, quotations, or current-event predictions as final until review is complete.

## LLM Prompt

Paste this folder link into ChatGPT, Claude, or Grok and ask:

> Guide me through this chapter folder as a public study packet. Start with the essay, then use the commentary canvas and orientation/card guardrails. Keep provisional claims bounded and separate source representation from verification.
>
> Use a source-lattice reading order: README first, essay and source capture second, commentary/orientation/card third, and broader interpretation only after the source floor is stable.

## Guardrails

This folder represents the public essay material and companion study apparatus. It is not a private note dump, not an endorsement layer, and not a substitute for source review.
"""


def build_card_md(source_id: str, title: str) -> str:
    return f"""---
source_id: {source_id}
title: {title}
series: essays
part: civilization
placement_weight: strong
review_status: in_review
---

# {title}

## Where This Sits

`{source_id}` sits on the ph-civ essays surface (`part: civilization`). It preserves the Substack essay as a public study packet with bounded commentary.

## Reading Posture

Read this as an orientation card, not as a substitute for the essay body or commentary canvas. Separate source representation from verification.

## Historical Pressure Points

- Seed pressure points pending commentary pass
- Civilizational framing and present-day application hooks to be extracted from the essay

## Limits of the Frame

This entry is in review. Do not treat interpretive frames, hidden-intention claims, or forecasts as verified fact without external review.

## Return Path

Return through `essays/{source_id}.md` for exact essay wording and `commentaries/{source_id}-commentary.md` for bounded analysis.
"""


def build_card_jsonl(source_id: str, meta: dict) -> dict:
    title = meta["title"]
    pub = str(meta.get("publication_date", ""))[:10]
    return {
        "cross_volume_corridor": "",
        "derived_corpus": "ph-civ",
        "part": "civilization",
        "placement_weight": "strong",
        "publication_date": pub,
        "review_status": "in_review",
        "sections": {
            "Historical Pressure Points": "- Seed pressure points pending commentary pass\n- Civilizational framing hooks to be extracted from the essay",
            "Limits of the Frame": "This entry is in review. Do not treat interpretive frames or forecasts as verified fact without external review.",
            "Reading Posture": "Read this as an orientation card, not as a substitute for the essay body or commentary canvas.",
            "Return Path": f"Return through `essays/{source_id}.md`, `commentaries/{source_id}-commentary.md`, and the public card.",
            "Where This Sits": f"`{source_id}` is a public essay packet on the ph-civ essays surface (`part: civilization`).",
        },
        "series": "essays",
        "source_id": source_id,
        "source_paths": {
            "commentary_path": f"commentaries/{source_id}-commentary.md",
            "orientation_payload_path": "",
            "source_chapter_path": f"essays/{source_id}.md",
            "source_corpus_path": f"corpus/essays/{source_id}.md",
        },
        "source_snapshot": {
            "commit": "workshop-promotion",
            "path": f"data/cards/{source_id}.md",
            "repo": "public-source-capture",
        },
        "title": title,
    }


def intake_essay(meta: dict, existing_ids: set[str]) -> str:
    es_id = meta["source_id"]
    pub = str(meta.get("publication_date", ""))[:10]
    url = meta["canonical_url"]
    workshop_path = WORKSHOP / meta["lecture_path"]
    workshop_text = workshop_path.read_text(encoding="utf-8")
    workshop_meta, _ = parse_frontmatter(workshop_text)
    slug = workshop_meta.get("substack_slug") or slug_from_url(url)
    source_id = dated_essay_id(pub, str(slug))
    assert_unique_dated_id(source_id, existing_ids)
    essay_path = PH_CIV / "essays" / f"{source_id}.md"
    commentary_path = PH_CIV / "commentaries" / f"{source_id}-commentary.md"
    if essay_path.exists() or commentary_path.exists():
        raise SystemExit(f"refusing to overwrite existing packet: {essay_path} or {commentary_path}")

    body = extract_essay_body(workshop_text)
    if not body.strip():
        raise SystemExit(f"empty essay body: {workshop_path}")

    PH_CIV.joinpath("commentaries").mkdir(exist_ok=True)
    title = meta["title"]

    essay_path.write_text(
        build_transcript(source_id, meta, workshop_meta, body), encoding="utf-8", newline="\n"
    )
    commentary_path.write_text(
        build_commentary(source_id, title), encoding="utf-8", newline="\n"
    )

    card_md = PH_CIV / "data" / "cards" / f"{source_id}.md"
    card_md.write_text(build_card_md(source_id, title), encoding="utf-8", newline="\n")
    existing_ids.add(source_id)
    return source_id


def merge_cards_jsonl(new_cards: list[dict]) -> None:
    path = PH_CIV / "data" / "cards.jsonl"
    existing = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    new_ids = {c["source_id"] for c in new_cards}
    existing = [c for c in existing if c["source_id"] not in new_ids]

    out: list[dict] = []
    inserted = False
    for card in existing:
        if not inserted and card.get("source_id") == "essay-2026-04-04-world-war-trump":
            out.extend(new_cards)
            inserted = True
        out.append(card)
    if not inserted:
        out.extend(new_cards)

    path.write_text(
        "\n".join(json.dumps(c, ensure_ascii=False) for c in out) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def sync_index_json() -> None:
    jsonl = [
        json.loads(line)
        for line in (PH_CIV / "data/cards.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    idx_path = PH_CIV / "data/index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    review = {c["source_id"]: c.get("review_status", "in_review") for c in idx.get("cards", [])}
    idx["cards"] = [
        {
            "part": c["part"],
            "path": f"data/cards/{c['source_id']}.md",
            "placement_weight": c.get("placement_weight", "strong"),
            "review_status": review.get(c["source_id"], c.get("review_status", "in_review")),
            "series": c["series"],
            "source_id": c["source_id"],
            "title": c["title"],
        }
        for c in jsonl
    ]
    idx["card_count"] = len(jsonl)
    idx_path.write_text(json.dumps(idx, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def update_essays_readme(count: int) -> None:
    path = PH_CIV / "essays" / "README.md"
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r"\*\*Public today:\*\* \d+ essay chapter packets.*",
        f"**Public today:** {count} essay chapter packets (`essay-2025-08-06-vision-mission-goals` … see manifest).",
        text,
        count=1,
    )
    path.write_text(text, encoding="utf-8", newline="\n")


def main() -> int:
    manifest = load_essay_manifest()
    existing_ids = load_public_manifest_ids()
    created: list[str] = []
    new_cards: list[dict] = []
    for meta in manifest:
        source_id = intake_essay(meta, existing_ids)
        created.append(source_id)
        new_cards.append(build_card_jsonl(source_id, meta))

    merge_cards_jsonl(new_cards)
    public_count = len(list((PH_CIV / "essays").glob("essay-*.md")))
    update_essays_readme(public_count)

    print(f"intake complete: {len(created)} essays -> {', '.join(created[:3])} ... {created[-1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
