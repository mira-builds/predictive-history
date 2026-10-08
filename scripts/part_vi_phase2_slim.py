#!/usr/bin/env python3
"""Part VI Phase 2: slim civ-29–34 to Layer 0–2 + Part apparatus pointer."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOL2 = ROOT / "book" / "volume-ii"

CHAPTERS: dict[str, dict[str, str]] = {
    "civ-29": {
        "part_blurb": "Augustine rebuttal, Commedia structure, Mary/paradox, imagination cosmology",
        "open_q1": "Dante-as-origin of Renaissance/Reformation/science — lecture hypothesis only.",
        "open_q2": "Augustine vs Dante contrast compresses medieval theology field.",
    },
    "civ-30": {
        "part_blurb": "Virgil/Homer displacement, unreliable guide, Beatrice love, poetic surgery",
        "open_q1": "Dido/Cato/Statius readings — textual review before complete.",
        "open_q2": "Protestant/scientific Revolution links bounded until later Parts.",
    },
    "civ-31": {
        "part_blurb": "Second-semester oceanic-currents model + prediction grammar (date-sensitive)",
        "open_q1": "Live geopolitics — stamp lecture date; not durable forecast.",
        "open_q2": "Oceanic-currents metaphor ≠ inevitability proof.",
    },
    "civ-32": {
        "part_blurb": "Rome recap, citizenship, Caracalla rupture, America analogy",
        "open_q1": "Rome-America structural analogy — not prediction proof.",
        "open_q2": "American war/civil-violence forecast — external verify.",
    },
    "civ-33": {
        "part_blurb": "Byzantine Roman survival, Nicaea, bureaucracy, lecture refutation frame",
        "open_q1": "Scholarly consensus vs lecture refutation — keep labeled.",
        "open_q2": "Pagan-Christian contrast is worldview shorthand.",
    },
    "civ-34": {
        "part_blurb": "Holy Roman fiction, Charlemagne, Church coopt, Augustine blueprint close",
        "open_q1": "Useful-fiction frame vs institutional HRE history.",
        "open_q2": "Rome–Constantinople schism compression.",
    },
}

README_TEMPLATE = """# {title}

This chapter folder is a public study doorway for {cid}.

## Start Here

Use this folder when someone shares the GitHub chapter link in a YouTube comment or an LLM chat. Start with the transcript, then use the commentary canvas and orientation card to keep the reading bounded.

## Source-Lattice Reading Order

Treat this chapter folder as a small source-lattice:

1. Doorway - this README tells you what the packet is and what limits apply.
2. Primary source floor - read the transcript and public source capture first.
3. Chapter commentary - thin Layer 0-2 pin-cites in the companion commentary file.
4. Part apparatus - [Part VI commentary](../../../docs/routes/volume-i-parts/part-06-medieval-imagination-commentary.md) and [Part VI bibliography](../../../docs/routes/volume-i-parts/part-06-medieval-imagination-bibliography.md) for cross-chapter synthesis and external sources.
5. Public card - orientation payload after the chapter and Part floors are open.
6. Widened interpretation - corridors and bridges only after the above are stable.

## Files

- [Transcript]({cid}-transcript.md)
- [Commentary canvas (thin)]({cid}-commentary.md)
- [Part VI commentary](../../../docs/routes/volume-i-parts/part-06-medieval-imagination-commentary.md#{cid})
- [Part VI bibliography](../../../docs/routes/volume-i-parts/part-06-medieval-imagination-bibliography.md)
- [Public card](../../../data/cards/{cid}.md)

## Review Status

in_review. Do not treat provisional transcript text, named claims, quotations, or current-event predictions as final until review is complete.

## LLM Prompt

Paste this folder link into ChatGPT, Claude, or Grok and ask:

> Guide me through this chapter folder as a public study packet. Start with the transcript, then use the thin chapter commentary (Layer 0-2 pin-cites), then Part VI commentary and bibliography for cross-chapter synthesis. Keep provisional claims bounded and separate lecture representation from verification.
>
> Use a source-lattice reading order: README first, transcript second, chapter commentary third, Part apparatus fourth, public card fifth, and broader interpretation only after those floors are stable.

## Guardrails

This folder represents the public lecture material and companion study apparatus. It is not a private note dump, not an endorsement layer, and not a substitute for source review.
"""


def slim_commentary(cid: str) -> None:
    meta = CHAPTERS[cid]
    path = VOL2 / cid / f"{cid}-commentary.md"
    text = path.read_text(encoding="utf-8")
    if "## Part apparatus" in text and "## Layer 3" not in text:
        print(f"skip commentary (already slim): {path.relative_to(ROOT)}")
        return
    m = re.search(r"\n## Layer 3\b", text)
    if not m:
        raise ValueError(f"No Layer 3 marker in {path}")
    head = text[: m.start()].rstrip() + "\n"
    tail = f"""
---

## Part apparatus

Cross-chapter synthesis, predictions, external counter-readings, and bibliography for Part VI live in the Part files:

- [Part VI commentary](../../../docs/routes/volume-i-parts/part-06-medieval-imagination-commentary.md#{cid}) — {meta["part_blurb"]}
- [Part VI bibliography](../../../docs/routes/volume-i-parts/part-06-medieval-imagination-bibliography.md)

Layer 0–2 above remain the transcript pin-cite floor for this chapter.

---

## Project Canvas (chapter-local)

### Open Questions

- {meta["open_q1"]}
- {meta["open_q2"]}

### Build Notes

- Cross-chapter work: use Part apparatus; do not duplicate Part bibliography here.
- Phase 2 slim (2026-06-09): Layers 3–6 moved to Part commentary.
"""
    text = head + tail
    if "part_commentary_path:" not in text:
        text = text.replace(
            "scaffold_version: ph_civ_commentary_canvas_v1\n",
            "scaffold_version: ph_civ_commentary_canvas_v1\n"
            "part_commentary_path: ../../../docs/routes/volume-i-parts/"
            "part-06-medieval-imagination-commentary.md#"
            f"{cid}\n"
            "part_bibliography_path: ../../../docs/routes/volume-i-parts/"
            "part-06-medieval-imagination-bibliography.md\n",
            1,
        )
    path.write_text(text, encoding="utf-8")
    print(f"slim commentary: {path.relative_to(ROOT)}")


def update_readme(cid: str) -> None:
    readme = VOL2 / cid / "README.md"
    title_match = re.search(
        r'^title:\s*"(.+)"',
        (VOL2 / cid / f"{cid}-commentary.md").read_text(encoding="utf-8"),
        re.M,
    )
    title = title_match.group(1) if title_match else cid
    readme.write_text(README_TEMPLATE.format(title=title, cid=cid), encoding="utf-8")
    print(f"updated README: {readme.relative_to(ROOT)}")


def main() -> None:
    for cid in CHAPTERS:
        slim_commentary(cid)
        update_readme(cid)
    print("part_vi_phase2_slim: done")


if __name__ == "__main__":
    main()
