#!/usr/bin/env python3
"""Part IV pin-cite: civ-19/20 transcript sections + civ-21-23 chapter L2 refresh."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOL2 = ROOT / "book" / "volume-ii"
PART_IV = (
    ROOT
    / "book"
    / "volume-i-civilization"
    / "parts"
    / "part-04-ancient-foundations-commentary.md"
)
READINESS = ROOT / "docs/routes/volume-i-parts/PART-04-HYBRID-READINESS.md"

TRANSCRIPT_SECTIONS: dict[str, list[tuple[str, str]]] = {
    "civ-18": [
        ("three-questions-opening", "today in today's class I'm going to look at three questions"),
        ("houdin-inside-out-model", "French architect named Jean-Pierre Houdin"),
        ("tomb-resurrection-debate", "for the longest time the accepted theory is this was a"),
        ("manhattan-project-frame", "Great Pyramid was designed as Egypt's Manhattan Project"),
        ("drought-kiloyear-event", "kiloyear event happened"),
        ("pyramid-economy-costs", "you need a pyramid economy okay a pyramid economy"),
        ("imhotep-knowledge-system", "his name is Imhotep"),
        ("bronze-age-preview", "next class we'll we'll look at Mesopotamia"),
    ],
    "civ-19": [
        ("framework-mythology-dialectic", "before I begin um I want to make three General points"),
        ("egypt-mesopotamia-contrast", "Mesopotamia is a very different culture and civilization than Egypt"),
        ("sumerian-uruk-origins", "first great civilization of the Mesopotamia were the Sumerians"),
        ("enuma-elish-creation", "Mesopotamians okay they have a different myth of creation called the enuma elesh"),
        (
            "gilgamesh-immortality-quest",
            "create something called The Epic of gilam mas and today we celebrate the Epic of gamh",
        ),
        ("gilgamesh-pyramid-dialectic", "dialectic with the pyramids"),
        ("social-evolution-myth", "evolution of societies over time"),
        ("indus-preview", "next class we'll discuss the indis valley civilization"),
    ],
    "civ-20": [
        ("three-questions-opening", "Today I'm going to look at three questions"),
        ("bronze-trade-context", "Middle Bronze Age"),
        ("peaceful-egalitarian-evidence", "we have not found any weapons of war"),
        ("urban-design-standardization", "In terms of sanitation"),
        ("unreadable-script", "impossible for us to decipher their written language"),
        ("decline-multi-cause", "collapsing trade networks"),
        ("legacy-indian-religions", "The first we know as **Hinduism**"),
        ("proto-buddhist-speculative", "Proto-Buddhist** religion"),
    ],
    "civ-21": [
        ("bible-library-frame", "good morning so today we start the Bible"),
        ("three-myths-correction", "there were three ideas about the Hebrew Bible"),
        ("levant-history-david", "now I'm going to talk a little about the broad history"),
        ("exile-persian-shift", "but after the Persian Empire returns them to judism"),
        ("bible-apology-framework", "now I want to talk about the Bible okay because the Bible is the mythology"),
        ("jedp-political-real-estate", "the school that supports the House of David"),
        ("david-legitimacy-stories", "so the last thing I want to talk about today is the apology of David"),
    ],
    "civ-22": [
        ("cosmology-not-chronology", "okay so good morning we are continuing the Hebrew Bible"),
        ("poet-god-covenants", "so these are the three major reasons why Kings sponsor"),
        ("cohesion-synchronization", "the second purpose is create cohesion"),
        ("differentiation-fluid-identity", "all right now the last question is differentiation"),
        ("yahwist-author", "but the person who wrote the Bible especially Genesis"),
        ("adam-eve-close-read", "so let's go over some of her literary contributions"),
        ("cain-abel-close-read", "Cain argued with him okay Cain argued back"),
        ("rachel-jacob-irony", "the last story I will mention is a story of um Rachel and Jacob"),
    ],
    "civ-23": [
        ("judaism-periods-overview", "okay good morning so um let us do an overview"),
        ("cyrus-messiah-frame", "so what I will do now is I'm going to focus specifically on this period"),
        ("zoroastrianism-doctrine", "all right let's continue so we have this religion Zionism"),
        ("ezra-canon-merge", "a priest a Jewish priest named Ezra he returns to Jerusalem"),
        ("christianity-forward-bridge", "the Christians basically take all this"),
    ],
}

CHAPTER_CLAIM_REFS: dict[str, list[str]] = {
    "civ-18": [
        "#three-questions-opening",
        "#houdin-inside-out-model",
        "#tomb-resurrection-debate",
        "#manhattan-project-frame",
        "#drought-kiloyear-event",
        "#pyramid-economy-costs",
        "#imhotep-knowledge-system",
        "#bronze-age-preview",
    ],
    "civ-19": [
        "#framework-mythology-dialectic",
        "#egypt-mesopotamia-contrast",
        "#sumerian-uruk-origins",
        "#enuma-elish-creation",
        "#gilgamesh-immortality-quest",
        "#gilgamesh-pyramid-dialectic",
        "#social-evolution-myth",
        "#indus-preview",
    ],
    "civ-20": [
        "#three-questions-opening",
        "#bronze-trade-context",
        "#peaceful-egalitarian-evidence",
        "#urban-design-standardization",
        "#unreadable-script",
        "#decline-multi-cause",
        "#legacy-indian-religions",
        "#proto-buddhist-speculative",
    ],
    "civ-21": [
        "#bible-library-frame",
        "#three-myths-correction",
        "#levant-history-david",
        "#exile-persian-shift",
        "#bible-apology-framework",
        "#jedp-political-real-estate",
        "#bible-apology-framework",
        "#david-legitimacy-stories",
    ],
    "civ-22": [
        "#cosmology-not-chronology",
        "#poet-god-covenants",
        "#cohesion-synchronization",
        "#differentiation-fluid-identity",
        "#yahwist-author",
        "#adam-eve-close-read",
        "#cain-abel-close-read",
        "#rachel-jacob-irony",
    ],
    "civ-23": [
        "#judaism-periods-overview",
        "#judaism-periods-overview",
        "#cyrus-messiah-frame",
        "#zoroastrianism-doctrine",
        "#cyrus-messiah-frame",
        "#ezra-canon-merge",
        "#ezra-canon-merge",
        "#christianity-forward-bridge",
    ],
}

PART_CIV19_REFS = CHAPTER_CLAIM_REFS["civ-19"]
PART_CIV20_REFS = CHAPTER_CLAIM_REFS["civ-20"]


def split_transcript_body(body: str, sections: list[tuple[str, str]]) -> str:
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


def normalize_inline_anchors(text: str) -> str:
    """Move inline ` ### slug` markers to own lines."""
    return re.sub(r" ### ([a-z0-9-]+)", r"\n\n### \1\n\n", text)


LINE_SECTION_RE = re.compile(r"^### ([a-z0-9-]+)\s*$", re.MULTILINE)


def line_start_sections_ok(text: str, slugs: list[str]) -> bool:
    return all(
        re.search(rf"^### {re.escape(slug)}\s*$", text, re.MULTILINE) for slug in slugs
    )


def patch_transcript(chapter_id: str) -> None:
    path = VOL2 / chapter_id / f"{chapter_id}-transcript.md"
    text = path.read_text(encoding="utf-8")
    sections = TRANSCRIPT_SECTIONS.get(chapter_id, [])
    if not sections:
        return
    slugs = [slug for slug, _ in sections]
    if line_start_sections_ok(text, slugs):
        print(f"skip transcript (line-start rails ok): {path.relative_to(ROOT)}")
        return
    if chapter_id == "civ-20":
        marker = "## Full transcript\n"
        if marker not in text:
            raise ValueError(f"No Full transcript block in {path}")
        head, body = text.rsplit(marker, 1)
        body = body.strip() + "\n"
        patched = split_transcript_body(body, sections)
        path.write_text(head + marker + patched, encoding="utf-8")
    elif chapter_id in ("civ-21", "civ-22", "civ-23"):
        marker = "## Part I: Full transcript\n\n"
        head, rest = text.split(marker, 1)
        rest = normalize_inline_anchors(rest)
        body = rest.strip() + "\n"
        extra = TRANSCRIPT_SECTIONS.get(chapter_id, [])
        extra_slugs = [slug for slug, _ in extra]
        if extra and not line_start_sections_ok(body, extra_slugs):
            body = split_transcript_body(body, extra)
        path.write_text(head + marker + body.strip() + "\n", encoding="utf-8")
        print(f"patched transcript: {path.relative_to(ROOT)}")
        return
    else:
        marker = "## Part I: Full transcript\n\n"
        if marker not in text:
            raise ValueError(f"Missing transcript marker in {path}")
        head, rest = text.split(marker, 1)
        body = rest.strip() + "\n"
        patched = split_transcript_body(body, sections)
        path.write_text(head + marker + patched, encoding="utf-8")
    print(f"patched transcript: {path.relative_to(ROOT)}")


def update_chapter_commentary(chapter_id: str) -> None:
    path = VOL2 / chapter_id / f"{chapter_id}-commentary.md"
    text = path.read_text(encoding="utf-8")
    refs = CHAPTER_CLAIM_REFS[chapter_id]
    for i, anchor in enumerate(refs, start=1):
        new_ref = f"`{chapter_id}-transcript.md{anchor}`"
        if new_ref in text:
            continue
        pattern = rf"(\| {i} \|[^\n]+\| )`?{chapter_id}-transcript\.md(?::\d+)?`?"
        text, n = re.subn(pattern, rf"\1{new_ref}", text, count=1)
        if n == 0 and f"{chapter_id}-transcript.md{anchor}" not in text:
            raise ValueError(f"Row {i} not updated in {path}")
    if "analysis_depth: seed" in text:
        text = text.replace("analysis_depth: seed", "analysis_depth: layer2_drafted")
    path.write_text(text, encoding="utf-8")
    print(f"patched commentary: {path.relative_to(ROOT)}")


def update_part_iv_tables() -> None:
    text = PART_IV.read_text(encoding="utf-8")
    for chapter_id in ("civ-19", "civ-20"):
        refs = CHAPTER_CLAIM_REFS[chapter_id]
        for i, anchor in enumerate(refs, start=1):
            new_ref = f"`{chapter_id}-transcript.md{anchor}`"
            if new_ref in text:
                continue
            section_pat = (
                rf"(### {chapter_id}\n\n.*?)(\| {i} \|[^\n]+\| )`[^`]+`"
            )
            text, n = re.subn(
                section_pat,
                rf"\1\2{new_ref}",
                text,
                count=1,
                flags=re.DOTALL,
            )
            if n == 0:
                raise ValueError(f"Part IV {chapter_id} row {i} not updated")
    PART_IV.write_text(text, encoding="utf-8")
    print(f"patched: {PART_IV.relative_to(ROOT)}")


def update_readiness() -> None:
    if not READINESS.exists():
        return
    text = READINESS.read_text(encoding="utf-8")
    text = text.replace(
        "**Pin-cite debt:** `civ-21`–`civ-23` Layer 2 refs overwhelmingly `civ-*-transcript.md:32`; split megagraphs into `###` sections before or during Phase 1 claim authoring.",
        "**Pin-cite debt:** **Cleared** (2026-06-09) — `civ-19`–`23` sectioned/refreshed; chapter L2 uses `#anchor` slugs.",
    )
    READINESS.write_text(text, encoding="utf-8")
    print(f"patched: {READINESS.relative_to(ROOT)}")


def main() -> None:
    for cid in ("civ-18", "civ-19", "civ-20", "civ-21", "civ-22", "civ-23"):
        patch_transcript(cid)
    for cid in CHAPTER_CLAIM_REFS:
        update_chapter_commentary(cid)
    update_part_iv_tables()
    update_readiness()
    print("part_iv_pin_cite_prep: done")


if __name__ == "__main__":
    main()
