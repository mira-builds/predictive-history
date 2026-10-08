#!/usr/bin/env python3
"""Part V Phase 2: slim civ-24–28 to Layer 0–2 + Part apparatus pointer."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOL2 = ROOT / "book" / "volume-ii"

CHAPTERS: dict[str, dict[str, str]] = {
    "civ-24": {
        "part_blurb": "Jesus source layers, Gnostic martyrdom, Yahwist clash, Paul preview",
        "open_q1": "Historical vs biblical vs Gnostic Jesus — source-layer discipline.",
        "open_q2": "Original sin vs Part IV Yahwist grammar; Pilate/Roman authority.",
    },
    "civ-25": {
        "part_blurb": "Pauline hinge, Gentile opening, spy thesis (bounded in Part commentary)",
        "open_q1": "Paul-as-spy thesis — lecture hypothesis only.",
        "open_q2": "Tolstoy Lens adjunct lives in Part `civ-25` section (not chapter body).",
    },
    "civ-26": {
        "part_blurb": "Constantine, Nicaea, godhead monotheism, empire-doctrine weld",
        "open_q1": "Imperial history vs lecture philosophy of closed reality-order.",
        "open_q2": "Money/science/nation-state extensions — verify against external sources.",
    },
    "civ-27": {
        "part_blurb": "Augustine, City of God, obedience doctrine, Church out of history",
        "open_q1": "Lucretia/obedience passages — text vs institutional reading.",
        "open_q2": "Eastward dissent after Rome's sack — bibliography depth.",
    },
    "civ-28": {
        "part_blurb": "Muhammad, Islam, jihad/revolution framing, imperial whitewash",
        "open_q1": "Muhammad source scarcity — analogies are not proof.",
        "open_q2": "Jihad framing — Islamic-studies review before `complete`.",
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
4. Part apparatus - [Part V commentary](../../../docs/routes/volume-i-parts/part-05-christianity-and-islam-commentary.md) and [Part V bibliography](../../../docs/routes/volume-i-parts/part-05-christianity-and-islam-bibliography.md) for cross-chapter synthesis and external sources.
5. Public card - orientation payload after the chapter and Part floors are open.
6. Widened interpretation - corridors and bridges only after the above are stable.

## Files

- [Transcript]({cid}-transcript.md)
- [Commentary canvas (thin)]({cid}-commentary.md)
- [Part V commentary](../../../docs/routes/volume-i-parts/part-05-christianity-and-islam-commentary.md#{cid})
- [Part V bibliography](../../../docs/routes/volume-i-parts/part-05-christianity-and-islam-bibliography.md)
- [Public card](../../../data/cards/{cid}.md)

## Review Status

in_review. Do not treat provisional transcript text, named claims, quotations, or current-event predictions as final until review is complete.

## LLM Prompt

Paste this folder link into ChatGPT, Claude, or Grok and ask:

> Guide me through this chapter folder as a public study packet. Start with the transcript, then use the thin chapter commentary (Layer 0-2 pin-cites), then Part V commentary and bibliography for cross-chapter synthesis. Keep provisional claims bounded and separate lecture representation from verification.
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

Cross-chapter synthesis, predictions, external counter-readings, and bibliography for Part V live in the Part files:

- [Part V commentary](../../../docs/routes/volume-i-parts/part-05-christianity-and-islam-commentary.md#{cid}) — {meta["part_blurb"]}
- [Part V bibliography](../../../docs/routes/volume-i-parts/part-05-christianity-and-islam-bibliography.md)

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
            "part-05-christianity-and-islam-commentary.md#"
            f"{cid}\n"
            "part_bibliography_path: ../../../docs/routes/volume-i-parts/"
            "part-05-christianity-and-islam-bibliography.md\n",
            1,
        )
    path.write_text(text, encoding="utf-8")
    print(f"slim commentary: {path.relative_to(ROOT)}")


def update_readme(cid: str) -> None:
    readme = VOL2 / cid / "README.md"
    title_match = re.search(r'^title:\s*"(.+)"', (VOL2 / cid / f"{cid}-commentary.md").read_text(encoding="utf-8"), re.M)
    title = title_match.group(1) if title_match else cid
    readme.write_text(README_TEMPLATE.format(title=title, cid=cid), encoding="utf-8")
    print(f"updated README: {readme.relative_to(ROOT)}")


def main() -> None:
    for cid in CHAPTERS:
        slim_commentary(cid)
        update_readme(cid)
    print("part_v_phase2_slim: done")


if __name__ == "__main__":
    main()
