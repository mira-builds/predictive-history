#!/usr/bin/env python3
"""Shared helpers for PH-TRANSCRIPT-EDIT section patch scripts (interviews + lectures)."""
from __future__ import annotations

import re
from collections.abc import Callable, Sequence
from datetime import date
from pathlib import Path

PART_I_MARKER = "## Part I: Full transcript\n"
REPO_ROOT = Path(__file__).resolve().parents[1]
UNICODE_APOSTROPHE = r"['\u2019]"


def normalize_for_anchor(text: str) -> str:
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2014", "-").replace("\u2013", "-")
    return text.lower()


def find_anchor_pos(flat: str, anchor: str, start: int) -> int:
    hay = normalize_for_anchor(flat)
    needle = normalize_for_anchor(anchor)
    pos = hay.find(needle, start)
    if pos == -1:
        raise ValueError(f"anchor not found: {anchor!r} (from pos {start})")
    return pos


def insert_sections(
    body: str,
    section_titles: Sequence[str],
    section_anchors: Sequence[str],
    *,
    asr_cleanup_fn: Callable[[str], str] | None = None,
    anchor_slice: slice | None = None,
) -> str:
    """Split flat transcript body into Title Case `###` sections.

    Uses N−1 anchors for N sections. Final section runs to EOF. Optional
    ``anchor_slice`` (e.g. ``slice(1, None)`` for DOAC) selects which anchors
    delimit internal section boundaries after the opening section.
    """
    if len(section_titles) != len(section_anchors) + 1 and anchor_slice is None:
        raise ValueError(
            f"expected {len(section_titles) - 1} anchors for "
            f"{len(section_titles)} sections, got {len(section_anchors)}"
        )

    flat = asr_cleanup_fn(body) if asr_cleanup_fn else body
    anchors = (
        section_anchors[anchor_slice]
        if anchor_slice is not None
        else section_anchors
    )
    if len(section_titles) != len(anchors) + 1:
        raise ValueError(
            f"after anchor_slice, expected {len(section_titles) - 1} anchors, "
            f"got {len(anchors)}"
        )

    positions = [0]
    cursor = 0
    for anchor in anchors:
        pos = find_anchor_pos(flat, anchor, cursor)
        positions.append(pos)
        cursor = pos + len(normalize_for_anchor(anchor))
    positions.append(len(flat))

    parts: list[str] = []
    for i, heading in enumerate(section_titles):
        end = len(flat) if i == len(section_titles) - 1 else positions[i + 1]
        chunk = flat[positions[i] : end].strip()
        parts.append(f"### {heading}\n\n{chunk}")
    return "\n\n".join(parts)


def common_asr_cleanup(
    text: str,
    *,
    replacements: dict[str, str] | None = None,
) -> str:
    text = text.replace("Professor Dieng.", "Professor Jiang.")
    text = text.replace("Professor Dieng,", "Professor Jiang,")
    text = text.replace("Professor Dieng", "Professor Jiang")
    for old, new in (replacements or {}).items():
        text = text.replace(old, new)
    text = re.sub(r"\bThe The\b", "The", text)
    text = re.sub(r"\bIt It\b", "It", text)
    text = re.sub(r"\bTrump Trump\b", "Trump", text)
    text = re.sub(r"\bdemystify all of all of\b", "demystify all of", text)
    text = re.sub(r"\bMiddle Middle East\b", "Middle East", text)
    text = re.sub(r"\bof of\b", "of", text)
    text = re.sub(r"\bthe the\b", "the", text, flags=re.I)
    text = re.sub(r"\bhave has\b", "have", text, flags=re.I)
    return text


def strip_speakers_before_section_headings(body: str, speaker_pattern: str) -> str:
    return re.sub(
        rf"\n\n\*\*(?:{speaker_pattern}):\*\*\n\n(### )",
        r"\n\n\1",
        body,
    )


def prepend_speaker_at_section_opens(
    body: str,
    fixes: Sequence[tuple[str, str, str]],
) -> str:
    """Each fix: (section title without ###, speaker label, opener regex)."""
    for section, speaker, opener in fixes:
        pattern = (
            rf"(### {re.escape(section)}\n\n)"
            rf"(?!\*\*{re.escape(speaker)}:\*\*)"
            rf"({opener})"
        )
        body = re.sub(pattern, rf"\1**{speaker}:** \2", body, count=1)
    return body


