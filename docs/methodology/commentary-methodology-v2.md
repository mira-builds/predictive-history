# Commentary Methodology v2

**Status:** Active SSOT for ph-civ commentary rebuild (2026-06).  
**Supersedes:** [commentary-canvas.md](commentary-canvas.md) (v1 hybrid Part model), thin-chapter + Part apparatus law.

## v1 → v2 breaking changes

| Topic | v1 | v2 |
|-------|----|----|
| Interpretation SSOT | Chapter L0–2 + Part thick | **Chapter L0–6 only** |
| Volume I navigation | Part I–X + `part_tour` | **Interwoven spine** + [`volume-i-spine-tour.json`](../data/routes/volume-i-spine-tour.json) + [`volume-i-companions.json`](../data/weave/volume-i-companions.json) |
| GB/SH commentaries | `stub_routed_to_part` | **Full chapter commentaries** |
| Bibliography | Part-scoped bib files | **L4/L6 per chapter** |
| Pin-cite | Part ↔ chapter sync | **Chapter only**; grandfather existing `#anchor` rails |
| Progress | `PART-*-HYBRID-READINESS` | **`commentary_maturity`** on [`predictive-history-index.json`](../docs/predictive-history-index.json) |
| `analysis_depth` | seed / slimmed / stub | **`commentary_maturity`** ladder |

---

## 1. Purpose and non-goals

**Purpose:** Rules for writing and rebuilding **interpretation-bearing** chapter commentaries while **transcripts remain fidelity-bearing** ([`book/volume-ii/README.md`](../docs/archive/two-volume-ph-civ-apo-deprecated.md)).

**SSOT hierarchy:**

1. Lecture **transcript** (verbatim body; guardrails in commentary only)
2. Chapter **commentary** (L0–6 + Project Canvas)
3. **Card** ([`data/cards/`](../data/cards/)) — placement, posture, limits (doorway, not claim tables)
4. **Routes / patterns / corridors** — widened interpretation after chapter floor is stable

**Non-goals:**

- Finished scholarship or quotation-grade live operational analysis (especially ph-apo)
- Rewriting transcript bodies to match commentary guardrails
- Replacing cards with commentary claim tables
- Reviving Volume I **Part apparatus** as synthesis authority

Commentaries remain **open canvases** (`canvas_status: open`) until explicit review promotion.

---

## 2. Authority stack (source-lattice)

Align with [source-lattice.md](source-lattice.md) — **no Part apparatus step**.

```text
README / card → transcript → chapter commentary (L0→6) → corridors / routes / patterns
```

Do not widen to routes or present-day application before L0–2 are pinned to the transcript.

---

## 3. Chapter-only authority; Parts deprecated

| Artifact | v2 status |
|----------|-----------|
| `*-commentary.md` per chapter | **SSOT** — full L0–6 + Project Canvas |
| `docs/routes/volume-i-parts/part-*-commentary.md` | **Deprecated** — archive; extract then freeze |
| `gb-*` / `sh-*` chapter files | Full commentaries; **no** permanent `stub_routed_to_part` |
| Interwoven reader | Human reading order SSOT |
| [`data/weave/volume-i-companions.json`](../data/weave/volume-i-companions.json) | Machine weave SSOT (gb/sh @ civ hosts) |

See [archive/parts-v1-hybrid.md](archive/parts-v1-hybrid.md).

---

## 4. Layer model (L0–6 + Canvas)

| Layer | Name | Rules |
|-------|------|--------|
| **L0** | Metadata & quick reference | One-sentence thesis, focus, fidelity confidence |
| **L1** | Neutral summary | Paraphrase only; no evaluation |
| **L2** | Source-backed claims | Pin-cite table: claim, `#anchor`, strength, confidence |
| **L3** | Predictions & falsifiers | Required; see §5 |
| **L4** | Counter-readings | Sourced alternatives |
| **L5** | Synthesis & cross-volume links | Patterns + corridor **links** (see §9) |
| **L6** | Open issues | Review-oriented follow-ups |
| **Canvas** | Project leverage | Patterns, volume role, bounded application |

Template: `lectures/civilization/civ-XX/civ-XX-commentary.md` (body); v2 frontmatter uses `scaffold_version: ph_civ_commentary_canvas_v2`.

---

## 5. Falsifier discipline (L3)

### Row schema

| Column | Content |
|--------|---------|
| Prediction | Verbatim or tight paraphrase of lecture forecast |
| Strength | E (explicit) / SI (strong implied) / C (contextual) |
| Falsifier Criteria | Observable event, date boundary, or scholarly consensus that would weaken the claim |
| Review Date | When to revisit |
| Current Status | Pending / Partially confirmed / Weakened / Falsified / N/A |
| Notes | Optional wire-verify receipt or `verify:` pointer |

