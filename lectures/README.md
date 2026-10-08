# Lectures

Reserved root namespace for Predictive History **lecture** chapter packets (video-sourced transcript bodies).

Repo path: **`lectures/`** at the repository root (sibling to [`essays/`](../essays/README.md), [`commentaries/`](../commentaries/README.md), [`interviews/`](../interviews/README.md); deprecated [`book/`](../book/) tombstone; [`ph-civ/`](../ph-civ/README.md)).

## Series partitions

| Folder | Catalog `series` | Typical `source_id` prefix |
| --- | --- | --- |
| [`civilization/`](civilization/README.md) | `civilization` | `civ-*` |
| [`great-books/`](great-books/README.md) | `great-books` | `gb-*` |
| [`geo-strategy/`](geo-strategy/README.md) | `geo-strategy` | `geo-*` |
| [`game-theory/`](game-theory/README.md) | `game-theory` | `gt-*` |
| [`secret-history/`](secret-history/README.md) | `secret-history` | `sh-*` |

Canonical lecture packets live under `lectures/<series>/`.

Related: [`docs/migrations/PH-LECTURES-RELOCATION.md`](../docs/migrations/PH-LECTURES-RELOCATION.md) · full hub [`docs/predictive-history-index.md`](../docs/predictive-history-index.md) · lectures slice [`predictive-history-lecture-index.md`](predictive-history-lecture-index.md).

## Transcript pass ladder (sections + turn labeling)

After section rails exist (pass **A** — slug retitle, anchor split, or future per-packet scripts), use the repo-native runbook for classroom Q&A cleanup and turn labeling:

- **Runbook (SSOT):** [`docs/runbooks/ph-transcript-curation.md`](../docs/runbooks/ph-transcript-curation.md)
- **Cursor skill (this repo):** [`.cursor/skills/ph-transcript-curation/SKILL.md`](../.cursor/skills/ph-transcript-curation/SKILL.md) — repo-native; not a mirrored junction skill

**Lecture shapes:** monologue + slug rails (`civ-*`), flat monologue (`geo-*`, many `gt-*`), classroom Q&A with `>>` (`gt-29`, many `gb-*` / `sh-*`). Passes **B / C / D** when dialogue exists; pure monologue often stops at pass **A** + **D**. Commit prefix **`PH-TRANSCRIPT-EDIT:`**. Reference exemplars: `gt-29` (Q&A pilot) · `civ-59` (slug rails).

## Rails everywhere (pass A)

**Tooling:** [`scripts/lecture_section_pass.py`](../scripts/lecture_section_pass.py) · [`scripts/verify_transcript_pin_cites.py`](../scripts/verify_transcript_pin_cites.py)

```bash
python scripts/lecture_section_pass.py audit --strict
python scripts/verify_transcript_pin_cites.py
```

Section maps: [`data/lectures/section-maps/`](../data/lectures/section-maps/). Runbook: [`docs/runbooks/ph-transcript-curation.md`](../docs/runbooks/ph-transcript-curation.md) § Rails everywhere.

| Audit (pass A complete) | Count |
| --- | ---: |
| Title Case rails | **149/149** |
| Pin-cite verifier | green |
| Orphan transcripts (no card) | `gb-11`, `gb-12` |
