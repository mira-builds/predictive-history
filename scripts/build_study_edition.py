#!/usr/bin/env python3
"""Build Phase 0 study-edition bundles and static HTML from chapter packets."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from pathlib import Path

from study_edition_phase1 import (  # noqa: E402
    CONTRAST_SLUG,
    enrich_bundle,
    render_floor_section,
    render_notes_phase1,
)

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_ROOT = ROOT / "lectures" / "civilization"
PARTS_JSON = ROOT / "data" / "parts" / "volume-i-parts.json"
SPINE_JSON = ROOT / "data" / "spines" / "homer-to-tolstoy.json"
SITE_DATA = ROOT / "site" / "_data" / "chapters"
SITE_DIST = ROOT / "site" / "dist"
ASSETS = ROOT / "site" / "assets"

PART_STUDY_CHAPTERS: dict[str, list[str]] = {
    "01": [f"civ-{n:02d}" for n in range(1, 7)],
    "02": [f"civ-{n:02d}" for n in range(7, 14)],
    "03": [f"civ-{n:02d}" for n in range(14, 18)],
    "04": [f"civ-{n:02d}" for n in range(18, 24)],
    "05": [f"civ-{n:02d}" for n in range(24, 29)],
    "06": [f"civ-{n:02d}" for n in range(29, 35)],
    "07": [f"civ-{n:02d}" for n in range(35, 42)],
    "08": [f"civ-{n:02d}" for n in range(42, 51)],
    "09": [f"civ-{n:02d}" for n in range(51, 54)],
    "10": [f"civ-{n:02d}" for n in range(54, 61)],
}

TRANSCRIPT_MARKER = "## Part I: Full transcript\n\n"
SOURCE_ID_RE = re.compile(r"^civ-\d{2}$")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
SECTION_RE = re.compile(r"^### (.+?)\s*$", re.MULTILINE)
L2_ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*`[^`]*#([a-z0-9-]+)`\s*\|\s*([^|]+)\|\s*([^|]+)\|",
    re.MULTILINE,
)
CONCEPT_RE = re.compile(
    r"^- \*\*([^*]+)\*\*:\s*(.+?)\s*`[^`]*#([a-z0-9-]+)`",
    re.MULTILINE,
)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    meta: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"')
    return meta, text[match.end() :]


def slug_label(slug: str) -> str:
    return slug.replace("-", " ").title()


def heading_slug(heading: str) -> str:
    """Match the stable GitHub-style anchors used by the transcript rails."""
    return re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-")


def transcript_body(text: str) -> str:
    if TRANSCRIPT_MARKER not in text:
        raise ValueError("transcript missing Part I marker")
    body = text.split(TRANSCRIPT_MARKER, 1)[1]
    full_marker = "## Full transcript\n"
    if full_marker in body:
        alt_body = body.split(full_marker, 1)[1]
        if SECTION_RE.search(alt_body):
            return alt_body
    return body


def parse_sections(body: str) -> tuple[str, list[dict[str, str]]]:
    parts = SECTION_RE.split(body)
    if len(parts) < 2:
        raise ValueError("transcript has no ### section rails")
    opening = parts[0].strip()
    sections: list[dict[str, str]] = []
    i = 1
    while i < len(parts):
        slug = heading_slug(parts[i].strip())
        content = parts[i + 1].strip() if i + 1 < len(parts) else ""
        sections.append({"slug": slug, "body": content})
        i += 2
    return opening, sections


def parse_layer1(commentary: str) -> str:
    marker = "## Layer 1 - Neutral Summary\n\n"
    if marker not in commentary:
        return ""
    chunk = commentary.split(marker, 1)[1]
    end = chunk.find("\n---\n")
    if end >= 0:
        chunk = chunk[:end]
    return chunk.strip()


def parse_claims(commentary: str) -> list[dict[str, str]]:
    block = commentary
    start = block.find("### Major Claims")
    if start < 0:
        return []
    block = block[start:]
    end = block.find("### Core Concepts")
    if end >= 0:
        block = block[:end]
    claims: list[dict[str, str]] = []
    for match in L2_ROW_RE.finditer(block):
        claims.append(
            {
                "n": int(match.group(1)),
                "claim": match.group(2).strip(),
                "anchor": match.group(3).strip(),
                "strength": match.group(4).strip(),
                "confidence": match.group(5).strip(),
            }
        )
    return claims


def parse_concepts(commentary: str) -> list[dict[str, str]]:
    start = commentary.find("### Core Concepts Defined")
    if start < 0:
        return []
    block = commentary[start:]
    end = block.find("\n---\n")
    if end >= 0:
        block = block[:end]
    concepts: list[dict[str, str]] = []
    for match in CONCEPT_RE.finditer(block):
        concepts.append(
            {
                "term": match.group(1).strip(),
                "definition": match.group(2).strip(),
                "anchor": match.group(3).strip(),
            }
        )
    return concepts


def load_part_meta(part_id: str) -> dict[str, str]:
    data = json.loads(PARTS_JSON.read_text(encoding="utf-8"))
    for part in data.get("parts", []):
        if part.get("part_id") == part_id:
            return {
                "part_id": part_id,
                "display_title": part.get("display_title", part_id),
                "title": part.get("title", part_id),
            }
    return {"part_id": part_id, "display_title": part_id, "title": part_id}


def route_context(source_id: str) -> dict[str, object] | None:
    if not SPINE_JSON.is_file():
        return None
    spine = json.loads(SPINE_JSON.read_text(encoding="utf-8"))
    for idx, step in enumerate(spine.get("sequence", []), start=1):
        ids = step.get("source_ids", [])
        if source_id in ids:
            return {
                "spine_id": spine.get("spine_id"),
                "title": spine.get("title"),
                "step": idx,
                "author": step.get("author"),
                "source_ids": ids,
            }
    return None


def resolve_chapter(source_id: str) -> Path:
    if not SOURCE_ID_RE.match(source_id):
        raise ValueError(f"unsupported source_id for Phase 0: {source_id}")
    folder = CHAPTER_ROOT / source_id
    if not folder.is_dir():
        raise FileNotFoundError(f"missing chapter folder: {folder.relative_to(ROOT)}")
    return folder


def build_bundle(source_id: str) -> dict[str, object]:
    folder = resolve_chapter(source_id)
    transcript_path = folder / f"{source_id}-transcript.md"
    commentary_path = folder / f"{source_id}-commentary.md"
    t_meta, t_rest = parse_frontmatter(transcript_path.read_text(encoding="utf-8"))
    c_meta, c_rest = parse_frontmatter(commentary_path.read_text(encoding="utf-8"))
    opening, sections = parse_sections(transcript_body(t_rest))
    claims = parse_claims(c_rest)
    concepts = parse_concepts(c_rest)
    part_id = t_meta.get("part_id") or c_meta.get("part_id", "")
    part = load_part_meta(part_id) if part_id else {}
    anchors = {row["slug"] for row in sections}
    for claim in claims:
        if claim["anchor"] not in anchors:
            raise ValueError(
                f"{source_id}: claim {claim['n']} anchor #{claim['anchor']} missing in transcript"
            )
    claims_by_anchor: dict[str, list[int]] = {}
    for claim in claims:
        claims_by_anchor.setdefault(claim["anchor"], []).append(claim["n"])
    bundle = {
        "source_id": source_id,
        "title": t_meta.get("title") or c_meta.get("title", source_id),
        "part_id": part_id,
        "part": part,
        "review_status": t_meta.get("review_status", "unknown"),
        "transcript_status": t_meta.get("transcript_status", ""),
        "source_video": t_meta.get("canonical_url", ""),
        "route": route_context(source_id),
        "opening": opening,
        "sections": [
            {
                "slug": row["slug"],
                "label": slug_label(row["slug"]),
                "body": row["body"],
                "claim_numbers": claims_by_anchor.get(row["slug"], []),
            }
            for row in sections
        ],
        "claims": claims,
        "concepts": concepts,
        "layer1_summary": parse_layer1(c_rest),
        "paths": {
            "transcript": str(transcript_path.relative_to(ROOT)).replace("\\", "/"),
            "commentary": str(commentary_path.relative_to(ROOT)).replace("\\", "/"),
            "part_commentary": t_meta.get("part_commentary_path", ""),
            "part_bibliography": t_meta.get("part_bibliography_path", ""),
        },
    }
    return enrich_bundle(ROOT, bundle)


def render_html(bundle: dict[str, object]) -> str:
    title = html.escape(str(bundle["title"]))
    source_id = html.escape(str(bundle["source_id"]))
    part = bundle.get("part") or {}
    part_title = html.escape(str(part.get("display_title", "")))
    review = html.escape(str(bundle.get("review_status", "")))
    transcript_status = html.escape(str(bundle.get("transcript_status", "")))
    video = str(bundle.get("source_video") or "")
    route = bundle.get("route") or {}
    route_line = ""
    if route:
        route_line = (
            f"Homer-to-Tolstoy · step {route.get('step')} · {html.escape(str(route.get('author', '')))}"
        )

    outline_items = []
    for section in bundle["sections"]:  # type: ignore[union-attr]
        slug = section["slug"]
        label = html.escape(section["label"])
        nums = section.get("claim_numbers") or []
        badge = ""
        if nums:
            badge = f'<span class="claim-badge">{",".join(str(n) for n in nums)}</span>'
        outline_items.append(
            f'<li><button type="button" class="outline-btn" data-slug="{html.escape(slug)}">'
            f"{label}{badge}</button></li>"
        )

    floor_parts = []
    opening = str(bundle.get("opening") or "").strip()
    if opening:
        floor_parts.append(
            f'<section class="transcript-section opening" id="opening">'
            f"<p>{html.escape(opening)}</p></section>"
        )
    for section in bundle["sections"]:  # type: ignore[union-attr]
        floor_parts.append(render_floor_section(section, bundle.get("phase1")))

    claim_items = []
    for claim in bundle["claims"]:  # type: ignore[union-attr]
        claim_items.append(
            f'<article class="claim-card" id="claim-{claim["n"]}" data-claim="{claim["n"]}" '
            f'data-anchor="{html.escape(claim["anchor"])}">'
            f'<div class="claim-head"><span class="claim-n">{claim["n"]}</span>'
            f'<button type="button" class="claim-jump" data-anchor="{html.escape(claim["anchor"])}">'
            f"↗ passage</button></div>"
            f'<p class="claim-text">{html.escape(claim["claim"])}</p>'
            f'<p class="claim-meta">{html.escape(claim["strength"])} · {html.escape(claim["confidence"])}</p>'
            f"</article>"
        )

    concept_items = []
    for concept in bundle.get("concepts") or []:
        concept_items.append(
            f'<article class="concept-card" data-anchor="{html.escape(concept["anchor"])}">'
            f"<strong>{html.escape(concept['term'])}</strong> "
            f"{html.escape(concept['definition'])}</article>"
        )

    summary = html.escape(str(bundle.get("layer1_summary") or ""))
    video_link = ""
    if video:
        video_link = (
            f'<a class="status-link" href="{html.escape(video)}" target="_blank" rel="noopener">'
            "Source video</a>"
        )

    phase1 = bundle.get("phase1")
    body_class = ' class="phase1-pilot"' if phase1 else ""
    claims_block = (
        render_notes_phase1(claim_items, phase1)
        if phase1
        else f'<div class="claims-list">{"".join(claim_items)}</div>'
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} · Predictive History study edition</title>
  <link rel="stylesheet" href="../../assets/study-edition.css">
</head>
<body{body_class}>
  <header class="top-bar">
    <div class="brand">Predictive History study edition</div>
    <div class="meta">
      <span class="chip">{source_id}</span>
      <span class="chip warn">{review}</span>
      {f'<span class="chip">{route_line}</span>' if route_line else ''}
      {video_link}
    </div>
  </header>
  <main class="study-grid" data-chapter="{source_id}">
    <aside class="panel outline-panel" aria-label="Outline">
      <h2>{part_title}</h2>
      <p class="panel-sub">{title}</p>
      <nav>
        <ol class="outline-list">
          {''.join(outline_items)}
        </ol>
      </nav>
    </aside>
    <article class="panel floor-panel" aria-label="Transcript">
      <div class="status-ribbon">
        Transcript floor · {transcript_status or 'verbatim lecture'} · not quotation-grade until review complete
      </div>
      {''.join(floor_parts)}
    </article>
    <aside class="panel notes-panel" aria-label="Study notes">
      <details class="summary-block" open>
        <summary>Layer 1 summary</summary>
        <p>{summary}</p>
      </details>
      <h3>Layer 2 claims</h3>
      {claims_block}
      <h3>Core concepts</h3>
      <div class="concepts-list">
        {''.join(concept_items)}
      </div>
      <footer class="notes-footer">
        <p>Part apparatus and bibliography remain in repo markdown for Phase 0.</p>
      </footer>
    </aside>
  </main>
  <script src="../../assets/study-edition.js"></script>
  {f'<script>window.STUDY_PHASE1 = {{ "contrastSlug": "{CONTRAST_SLUG}", "focusClaim": 16 }};</script>' if phase1 else ''}
</body>
</html>
"""


