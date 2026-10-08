#!/usr/bin/env python3
"""Phase 1: promote workshop vi-* interviews -> public interviews/interview-YYYY-MM-DD-{host-slug}/ packets."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

import yaml

PH_CIV = Path(__file__).resolve().parents[1]
DEFAULT_WORKSHOP = PH_CIV.parent / "strategy-codex" / "codex" / "predictive-history"
MANIFEST_PATH = PH_CIV / "data" / "interviews" / "manifest.json"
INGESTED_AT = date.today().isoformat()

COMMENTARY_CANVAS = """
## Project Canvas

### Project Leverage

- What this interview can unlock for provenance review and cross-volume comparison:
- How this packet supports source-lattice reading without foregrounding Volume I/II routes:

### Laws / Patterns Exposed

- Candidate law or pattern from workshop analysis:
- Supporting transcript evidence to extract later:

### Volume Role

- Provenance-only (`part: provenance`); not an interwoven spine chapter.
- Cross-link to [`book/provenance/`](../../docs/archive/book-provenance-index.md) when commentary matures.

### Strategy / Present-Day Application

- Possible present-day analogy or strategic use (provisional):
- Evidence needed before operational use:

### Counter-Readings

- Strongest alternative explanation from workshop analysis or external review:

### Open Questions

- Questions for close rereading and external verification:

### Build Notes / Future Enhancements

- Next commentary enhancement pass:
- Needed falsifiers and dated claims review:
"""


def escape_yaml(value: str) -> str:
    if not value:
        return '""'
    if any(ch in value for ch in ':"\\#\n') or value.startswith((" ", "-", "?")):
        return json.dumps(value, ensure_ascii=False)
    return value


def load_manifest() -> list[dict]:
    payload = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return payload["entries"]


def load_workshop_sources(workshop_root: Path) -> dict[str, dict]:
    sources_yaml = workshop_root / "metadata" / "sources.yaml"
    data = yaml.safe_load(sources_yaml.read_text(encoding="utf-8"))
    return {row["source_id"]: row for row in data["sources"] if str(row.get("source_id", "")).startswith("vi-")}


def parse_upload_date(lecture_text: str) -> str:
    match = re.search(
        r"\*\*Date \(YouTube upload\):\*\*\s*(\d{4}-\d{2}-\d{2})",
        lecture_text,
    )
    if match:
        return match.group(1)
    return ""


def extract_full_transcript(lecture_text: str) -> str:
    if "## Full transcript" not in lecture_text:
        raise ValueError("lecture missing ## Full transcript section")
    return lecture_text.split("## Full transcript", 1)[1].strip()


def extract_analysis_section(analysis_text: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\s*\n(.*?)(?=^## |\Z)"
    match = re.search(pattern, analysis_text, flags=re.MULTILINE | re.DOTALL)
    if not match:
        return ""
    body = match.group(1).strip()
    body = re.sub(r"\*\*([^*]+)\*\*", r"\1", body)
    body = re.sub(r" +", " ", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body


def build_transcript(
    source_id: str,
    title: str,
    *,
    publication_date: str,
    url: str,
    video_id: str,
    workshop_source_id: str,
    interviews_episode: int,
    body: str,
) -> str:
    return f"""---
source_id: {source_id}
title: {escape_yaml(title)}
source_series: "Predictive History Interviews"
publication_date: {publication_date}
source_url: {escape_yaml(url)}
canonical_url: {escape_yaml(url)}
source_kind: youtube_interview
video_id: {video_id}
workshop_source_id: {workshop_source_id}
interviews_episode: {interviews_episode}
ingested_at: "{INGESTED_AT}"
transcript_status: curated_transcript
transcript_fidelity: exact_body_match
transcript_source: workshop_promotion
representation_not_endorsement: true
review_status: source_reviewed
source_reviewed_at: {INGESTED_AT}
part: provenance
part_role: provenance
series: interviews
---

# {title}

## Part I: Full transcript

{body}
"""


def build_commentary(
    source_id: str,
    title: str,
    *,
    thesis: str,
    terms: str,
    claims: str,
    workshop_source_id: str,
) -> str:
    thesis_block = thesis or "Seed thesis pending close reread."
    terms_block = terms or "- To be extracted on commentary pass"
    claims_block = claims or "- Treat predictive or motive-attribution claims as provisional until externally reviewed."
    return f"""---
source_id: {source_id}
title: {escape_yaml(title)}
source_series: "Predictive History Interviews"
source_chapter_path: interviews/{source_id}/{source_id}.md
commentary_status: in-review
review_status: source_reviewed
annotation_status: drafted
source_reviewed_at: {INGESTED_AT}
template_family: provenance-interview-commentary
part: provenance
part_role: provenance
workshop_source_id: {workshop_source_id}
representation_not_endorsement: true
canvas_status: open
analysis_depth: seed
scaffold_version: ph_civ_commentary_canvas_v1
---

