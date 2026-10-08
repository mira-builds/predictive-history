#!/usr/bin/env python3
"""Shared helpers for lecture pass A (section rails) — interviews + lectures."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

import yaml

from interview_transcript_sections import (
    PART_I_MARKER,
    common_asr_cleanup,
    find_anchor_pos,
    insert_sections,
    normalize_for_anchor,
    update_fidelity_reviewed_at,
    update_sectioned_frontmatter,
    write_slug_retitle_transcript,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
LECTURES_ROOT = REPO_ROOT / "lectures"
MAPS_ROOT = REPO_ROOT / "data" / "lectures" / "section-maps"
CARDS_PATH = REPO_ROOT / "data" / "cards.jsonl"

SLUG_HEADING_RE = re.compile(r"^### ([a-z][a-z0-9-]*)\s*$", re.M)
ANY_SECTION_RE = re.compile(r"^### (.+)$", re.M)
PIN_CITE_RE = re.compile(
    r"`(?P<file>[a-z0-9-]+-transcript\.md)#(?P<fragment>[a-z0-9-]+)`"
)
GEO_TIMESTAMP_LINE_RE = re.compile(
    r"^-\s*(?P<title>.+?):\s*`[^`]+`",
    re.M,
)
GEO_TIMESTAMP_SKIP_RE = re.compile(r"not supplied", re.I)
PIVOT_TRIGGER_RE = re.compile(
    r"\b("
    r"today we look|today we will|today i'm going|going to share|"
    r"third and final|the year is \d{4}|"
    r"let's look at a map|let's review|let's begin|let's start|"
    r"question now is|the question then is|the question is|"
    r"moving on|next topic|in conclusion|to summarize|"
    r"all right so|okay so the|so um today|regime change|three pillars"
    r")\b",
    re.I,
)
PRE_RAILS_GIT_REF = "f108cb2^"


@dataclass
class TranscriptAuditRow:
    source_id: str
    series: str
    path: str
    rail_status: str
    section_count: int
    warn: str = ""


def slug_to_title(slug: str) -> str:
    """Mechanical kebab-slug → Title Case words (preserves GitHub #fragment)."""
    return " ".join(part.capitalize() for part in slug.split("-") if part)


def github_heading_anchor(heading: str) -> str:
    text = heading.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "-", text.strip())
    return text


def is_title_case_heading(heading: str) -> bool:
    heading = heading.strip()
    if SLUG_HEADING_RE.match(f"### {heading}"):
        return False
    if not heading:
        return False
    if heading[0].islower():
        return False
    return True


def split_part_i(doc: str) -> tuple[str, str]:
    if PART_I_MARKER not in doc:
        raise ValueError("missing Part I marker")
    head, body = doc.split(PART_I_MARKER, 1)
    return head, body.lstrip("\n")


def list_transcript_paths(series: str | None = None) -> list[Path]:
    root = LECTURES_ROOT / series if series else LECTURES_ROOT
    paths = sorted(root.rglob("*-transcript.md"))
    return [p for p in paths if p.is_file()]


def load_lecture_card_ids() -> set[str]:
    ids: set[str] = set()
    for line in CARDS_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        card = json.loads(line)
        path = card.get("source_paths", {}).get("source_chapter_path", "")
        if path.startswith("lectures/"):
            ids.add(card["source_id"])
    return ids


def classify_transcript(path: Path) -> TranscriptAuditRow:
    rel = path.relative_to(REPO_ROOT).as_posix()
    series = path.parts[path.parts.index("lectures") + 1]
    source_id = path.name.replace("-transcript.md", "")
    doc = path.read_text(encoding="utf-8")
    if PART_I_MARKER not in doc:
        return TranscriptAuditRow(source_id, series, rel, "missing_part_i", 0)

    _, body = split_part_i(doc)
    headings = ANY_SECTION_RE.findall(body)
    if not headings:
        return TranscriptAuditRow(source_id, series, rel, "flat", 0, "no sections")

    slug_count = len(SLUG_HEADING_RE.findall(body))
    title_count = sum(1 for h in headings if is_title_case_heading(h))
    if slug_count and slug_count == len(headings):
        status = "slug"
    elif title_count == len(headings):
        status = "title_case"
    else:
        status = "mixed"

    warn = ""
    if status == "title_case" and len(headings) == 1:
        warn = "single_rail"
    return TranscriptAuditRow(
        source_id, series, rel, status, len(headings), warn
    )


