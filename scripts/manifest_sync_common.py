#!/usr/bin/env python3
"""Shared helpers for syncing sweep SSOT into volume-i-anchors.yaml."""

from __future__ import annotations

import re
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "pin-cite" / "volume-i-anchors.yaml"
VOL2 = ROOT / "book" / "volume-ii"

from part_i_pin_cite_prep import (  # noqa: E402
    CLAIM_REFS as PART_I_CLAIMS,
    TRANSCRIPT_SECTIONS as PART_I_SECTIONS,
)
from part_ii_tier_b_uplift import (  # noqa: E402
    CHAPTER_CLAIM_REFS as TIER_B_CLAIMS,
    TRANSCRIPT_SECTIONS as TIER_B_SECTIONS,
)
from part_ii_iii_pin_cite_sweep import (  # noqa: E402
    CHAPTER_CLAIM_REFS as SWEEP_CLAIMS,
    TRANSCRIPT_SECTIONS as SWEEP_SECTIONS,
)
from part_iv_pin_cite_prep import (  # noqa: E402
    CHAPTER_CLAIM_REFS as PART_IV_CLAIMS,
    TRANSCRIPT_SECTIONS as PART_IV_SECTIONS,
)
from part_v_pin_cite_prep import (  # noqa: E402
    CLAIM_REFS as PART_V_CLAIMS,
    TRANSCRIPT_SECTIONS as PART_V_SECTIONS,
)
from part_vi_pin_cite_prep import (  # noqa: E402
    CLAIM_REFS as PART_VI_CLAIMS,
    TRANSCRIPT_SECTIONS as PART_VI_SECTIONS,
)
from part_vii_pin_cite_prep import (  # noqa: E402
    CLAIM_REFS as PART_VII_CLAIMS,
    TRANSCRIPT_SECTIONS as PART_VII_SECTIONS,
)

PART_I_CHAPTERS = [f"civ-{n:02d}" for n in range(1, 7)]
PART_II_CHAPTERS = [f"civ-{n:02d}" for n in range(7, 14)]
PART_III_CHAPTERS = [f"civ-{n:02d}" for n in range(14, 18)]
PART_IV_CHAPTERS = [f"civ-{n:02d}" for n in range(18, 24)]
PART_V_CHAPTERS = [f"civ-{n:02d}" for n in range(24, 29)]
PART_VI_CHAPTERS = [f"civ-{n:02d}" for n in range(29, 35)]
PART_VII_CHAPTERS = [f"civ-{n:02d}" for n in range(35, 42)]
PART_VIII_CHAPTERS = [f"civ-{n:02d}" for n in range(42, 51)]
PART_IX_CHAPTERS = [f"civ-{n:02d}" for n in range(51, 54)]
PART_X_CHAPTERS = [f"civ-{n:02d}" for n in range(54, 61)]

PART_SPECS: dict[str, dict[str, object]] = {
    "01": {
        "part_id": "part-01-dawn-of-civilization",
        "chapters": PART_I_CHAPTERS,
    },
    "02": {
        "part_id": "part-02-hellenic-world",
        "chapters": PART_II_CHAPTERS,
    },
    "03": {
        "part_id": "part-03-roman-imperium",
        "chapters": PART_III_CHAPTERS,
    },
    "04": {
        "part_id": "part-04-ancient-foundations",
        "chapters": PART_IV_CHAPTERS,
    },
    "05": {
        "part_id": "part-05-christianity-and-islam",
        "chapters": PART_V_CHAPTERS,
    },
    "06": {
        "part_id": "part-06-medieval-imagination",
        "chapters": PART_VI_CHAPTERS,
    },
    "07": {
        "part_id": "part-07-world-after-rome",
        "chapters": PART_VII_CHAPTERS,
    },
    "08": {
        "part_id": "part-08-birth-of-modernity",
        "chapters": PART_VIII_CHAPTERS,
    },
    "09": {
        "part_id": "part-09-age-of-conscience",
        "chapters": PART_IX_CHAPTERS,
    },
    "10": {
        "part_id": "part-10-rise-of-the-nation-state",
        "chapters": PART_X_CHAPTERS,
    },
}

