#!/usr/bin/env python3
"""Insert transcript ### section anchors for Part VII (civ-35..41) and refresh L2 refs."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOL2 = ROOT / "book" / "volume-ii"
READINESS = ROOT / "docs/routes/volume-i-parts/PART-07-HYBRID-READINESS.md"

TRANSCRIPT_SECTIONS: dict[str, list[tuple[str, str]]] = {
    "civ-35": [
        ("fifth-pillar-thesis", "five pillars"),
        ("viking-age-frame", "793 to 1066"),
        ("normandy-england-afterlife", "normandy the normans"),
        ("expansion-settlement-trade", "settlements the first"),
        ("community-before-individual", "community is distinct from the individual"),
        ("premodern-race-contrast", "race and racism"),
    ],
    "civ-36": [
        ("oral-reconstruction-limit", "purposefully an oral tradition"),
        ("archaeology-graves", "dig up their graves"),
        ("oral-intimacy-imagination", "intimacy and bonding"),
        ("literary-shame-watchfulness", "shame you're very conscious"),
        ("homer-dante-shakespeare", "dante and shakespeare"),
        ("civilization-creativity-loss", "less creative because of civilization"),
    ],
    "civ-37": [
        ("golden-age-divergence", "dark ages uh islam was embarked"),
        ("islam-sunni-shia-orientation", "shia which is based primarily"),
        ("baghdad-cosmopolitan-center", "baghdad okay it"),
        ("house-of-wisdom-translation", "house of wisdom and it"),
        ("golden-age-decline-mongols", "mongols will sack baghdad"),
        ("empire-literature-threshold", "when it becomes an empire"),
    ],
    "civ-38": [
        ("china-model-test", "china um obviously we are in china"),
        ("four-inventions-creativity", "compass paper print"),
        ("hundred-schools-foundations", "hundred schools"),
        ("open-cooperative-competition", "open cooperative"),
        ("examination-center-control", "examination that um promoted bureaucrats"),
        ("confucian-bureaucratic-legitimation", "bureaucratic"),
    ],
    "civ-39": [
        (
            "mongol-brutality-constraints",
            "mongols have a terrible reputation for their brutality",
        ),
        ("nomadic-pastoral-culture", "nomadic pastoral"),
        ("steppe-agricultural-contrast", "agricultural empires"),
        ("walls-fortifications-response", "great wall of of china"),
        ("mongol-specialist-absorption", "indian engineers"),
        ("mythology-cultural-values", "mythology"),
    ],
    "civ-40": [
        ("opening-crusades-bridge", "doing the crusades"),
        ("jesus-poverty-contrast", "camel to go through"),
        ("roman-successor-church", "catholic church basically became"),
        ("salvation-orthodoxy-power", "enforce right thinking"),
        ("scapegoating-mechanism", "scapegoat"),
        ("afterlife-worldview", "happy afterlife"),
    ],
    "civ-41": [
        ("opening-renaissance-question", "how did the Renaissance start"),
        ("greece-christian-modernity", "re-imagining of classical Greece"),
        ("italian-citystates-competition", "city states of Italy"),
        ("divine-comedy-imagination", "Divine Comedy"),
        ("dante-most-responsible", "Dante is most responsible"),
        ("michelangelo-creation-adam", "Creation of Adam"),
        ("quiet-revolution-poetry", "peacefully through the power of poetry"),
    ],
}

CLAIM_REFS: dict[str, list[str]] = {
    "civ-35": [
        "#fifth-pillar-thesis",
        "#viking-age-frame",
        "#expansion-settlement-trade",
        "#normandy-england-afterlife",
        "#community-before-individual",
        "#premodern-race-contrast",
    ],
    "civ-36": [
        "#oral-reconstruction-limit",
        "#archaeology-graves",
        "#oral-intimacy-imagination",
        "#literary-shame-watchfulness",
        "#homer-dante-shakespeare",
        "#civilization-creativity-loss",
    ],
    "civ-37": [
        "#golden-age-divergence",
        "#islam-sunni-shia-orientation",
        "#baghdad-cosmopolitan-center",
        "#house-of-wisdom-translation",
        "#golden-age-decline-mongols",
        "#empire-literature-threshold",
    ],
    "civ-38": [
        "#china-model-test",
        "#four-inventions-creativity",
        "#hundred-schools-foundations",
        "#open-cooperative-competition",
        "#confucian-bureaucratic-legitimation",
        "#examination-center-control",
    ],
    "civ-39": [
        "#mongol-brutality-constraints",
        "#nomadic-pastoral-culture",
        "#steppe-agricultural-contrast",
        "#walls-fortifications-response",
        "#mongol-specialist-absorption",
        "#mythology-cultural-values",
    ],
    "civ-40": [
        "#opening-crusades-bridge",
        "#jesus-poverty-contrast",
        "#roman-successor-church",
        "#salvation-orthodoxy-power",
        "#scapegoating-mechanism",
        "#afterlife-worldview",
    ],
    "civ-41": [
        "#greece-christian-modernity",
        "#italian-citystates-competition",
        "#dante-most-responsible",
        "#divine-comedy-imagination",
        "#michelangelo-creation-adam",
        "#quiet-revolution-poetry",
    ],
}

PART_PATHS: dict[str, str] = {
    "civ-35": "#civ-35",
    "civ-36": "#civ-36",
    "civ-37": "#civ-37",
    "civ-38": "#civ-38",
    "civ-39": "#civ-39",
    "civ-40": "#civ-40",
    "civ-41": "#civ-41",
}


def split_transcript_body(body: str, sections: list[tuple[str, str]]) -> str:
    body = re.sub(r"\s+", " ", body).strip() + "\n"
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
    if "transcript_curation:" not in head:
        head = head.replace(
            "transcript_fidelity: exact_body_match\n",
            "transcript_fidelity: exact_body_match\n"
            "transcript_curation: curated_sectioned\n"
            "pin_cite_reviewed_at: 2026-06-09\n",
        )
    anchor = PART_PATHS[chapter_id]
    if "part_id:" not in head:
        head = head.replace(
            "part: I\n",
            f"part: I\npart_id: part-07-world-after-rome\n"
            f"part_commentary_path: ../../../docs/routes/volume-i-parts/"
            f"part-07-world-after-rome-commentary.md{anchor}\n"
            f"part_bibliography_path: ../../../docs/routes/volume-i-parts/"
            f"part-07-world-after-rome-bibliography.md\n",
        )
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
        for old in (":32", ":29"):
            pattern = rf"(\| {i} \|[^\n]+\| )`?{chapter_id}-transcript\.md{old}`?"
            text, n = re.subn(pattern, rf"\1{new_ref}", text, count=1)
            if n:
                break
        else:
            pattern2 = rf"(\| {i} \|[^\n]+\| )TBD pin-cite"
            text, n2 = re.subn(pattern2, rf"\1{new_ref}", text, count=1)
            if n2 == 0 and new_ref not in text:
                raise ValueError(f"Row {i} not updated in {path}")
    if "analysis_depth: seed" in text:
        text = text.replace("analysis_depth: seed", "analysis_depth: layer2_drafted")
    anchor = PART_PATHS[chapter_id]
    if "part_id:" not in text:
        text = text.replace(
            f"companion_transcript_path: ./{chapter_id}-transcript.md\n",
            f"companion_transcript_path: ./{chapter_id}-transcript.md\n"
            f"part_id: part-07-world-after-rome\n"
            f"part_commentary_path: ../../../docs/routes/volume-i-parts/"
            f"part-07-world-after-rome-commentary.md{anchor}\n"
            f"part_bibliography_path: ../../../docs/routes/volume-i-parts/"
            f"part-07-world-after-rome-bibliography.md\n",
        )
    path.write_text(text, encoding="utf-8")
    print(f"patched commentary: {path.relative_to(ROOT)}")


def update_readiness() -> None:
    if not READINESS.is_file():
        return
    text = READINESS.read_text(encoding="utf-8")
    replacements = [
        (
            "plan_status: phase0_inventory",
            "plan_status: phase3_complete",
        ),
        (
            "| Pin-cite `civ-35`–`41` | **Partial** — `civ-35`–`37` + wedge `civ-40`/`civ-41`; `civ-38`–`39` **deferred** |",
            "| Pin-cite `civ-35`–`41` | **Done** — `scripts/part_vii_pin_cite_prep.py` |",
        ),
        (
            "| README 6-step lattice + Part links | **Partial** — `civ-35`/`civ-36` + wedge `civ-40`/`civ-41`; `civ-37`–`39` deferred |",
            "| README 6-step lattice + Part links | **Done** — all `civ-35`–`41` |",
        ),
        (
            "| Validator Part VII README checks | **Done** — wedge chapters `civ-40`/`civ-41` |",
            "| Validator Part VII README checks | **Done** — all `civ-35`–`41` |",
        ),
        (
            "| `part-07-world-after-rome-commentary.md` | **Phase 1 wedge + `civ-35` live** — `civ-35` + `civ-41` + `gb-10` (close); `civ-36`–`39` stub |",
            "| `part-07-world-after-rome-commentary.md` | **Phase 3 complete** — all `civ-35`–`41` + `gb-10` (close) |",
        ),
        (
            "| `part-07-world-after-rome-bibliography.md` | **Phase 1 wedge stub** |",
            "| `part-07-world-after-rome-bibliography.md` | **Phase 3** — `supports:`/`counters:` for `civ-35`–`41` |",
        ),
        (
            "**Pin-cite debt:** **Open** — no `scripts/part_vii_pin_cite_prep.py`; transcripts lack `###` section rails; L2 refs use coarse line pointers only.",
            "**Pin-cite debt:** **Cleared** (2026-06-09) — `scripts/part_vii_pin_cite_prep.py`; all seven chapters sectioned.",
        ),
    ]
    for old, new in replacements:
        if old in text:
            text = text.replace(old, new)
    READINESS.write_text(text, encoding="utf-8")
    print(f"patched: {READINESS.relative_to(ROOT)}")


def main() -> None:
    for cid in TRANSCRIPT_SECTIONS:
        patch_transcript(cid)
        update_chapter_commentary(cid)
    update_readiness()
    print("part_vii_pin_cite_prep: done")


if __name__ == "__main__":
    main()