# {title}

## Core Strategic Thesis

{thesis_block}

## Defined Terms (speaker usage)

{terms_block}

## Claims, Forecasts, And Falsifiers

{claims_block}

## Evidence Limits And Date Sensitivity

This commentary seeds workshop analysis into a provenance packet. Current-event claims and strategic predictions require external review before reuse as operational guidance.

## Counter-Readings

- Alternative explanations should be added during the next commentary pass.

## Open Issues For Review

- Mark which claims are descriptive, interpretive, predictive, and theatrical.
- Add external chronology where the interview cites current events.
- Link related interviews when commentary matures.

{COMMENTARY_CANVAS}
"""


def build_readme(source_id: str, title: str, url: str) -> str:
    return f"""# {title}

This chapter folder is a public study doorway for `{source_id}`.

## Start Here

Use this folder when someone shares the GitHub chapter link in a YouTube comment or an LLM chat. Start with the transcript, then use the commentary canvas and orientation card to keep the reading bounded.

## Source-Lattice Reading Order

Treat this chapter folder as a small source-lattice:

1. `Doorway` - this README tells you what the packet is and what limits apply.
2. `Primary source floor` - read the transcript and public source capture first.
3. `Secondary support` - use the commentary canvas, orientation payload, and public card only after the source floor is open.
4. `Widened interpretation` - draw comparisons or broader claims only after keeping the review status in view.

## Source Video

- YouTube: {url}

## Files

- [Transcript]({source_id}.md)
- [Commentary canvas]({source_id}-commentary.md)
- [Public card](../../data/cards/{source_id}.md)

## Review Status

`in_review`. Do not treat provisional transcript text, named claims, quotations, or current-event predictions as final until review is complete.

## LLM Prompt

Paste this folder link into ChatGPT, Claude, or Grok and ask:

> Guide me through this chapter folder as a public study packet. Start with the transcript, then use the commentary canvas and orientation/card guardrails. Keep provisional claims bounded and separate source representation from verification.
>
> Use a source-lattice reading order: README first, transcript and source capture second, commentary/orientation/card third, and broader interpretation only after the source floor is stable.

## Guardrails

This folder represents public interview material on the provenance surface. It is not a private note dump, not an endorsement layer, and not a substitute for source review.
"""


def build_card_md(source_id: str, title: str, workshop_source_id: str) -> str:
    return f"""---
source_id: {source_id}
title: {title}
series: interviews
part: provenance
placement_weight: light
review_status: in_review
workshop_source_id: {workshop_source_id}
---

# {title}

## Where This Sits

`{source_id}` sits on the provenance surface (`part: provenance`, `series: interviews`). Workshop crosswalk: `{workshop_source_id}`.

## Reading Posture

Read this as a provenance orientation card, not as a substitute for the transcript or commentary canvas. Separate source representation from verification.

## Historical Pressure Points

- Seed pressure points pending commentary pass
- Interview framing and present-day application hooks to be extracted from the transcript

## Limits of the Frame

This entry is in review. Do not treat interpretive frames, hidden-intention claims, or forecasts as verified fact without external review.

## Return Path

