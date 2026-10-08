---
part_id: part-07-world-after-rome
plan_status: phase2_slimmed
scaffold_version: ph_civ_part_commentary_v1
template_from: part-06-medieval-imagination (hybrid pilot complete)
inventory_date: 2026-06-09
---

# Part VII Hybrid Apparatus — Readiness Inventory

Planning doc for extending the **Part II–VI hybrid model** (thin chapter + thick Part commentary/bibliography) to **Part VII — The World After Rome** (`civ-35`–`civ-41` + `gb-10` weave @ `civ-41` close).

**Law-discovery question (registry):** How do Viking, Islamic, steppe, and church orders carry Rome's medieval afterlife?

**Spine note:** `spine_slice_warning: false` — contiguous block (`civ-35`→`civ-41`). **Structural seam:** Dante is **off stage** for `civ-35`–`40`; [Homer-to-Dante](../../../data/corridors/homer-to-dante.md) **closes** at `civ-41` with `gb-10` interwoven. Do not reopen the Part VI Dante open (`civ-29`–`30`) here.

**Cross-Part ingress:** [Part VI `civ-34`](./part-06-medieval-imagination-commentary.md#civ-34) Holy Roman fiction → plural world orders (`civ-35`); oceanic-currents bridge from [`civ-31`](./part-06-medieval-imagination-commentary.md#civ-31) still **Pending** Part VII test.

---

## Maturity gate (when to implement)

| Gate | Threshold | Current (2026-06-09) |
|------|-----------|----------------------|
| Chapter Layer 0–2 | All seven chapters have transcript-anchored claims + section/line refs | **Partial** — 6 L2 claims each; `analysis_depth: seed`; refs collapse to single line (`:29`/`:32`) — **no** transcript `###` rails |
| Chapter slimming | Willing to move Layers 3–6 to Part apparatus | **Not met** — full Layers 0–6 on all packets |
| GB weave | Registry `great_books_weave` + Part `### gb-NN` sections | **Partial** — registry `gb-10` @ `civ-41` only; canonical `### gb-10` lives in **Part VI** (Inferno); **no** Part VII `### gb-10` close section |
| Cross-Part bridge | Part VI Dante open → world orders → Dante close | **Partial** — doorway + corridor wired; Part VI prediction rows still **Pending** egress test |
| Validator | `volume_i_parts.py` Part VII README checks | **Not met** — no `commentary_path` / `bibliography_path` in registry |
| Plural-order guardrails | Bibliography + counter-readings for Islam, steppe, church, China claims | **Not met** |

**Recommendation:** Phase 0 inventory **done** (this doc). **Before Phase 1:** run pin-cite prep on `civ-35`–`41` (mirror Part VI `#anchor` discipline). **Pilot wedge (operator pick C):** author Part VII apparatus starting with **`civ-41` + `gb-10` close** before thickening `civ-35`–`40` world-order block.

---

## Chapter inventory (`volume-ii/` packets)

| Chapter | Core thesis (Layer 0) | L2 claims | L3 | analysis_depth | Part section weight (draft) |
|---------|----------------------|-----------|-----|----------------|-----------------------------|
| `civ-35` | Vikings as fifth pillar — raiding, settlement, community/exile | 6 | yes | seed | **Thick** — opens Part law question (plural orders after Rome) |
| `civ-36` | Norse memory — oral vs literary; creativity under civilization | 6 | yes | seed | **Medium** — epistemic/method bridge |
| `civ-37` | Islamic Golden Age — divergence from Europe; Frye empire-literature | 6 | yes | seed | **Thick** — Abbasid cosmopolitan center |
| `civ-38` | China twilight — Warring States, Confucian legitimation, exams | 6 | yes | seed | **Medium** — comparative order (non-Europe stress test) |
| `civ-39` | Genghis Khan — steppe vs agricultural empire; absorption | 6 | yes | seed | **Thick** — Mongol shatter + Eurasian rewiring |
| `civ-40` | Church and empire — Crusades bridge; salvation power; scapegoating | 6 | yes | seed | **Thick** — sets stage for `civ-41` quiet revolution |
| `civ-41` | Dante's quiet revolution — Renaissance hinge; love/imagination | 6 | yes | seed | **Thick** — corridor **close**; `gb-10` weave capstone |

**Legacy wrappers:** `civilization-spine/civ-35`–`civ-39` READMEs exist; all `volume-ii/` READMEs use **4-step** lattice — **no** Part apparatus links.

**Pin-cite debt:** **Cleared** (2026-06-09) — `scripts/part_vii_pin_cite_prep.py`; all seven chapters sectioned.

**Commentary shape:** Full Layers 0–6 (not slimmed). `completeness_state: in-review` on sampled packets.

---

## Great Books weave

| GB | Anchor(s) | Role | Packet | Part VII placement (draft) |
|----|-----------|------|--------|---------------------------|
| `gb-10` | `civ-41` (registry); also `civ-30` (Part VI) | interwoven | `lectures/great-books/gb-10/` — stub → **Part VI** § `gb-10` (Inferno); **needs** Part VII § close pointer @ `civ-41` | **`### gb-10` (close)** — Renaissance/Inferno synthesis; do **not** duplicate Part VI claims table |

**Law:** `gb-10` is **dual-placed** by design — Inferno architecture @ Part VI open; registry close @ `civ-41`. Part VII section should **cross-link** Part VI `### gb-10` and add **close-read** rows (quiet revolution ↔ hell/spark cosmology), not fork a second canonical Inferno apparatus.

**Not in registry weave (corridor only):** `gb-09`, `gb-11`, `gb-12` — read via [Homer-to-Dante](../../../data/corridors/homer-to-dante.md) steps 10–13; do **not** add to `great_books_weave` without spine-anchor decision.

**Registry:** `secret_history_companions: []` · corridors: `homer-to-dante`, `homer-to-tolstoy`

---

## Corridor touchpoints

| Corridor | Part VII role | Notes |
|----------|---------------|-------|
| [homer-to-dante](../../../data/corridors/homer-to-dante.md) | **Closes** @ `civ-41` (step 9); GB steps 10–13 | Part VI **opens** @ `civ-29`; public mirror complete through `gb-12` |
| [homer-to-tolstoy](../../../data/corridors/homer-to-tolstoy.md) | Dante hinge before Shakespeare/Dostoevsky | `civ-41` + `gb-09`–`gb-12` carry segment 3 |

---

## Part VII artifacts

| Artifact | Status (2026-06-09) |
|----------|---------------------|
| `part-07-world-after-rome-commentary.md` | **Phase 3 complete** — all `civ-35`–`41` + `gb-10` (close) |
| `part-07-world-after-rome-bibliography.md` | **Phase 3** — `supports:`/`counters:` for `civ-35`–`41` |
| `volume-i-parts.json` `commentary_path` / `bibliography_path` | **Wired** (2026-06-09) |
| `part-07-world-after-rome.md` Apparatus block | **Done** — commentary/bib links + Part VI ingress |
| `PART-07-HYBRID-READINESS.md` | **Done** — this inventory |
| Pin-cite `civ-35`–`41` | **Done** — `scripts/part_vii_pin_cite_prep.py` |
| Slim `civ-35`–`41` commentaries | **Not started** |
| README 6-step lattice + Part links | **Done** — all `civ-35`–`41` |
| Validator Part VII README checks | **Done** — all `civ-35`–`41` |
| `gb-10` Part VII close section @ `civ-41` | **Done** — wedge § `gb-10` (close pointer) |
| `civ-41` README 6-step + Part links | **Done** |
| Pin-cite `civ-41` | **Done** — `scripts/part_vii_pin_cite_civ41.py` |
| Pin-cite `civ-35` | **Done** — `scripts/part_vii_pin_cite_civ35.py` |
| Pin-cite `civ-36` | **Done** — `scripts/part_vii_pin_cite_civ36.py` |
| `civ-35` README 6-step + Part links | **Done** |
| Pin-cite `civ-40` | **Done** — `scripts/part_vii_pin_cite_civ40.py` |
| `civ-35` Part VII § open | **Done** |
| `civ-36` Part VII § (Viking pair close) | **Done** |
| `civ-36` README 6-step + Part links | **Done** |
| `civ-37` Part VII § (Islamic Golden Age) | **Done** |
| Pin-cite `civ-37` | **Done** — `scripts/part_vii_pin_cite_civ37.py` |
| `civ-40` Part VII § bridge | **Done** |
| `civ-40` README 6-step + Part links | **Done** |
| `gb-10` stub dual-route (Part VI + Part VII) | **Done** |

---

## Cross-Part ingress (from Part VI)

| Prediction | Strength | Status (Part VI ledger) | Part VII test |
|------------|----------|-------------------------|---------------|
| Oceanic-currents model bridges to Part VII world orders | C | **Pending** | `civ-31` frame vs `civ-35`–`40` plural orders |
| Holy Roman useful fiction closes Part law question | C | **Pending** | `civ-34` fiction → `civ-35` Viking opening |
| Homer→Dante corridor continues past `gb-10` | E | **Partially supported** | `civ-41` + `gb-10` close must cite `gb-11`/`gb-12` corridor completion |
| Dante rebuts Augustinian frame | E | **Partially supported** | `civ-41` Renaissance re-entry; pairs `civ-40` church power |

---

## civ-41 + gb-10 close — narrow inventory slice (operator pick C)

Focused readiness for the **Homer-to-Dante bookend close** before authoring the full `civ-35`–`40` block.

### Load-bearing seams

| Seam | What must hold | Current state |
|------|----------------|---------------|
| **Corridor close** | Step 9 `civ-41` completes literary arc opened @ `civ-29` | Card + corridor wired; **no** Part VII synthesis |
| **gb-10 dual placement** | Inferno depth in Part VI; Renaissance close in Part VII | Part VI `### gb-10` **live**; `gb-10` stub notes `civ-41` close — **no** Part VII section |
| **GB cluster order** | Reader path: `civ-29`/`30` → `gb-09`–`gb-12` → `civ-41` | Corridor steps 7–13 + step 9; doorway lists only `gb-10` |
| **Part VIII egress** | `civ-41` → `civ-42` modernity birth | `civ-41` L5 links `civ-42`/`civ-43`; Part VIII apparatus **not started** |

### civ-41 packet snapshot

| Layer | Finding |
|-------|---------|
| Transcript | `exact_body_match`; **no** `###` section rails; ASR line-wrap prose |
| Commentary | 6 L2 claims; all refs → `civ-41-transcript.md:29` (pin-cite debt) |
| README | 4-step lattice; **no** Part VII / `gb-10` links |
| Card | Strong placement; Homer-to-Dante corridor named |
| Frontmatter | **no** `part_id`, `part_commentary_path`, `gb-10` weave paths |

### gb-10 @ civ-41 — draft Part VII section shape

Proposed `### gb-10` (close) block in `part-07-world-after-rome-commentary.md` (pointer + delta, not Inferno reprint):

| # | Close claim (draft) | Upstream | Confidence |
|---|---------------------|----------|------------|
| 1 | Inferno spark/love cosmology **returns** in `civ-41` as Renaissance imagination motor | Part VI `### gb-10` + `civ-41` L2 #4 | High |
| 2 | Quiet revolution = poetry transforming church order without institutional overthrow | `civ-41` L2 #6 | High |
| 3 | `civ-41` re-enters Dante **after** world-order pause (`civ-35`–`40`) | Part VII doorway bookend table | High |
| 4 | Corridor reader should complete `gb-09`–`gb-12` before judging `civ-41` hinge | homer-to-dante steps 10–13 | Medium |
| 5 | Dante→Reformation/Science chain is lecture hypothesis — keep in prediction ledger | `civ-41` counter-readings | High |

**Counter-readings to front-load:** single-poet Renaissance causation; Michelangelo brain-reading; neuroscience metaphor in lecture; duplicate Dante entry without Part VI distinction.

### civ-41 Phase 1 wedge checklist (minimal)

1. Add `### civ-41` + `### gb-10` (close) to Part VII commentary stub
2. Seed Part VII prediction ledger (3–5 rows: corridor close, church→Dante, Part VIII egress)
3. Pin-cite `civ-41` transcript (`###` rails + `#anchor` refs)
4. Update `civ-41` README to 6-step lattice + Part VII + `gb-10` handoff
5. Extend `gb-10-commentary.md` stub with Part VII § link (mirror `gb-02` dual-routing pattern)
6. **Defer** full `civ-35`–`40` Part sections until wedge validates

---

## Phased rollout (draft)

### Phase 0 — Inventory — **Done** (2026-06-09)

- This doc + doorway cross-check

### Phase 1 — Apparatus seed (~1 session) — **Wedge done** (2026-06-09)

- **Option B (wedge):** `part-07-*-commentary.md` + bibliography stub + registry + `civ-41` + `gb-10` (close) ✓
- **Option A (full):** thick `civ-35`–`40` sections — **deferred**

### Phase 2 — Reader reshape (~1–2 sessions)

- `scripts/part_vii_pin_cite_prep.py`
- Slim `civ-35`–`41` to Layer 0–2 + Part pointer
- 6-step README lattice

### Phase 3 — Validator + docs (~half session) — **Wedge done** (2026-06-09)

- `volume_i_parts.py` Part VII block (wedge `civ-40`/`civ-41` README checks) ✓
- `parts/README.md`, `docs/methodology/commentary-canvas.md`, `docs/methodology/source-lattice.md` (Part VII wedge) ✓
- Pin-cite `civ-40` + `civ-40` README 6-step ✓
- Full `civ-35`–`39` in docs/validator — **deferred** until Phase 2

---

## Risks / counter-readings to front-load

| Topic | Note |
|-------|------|
| Viking fifth-pillar (`civ-35`) | Structural claim vs standard Western-civ framing |
| Islam Golden Age decline (`civ-37`) | Lecture causation vs scholarly historiography |
| China exam meritocracy (`civ-38`) | Bureaucratic control vs fairness narrative |
| Mongol brutality (`civ-39`) | Constraint explanation ≠ moral endorsement |
| Church scapegoating (`civ-40`) | Sensitive historical framing |
| Dante→Renaissance single spark (`civ-41`) | High lecture thesis — prediction ledger required |
| `gb-10` dual placement | Avoid duplicate Inferno apparatus in Part VII |
| Homer-to-Dante close | `civ-41` is **not** `gb-12` — Commedia close lives in GB cluster; civ lecture is Renaissance hinge |

---

## Out of scope (Part VII pilot)

- Parts VIII–X apparatus · SH companions · `gb-11`/`gb-12` registry weave rows · full `civ-35`–`40` thick sections if wedge path chosen · `gb-10` audio re-align

---

## Next operator pick

**Phase 1 wedge** (`civ-41` + `gb-10` close) · **full Phase 1** (all seven chapters) · **pin-cite `civ-41` only** · **commit** inventory doc · **compare** Part VII gates vs Part VI completed state (gap table).
