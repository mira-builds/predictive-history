#!/usr/bin/env python3
"""Insert transcript ### section anchors for Part VI (civ-29..34) and refresh L2 refs."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOL2 = ROOT / "book" / "volume-ii"
READINESS = ROOT / "docs/routes/volume-i-parts/PART-06-HYBRID-READINESS.md"

# (slug, unique substring to split BEFORE — first match wins in lecture order)
TRANSCRIPT_SECTIONS: dict[str, list[tuple[str, str]]] = {
    "civ-29": [
        (
            "opening-dante-peak",
            "today we do Dante and Dante really is the height of civilization",
        ),
        ("tuscan-vernacular-epic", "he chooses to write it in tusin"),
        (
            "mary-center-theology",
            "in Dante's rendering of Christian theology Mary is at the",
        ),
        ("paradox-structure-jigsaw", "the first is the idea of paradox"),
        (
            "three-revolutions-seeds",
            "seeds of these three major revolutions",
        ),
        ("apocalyptic-overturn", "completely overturn this tradition"),
        ("augustine-review-frame", "let's review Augustine"),
        ("augustine-rebuttal", "Dante is trying to rebut Augustine"),
        ("god-imagination", "you have to imagine God"),
    ],
    "civ-30": [
        (
            "first-semester-close",
            "we finished Dante today and this will be our last session",
        ),
        ("poetry-memorized", "poetry is meant to be memorized"),
        ("supplant-virgil", "his mission is to supplant Virgil"),
        ("unreliable-narrator", "turns him into an unreliable guide"),
        ("dido-virgil-limits", "Virgil refuses to name ditto"),
        ("kato-statius-merit", "Kato is in purgatory"),
        ("virgil-disappears-refusal", "Virgil has run away at this climax"),
        (
            "beatrice-love-trust",
            "love is not about possession it's about trust",
        ),
        ("protestant-scientific-access", "direct access to God"),
    ],
    "civ-31": [
        ("second-semester-frame", "first class of the second semester"),
        ("cycle-and-line-models", "there's a cycle and then there's a line"),
        ("oceanic-curve-model", "call the oceanic curve of"),
        ("no-moral-judgment", "proposing is there's no moral"),
        ("borderlands-pattern", "called the Borderlands okay"),
        (
            "boundary-collapse-pressures",
            "boundary conditions of all",
        ),
        ("conflict-zone-hurricanes", "this war in Ukraine it is a"),
    ],
    "civ-32": [
        ("rome-america-parallels", "Rome and United States it's very"),
        ("cultural-military-triumph", "cultural system that allowed it to"),
        ("roman-citizenship-value", "who gets to be a citizen who doesn't"),
        ("republic-empire-tension", "America cannot both be a"),
        ("caracalla-rupture", "of Caracalla which made"),
        ("america-war-civil-violence", "America will start a Civil War as"),
    ],
    "civ-33": [
        ("byzantine-roman-continuation", "seen the Byzantine Empire as a"),
        ("scholarly-consensus-first", "I want to present the scholarly"),
        ("nicaea-trinity", "Nicaea Nakia established the idea of the"),
        ("theodosian-walls", "the Theodosian walls which makes Conant"),
        ("pagan-christian-contrast", "individual soul is what"),
        ("bureaucracy-stagnation", "stagnation okay there's nothing new"),
    ],
    "civ-34": [
        (
            "holy-roman-western-continuation",
            "Holy Roman Empire in the west we think",
        ),
        ("charlemagne-crowned", "Charlemagne was crowned Holy Roman"),
        ("catholic-church-coopt", "in trying to co-op new people"),
        ("rome-constantinople-schism", "Rome and Conant pople"),
        (
            "augustine-city-of-god-blueprint",
            "he basically made city of God the",
        ),
        ("useful-fiction-close", "Roman Empire was a useful fiction for"),
    ],
}

CLAIM_REFS: dict[str, list[str]] = {
    "civ-29": [
        "#opening-dante-peak",
        "#tuscan-vernacular-epic",
        "#apocalyptic-overturn",
        "#augustine-rebuttal",
        "#mary-center-theology",
        "#paradox-structure-jigsaw",
        "#god-imagination",
        "#three-revolutions-seeds",
    ],
    "civ-30": [
        "#first-semester-close",
        "#poetry-memorized",
        "#supplant-virgil",
        "#unreliable-narrator",
        "#dido-virgil-limits",
        "#beatrice-love-trust",
        "#virgil-disappears-refusal",
        "#protestant-scientific-access",
    ],
    "civ-31": [
        "#second-semester-frame",
        "#cycle-and-line-models",
        "#no-moral-judgment",
        "#boundary-collapse-pressures",
        "#borderlands-pattern",
        "#conflict-zone-hurricanes",
    ],
    "civ-32": [
        "#rome-america-parallels",
        "#cultural-military-triumph",
        "#roman-citizenship-value",
        "#republic-empire-tension",
        "#caracalla-rupture",
        "#america-war-civil-violence",
    ],
    "civ-33": [
        "#byzantine-roman-continuation",
        "#scholarly-consensus-first",
        "#theodosian-walls",
        "#nicaea-trinity",
        "#pagan-christian-contrast",
        "#bureaucracy-stagnation",
    ],
    "civ-34": [
        "#holy-roman-western-continuation",
        "#charlemagne-crowned",
        "#catholic-church-coopt",
        "#rome-constantinople-schism",
        "#augustine-city-of-god-blueprint",
        "#useful-fiction-close",
    ],
}


def split_transcript_body(body: str, sections: list[tuple[str, str]]) -> str:
    """Insert ### anchors before each anchor phrase (case-insensitive)."""
    lower = body.lower()
    markers: list[tuple[int, str]] = []
    search_from = 0
    for slug, phrase in sections:
        idx = lower.find(phrase.lower(), search_from)
        if idx < 0:
            raise ValueError(f"Anchor not found: {slug!r} -> {phrase[:60]!r}...")
        markers.append((idx, slug))
        search_from = idx + 1
    markers.sort(key=lambda x: x[0])
    out: list[str] = []
    pos = 0
    for idx, slug in markers:
        if idx > pos:
            chunk = body[pos:idx].rstrip()
            if chunk:
                out.append(chunk)
        out.append(f"\n\n### {slug}\n\n")
        pos = idx
    out.append(body[pos:])
    return "".join(out).strip() + "\n"