L2_REF_RE = re.compile(
    r"^\|\s*\d+\s*\|[^\n]+\|\s*`[^`]*#([a-z0-9-]+)`",
    re.MULTILINE,
)


def load_manifest_chapters() -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    data = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    return data.get("chapters", {})


def sections_for(chapter_id: str) -> list[dict[str, str]]:
    pairs = (
        PART_I_SECTIONS.get(chapter_id)
        or TIER_B_SECTIONS.get(chapter_id)
        or SWEEP_SECTIONS.get(chapter_id)
        or PART_IV_SECTIONS.get(chapter_id)
        or PART_V_SECTIONS.get(chapter_id)
        or PART_VI_SECTIONS.get(chapter_id)
        or PART_VII_SECTIONS.get(chapter_id)
    )
    if not pairs:
        raise KeyError(f"no TRANSCRIPT_SECTIONS for {chapter_id}")
    return [{"slug": slug, "phrase": phrase} for slug, phrase in pairs]


def claim_refs_from_commentary(chapter_id: str) -> list[str]:
    path = VOL2 / chapter_id / f"{chapter_id}-commentary.md"
    text = path.read_text(encoding="utf-8")
    start = text.find("### Major Claims")
    if start < 0:
        raise ValueError(f"no Major Claims in {path}")
    block = text[start:]
    end = block.find("### Core Concepts")
    if end >= 0:
        block = block[:end]
    refs = [f"#{m.group(1)}" for m in L2_REF_RE.finditer(block)]
    if refs:
        return refs
    fallback = (
        PART_I_CLAIMS.get(chapter_id)
        or TIER_B_CLAIMS.get(chapter_id)
        or SWEEP_CLAIMS.get(chapter_id)
        or PART_IV_CLAIMS.get(chapter_id)
        or PART_V_CLAIMS.get(chapter_id)
        or PART_VI_CLAIMS.get(chapter_id)
        or PART_VII_CLAIMS.get(chapter_id)
    )
    if fallback:
        return fallback
    raise ValueError(f"no claim refs for {chapter_id}")


def build_entry(
    chapter_id: str,
    part_id: str,
    *,
    sections: list[dict[str, str]] | None = None,
) -> dict:
    sect = sections if sections is not None else sections_for(chapter_id)
    claim_refs = claim_refs_from_commentary(chapter_id)
    slugs = {row["slug"] for row in sect}
    for ref in claim_refs:
        slug = ref.lstrip("#")
        if slug not in slugs:
            raise ValueError(f"{chapter_id}: claim ref {ref} not in section slugs")
    return {
        "part_id": part_id,
        "sections": sect,
        "claim_refs": claim_refs,
    }


def ordered_chapters(chapters: dict) -> dict:
    """civ-01..06, Part II–X in lecture order."""
    ordered_keys: list[str] = []
    for cid in PART_I_CHAPTERS:
        if cid in chapters:
            ordered_keys.append(cid)
    for cid in PART_II_CHAPTERS:
        if cid in chapters:
            ordered_keys.append(cid)
    for cid in PART_III_CHAPTERS:
        if cid in chapters:
            ordered_keys.append(cid)
    for cid in PART_IV_CHAPTERS:
        if cid in chapters:
            ordered_keys.append(cid)
    for cid in PART_V_CHAPTERS:
        if cid in chapters:
            ordered_keys.append(cid)
    for cid in PART_VI_CHAPTERS:
        if cid in chapters:
            ordered_keys.append(cid)
    for cid in PART_VII_CHAPTERS:
        if cid in chapters:
            ordered_keys.append(cid)
    for cid in PART_VIII_CHAPTERS:
        if cid in chapters:
            ordered_keys.append(cid)
    for cid in PART_IX_CHAPTERS:
        if cid in chapters:
            ordered_keys.append(cid)
    for cid in PART_X_CHAPTERS:
        if cid in chapters:
            ordered_keys.append(cid)
    for cid in sorted(chapters):
        if cid not in ordered_keys:
            ordered_keys.append(cid)
    return {k: chapters[k] for k in ordered_keys}