Return through `interviews/{source_id}/{source_id}.md` for exact transcript wording and `interviews/{source_id}/{source_id}-commentary.md` for bounded analysis.
"""


def build_card_jsonl(
    source_id: str,
    title: str,
    publication_date: str,
    workshop_source_id: str,
) -> dict:
    return {
        "cross_volume_corridor": "",
        "derived_corpus": "provenance",
        "part": "provenance",
        "part_role": "provenance",
        "placement_weight": "light",
        "publication_date": publication_date,
        "review_status": "in_review",
        "workshop_source_id": workshop_source_id,
        "sections": {
            "Historical Pressure Points": "- Seed pressure points pending commentary pass\n- Interview framing hooks to be extracted from the transcript",
            "Limits of the Frame": "This entry is in review. Do not treat interpretive frames or forecasts as verified fact without external review.",
            "Reading Posture": "Read this as a provenance orientation card, not as a substitute for the transcript or commentary canvas.",
            "Return Path": f"Return through `interviews/{source_id}/`, the commentary canvas, and `interviews/{source_id}/{source_id}.md`.",
            "Where This Sits": f"`{source_id}` is a public interview packet on the provenance surface (`part: provenance`, workshop `{workshop_source_id}`).",
        },
        "series": "interviews",
        "source_id": source_id,
        "source_kind": "youtube_interview",
        "source_paths": {
            "commentary_path": f"interviews/{source_id}/{source_id}-commentary.md",
            "source_chapter_path": f"interviews/{source_id}/{source_id}.md",
        },
        "source_snapshot": {
            "commit": "workshop-promotion",
            "path": f"data/cards/{source_id}.md",
            "repo": "public-source-capture",
        },
        "title": title,
    }


def merge_cards_jsonl(new_cards: list[dict]) -> None:
    path = PH_CIV / "data" / "cards.jsonl"
    existing = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    new_ids = {c["source_id"] for c in new_cards}
    existing = [c for c in existing if c["source_id"] not in new_ids]
    existing.extend(new_cards)
    existing.sort(key=lambda row: row["source_id"])
    path.write_text(
        "\n".join(json.dumps(c, ensure_ascii=False) for c in existing) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def intake_interview(
    manifest_row: dict,
    workshop_row: dict,
    workshop_root: Path,
) -> str:
    workshop_source_id = manifest_row["workshop_source_id"]
    source_id = manifest_row["source_id"]
    if manifest_row["source_id"] != source_id:
        raise ValueError(f"manifest source_id mismatch for {workshop_source_id}")

    lecture_path = workshop_root / workshop_row["lecture_path"]
    analysis_path = workshop_root / workshop_row["analysis_path"]
    lecture_text = lecture_path.read_text(encoding="utf-8")
    upload_date = parse_upload_date(lecture_text) or str(workshop_row.get("publication_date", ""))[:10]
    pub_date = manifest_row["publication_date"]
    if upload_date and upload_date != pub_date:
        raise ValueError(
            f"{workshop_source_id}: lecture upload date {upload_date} != manifest {pub_date}"
        )

    title = workshop_row["title"]
    url = workshop_row["canonical_url"]
    video_id = workshop_row["video_id"]
    interviews_episode = manifest_row["interviews_episode"]
    body = extract_full_transcript(lecture_text)

    analysis_text = analysis_path.read_text(encoding="utf-8") if analysis_path.exists() else ""
    thesis = extract_analysis_section(analysis_text, "Thesis / aim")
    terms = extract_analysis_section(analysis_text, "Defined terms (speaker usage)")
    claims = extract_analysis_section(analysis_text, "Claims (numbered)")

    target = PH_CIV / "interviews" / source_id
    target.mkdir(parents=True, exist_ok=True)

    (target / f"{source_id}.md").write_text(
        build_transcript(
            source_id,
            title,
            publication_date=pub_date,
            url=url,
            video_id=video_id,
            workshop_source_id=workshop_source_id,
            interviews_episode=interviews_episode,
            body=body,
        ),
        encoding="utf-8",
        newline="\n",
    )
    (target / f"{source_id}-commentary.md").write_text(
        build_commentary(
            source_id,
            title,
            thesis=thesis,
            terms=terms,
            claims=claims,
            workshop_source_id=workshop_source_id,
        ),
        encoding="utf-8",
        newline="\n",
    )
    (target / "README.md").write_text(build_readme(source_id, title, url), encoding="utf-8", newline="\n")

    card_md = PH_CIV / "data" / "cards" / f"{source_id}.md"
    card_md.write_text(build_card_md(source_id, title, workshop_source_id), encoding="utf-8", newline="\n")
    return source_id


def ensure_ph_civ_index() -> None:
    sys.path.insert(0, str(PH_CIV / "src"))
    from civ_ph.ph_civ_index import ensure_ph_civ_index as regen

    regen(force=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote workshop vi-* interviews to public interviews/")
    parser.add_argument(
        "--workshop-root",
        type=Path,
        default=DEFAULT_WORKSHOP,
        help="Path to strategy-codex codex/predictive-history (read-only)",
    )
    args = parser.parse_args()
    workshop_root: Path = args.workshop_root
    if not workshop_root.is_dir():
        print(f"workshop root not found: {workshop_root}", file=sys.stderr)
        return 1

    manifest = load_manifest()
    workshop_sources = load_workshop_sources(workshop_root)
    created: list[str] = []
    new_cards: list[dict] = []

    for row in manifest:
        ws_id = row["workshop_source_id"]
        if ws_id not in workshop_sources:
            print(f"missing workshop source: {ws_id}", file=sys.stderr)
            return 1
        ws = workshop_sources[ws_id]
        source_id = intake_interview(row, ws, workshop_root)
        created.append(source_id)
        new_cards.append(
            build_card_jsonl(
                source_id,
                ws["title"],
                row["publication_date"],
                ws_id,
            )
        )

    merge_cards_jsonl(new_cards)
    ensure_ph_civ_index()
    print(f"intake complete: {len(created)} interviews -> {created[0]} ... {created[-1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
