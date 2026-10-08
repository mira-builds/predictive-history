#!/usr/bin/env python3
"""Insert transcript ### section anchors for Part V (civ-24..28) and refresh L2 refs."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOL2 = ROOT / "book" / "volume-ii"
PART_COMMENTARY = (
    ROOT
    / "book"
    / "volume-i-civilization"
    / "parts"
    / "part-05-christianity-and-islam-commentary.md"
)

# (slug, unique substring to split BEFORE — first match wins in order)
TRANSCRIPT_SECTIONS: dict[str, list[tuple[str, str]]] = {
    "civ-24": [
        ("opening-frame", "okay uh good morning today we are doing Jesus"),
        (
            "historical-jesus",
            "let's look at first what we know about the historical Jesus",
        ),
        (
            "biblical-jesus",
            "now that we looked at the Historical Jesus let's look at the biblical Jesus",
        ),
        (
            "original-sin-atonement",
            "the biggest problem is the idea of atonement and original sin",
        ),
        (
            "jews-killed-jesus",
            "the Bible says very explicitly at times that it was the Jews who killed Jesus",
        ),
        (
            "jerusalem-context",
            "before I talk about Jesus I want to talk about the historical circumstance",
        ),
        ("gnostic-layers", "today we call these new religions narcissism"),
        (
            "gospel-of-thomas",
            "Gospel of Thomas which we recently discovered",
        ),
        (
            "martyrdom-paul-preview",
            "if Jesus himself was a gnostic if this is what he taught",
        ),
    ],
    "civ-25": [
        ("opening-paradox", "okay good morning um so last class we talked about"),
        (
            "jesus-christianity-paradox",
            "the kingdom of God is within us",
        ),
        (
            "paul-acts-frame",
            "now let's talk about the life in Times of Paul",
        ),
        ("paul-biography", "who is Paul we actually know very little"),
        (
            "faith-circumcision",
            "through faith in Jesus you will achieve salvation",
        ),
        (
            "james-conflict",
            "James the just hears about this from all his Jewish friends",
        ),
        ("acts-rome-ending", "when we come into Rome Paul was allowed"),
        (
            "paul-spy-thesis",
            "but I believe he was a spy for the Roman Empire",
        ),
    ],
    "civ-26": [
        ("opening-monotheism", "okay so good morning uh we are doing monotheism today"),
        ("christian-tradition", "let's look at the Christian tradition"),
        (
            "lecture-reconstruction",
            "as we discuss in our class historically that's not what happened",
        ),
        ("pauline-triumph", "why is it that Paul's Church"),
        (
            "constantine-nicaea",
            "eventually emerged an emperor named Constantine and he had fought",
        ),
        ("godhead-equation", "this is called The godhead all right"),
        (
            "monotheism-modernity",
            "these three new ideas are capitalism science and the nation state",
        ),
    ],
    "civ-27": [
        ("opening-augustine", "okay good morning um so we are doing Augustine today"),
        ("end-of-history", "call the end of History this is a concept"),
        ("rome-sack-crisis", "in 410 Rome is sacked and this is a problem"),
        ("city-of-god", "he writes a book called city of God"),
        ("confessions-eden", "we are going to look at two major works of um Augustine"),
        ("lucretia-obedience", "he talks about Lu lucrecia lucrecia"),
        (
            "dark-ages-eastward",
            "from Arabia will come a new religious moov called Islam",
        ),
    ],
    "civ-28": [
        ("source-scarcity", "okay good morning um so we are doing Muhammad"),
        (
            "abraham-family",
            "Christians Jews and Arabs are all one big family why because in the Bible",
        ),
        (
            "hadith-traditional",
            "let's go over what is traditionally understood about Muhammad",
        ),
        (
            "revolutionary-analogies",
            "the first is from 1850 to 1864 in China there's something called the typing Rebellion",
        ),
        (
            "arabia-innovation-zone",
            "in 600 CE the hotbed of innovation was actually here in the araban peninsula",
        ),
        (
            "jihad-land-promise",
            "therefore we must fight a Jihad to take it back because that is God's will",
        ),
        (
            "muhammad-unification",
            "Muhammad was a revolutionary who wanted to overthrow the social order",
        ),
        (
            "whitewashing-close",
            "why don't we know any of this why isn't this hot in history books",
        ),
    ],
}

# chapter_id -> list of 8 anchor slugs for Major Claims rows 1-8
CLAIM_REFS: dict[str, list[str]] = {
    "civ-24": [
        "#historical-jesus",
        "#historical-jesus",
        "#biblical-jesus",
        "#original-sin-atonement",
        "#jews-killed-jesus",
        "#gnostic-layers",
        "#gospel-of-thomas",
        "#martyrdom-paul-preview",
    ],
    "civ-25": [
        "#jesus-christianity-paradox",
        "#paul-biography",
        "#faith-circumcision",
        "#paul-acts-frame",
        "#acts-rome-ending",
        "#paul-spy-thesis",
        "#paul-spy-thesis",
        "#faith-circumcision",
    ],
    "civ-26": [
        "#christian-tradition",
        "#lecture-reconstruction",
        "#constantine-nicaea",
        "#godhead-equation",
        "#godhead-equation",
        "#monotheism-modernity",
        "#monotheism-modernity",
        "#monotheism-modernity",
    ],
    "civ-27": [
        "#opening-augustine",
        "#end-of-history",
        "#rome-sack-crisis",
        "#city-of-god",
        "#confessions-eden",
        "#lucretia-obedience",
        "#dark-ages-eastward",
        "#dark-ages-eastward",
    ],
    "civ-28": [
        "#source-scarcity",
        "#abraham-family",
        "#revolutionary-analogies",
        "#arabia-innovation-zone",
        "#arabia-innovation-zone",
        "#muhammad-unification",
        "#jihad-land-promise",
        "#whitewashing-close",
    ],
}

PART_CLAIM_REFS: dict[str, list[str]] = CLAIM_REFS  # same mapping for part tables


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
        pattern = (
            rf"(\| {i} \|[^\n]+\| )`?{chapter_id}-transcript\.md:32`?"
        )
        text, n = re.subn(pattern, rf"\1{new_ref}", text, count=1)
        if n == 0 and f"{chapter_id}-transcript.md{anchor}" not in text:
            raise ValueError(f"Row {i} not updated in {path}")
    if "analysis_depth: seed" in text:
        text = text.replace("analysis_depth: seed", "analysis_depth: layer2_drafted")
    path.write_text(text, encoding="utf-8")
    print(f"patched commentary: {path.relative_to(ROOT)}")


def update_part_commentary() -> None:
    text = PART_COMMENTARY.read_text(encoding="utf-8")
    for chapter_id, refs in PART_CLAIM_REFS.items():
        for i, anchor in enumerate(refs, start=1):
            pattern = (
                rf"(\| {i} \|[^\n]+\| )`:32`"
            )
            # Only within civ-NN block — match per chapter section
            section_pat = (
                rf"(### {chapter_id}\n\n.*?)(\| {i} \|[^\n]+\| )`:32`"
            )
            text, n = re.subn(
                section_pat,
                rf"\1\2`{anchor}`",
                text,
                count=1,
                flags=re.DOTALL,
            )
            if n == 0 and f"| `{anchor}`" not in text:
                raise ValueError(f"Part commentary row {chapter_id} #{i} not updated")
    # build notes
    text = text.replace(
        "- Pin-cite megagraphs `civ-24`–`28` (Phase 1 used `:32` line refs).",
        "- Pin-cite `civ-24`–`28` (2026-06-09): transcript `###` sections + `#anchor` L2 refs.",
    )
    PART_COMMENTARY.write_text(text, encoding="utf-8")
    print(f"patched: {PART_COMMENTARY.relative_to(ROOT)}")


def update_readiness() -> None:
    path = ROOT / "docs/routes/volume-i-parts/PART-05-HYBRID-READINESS.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "**Partial** — 8 L2 claims each; **`analysis_depth: seed`**; all L2 refs **`civ-*-transcript.md:32`** (single megagraph; **no `###` transcript sections**)",
        "**Met** — 8 L2 claims each; transcript `###` sections + `#anchor` refs (pin-cite prep 2026-06-09); chapter `analysis_depth: layer2_drafted`",
    )
    text = text.replace(
        "**Pin-cite debt:** **All five** chapters — Layer 2 refs overwhelmingly `civ-*-transcript.md:32`; transcripts have **no `###` section anchors**.",
        "**Pin-cite debt:** **Cleared** (2026-06-09) — `civ-24`–`28` transcripts sectioned; chapter + Part L2 refs use `#anchor` slugs.",
    )
    path.write_text(text, encoding="utf-8")
    print(f"patched: {path.relative_to(ROOT)}")


def main() -> None:
    for cid in TRANSCRIPT_SECTIONS:
        patch_transcript(cid)
        update_chapter_commentary(cid)
    update_part_commentary()
    update_readiness()
    print("part_v_pin_cite_prep: done")


if __name__ == "__main__":
    main()