### Prediction classes

1. **Historical** — falsifier = archival / scholarly counter-evidence  
2. **Structural** — falsifier = counterexample civilization or period  
3. **Event-timed** — falsifier = date passed + outcome (ph-apo: mandatory where lecture forecasts)  
4. **Meta-pattern** — falsifier = later chapter contradicts series framing  

**ph-apo:** Event-timed rows default `Pending`; maturity cap `l3_falsifiers` until wire-verify where applicable.

---

## 6. Series templates and maturity ceilings

| Family | `template_family` | Notes |
|--------|-------------------|--------|
| Civilization / Great Books (Vol I) | `civilization-commentary`, `great-books-commentary` | Full L0–6 |
| Apocalypse lanes | `world-war-strategic-commentary` | Full L0–6; L3 emphasizes actors, incentives, falsifiers |

**Ceilings without wire-verify:**

- `geo-*`, provisional `gt-*`: max `l3_falsifiers`
- `sh-*`, `essays`: max `l6_drafted` only after transcript fidelity confirmed

---

## 7. Maturity ladder

Frontmatter:

- `scaffold_version: ph_civ_commentary_canvas_v2`
- `commentary_maturity:` one of:

| Maturity | Meaning |
|----------|---------|
| `scaffold` | Headings present; tables empty or TBD |
| `l2_pinned` | L0–2 complete with `#anchor` cites |
| `l3_falsifiers` | L3 populated (≥1 row or explicit N/A) |
| `l6_drafted` | L4–6 + canvas drafted |
| `in_review` | Ready for operator review |
| `calibration` | Pilot anchor (e.g. civ-07) |

Optional: `migration_source`: `upgrade` | `regen` | `extracted_from_part`

**Legacy map:** `seed`→`scaffold`; `layer2_drafted`→`l2_pinned`; `layer2_slimmed`→upgrade required; `stub_routed_to_part`→obsolete.

---

## 8. Pin-cite policy

- **Grandfather** existing transcript `###` rails and [`data/pin-cite/volume-i-anchors.yaml`](../data/pin-cite/volume-i-anchors.yaml) on upgrade-in-place.
- L2 references use `transcript.md#anchor` (not blanket line numbers after anchor sweep).
- Re-slug only on **full chapter rewrite**; document anchor changes in L6.

See [PIN-CITE-DISCIPLINE.md](PIN-CITE-DISCIPLINE.md) — chapter-only authority (Part sync rules retired).

---

## 9. L5 vs corridors and patterns

**L5** — chapter-local synthesis; required table linking to [`data/patterns.json`](../data/patterns.json) IDs where applicable:

| pattern_id | How this chapter supports or limits it |
|------------|----------------------------------------|

**Corridors** ([`book/corridors/`](../book/corridors/)) — multi-chapter arcs.

**Decision tree:**

- Single-chapter placement → L5 only  
- Chapter is on a named corridor spine → L5 must include **one link** to corridor doc; do **not** paste full corridor thesis  
- Pattern reuse → cite pattern ID in L5 with limits from card/commentary  

---

## 10. Migration recipe (Part → chapter)

Script: [`scripts/extract_part_section_to_chapter.py`](../scripts/extract_part_section_to_chapter.py)

1. Input: deprecated Part commentary path, target `source_id`  
2. Extract `### {source_id}` or `### gb-NN` / `### sh-NN` section  
3. Map: prediction tables → L3; counter-readings → L4; bib → L6 / canvas  
4. Merge into chapter file; preserve L0–2 if `l2_pinned`  
5. Set `migration_source: extracted_from_part`  

### Per-chapter acceptance checklist

- [ ] No unique claims remain only in Part file  
- [ ] L3 has ≥1 row or explicit N/A  
- [ ] Part pointer frontmatter removed or marked deprecated  
- [ ] Pin-cite anchors unchanged or documented in L6  
- [ ] `commentary_maturity` updated  
- [ ] Card **Limits of the Frame** aligned if L3/L4 tightened limits  
- [ ] Chapter README uses 3-step lattice (no Part apparatus)  
- [ ] `predictive-history validate` passes

### Tiered rebuild strategy

| Starting state | Action |
|----------------|--------|
| `l2_pinned` civ (60) | Upgrade in place — add L3–6 |
| `layer2_slimmed` | Expand to full L0–6 |
| `stub_routed_to_part` | Extract Part section → full chapter |
| `seed` | Regen v2 scaffold ([`scripts/regenerate_commentary_v2_scaffold.py`](../scripts/regenerate_commentary_v2_scaffold.py)) |
| ph-apo provisional | v2 scaffold; cap `l3_falsifiers` until wire-verify |

