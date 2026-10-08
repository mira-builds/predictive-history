#!/usr/bin/env python3
"""Insert transcript ### section anchors for Part I (civ-01..06) and refresh L2 refs."""

from __future__ import annotations

import re
from pathlib import Path

from part_pin_cite_common import ROOT, VOL2, patch_transcript

READINESS = ROOT / "docs/routes/volume-i-parts/PART-01-HYBRID-READINESS.md"
PART_ID = "part-01-dawn-of-civilization"

TRANSCRIPT_SECTIONS: dict[str, list[tuple[str, str]]] = {
    "civ-01": [
        ("reject-farming-progress", "there's no evidence for this"),
        ("farming-harder-than-gathering", "it was actually pretty stupid to transition from hunter gatherer into farming"),
        ("four-theory-families", "there are four different disciplines from which we can collect evidence"),
        ("religion-leading-theory", "the consensus what most people agree on today okay most Scholars"),
        ("gobekli-tepe-ritual-center", "Gobekli Tepe is a place of religious worship"),
        ("catalhoyuk-religion-everywhere", "religion permeated or was in every place they were"),
    ],
    "civ-02": [
        ("religious-impulse-before-farming", "religious impulse this need for religion"),
        ("ice-age-cave-paintings", "Ice Age cave paintings"),
        ("cave-as-portal", "portal a door"),
        ("animism-defined", "we have actually a word for this religion and this word is um animism"),
        ("durkheim-collective-consciousness", "religion is our Collective Consciousness"),
        ("religious-animals-thesis", "we are first and foremost a religious animal"),
    ],
    "civ-03": [
        ("peaceful-egalitarian-artistic", "for most of human history we have been peaceful egalitarian and artistic"),
        ("yamnaya-preview", "a new group of uh people called the Yamnaya came came into being"),
        ("animism-shamanism-model", "it was animism and shamanism"),
        ("creation-myth-legal-order", "this is what we call a creation myth"),
        ("grandness-completeness-unity", "you need these three ideas grandness completeness and unity"),
        ("molimo-sleep-taboo", "the greatest crimes that the pygmy can commit if not the greatest is to be found asleep when the malomo is singing"),
    ],
    "civ-04": [
        ("war-property-patriarchy-question", "how is it that today we have War private property and patriarchy"),
        ("gimbutas-old-europe", "the anthropologist Marija Gimbutas called Old Europe"),
        ("proto-indo-european", "we call Proto indoan"),
        ("dna-yamnaya-evidence", "advances in genetics DNA technology"),
        ("conquest-not-diffusion", "overwhelming DNA evidence that it was in fact Conquest"),
        ("women-political-class", "Old Europe was ruled by women or women were part of the political class"),
    ],
    "civ-05": [
        ("three-yamnaya-questions", "who are the Yamnaya second question is where do they come from"),
        ("near-east-mother-goddess", "they worship the mother goddess who gives life to everything"),
        ("social-evolution-definition", "Evolution means open Cooperative competition"),
        ("steppe-scarcity", "there are very scarce resources in the steps"),
        ("pastoralism-innovation", "the first Innovation they adopted was a pastoral economy"),
        ("sky-father-religion", "they worship someone called the sky father"),
    ],
    "civ-06": [
        ("bronze-age-interconnected", "Bronze Age and why is it called the Bronze Age"),
        ("bronze-like-oil", "bronze is like oil today"),
        ("troy-toll-gate", "this place is called Troy"),
        ("bronze-age-collapse", "Bronze Age collapse"),
        ("elite-overproduction-turchin", "Peter Turchin Peter Turchin who's a historian"),
        ("collapse-generative-greece-israel", "Mycenaean Greece changed into a new society that gave us Greek civilization"),
    ],
}