def apply_slug_to_title_headings(
    body: str,
    slug_headings: Sequence[tuple[str, str]],
) -> str:
    out = body
    for slug, heading in slug_headings:
        old = f"### {slug}"
        new = f"### {heading}"
        if old not in out and new in out:
            continue
        if old not in out:
            raise ValueError(f"missing section slug: {slug}")
        out = out.replace(old, new, 1)
    return out


def update_sectioned_frontmatter(
    head: str,
    *,
    curation: str = "curated_sectioned",
    source_reviewed_at: str = "2026-06-25",
) -> str:
    today = date.today().isoformat()
    if re.search(r"^transcript_curation:", head, flags=re.M):
        head = re.sub(
            r"^transcript_curation:.*$",
            f"transcript_curation: {curation}",
            head,
            count=1,
            flags=re.M,
        )
    elif "transcript_fidelity: exact_body_match\n" in head:
        head = head.replace(
            "transcript_fidelity: exact_body_match\n",
            f"transcript_fidelity: exact_body_match\ntranscript_curation: {curation}\n",
            1,
        )
    if re.search(r"^fidelity_reviewed_at:", head, flags=re.M):
        head = re.sub(
            r"^fidelity_reviewed_at:.*$",
            f"fidelity_reviewed_at: {today}",
            head,
            count=1,
            flags=re.M,
        )
    else:
        head = head.replace(
            f"source_reviewed_at: {source_reviewed_at}\n",
            f"source_reviewed_at: {source_reviewed_at}\nfidelity_reviewed_at: {today}\n",
            1,
        )
    return head


def update_fidelity_reviewed_at(head: str) -> str:
    today = date.today().isoformat()
    if re.search(r"^fidelity_reviewed_at:", head, flags=re.M):
        return re.sub(
            r"^fidelity_reviewed_at:.*$",
            f"fidelity_reviewed_at: {today}",
            head,
            count=1,
            flags=re.M,
        )
    return head


def write_sectioned_transcript(
    transcript_path: Path,
    section_titles: Sequence[str],
    section_anchors: Sequence[str],
    *,
    asr_cleanup_fn: Callable[[str], str] | None = None,
    speaker_cleanup_fn: Callable[[str], str] | None = None,
    anchor_slice: slice | None = None,
    reject_if_sectioned: bool = True,
) -> None:
    doc = transcript_path.read_text(encoding="utf-8")
    if PART_I_MARKER not in doc:
        raise ValueError("missing Part I marker")

    head, body = doc.split(PART_I_MARKER, 1)
    if reject_if_sectioned and body.lstrip().startswith("### "):
        raise ValueError("transcript already sectioned")

    head = update_sectioned_frontmatter(head)
    body = insert_sections(
        body.strip(),
        section_titles,
        section_anchors,
        asr_cleanup_fn=asr_cleanup_fn,
        anchor_slice=anchor_slice,
    )
    if speaker_cleanup_fn:
        body = speaker_cleanup_fn(body)

    doc = f"{head}{PART_I_MARKER}\n\n{body}\n"
    transcript_path.write_text(doc, encoding="utf-8", newline="\n")
    print(
        f"wrote {transcript_path} "
        f"({len(body.split()):,} words, {len(section_titles)} sections)"
    )


def write_slug_retitle_transcript(
    transcript_path: Path,
    slug_headings: Sequence[tuple[str, str]],
    *,
    asr_cleanup_fn: Callable[[str], str] | None = None,
) -> None:
    doc = transcript_path.read_text(encoding="utf-8")
    if PART_I_MARKER not in doc:
        raise ValueError("missing Part I marker")

    head, body = doc.split(PART_I_MARKER, 1)
    if asr_cleanup_fn:
        body = asr_cleanup_fn(body)
    body = apply_slug_to_title_headings(body, slug_headings)
    head = update_fidelity_reviewed_at(head)
    doc = head + PART_I_MARKER + body
    transcript_path.write_text(doc, encoding="utf-8", newline="\n")
    print(
        f"wrote {transcript_path} "
        f"({len(body.split()):,} words, {len(slug_headings)} sections)"
    )