Wave order: civ → gb → Vol I gt → geo → sh → gt apo → essays.

---

## 11. Weave registry and spine tour

**Weave SSOT:** [`data/weave/volume-i-companions.json`](../data/weave/volume-i-companions.json)  
- `by_civ_host`: civ → woven gb/sh companions  
- `by_companion`: gb/sh → anchor civ  
- Deprecated redirect: [`data/parts/volume-i-parts.deprecated.json`](../data/parts/volume-i-parts.deprecated.json)

**Spine tour:** [`data/routes/volume-i-spine-tour.json`](../data/routes/volume-i-spine-tour.json)  
- Replaces `part-boundary-tour.json`  
- Stops = `source_id` at interwoven spine boundaries (not Part IDs)

**LLM mode:** `spine_tour` in [`llm-experience.json`](../data/llm-experience.json) (replaces `part_tour`).

---

## 12. Cards alignment

- Cards are **not** wiped with commentary rebuild  
- When L3/L4 tightens limits, update card **Limits of the Frame** in the same slice  
- Cards do not duplicate L2 claim tables  

---

## 13. Operator theory (calibration on civ-07)

Frozen after operator calibration workshop on **civ-07**. Until frozen, treat blocks below as **TODO (operator)**.

### TODO (operator): Governing inversions

What each commentary must extract as the lecture's deepest move (see [ph-civ-comment-proof-objects](../../.cursor/skills/ph-civ-comment-proof-objects/SKILL.md)).

### TODO (operator): Pressure grammar

How L2 rows name mechanisms vs anecdotes; minimum claim density per chapter.

### TODO (operator): Disproportion rule

When falsifiers outweigh counter-readings in L3 vs L4 weight.

### TODO (operator): Volume I vs II voice

Discovery (civ) vs application (apo) boundaries for L5 and canvas.

### TODO (operator): Pattern linkage

When `data/patterns.json` IDs are mandatory in L5 vs canvas-only.

### Calibration anchor: civ-07

Use [`lectures/civilization/civ-07/civ-07-commentary.md`](../../lectures/civilization/civ-07/civ-07-commentary.md) as the reference v2 upgrade before scaling waves.

**Proof-object gate for `l2_pinned`:** L0 thesis + ≥2 L2 claims must reflect governing inversion + two concrete historical examples bearing argumentative weight.

---

## 14. Rebuild waves and public continuity

- Archive v1 commentary snapshots under [`docs/archive/commentary-v1/`](archive/commentary-v1/) (git tag per wave optional)  
- Chapter README may show `commentary_maturity` badge  
- Do not publish to `mira-builds/predictive-history` mid-wave without explicit operator publish  
- Progress: `ph-civ commentary status` + [`predictive-history-index.json`](../docs/predictive-history-index.json)

**Phased slices:** Outline (this doc) → A (pilot + validate) → B (ledger) → C (Parts sunset) → D (tiered waves).

---

## Appendix A: Parts dependency inventory (Slice C)

Grep targets before declaring Parts sunset complete:

- `part_tour`, `volume-i-parts.json`, `part-boundary-tour`, `Part apparatus`  
- `part_commentary_path`, `part_bibliography_path`  
- `validate_volume_i_parts`, `PART-*-HYBRID`  
- `study-edition.md` Part column  
- `scaffold_part_doorway.py`, `part_*_pin_cite_prep.py`  

---

## Appendix B: JSON schemas (machine surfaces)

### `volume-i-companions.json`

```json
{
  "schema_version": 1,
  "spine_ssot": "docs/archive/two-volume-reader-order-interwoven.md",
  "by_civ_host": {
    "civ-07": {
      "great_books": [{"gb_id": "gb-02", "role": "interwoven"}],
      "secret_history": [],
      "corridor_touchpoints": []
    }
  },
  "by_companion": {
    "gb-02": {"anchor_civ": "civ-07", "kind": "great-books"}
  }
}
```

### `volume-i-spine-tour.json`

```json
{
  "tour_id": "volume_i_spine_tour",
  "registry": "data/weave/volume-i-companions.json",
  "related_seed_id": "ten_route_spine_seed",
  "stops": [
    {"source_id": "civ-01", "label": "Dawn of agriculture", "corridor_id": null}
  ]
}
```

---

## Related docs (redirects)

| Doc | Role |
|-----|------|
| [commentary-canvas.md](commentary-canvas.md) | v1 — superseded |
| [PIN-CITE-DISCIPLINE.md](PIN-CITE-DISCIPLINE.md) | Chapter-only pin-cite |
| [source-lattice.md](source-lattice.md) | Reading discipline (update Part step out) |
| [archive/parts-v1-hybrid.md](archive/parts-v1-hybrid.md) | Parts retirement record |
