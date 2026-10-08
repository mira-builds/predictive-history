#!/usr/bin/env python3
"""Low-debt pin-cite sweep: Parts II–III civ-11, civ-13–17."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOL2 = ROOT / "book" / "volume-ii"

TRANSCRIPT_SECTIONS: dict[str, list[tuple[str, str]]] = {
    "civ-11": [
        ("conquest-not-diffusion", "spread through a process of Conquest"),
        ("father-son-analogy", "there's a father and there's a son"),
        ("poor-rich-thought-experiment", "let's compare North Korea with South Korea"),
        ("macedon-geography-pressure", "Macedon is very poor weak"),
        ("thebes-sacred-band", "hostage in Thebes"),
        ("philip-meritocracy-parmenion", "turn it into a meritocracy"),
        ("amphipolis-gold", "invades a city called amphipolis"),
        ("chaeronea-sacred-band", "Battle of Chaeronea"),
    ],
    "civ-13": [
        ("aristotle-paradox-opening", "Aristotle is a paradox"),
        ("plato-forms-contrast", "form of the good"),
        ("aristotle-cosmology-telos", "God is a prime mover"),
        ("aristotle-as-censor", "what I refer to as a sensor"),
        ("philip-aristotle-parallel", "compare contrast the life of Philip"),
        ("pan-hellenic-project", "pan helenic project"),
        ("hellenistic-successor-kingdoms", "empire was divided into three major fragments"),
        ("library-alexandria-museum", "Library of Alexandria"),
    ],
    "civ-14": [
        ("rome-power-map-opening", "we start Rome today"),
        ("open-citizenship-manpower", "welcome you as a citizen"),
        ("character-values-frame", "value system or what is known as the character"),
        ("pyrrhus-first-punic", "his name is Pyrrhus"),
        ("hannibal-cannae-crisis", "Battle of Cannae"),
        ("cohesion-discipline-devotion", "cohesion do the soldiers"),
        ("carthage-destruction-close", "Rome in the third Punic War from 149"),
        ("brutus-republic-myth", "Lucius Brutus"),
    ],
    "civ-15": [
        ("three-questions-mythmaker", "what did he want what were his motivations"),
        ("mythmaker-definition", "he was a myth maker okay A mythmaker"),
        ("assassination-identity-threat", "they killed Julius Caesar because"),
        ("post-146-imperial-republic", "by 146 Rome had become a contradiction"),
        ("first-triumvirate", "called the first triumvirate"),
        ("caesar-commentaries-dispatches", "read the composition of Caesar"),
        ("civil-war-rubicon", "cross the Rubicon"),
        ("clemency-personality-cult", "offers clemency to the enemy"),
    ],
    "civ-16": [
        ("caesar-will-octavian-frame", "read the will of Caesar"),
        ("second-triumvirate-phases", "second triumvirate"),
        ("philippi-actium-settlement", "Battle of Philippi"),
        ("augustan-settlement", "declare him Augustus Caesar"),
        ("assassination-myth-crystallizes", "death of Caesar allow Octavian"),
        ("pomerium-senate-taboo", "idea of the pomerium"),
        ("antony-self-defeat", "he basically self-destructs he didn't have to"),
        ("adoptive-succession-weakness", "Emperors would be adopted"),
    ],
    "civ-17": [
        ("rome-greece-review", "comparing contrast it to the Greeks"),
        ("augustus-praetorian-army", "Praetorian Guard"),
        ("aeneas-myth-legitimacy", "man named Aeneas"),
        ("literature-roman-identity", "greatest work of propaganda ever in human history"),
        ("homer-virgil-frame", "compare and contrast the Iliad and the Odyssey"),
        ("homer-love-imagination", "love is the basis of civilization"),
        ("virgil-piety-eternity", "piety is the basis of civilization"),
        ("egypt-eternity-handoff", "Where do they get the idea of Eternity from"),
    ],
}

CHAPTER_CLAIM_REFS: dict[str, list[str]] = {
    "civ-11": [
        "#conquest-not-diffusion",
        "#father-son-analogy",
        "#poor-rich-thought-experiment",
        "#macedon-geography-pressure",
        "#thebes-sacred-band",
        "#philip-meritocracy-parmenion",
        "#amphipolis-gold",
        "#chaeronea-sacred-band",
    ],
    "civ-13": [
        "#aristotle-paradox-opening",
        "#plato-forms-contrast",
        "#aristotle-cosmology-telos",
        "#aristotle-as-censor",
        "#philip-aristotle-parallel",
        "#pan-hellenic-project",
        "#hellenistic-successor-kingdoms",
        "#library-alexandria-museum",
    ],
    "civ-14": [
        "#rome-power-map-opening",
        "#open-citizenship-manpower",
        "#pyrrhus-first-punic",
        "#hannibal-cannae-crisis",
        "#cohesion-discipline-devotion",
        "#character-values-frame",
        "#brutus-republic-myth",
        "#carthage-destruction-close",
    ],
    "civ-15": [
        "#three-questions-mythmaker",
        "#mythmaker-definition",
        "#post-146-imperial-republic",
        "#caesar-commentaries-dispatches",
        "#first-triumvirate",
        "#civil-war-rubicon",
        "#clemency-personality-cult",
        "#assassination-identity-threat",
    ],
    "civ-16": [
        "#caesar-will-octavian-frame",
        "#assassination-myth-crystallizes",
        "#philippi-actium-settlement",
        "#antony-self-defeat",
        "#pomerium-senate-taboo",
        "#assassination-myth-crystallizes",
        "#augustan-settlement",
        "#adoptive-succession-weakness",
    ],
    "civ-17": [
        "#rome-greece-review",
        "#augustus-praetorian-army",
        "#aeneas-myth-legitimacy",
        "#homer-virgil-frame",
        "#homer-love-imagination",
        "#virgil-piety-eternity",
        "#literature-roman-identity",
        "#egypt-eternity-handoff",
    ],
}


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


def patch_transcript(chapter_id: str) -> None:
    path = VOL2 / chapter_id / f"{chapter_id}-transcript.md"
    sections = TRANSCRIPT_SECTIONS[chapter_id]
    if all(f"### {slug}" in path.read_text(encoding="utf-8") for slug, _ in sections):
        print(f"skip transcript (already sectioned): {path.relative_to(ROOT)}")
        return
    text = path.read_text(encoding="utf-8")
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
        pattern = (
            rf"(\| {i} \|[^\n]+\| )`?{chapter_id}-transcript\.md(?::[\d-]+)?`?"
        )
        text, n = re.subn(pattern, rf"\1{new_ref}", text, count=1)
        if n == 0:
            raise ValueError(f"Row {i} not updated in {path}")
    if "analysis_depth: seed" in text:
        text = text.replace("analysis_depth: seed", "analysis_depth: layer2_drafted")
    path.write_text(text, encoding="utf-8")
    print(f"patched commentary: {path.relative_to(ROOT)}")


def main() -> None:
    for cid in TRANSCRIPT_SECTIONS:
        patch_transcript(cid)
        update_chapter_commentary(cid)
    print("part_ii_iii_pin_cite_sweep: done")


if __name__ == "__main__":
    main()