CLAIM_REFS: dict[str, list[str]] = {
    "civ-01": [
        "#reject-farming-progress",
        "#farming-harder-than-gathering",
        "#four-theory-families",
        "#religion-leading-theory",
        "#gobekli-tepe-ritual-center",
        "#catalhoyuk-religion-everywhere",
    ],
    "civ-02": [
        "#religious-impulse-before-farming",
        "#ice-age-cave-paintings",
        "#cave-as-portal",
        "#animism-defined",
        "#durkheim-collective-consciousness",
        "#religious-animals-thesis",
    ],
    "civ-03": [
        "#peaceful-egalitarian-artistic",
        "#yamnaya-preview",
        "#animism-shamanism-model",
        "#creation-myth-legal-order",
        "#grandness-completeness-unity",
        "#molimo-sleep-taboo",
    ],
    "civ-04": [
        "#war-property-patriarchy-question",
        "#proto-indo-european",
        "#gimbutas-old-europe",
        "#dna-yamnaya-evidence",
        "#conquest-not-diffusion",
        "#women-political-class",
    ],
    "civ-05": [
        "#three-yamnaya-questions",
        "#near-east-mother-goddess",
        "#social-evolution-definition",
        "#steppe-scarcity",
        "#pastoralism-innovation",
        "#sky-father-religion",
    ],
    "civ-06": [
        "#bronze-age-interconnected",
        "#bronze-like-oil",
        "#troy-toll-gate",
        "#bronze-age-collapse",
        "#elite-overproduction-turchin",
        "#collapse-generative-greece-israel",
    ],
}


def _update_commentary_refs(chapter_id: str) -> None:
    path = VOL2 / chapter_id / f"{chapter_id}-commentary.md"
    text = path.read_text(encoding="utf-8")
    refs = CLAIM_REFS[chapter_id]
    for i, anchor in enumerate(refs, start=1):
        new_ref = f"`{chapter_id}-transcript.md{anchor}`"
        if new_ref in text:
            continue
        patterns = [
            rf"(\| {i} \|[^\n]+\| )`?{chapter_id}-transcript\.md:\d+(?:-\d+)?`?",
            rf"(\| {i} \|[^\n]+\| )`?{chapter_id}-transcript\.md:32`?",
            rf"(\| {i} \|[^\n]+\| )`?{chapter_id}-transcript\.md:29`?",
            rf"(\| {i} \|[^\n]+\| )`?{chapter_id}-transcript\.md:31`?",
            rf"(\| {i} \|[^\n]+\| )TBD pin-cite",
        ]
        for pattern in patterns:
            text, n = re.subn(pattern, rf"\1{new_ref}", text, count=1)
            if n:
                break
        else:
            if new_ref not in text:
                raise ValueError(f"Row {i} not updated in {path}")
    if "analysis_depth: seed" in text:
        text = text.replace("analysis_depth: seed", "analysis_depth: layer2_drafted")
    path.write_text(text, encoding="utf-8")
    print(f"patched commentary refs: {path.relative_to(ROOT)}")


def _patch_commentary_with_part_paths(chapter_id: str) -> None:
    path = VOL2 / chapter_id / f"{chapter_id}-commentary.md"
    text = path.read_text(encoding="utf-8")
    anchor = f"#{chapter_id}"
    if "part_id:" not in text:
        text = text.replace(
            f"companion_transcript_path: ./{chapter_id}-transcript.md\n",
            f"companion_transcript_path: ./{chapter_id}-transcript.md\n"
            f"part_id: {PART_ID}\n"
            f"part_commentary_path: ../../../docs/routes/volume-i-parts/"
            f"part-01-dawn-of-civilization-commentary.md{anchor}\n"
            f"part_bibliography_path: ../../../docs/routes/volume-i-parts/"
            f"part-01-dawn-of-civilization-bibliography.md\n",
        )
        path.write_text(text, encoding="utf-8")
        print(f"patched commentary frontmatter: {path.relative_to(ROOT)}")


def update_readiness() -> None:
    if not READINESS.is_file():
        return
    text = READINESS.read_text(encoding="utf-8")
    replacements = [
        ("plan_status: phase0_inventory", "plan_status: phase3_complete"),
        (
            "**Pin-cite debt:** **Open**",
            "**Pin-cite debt:** **Cleared** (2026-06-10)",
        ),
    ]
    for old, new in replacements:
        if old in text:
            text = text.replace(old, new)
    READINESS.write_text(text, encoding="utf-8")
    print(f"patched: {READINESS.relative_to(ROOT)}")


def main() -> None:
    for cid in TRANSCRIPT_SECTIONS:
        patch_transcript(cid, TRANSCRIPT_SECTIONS[cid], part_id=PART_ID)
        _update_commentary_refs(cid)
        _patch_commentary_with_part_paths(cid)
    update_readiness()
    print("part_i_pin_cite_prep: done")


if __name__ == "__main__":
    main()