def patch_transcript(chapter_id: str) -> None:
    path = VOL2 / chapter_id / f"{chapter_id}-transcript.md"
    text = path.read_text(encoding="utf-8")
    first_slug = TRANSCRIPT_SECTIONS[chapter_id][0][0]
    if f"### {first_slug}" in text:
        print(f"skip transcript (already sectioned): {path.relative_to(ROOT)}")
        return
    marker = "## Part I: Full transcript\n\n"
    if marker not in text:
        raise ValueError(f"Missing transcript marker in {path}")
    head, rest = text.split(marker, 1)
    body = rest.strip() + "\n"
    patched = split_transcript_body(body, TRANSCRIPT_SECTIONS[chapter_id])
    path.write_text(head + marker + patched, encoding="utf-8")
    print(f"patched transcript: {path.relative_to(ROOT)}")


def update_chapter_commentary(chapter_id: str) -> None:
    path = VOL2 / chapter_id / f"{chapter_id}-commentary.md"
    text = path.read_text(encoding="utf-8")
    refs = CLAIM_REFS[chapter_id]
    for i, anchor in enumerate(refs, start=1):
        new_ref = f"`{chapter_id}-transcript.md{anchor}`"
        if new_ref in text:
            continue
        pattern = rf"(\| {i} \|[^\n]+\| )`?{chapter_id}-transcript\.md:32`?"
        text, n = re.subn(pattern, rf"\1{new_ref}", text, count=1)
        if n == 0 and f"{chapter_id}-transcript.md{anchor}" not in text:
            raise ValueError(f"Row {i} not updated in {path}")
    if "analysis_depth: seed" in text:
        text = text.replace("analysis_depth: seed", "analysis_depth: layer2_drafted")
    path.write_text(text, encoding="utf-8")
    print(f"patched commentary: {path.relative_to(ROOT)}")


def update_readiness() -> None:
    text = READINESS.read_text(encoding="utf-8")
    text = text.replace(
        "| Chapter Layer 0–2 | All six chapters have transcript-anchored claims + line/section refs | **Partial** — L2 tables exist (6–8 claims each); **all** use blanket `transcript.md:32` (Tier C pin-cite debt) |",
        "| Chapter Layer 0–2 | All six chapters have transcript-anchored claims + line/section refs | **Met** — 6–8 L2 claims each; transcript `###` sections + `#anchor` refs (pin-cite prep 2026-06-09); chapter `analysis_depth: layer2_drafted` |",
    )
    text = text.replace(
        "**Pin-cite debt:** **High** — all six chapters: L2 refs → `*-transcript.md:32` only; transcripts need `###` section rails per [`docs/methodology/PIN-CITE-DISCIPLINE.md`](../../../docs/methodology/PIN-CITE-DISCIPLINE.md). No Part VI sweep script yet.",
        "**Pin-cite debt:** **Cleared** (2026-06-09) — `civ-29`–`34` transcripts sectioned; chapter L2 refs use `#anchor` slugs (`scripts/part_vi_pin_cite_prep.py`).",
    )
    text = text.replace(
        "| Pin-cite `civ-29`–`34` | **Not started** |",
        "| Pin-cite `civ-29`–`34` | **Done** — `scripts/part_vi_pin_cite_prep.py` |",
    )
    READINESS.write_text(text, encoding="utf-8")
    print(f"patched: {READINESS.relative_to(ROOT)}")


def main() -> None:
    for cid in TRANSCRIPT_SECTIONS:
        patch_transcript(cid)
        update_chapter_commentary(cid)
    update_readiness()
    print("part_vi_pin_cite_prep: done")


if __name__ == "__main__":
    main()