def audit_lectures(series: str | None = None) -> list[TranscriptAuditRow]:
    return [classify_transcript(p) for p in list_transcript_paths(series)]


def extract_slug_headings(body: str) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for match in SLUG_HEADING_RE.finditer(body):
        slug = match.group(1)
        pairs.append((slug, slug_to_title(slug)))
    return pairs


def retitle_slug_transcript(path: Path, *, dry_run: bool = False) -> int:
    doc = path.read_text(encoding="utf-8")
    _, body = split_part_i(doc)
    pairs = extract_slug_headings(body)
    if not pairs:
        print(f"skip {path.name}: no slug headings")
        return 0
    if dry_run:
        print(f"dry-run {path.name}: {len(pairs)} headings")
        return len(pairs)
    write_slug_retitle_transcript(path, pairs, asr_cleanup_fn=common_asr_cleanup)
    return len(pairs)


def parse_geo_timestamp_titles(doc: str) -> list[str]:
    block = doc.split("Source timestamps:", 1)
    if len(block) < 2:
        return []
    tail = block[1].split(PART_I_MARKER, 1)[0]
    titles: list[str] = []
    for match in GEO_TIMESTAMP_LINE_RE.finditer(tail):
        title = match.group("title").strip()
        if GEO_TIMESTAMP_SKIP_RE.search(title):
            continue
        if title.lower().startswith("opening"):
            titles.append("Opening")
        else:
            titles.append(title[0].upper() + title[1:] if title else title)
    return titles


