#!/usr/bin/env python3
"""Tier-B uplift: full sectioning + #anchor refs for civ-07–10, civ-12."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOL2 = ROOT / "book" / "volume-ii"

# Unique sections in lecture order (slug, split phrase).
TRANSCRIPT_SECTIONS: dict[str, list[tuple[str, str]]] = {
    "civ-07": [
        ("greek-western-source", "created western civilization"),
        ("bronze-age-collapse-greece", "Bronze Age collapse and three things"),
        ("destruction-enables-creativity", "because of these three things that Greece became the most creative"),
        ("three-pillars-polis-alphabet-homer", "three major reasons why Greek"),
        ("polis-competition-diversity", "competition okay these poleis"),
        ("alphabet-evolution", "development of writing systems"),
        ("alphabet-speech-revolution", "writing can become speaking"),
        ("oral-culture-advantages", "oral culture the first major advantage"),
        ("literary-culture-advantages", "advantages to writing culture"),
        ("oral-literary-synthesis", "combined the advantage of both cultures"),
        ("homer-poet-for-people", "problem with Homer is when he was around"),
        ("iliad-empathy", "we call this idea empathy"),
        ("iliad-psychology", "human psychology"),
        ("iliad-metaphor", "what are metaphors metaphors are connections"),
        ("homer-theory-of-human", "theory of human"),
        ("greece-china-contrast", "why is Greek civilization different from Chinese"),
    ],
    "civ-08": [
        ("greek-history-recap", "overview of Greek history"),
        ("geography-is-destiny", "geography is Destiny"),
        ("sparta-character", "let's first talk about Sparta"),
        ("athens-eudaimonia", "Athens was a completely opposite Society"),
        ("ostracism", "ostracism okay"),
        ("democracy-factional-nobility", "democracy usually was a battle between different factions"),
        ("sparta-athens-opposed", "diametrically opposed to each other"),
        ("persian-wars-narrative", "Battle of Marathon"),
        ("persia-strategic-errors", "Persians did not do that okay the Persian king"),
        ("delian-league-empire", "Delian League is a"),
        ("pericles-power", "Pericles comes into power"),
        ("peloponnesian-bully", "Athens is basically the big bully"),
        ("nobility-class-conflict", "only way to understand what happened is to understand that the very basis of conflict"),
        ("cleon-brasidas", "Cleon proposes this aggressive strategy"),
        ("lysander-persian-money", "Persia gets involved and gives Sparta a Navy"),
        ("athens-spared-elite-ties", "upper nobility of Sparta and the upper nobility of Athens"),
        ("rat-utopia-experiment", "rat Utopia"),
        ("wealthy-societies-war", "they were killing each other for no reason"),
        ("humans-not-rats", "humans are different from rats"),
    ],
    "civ-09": [
        ("collective-identity-institutions", "how do you create an identity"),
        ("theater-democratic-citizen", "identity as an as a democratic citizen"),
        ("festival-dionysus", "Festival of Dionysus"),
        ("prophets-of-democracy", "prophets of democracy"),
        ("oresteia-plot", "wrote a play called Oresteia"),
        ("oresteia-democracy-gift", "gods gave you democracy honor them"),
        ("oedipus-trilogy", "Oedipus trilogy okay Oedipus Trilogy"),
        ("antigone-unwritten-law", "laws in the universe ver that are Divine Unwritten"),
        ("sophocles-anti-king", "this is a message that's very much anti- King"),
        ("old-give-way-young", "world works when the old give way to the young"),
        ("euripides-critic", "Euripides he criticized Athenian democracy"),
        ("trojan-women-melos", "Trojan Women is a direct response to what"),
        ("bacchae-plot", "plot of the Bacchae"),
        ("bacchae-empire-metaphor", "mother holds the son's head in her hand"),
        ("bacchae-alt-interpretations", "most common interpretation is it is a play that explores"),
        ("revenge-hubris-themes", "very common theme is the idea of hubris"),
    ],
    "civ-10": [
        ("theater-socrates-opening", "profits of democracy"),
        ("democracy-needs-truth", "most people are not capable of exercising reason"),
        ("socratic-dialogue", "Socratic dialogue"),
        ("language-convention", "language is just a convention"),
        ("clouds-aristophanes", "play was called the clouds"),
        ("aristocratic-students", "children of the rich"),
        ("thirty-tyrants", "30 tyrants"),
        ("trial-399-bce", "399 BCE Socrates is put on trial"),
        ("trial-provocation", "Socrates refused to defend himself"),
        ("death-performance-art", "performance artist okay"),
        ("plato-redeems-socrates", "Redeeming the reputation of Socrates"),
        ("republic-cave-intro", "allegory of the cave"),
        ("cave-narrative", "imagine a cave deep under the Earth"),
        ("cave-christianity-bridge", "Christians Socrates becomes Jesus"),
        ("philosopher-king", "ruled by philosopher"),
        ("plato-influence-kings", "Kings hate democracy"),
        ("plato-influences-lost", "we don't know and the reason again is most of this is loss"),
        ("syracuse-failure", "went to a place called Syracuse"),
        ("macedonia-preview", "rise of Macedonia"),
    ],
    "civ-12": [
        ("alexander-model-predictions", "third prediction we can make about him"),
        ("philip-death-succession", "death of his father in 336"),
        ("thebes-destruction-fear", "destroying Thebes which is one of the great cultural"),
        ("persian-battle-pattern", "Battle of Granicus"),
        ("cohesion-discipline-devotion", "cohesion discipline and devotion"),
        ("siwa-divine-kingship", "goes to a place called The Temple of Zeus"),
        ("parmenion-cleitus-deaths", "Cleitus the Black killing him"),
        ("india-desert-limits", "they basically Mutiny they refuse to fight"),
    ],
}

CHAPTER_CLAIM_REFS: dict[str, list[str]] = {
    "civ-07": [
        "#greek-western-source",
        "#bronze-age-collapse-greece",
        "#destruction-enables-creativity",
        "#three-pillars-polis-alphabet-homer",
        "#polis-competition-diversity",
        "#alphabet-evolution",
        "#alphabet-speech-revolution",
        "#oral-culture-advantages",
        "#literary-culture-advantages",
        "#oral-literary-synthesis",
        "#homer-poet-for-people",
        "#iliad-empathy",
        "#iliad-psychology",
        "#iliad-metaphor",
        "#homer-theory-of-human",
        "#greece-china-contrast",
    ],
    "civ-08": [
        "#greek-history-recap",
        "#geography-is-destiny",
        "#sparta-character",
        "#athens-eudaimonia",
        "#ostracism",
        "#democracy-factional-nobility",
        "#sparta-athens-opposed",
        "#persian-wars-narrative",
        "#persia-strategic-errors",
        "#delian-league-empire",
        "#pericles-power",
        "#peloponnesian-bully",
        "#nobility-class-conflict",
        "#cleon-brasidas",
        "#lysander-persian-money",
        "#athens-spared-elite-ties",
        "#rat-utopia-experiment",
        "#wealthy-societies-war",
        "#humans-not-rats",
    ],
    "civ-09": [
        "#collective-identity-institutions",
        "#theater-democratic-citizen",
        "#festival-dionysus",
        "#prophets-of-democracy",
        "#oresteia-plot",
        "#oresteia-democracy-gift",
        "#oedipus-trilogy",
        "#antigone-unwritten-law",
        "#sophocles-anti-king",
        "#old-give-way-young",
        "#euripides-critic",
        "#trojan-women-melos",
        "#bacchae-plot",
        "#bacchae-empire-metaphor",
        "#bacchae-alt-interpretations",
        "#revenge-hubris-themes",
    ],
    "civ-10": [
        "#theater-socrates-opening",
        "#democracy-needs-truth",
        "#socratic-dialogue",
        "#language-convention",
        "#clouds-aristophanes",
        "#aristocratic-students",
        "#thirty-tyrants",
        "#trial-399-bce",
        "#trial-provocation",
        "#death-performance-art",
        "#plato-redeems-socrates",
        "#republic-cave-intro",
        "#cave-narrative",
        "#cave-christianity-bridge",
        "#philosopher-king",
        "#plato-influence-kings",
        "#plato-influences-lost",
        "#macedonia-preview",
        "#plato-influences-lost",
        "#syracuse-failure",
    ],
    "civ-12": [
        "#alexander-model-predictions",
        "#philip-death-succession",
        "#thebes-destruction-fear",
        "#cohesion-discipline-devotion",
        "#persian-battle-pattern",
        "#siwa-divine-kingship",
        "#parmenion-cleitus-deaths",
        "#india-desert-limits",
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
        if re.search(rf"\| {i} \|[^\n]+\| {re.escape(new_ref)}", text):
            continue
        pattern = (
            rf"(\| {i} \|[^\n]+\| )`?{chapter_id}-transcript\.md(?::[\d-]+)?`?"
        )
        text, n = re.subn(pattern, rf"\1{new_ref}", text, count=1)
        if n == 0:
            raise ValueError(f"Row {i} not updated in {path}")
    for anchor in set(refs):
        text = re.sub(
            rf"`{chapter_id}-transcript\.md:[\d-]+`(?=[^\n]*{re.escape(anchor.lstrip('#'))})",
            f"`{chapter_id}-transcript.md{anchor}`",
            text,
        )
    text = re.sub(
        rf"`{chapter_id}-transcript\.md:[\d-]+`",
        lambda m: m.group(0),
        text,
    )
    line_to_anchor = _line_ref_replacements(chapter_id)
    for old, new in line_to_anchor.items():
        text = text.replace(old, new)
    if "analysis_depth: seed" in text:
        text = text.replace("analysis_depth: seed", "analysis_depth: layer2_drafted")
    path.write_text(text, encoding="utf-8")
    print(f"patched commentary: {path.relative_to(ROOT)}")


def _line_ref_replacements(chapter_id: str) -> dict[str, str]:
    """Map legacy line-range refs in Core Concepts to #anchors."""
    refs = CHAPTER_CLAIM_REFS[chapter_id]
    slug_by_prefix: dict[str, str] = {}
    for slug, _ in TRANSCRIPT_SECTIONS[chapter_id]:
        slug_by_prefix[slug.split("-")[0]] = f"#{slug}"
    out: dict[str, str] = {}
    mapping: dict[str, list[tuple[str, str]]] = {
        "civ-07": [
            (":39-45", "#three-pillars-polis-alphabet-homer"),
            (":45-52", "#alphabet-speech-revolution"),
            (":52-55", "#oral-culture-advantages"),
            (":55-58", "#literary-culture-advantages"),
            (":59-67", "#homer-poet-for-people"),
            (":72-73", "#iliad-empathy"),
            (":74-80", "#iliad-psychology"),
            (":81-82", "#iliad-metaphor"),
            (":83-84", "#homer-theory-of-human"),
            (":87-93", "#greece-china-contrast"),
        ],
        "civ-08": [
            (":33-34", "#geography-is-destiny"),
            (":34-42", "#sparta-character"),
            (":42-50", "#athens-eudaimonia"),
            (":49-51", "#ostracism"),
            (":52-55", "#democracy-factional-nobility"),
            (":77-86", "#delian-league-empire"),
            (":111-126", "#humans-not-rats"),
            (":123-126", "#humans-not-rats"),
        ],
        "civ-09": [
            (":34-40", "#theater-democratic-citizen"),
            (":35-39", "#festival-dionysus"),
            (":39-40", "#prophets-of-democracy"),
            (":43-58", "#oresteia-democracy-gift"),
            (":65-71", "#antigone-unwritten-law"),
            (":75-79", "#trojan-women-melos"),
            (":80-96", "#bacchae-empire-metaphor"),
        ],
        "civ-10": [
            (":35-39", "#socratic-dialogue"),
            (":38-39", "#language-convention"),
            (":39-46", "#clouds-aristophanes"),
            (":48-50", "#thirty-tyrants"),
            (":50-58", "#trial-provocation"),
            (":58-68", "#plato-redeems-socrates"),
            (":60-74", "#cave-narrative"),
            (":67-74", "#cave-christianity-bridge"),
            (":74-76", "#philosopher-king"),
            (":81-82", "#plato-influence-kings"),
            (":89-90", "#macedonia-preview"),
        ],
    }
    for line_ref, anchor in mapping.get(chapter_id, []):
        out[f"`{chapter_id}-transcript.md{line_ref}`"] = (
            f"`{chapter_id}-transcript.md{anchor}`"
        )
    return out


def main() -> None:
    for cid in TRANSCRIPT_SECTIONS:
        patch_transcript(cid)
        update_chapter_commentary(cid)
    print("part_ii_tier_b_uplift: done")


if __name__ == "__main__":
    main()