def sync_dist_assets() -> None:
    dest = SITE_DIST / "assets"
    dest.mkdir(parents=True, exist_ok=True)
    for name in ("study-edition.css", "study-edition.js"):
        shutil.copy2(ASSETS / name, dest / name)


def write_site_index() -> Path:
    part_links = []
    for part_key in sorted(PART_STUDY_CHAPTERS):
        part_links.append(
            f'<li><a href="study/part-{part_key}/index.html">Part {part_key}</a></li>'
        )
    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Predictive History study edition</title>
  <link rel="stylesheet" href="assets/study-edition.css">
</head>
<body>
  <header class="top-bar">
    <div class="brand">Predictive History study edition</div>
    <div class="meta"><span class="chip">Phase 0 · Parts I–X + civ-07 Phase 1 pilot</span></div>
  </header>
  <main class="part-index">
    <h1>Predictive History · study reader</h1>
    <p class="panel-sub">Three-pane transcript · Layer 2 claims · Part outlines</p>
    <h2>Pilot chapter</h2>
    <ul class="part-chapter-list">
      <li><a href="study/civ-07/index.html">civ-07</a> — Homer / Hellenic World
        <span class="meta-count">(Phase 1 visual pilot)</span></li>
    </ul>
    <h2>Part indexes</h2>
    <ol class="part-chapter-list">
      {''.join(part_links)}
    </ol>
  </main>