def strip_section_headings(body: str) -> str:
    lines = [line for line in body.splitlines() if not line.startswith("### ")]
    text = "\n".join(lines)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def load_flat_transcript_body(path: Path, *, git_ref: str | None = PRE_RAILS_GIT_REF) -> str:
    """Return Part I body without section headings — prefer pre-rails git snapshot."""
    rel = path.relative_to(REPO_ROOT).as_posix()
    if git_ref:
        import subprocess

        proc = subprocess.run(
            ["git", "show", f"{git_ref}:{rel}"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        if proc.returncode == 0 and PART_I_MARKER in proc.stdout:
            _, body = split_part_i(proc.stdout)
            flat = strip_section_headings(body)
            if flat:
                return flat
    doc = path.read_text(encoding="utf-8")
    _, body = split_part_i(doc)
    return strip_section_headings(body)


def title_from_anchor_snippet(snippet: str) -> str:
    words = re.findall(r"[a-zA-Z']+", snippet.lower())
    stop = {
        "okay", "yeah", "well", "right", "lets", "look", "today", "start",
        "class", "review", "where", "are", "with", "that", "this", "have",
        "from", "your", "know", "will", "just", "very", "also", "then",
    }
    picked = [w for w in words if w not in stop and len(w) > 2][:6]
    if not picked:
        picked = words[:5]
    return " ".join(w.capitalize() for w in picked) or "Core Analysis"


def find_pivot_anchors(flat: str, count: int) -> list[str]:
    hits: list[tuple[int, str]] = [(0, flat.strip()[:55])]
    for match in PIVOT_TRIGGER_RE.finditer(flat):
        pos = match.start()
        if pos < 80:
            continue
        snippet = flat[pos : pos + 70].replace("\n", " ").strip()
        if any(abs(pos - h[0]) < 350 for h in hits[1:]):
            continue
        hits.append((pos, snippet))
    hits.sort(key=lambda x: x[0])

    if len(hits) < count:
        paragraphs = [p.strip() for p in re.split(r"\n\n+", flat) if p.strip()]
        if len(paragraphs) >= count:
            for i in range(1, count):
                idx = min(len(paragraphs) - 1, (i * len(paragraphs)) // count)
                snippet = paragraphs[idx][:70].replace("\n", " ").strip()
                pos = flat.find(paragraphs[idx][:30])
                if pos == -1:
                    pos = i * 1000
                if not any(abs(pos - h[0]) < 350 for h in hits):
                    hits.append((pos, snippet))
            hits.sort(key=lambda x: x[0])

    if len(hits) <= count:
        return [h[1] for h in hits]
    interior = hits[1:]
    step = max(1, len(interior) // max(1, count - 1))
    chosen = [hits[0][1]] + [interior[i][1] for i in range(0, len(interior), step)]
    return chosen[:count]


def fill_section_anchors(sections: list[dict], flat: str) -> list[dict]:
    titles = [s["title"] for s in sections]
    if sections[0].get("split") == "paragraph":
        return sections
    try:
        boundaries = build_anchors_for_titles(titles, flat)
    except ValueError:
        boundaries = []
    filled: list[dict] = []
    for i, section in enumerate(sections):
        entry: dict = {"title": section["title"]}
        if i == 0:
            filled.append(entry)
            continue
        anchor = section.get("anchor")
        if anchor and not section.get("anchor_missing"):
            try:
                find_anchor_pos(flat, str(anchor)[:40], 0)
                entry["anchor"] = str(anchor).strip()
            except ValueError:
                anchor = None
        if not anchor and i - 1 < len(boundaries):
            entry["anchor"] = boundaries[i - 1]
        elif not anchor:
            entry["anchor_missing"] = True
        filled.append(entry)
    return filled


def draft_pivot_geo_map(path: Path, flat: str, *, target_sections: int = 6) -> list[dict]:
    titles_from_ts = parse_geo_timestamp_titles(path.read_text(encoding="utf-8"))
    if not titles_from_ts:
        titles_from_ts = parse_geo_timestamp_titles(
            subprocess_get_git_doc(path) or path.read_text(encoding="utf-8")
        )
    if titles_from_ts:
        sections = [{"title": t} for t in titles_from_ts]
        return fill_section_anchors(sections, flat)

    anchors = find_pivot_anchors(flat, max(4, target_sections - 1))
    sections: list[dict] = [{"title": "Opening"}]
    for anchor in anchors[1:]:
        if len(sections) >= target_sections - 1:
            break
        sections.append({"title": title_from_anchor_snippet(anchor), "anchor": anchor[:80]})
    if len(sections) < 4:
        paragraphs = [p.strip() for p in re.split(r"\n\n+", flat) if p.strip()]
        needed = 4 - len(sections)
        for i in range(1, needed + 1):
            idx = min(len(paragraphs) - 1, (i * len(paragraphs)) // (needed + 1))
            anchor = paragraphs[idx][:70].replace("\n", " ").strip()
            sections.append({"title": title_from_anchor_snippet(anchor), "anchor": anchor[:80]})
    sections.append({"title": "Closing Questions"})
    return sections


def subprocess_get_git_doc(path: Path) -> str | None:
    import subprocess

    rel = path.relative_to(REPO_ROOT).as_posix()
    proc = subprocess.run(
        ["git", "show", f"{PRE_RAILS_GIT_REF}:{rel}"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    return proc.stdout if proc.returncode == 0 else None


def anchor_from_title(title: str, body: str, start: int = 0) -> str | None:
    """Find a short anchor phrase from title keywords in body."""
    words = [
        w
        for w in re.findall(r"[a-zA-Z']+", title.lower())
        if len(w) > 3 and w not in {"opening", "closing", "questions", "with", "from", "and", "the"}
    ]
    if not words:
        return None
    hay = normalize_for_anchor(body)
    for n in (4, 3, 2):
        if len(words) < n:
            continue
        phrase = " ".join(words[:n])
        pos = hay.find(phrase, start)
        if pos != -1:
            return body[pos : pos + min(60, len(body) - pos)].split("\n")[0][:60]
    return None


def insert_sections_paragraph_split(body: str, titles: list[str]) -> str:
    paragraphs = [p.strip() for p in re.split(r"\n\n+", body.strip()) if p.strip()]
    n = len(titles)
    if not paragraphs:
        raise ValueError("empty body")
    if n == 1:
        return f"### {titles[0]}\n\n{body.strip()}"

    parts: list[str] = []
    total = len(paragraphs)
    for i, title in enumerate(titles):
        start_idx = (i * total) // n
        end_idx = ((i + 1) * total) // n if i < n - 1 else total
        chunk = "\n\n".join(paragraphs[start_idx:end_idx]).strip()
        parts.append(f"### {title}\n\n{chunk}")
    return "\n\n".join(parts)


def build_anchors_for_titles(titles: list[str], body: str) -> list[str]:
    """Return N−1 boundary anchors at the start of sections 1..N−1."""
    boundaries: list[str] = []
    cursor = 0
    for title in titles[1:]:
        anchor = anchor_from_title(title, body, cursor)
        if not anchor and title.lower().startswith("closing"):
            hay = normalize_for_anchor(body)
            for cue in ("any questions", "questions", "thank you", "that's all"):
                pos = hay.find(cue, cursor)
                if pos != -1:
                    anchor = body[pos : pos + 60].split("\n")[0][:60]
                    break
        if not anchor:
            raise ValueError(f"could not derive boundary for section: {title!r}")
        pos = find_anchor_pos(body, anchor[:40], cursor)
        boundaries.append(anchor[:80].strip())
        cursor = pos + 1
    return boundaries


def section_boundary_anchors(sections: list[dict], flat: str) -> list[str]:
    """Map YAML section starts (sections[1:]) to insert_sections boundary anchors."""
    titles = [s["title"] for s in sections]
    need = len(titles) - 1
    boundaries: list[str] = []
    cursor = 0
    for i in range(1, len(sections)):
        sec = sections[i]
        is_closing = sec["title"].lower().startswith("closing")
        anchor = sec.get("anchor")
        if anchor and not sec.get("anchor_missing"):
            snippet = str(anchor).strip()
            try:
                pos = find_anchor_pos(flat, snippet[:40], cursor)
                boundaries.append(snippet[:80])
                cursor = pos + 1
                continue
            except ValueError:
                pass
        if is_closing and i == len(sections) - 1:
            hay = normalize_for_anchor(flat)
            for cue in ("any questions", "questions", "thank you", "that's all"):
                pos = hay.find(cue, cursor)
                if pos != -1:
                    derived = flat[pos : pos + 60].split("\n")[0][:60]
                    pos2 = find_anchor_pos(flat, derived[:40], cursor)
                    boundaries.append(derived[:80].strip())
                    cursor = pos2 + 1
                    break
            else:
                paragraphs = [p.strip() for p in re.split(r"\n\n+", flat) if p.strip()]
                eligible = [
                    p
                    for p in paragraphs
                    if flat.find(p[: min(30, len(p))], cursor) >= cursor
                ]
                if eligible:
                    idx = max(0, (len(eligible) * 3) // 4)
                    derived = eligible[idx][:70].replace("\n", " ").strip()
                    pos2 = find_anchor_pos(flat, derived[:40], cursor)
                    boundaries.append(derived[:80].strip())
                    cursor = pos2 + 1
                else:
                    raise ValueError(f"no boundary anchor for closing section in {sec['title']!r}")
            continue
        derived = anchor_from_title(sec["title"], flat, cursor)
        if not derived:
            raise ValueError(f"no boundary anchor for section {i}: {sec['title']!r}")
        pos = find_anchor_pos(flat, derived[:40], cursor)
        boundaries.append(derived[:80].strip())
        cursor = pos + 1
    if len(boundaries) != need:
        raise ValueError(
            f"expected {need} boundary anchors for {len(titles)} sections, got {len(boundaries)}"
        )
    return boundaries


def apply_section_map(
    path: Path,
    sections: list[dict],
    *,
    dry_run: bool = False,
    flat_body: str | None = None,
) -> None:
    doc = path.read_text(encoding="utf-8")
    head, body = split_part_i(doc)
    titles = [s["title"] for s in sections]
    flat = flat_body if flat_body is not None else strip_section_headings(body)

    if sections[0].get("split") == "paragraph":
        new_body = insert_sections_paragraph_split(flat, titles)
    else:
        try:
            anchors = section_boundary_anchors(sections, flat)
            new_body = insert_sections(
                flat, titles, anchors, asr_cleanup_fn=common_asr_cleanup
            )
        except ValueError:
            try:
                anchors = build_anchors_for_titles(titles, flat)
                new_body = insert_sections(
                    flat, titles, anchors, asr_cleanup_fn=common_asr_cleanup
                )
            except ValueError:
                new_body = insert_sections_paragraph_split(flat, titles)

    if dry_run:
        print(f"dry-run apply {path.name}: {len(titles)} sections")
        return

    head = update_sectioned_frontmatter(head)
    out = f"{head}{PART_I_MARKER}\n\n{new_body}\n"
    path.write_text(out, encoding="utf-8", newline="\n")
    print(f"wrote {path} ({len(titles)} sections)")


def load_section_map(source_id: str) -> list[dict]:
    map_path = MAPS_ROOT / f"{source_id}.yaml"
    if not map_path.exists():
        raise FileNotFoundError(map_path)
    data = yaml.safe_load(map_path.read_text(encoding="utf-8"))
    return data["sections"]


def save_section_map(source_id: str, sections: list[dict]) -> Path:
    MAPS_ROOT.mkdir(parents=True, exist_ok=True)
    path = MAPS_ROOT / f"{source_id}.yaml"
    payload = {"source_id": source_id, "sections": sections}
    path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return path


def load_card(source_id: str) -> dict | None:
    for line in CARDS_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        card = json.loads(line)
        if card.get("source_id") == source_id:
            return card
    return None


def seed_titles_from_card(card: dict) -> list[str]:
    """Derive section title stubs from card pressure points / placement text."""
    sections = card.get("sections") or {}
    titles: list[str] = []
    for key in ("Historical Pressure Points", "Where This Sits"):
        block = sections.get(key, "")
        for line in block.splitlines():
            line = line.strip().lstrip("-").strip()
            if not line or len(line) < 12:
                continue
            # First clause or ~6 words as a rail title stub
            clause = line.split(".")[0].split(":")[0].strip()
            words = clause.split()
            title = " ".join(words[:8]).strip(" ,;")
            if title and title not in titles:
                titles.append(title[0].upper() + title[1:] if title else title)
    if not titles:
        titles = ["Opening", "Core Lecture", "Examples", "Closing"]
    else:
        titles = ["Opening", *titles[:6], "Closing"]
    return titles


def draft_section_map(path: Path, *, template: str | None = None) -> list[dict]:
    """Seed insert-tier YAML from timestamps, card, or series template."""
    source_id = path.name.replace("-transcript.md", "")
    try:
        return draft_geo_map(path)
    except ValueError:
        pass

    if template:
        tpl_path = MAPS_ROOT / "_templates" / f"{template}.yaml"
        if tpl_path.exists():
            return yaml.safe_load(tpl_path.read_text(encoding="utf-8"))["sections"]

    card = load_card(source_id)
    if card:
        titles = seed_titles_from_card(card)
    else:
        titles = ["Opening", "Core Lecture", "Examples", "Closing"]

    return [{"title": t, "split": "paragraph"} for t in titles]


def draft_geo_map(path: Path) -> list[dict]:
    doc = path.read_text(encoding="utf-8")
    titles = parse_geo_timestamp_titles(doc)
    if not titles:
        git_doc = subprocess_get_git_doc(path)
        if git_doc:
            titles = parse_geo_timestamp_titles(git_doc)
    if not titles:
        raise ValueError(f"{path.name}: no usable Source timestamps block")
    flat = load_flat_transcript_body(path)
    sections = [{"title": t} for t in titles]
    return fill_section_anchors(sections, flat)


def transcript_heading_fragments(path: Path) -> set[str]:
    doc = path.read_text(encoding="utf-8")
    if PART_I_MARKER not in doc:
        return set()
    _, body = split_part_i(doc)
    frags: set[str] = set()
    for heading in ANY_SECTION_RE.findall(body):
        frags.add(github_heading_anchor(heading))
    return frags


def verify_pin_cites_for_packet(source_id: str) -> list[str]:
    errors: list[str] = []
    paths = list_transcript_paths()
    transcript_path = next(
        (p for p in paths if p.name == f"{source_id}-transcript.md"), None
    )
    if not transcript_path:
        return [f"{source_id}: transcript not found"]
    commentary_path = transcript_path.with_name(
        transcript_path.name.replace("-transcript.md", "-commentary.md")
    )
    if not commentary_path.exists():
        return []
    fragments = transcript_heading_fragments(transcript_path)
    for match in PIN_CITE_RE.finditer(commentary_path.read_text(encoding="utf-8")):
        frag = match.group("fragment")
        if frag not in fragments:
            errors.append(
                f"{source_id}: pin-cite #{frag} not in transcript headings {sorted(fragments)}"
            )
    return errors
