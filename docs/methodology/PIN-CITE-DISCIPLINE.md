# Pin-cite discipline — Volume I hybrid apparatus

**Scope:** WORK-layer coherence for `ph-civ` Part commentary + chapter Layer-2 claim tables + lecture transcripts. Not external legal citation or public `ph-civ` ship copy.

**Goal:** A general reader can move **Part overview → chapter claims → transcript passage** without scrolling a megagraph or trusting a blanket `:32`.

---

## Two layers (both required for “Met”)

| Layer | Artifact | What it does |
|-------|----------|----------------|
| **1. Transcript rails** | `### kebab-slug` headings in `*-transcript.md` | Breaks lecture wall into named movements; slugs are human-readable handles |
| **2. L2 pin-cites** | `civ-NN-transcript.md#slug` in chapter + Part claim tables | Ties each claim row to one movement, not a line number |

**Invariant:** Verbatim body text is not rewritten during pin-cite prep — only structural `###` inserts (and optional inline ` ### slug` normalization to own lines).

---

## Slug rules

- **Format:** `kebab-case`, ASCII, stable across Part and chapter tables (`#gilgamesh-pyramid-dialectic`, not `#section-4`).
- **Semantics:** Name the *argument neighborhood* (mechanism, close-read, handoff), not ASR noise.
- **Count:** Typically **6–10** sections per civ chapter; **8** when aligned to the standard L2 claim table.
- **Order:** Sections follow **lecture order**; script splits on first unique phrase match per slug (see `scripts/part_*_pin_cite_prep.py`).
- **Duplicates:** Reuse the same `#anchor` on multiple claim rows when one movement supports several claims (Part IV/V pattern).

---

## Sync rules (Part ↔ chapter)

1. **Part commentary** claim tables are SSOT for Part-facing refs once Phase 1+ claim authoring exists.
2. **Chapter commentary** Layer-2 rows must use the **same `#anchor` vocabulary** as the Part section for that chapter (no chapter-only line numbers left behind after a sweep).
3. **Great Books:** GB Part sections already use `#anchor` on `gb-NN-transcript.md`; civ chapters at the weave host follow the same discipline.
4. After refresh, set `analysis_depth: layer2_drafted` on chapter commentaries when rows were `:32` or bare line refs.

---

## Tiered debt (when full sectioning is optional)

| Tier | Ref shape | Reader experience | Action |
|------|-----------|-------------------|--------|
| **A — Met** | `#anchor` | Jump to movement by name | Done (Parts I–X hybrid pilot 2026-06-10; manifest SSOT [`volume-i-anchors.yaml`](../data/pin-cite/volume-i-anchors.yaml)) |
| **B — Interim** | `:32-35` line ranges | Better than blanket `:32`; still line-literacy | None in Part II civ spine after uplift |
| **C — Debt** | `:32` blanket or orphan line | “Somewhere in this file” | Section + anchor refresh (priority sweep) |

---

## Prep workflow (idempotent)

1. Draft or verify **8 claim rows** (chapter or Part table).
2. Choose **unique split phrases** per slug from the transcript (grep-first; no guessing).
3. Add or update manifest rows, then run `part_pin_cite_from_manifest.py --part NN` (or part-scoped prep script).
4. Run `python scripts/validate_pin_cite.py` and `python scripts/validate_volume_i_parts.py`.
5. Update the Part `PART-NN-HYBRID-READINESS.md` pin-cite row when the part clears.

**Do not:** substitute summary for verbatim in transcripts; invent anchors without a phrase match; mix Part slug names with different chapter slugs for the same movement.

---

## Scripts (repo)

| Script | Parts / chapters |
|--------|------------------|
| `scripts/part_i_pin_cite_prep.py` | `civ-01`–`06` (Part I dawn arc) |
| `scripts/part_iv_pin_cite_prep.py` | `civ-19`–`23` |
| `scripts/part_v_pin_cite_prep.py` | `civ-24`–`28` |
| `scripts/part_ii_iii_pin_cite_sweep.py` | `civ-11`, `civ-13`–`17` (low-debt sweep) |
| `scripts/part_ii_tier_b_uplift.py` | `civ-07`–`10`, `civ-12` (Tier-B → Tier A) |
| `scripts/part_vi_pin_cite_prep.py` | `civ-29`–`34` |
| `scripts/part_pin_cite_from_manifest.py` | Manifest-driven apply (`--part 01`–`10`, `--chapter civ-NN`) |
| `scripts/validate_pin_cite.py` | Manifest ↔ transcript `###` + L2 ref checks |
| `scripts/part_vii_pin_cite_prep.py` | `civ-35`–`41` |
| `scripts/part_viii_pin_cite_prep.py` | `civ-42`–`50` |
| `scripts/part_ix_pin_cite_prep.py` | `civ-51`–`53` |
| `scripts/part_x_pin_cite_prep.py` | `civ-54`–`60` |
| `scripts/part_i_pin_cite_prep.py` | `civ-01`–`06` |
| `scripts/part_hybrid_slim.py` | Phase 2 slim (`--part 01|07|08|09|10`) |

---

## Ceiling (honest limits)

- ASR transcripts → anchors mark **argument neighborhoods**, not word-perfect quotes.
- External-verify and public copy still need their own passes; pin-cite is **internal reader-orientation**, not merge authority.

**Readiness pointers:** [Part I](../docs/routes/volume-i-parts/PART-01-HYBRID-READINESS.md) · [Part III](../docs/routes/volume-i-parts/PART-03-HYBRID-READINESS.md) · [Part IV](../docs/routes/volume-i-parts/PART-04-HYBRID-READINESS.md) · [Part V](../docs/routes/volume-i-parts/PART-05-HYBRID-READINESS.md) · [Part VI](../docs/routes/volume-i-parts/PART-06-HYBRID-READINESS.md) · [Part VII](../docs/routes/volume-i-parts/PART-07-HYBRID-READINESS.md) · [Part VIII](../docs/routes/volume-i-parts/PART-08-HYBRID-READINESS.md) · [Part IX](../docs/routes/volume-i-parts/PART-09-HYBRID-READINESS.md) · [Part X](../docs/routes/volume-i-parts/PART-10-HYBRID-READINESS.md) · [manifest index](./pin-cite-manifest-index.md)