</body>
</html>
"""
    path = SITE_DIST / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html_doc, encoding="utf-8", newline="\n")
    return path


def finalize_site() -> None:
    sync_dist_assets()
    write_site_index()
    print(f"build_study_edition: site index -> {SITE_DIST.relative_to(ROOT)}/index.html")


def write_outputs(source_id: str, bundle: dict[str, object], *, write_json: bool = True) -> Path:
    html_path = SITE_DIST / "study" / source_id / "index.html"
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(render_html(bundle), encoding="utf-8", newline="\n")
    if write_json:
        json_path = SITE_DATA / f"{source_id}.json"
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(
            json.dumps(bundle, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    return html_path


def render_part_index(part_key: str, bundles: list[dict[str, object]]) -> str:
    part = bundles[0].get("part") or {} if bundles else {}
    part_title = html.escape(str(part.get("display_title", f"Part {part_key}")))
    items = []
    for bundle in bundles:
        sid = html.escape(str(bundle["source_id"]))
        title = html.escape(str(bundle["title"]))
        claims = len(bundle.get("claims") or [])
        sections = len(bundle.get("sections") or [])
        items.append(
            f'<li><a href="../{sid}/index.html">{sid}</a> — {title} '
            f'<span class="meta-count">({sections} sections · {claims} claims)</span></li>'
        )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{part_title} · Predictive History study edition</title>
  <link rel="stylesheet" href="../../assets/study-edition.css">
</head>
<body>
  <header class="top-bar">
    <div class="brand">Predictive History study edition</div>
    <div class="meta"><span class="chip">Part {html.escape(part_key)}</span></div>
  </header>
  <main class="part-index">
    <h1>{part_title}</h1>
    <p class="panel-sub">Chapter study pages — three-pane transcript · claims · outline</p>
    <ol class="part-chapter-list">
      {''.join(items)}
    </ol>
  </main>
</body>
</html>
"""


def write_part_index(part_key: str, bundles: list[dict[str, object]]) -> Path:
    path = SITE_DIST / "study" / f"part-{part_key}" / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_part_index(part_key, bundles), encoding="utf-8", newline="\n")
    return path


def build_chapters(chapter_ids: list[str], *, write_json: bool = True) -> list[dict[str, object]]:
    bundles: list[dict[str, object]] = []
    for source_id in chapter_ids:
        bundle = build_bundle(source_id)
        write_outputs(source_id, bundle, write_json=write_json)
        claims = len(bundle["claims"])  # type: ignore[arg-type]
        sections = len(bundle["sections"])  # type: ignore[arg-type]
        print(
            f"build_study_edition: ok {source_id} "
            f"({sections} sections, {claims} claims)"
        )
        bundles.append(bundle)
    return bundles


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build study-edition static pages.")
    parser.add_argument("--chapter", help="single source_id e.g. civ-07")
    parser.add_argument("--part", choices=sorted(PART_STUDY_CHAPTERS), help="batch Part chapters")
    parser.add_argument(
        "--from-chapter",
        help="first chapter id when batching (--part); default is first in Part",
    )
    parser.add_argument(
        "--all-parts",
        action="store_true",
        help="build all Part batches (01–10) plus site index/assets",
    )
    parser.add_argument("--no-json", action="store_true", help="skip site/_data JSON bundle")
    args = parser.parse_args(argv)

    if args.all_parts:
        exit_code = 0
        for part_key in sorted(PART_STUDY_CHAPTERS):
            chapter_ids = list(PART_STUDY_CHAPTERS[part_key])
            try:
                bundles = build_chapters(chapter_ids, write_json=not args.no_json)
                write_part_index(part_key, bundles)
                print(
                    f"build_study_edition: Part {part_key} index -> "
                    f"study/part-{part_key}/index.html ({len(bundles)} chapters)"
                )
            except (ValueError, FileNotFoundError) as exc:
                print(f"build_study_edition: {exc}", file=sys.stderr)
                exit_code = 1
        finalize_site()
        return exit_code

    if args.part:
        chapter_ids = list(PART_STUDY_CHAPTERS[args.part])
        if args.from_chapter:
            if args.from_chapter not in chapter_ids:
                print(f"build_study_edition: {args.from_chapter} not in Part {args.part}", file=sys.stderr)
                return 1
            chapter_ids = chapter_ids[chapter_ids.index(args.from_chapter) :]
        try:
            bundles = build_chapters(chapter_ids, write_json=not args.no_json)
            index_path = write_part_index(args.part, bundles)
        except (ValueError, FileNotFoundError) as exc:
            print(f"build_study_edition: {exc}", file=sys.stderr)
            return 1
        print(
            f"build_study_edition: Part {args.part} index -> "
            f"{index_path.relative_to(ROOT)} ({len(bundles)} chapters)"
        )
        finalize_site()
        return 0

    source_id = args.chapter or "civ-07"
    try:
        bundle = build_bundle(source_id)
        out = write_outputs(source_id, bundle, write_json=not args.no_json)
    except (ValueError, FileNotFoundError) as exc:
        print(f"build_study_edition: {exc}", file=sys.stderr)
        return 1
    claims = len(bundle["claims"])  # type: ignore[arg-type]
    sections = len(bundle["sections"])  # type: ignore[arg-type]
    print(
        f"build_study_edition: ok {source_id} "
        f"({sections} sections, {claims} claims) -> {out.relative_to(ROOT)}"
    )
    finalize_site()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
