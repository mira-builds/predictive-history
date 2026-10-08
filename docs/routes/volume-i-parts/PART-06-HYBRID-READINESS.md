---
part_id: part-06-medieval-imagination
plan_status: phase0_inventory
scaffold_version: ph_civ_part_commentary_v1
template_from: part-05-christianity-and-islam (hybrid pilot)
inventory_date: 2026-06-09
---

# Part VI Hybrid Apparatus — Readiness Inventory

Planning doc for extending the **Part II–V hybrid model** (thin chapter + thick Part commentary/bibliography) to **Part VI — The Medieval Imagination** (`civ-29`–`civ-34` + `gb-09`/`gb-10` weave @ `civ-29`–`30`).

**Law-discovery question (registry):** How does epic inheritance become pilgrimage, comedy, and a new architecture of the self?

**Spine note:** `spine_slice_warning: false` — contiguous block (`civ-29`→`civ-34`). **Structural seam:** Dante **opens** here (`civ-29`–`30`); the [Homer-to-Dante](../../../data/corridors/homer-to-dante.md) corridor **returns** at `civ-41` (Part VII) — this Part is a **bookend open**, not Dante's close.

**Cross-Part ingress:** [Part V `civ-28`](./part-05-christianity-and-islam-commentary.md#civ-28) Augustinian/Islamic field → Dante rebuttal (`civ-29`); prediction row **Pending** until Part VI apparatus exists.

---

## Maturity gate (when to implement)

| Gate | Threshold | Current (2026-06-09) |
|------|-----------|----------------------|
| Chapter Layer 0–2 | All six chapters have transcript-anchored claims + line/section refs | **Met** — 6–8 L2 claims each; transcript `###` sections + `#anchor` refs (pin-cite prep 2026-06-09); chapter `analysis_depth: layer2_drafted` |
| Chapter slimming | Willing to move Layers 3–6 to Part apparatus | **Met** — Phase 2 slim `civ-29`–`34` + Part chapter sections |
| GB weave | Registry `great_books_weave` + Part `### gb-NN` sections | **Partial** — `gb-09`/`gb-10` stub-routed; `gb-10` **sectioned** (ASR spot-check) |
| Cross-Part bridge | Part V `civ-28` → Dante/Augustine rebuttal; Homer corridor open | **Partial** — Part V forward row **Pending**; doorway + corridor links wired |
| Validator | `volume_i_parts.py` Part VI README checks | **Met** — Phase 3 (2026-06-09) |
| Theology / literary guardrails | Bibliography + counter-readings for Dante/Augustine/Rome claims | **Partial** — Phase 1 stub bibliography + `gb-09` counter-readings |

**Recommendation:** Phase 0 inventory **done**. Before Phase 1: run pin-cite prep on `civ-29`–`34` (mirror Parts II–V `#anchor` discipline); decide whether `civ-31` (oceanic currents) gets **thick** Part section or stays bridge to Part VII prediction grammar.

---

## Chapter inventory (`volume-ii/` packets)

| Chapter | Core thesis (Layer 0) | L2 claims | L3 | analysis_depth | Part section weight (draft) |
|---------|----------------------|-----------|-----|----------------|-----------------------------|
| `civ-29` | Dante rebuts Augustine — love, imagination, agency, poetic cosmology | 8 | yes | seed | **Thick** — Commedia opener; Augustine clash; corridor **open** |
| `civ-30` | Dante displaces Virgil/Homer — love, freedom, error, ascent | 8 | yes | seed | **Thick** — unreliable-guide arc; pairs `gb-09`/`gb-10` |
| `civ-31` | Second-semester reset — oceanic-currents model + live geopolitics | 6 | yes | seed | **Medium** — model bridge; date-sensitive L3 needs guardrails |
| `civ-32` | Rome as war republic/empire — citizenship, Caracalla, America analogy | 6 | yes | seed | **Medium** — Rome recap inside medieval Part |
| `civ-33` | Byzantium as eastern Roman survival — walls, Nicaea, bureaucracy | 6 | yes | seed | **Medium** — east/west legitimacy split |
| `civ-34` | Holy Roman Empire as useful fiction — Charlemagne, Augustine blueprint | 6 | yes | seed | **Thick** — closes Part law question (fiction + local order) |

**Legacy wrappers:** `civilization-spine/civ-29`–`civ-34` and `volume-ii/civ-29`–`34` READMEs use **4-step** lattice — **no Part apparatus links** (expected pre-implementation).

**Pin-cite debt:** **Cleared** (2026-06-09) — `civ-29`–`34` transcripts sectioned; chapter L2 refs use `#anchor` slugs (`scripts/part_vi_pin_cite_prep.py`).

**Commentary shape:** Full Layers 0–6 (not slimmed). `completeness_state: in-review` on sampled packets.

---

## Great Books weave

| GB | Anchor(s) | Role | Packet | Part VI placement (draft) |
|----|-----------|------|--------|---------------------------|
| `gb-09` | `civ-29`, `civ-30` | interwoven | `lectures/great-books/gb-09/` — **stub** → Part VI § `gb-09`; curated transcript | **`### gb-09`** — claims table live in Part commentary |
| `gb-10` | `civ-30` | interwoven | `lectures/great-books/gb-10/` — **stub** → Part VI § `gb-10`; ASR curated + 10 `#anchor` sections | **`### gb-10`** — claims table live |

**Law:** Civilization lectures own spine narrative; GB sections **pointer + close-read**, not full transcript mirror in Part file.

**Registry:** `secret_history_companions: []` · corridors: `homer-to-dante`, `homer-to-tolstoy`

---

## Corridor touchpoints

| Corridor | Part VI role | Notes |
|----------|--------------|-------|
| [homer-to-dante](../../../data/corridors/homer-to-dante.md) | **Opens** @ `civ-29` | Epic → pilgrimage; completes @ `civ-41` (Part VII) |
| [homer-to-tolstoy](../../../data/corridors/homer-to-tolstoy.md) | Touch @ Dante/Rome imagination | Long arc; Part VI supplies Dante + Roman afterlife beats |

---

## Part VI artifacts

| Artifact | Status (2026-06-09) |
|----------|---------------------|
| `part-06-medieval-imagination-commentary.md` | **Phase 1 done** — ledger + `gb-09`/`gb-10` sections |
| `part-06-medieval-imagination-bibliography.md` | **Phase 1 stub** |
| `volume-i-parts.json` `commentary_path` / `bibliography_path` | **Wired** |
| `part-06-medieval-imagination.md` Apparatus block | **Done** — commentary/bib links + Part III forward |
| `PART-06-HYBRID-READINESS.md` | **Done** — this inventory |
| Pin-cite `civ-29`–`34` | **Done** — `scripts/part_vi_pin_cite_prep.py` |
| Slim `civ-29`–`34` commentaries | **Done** — `scripts/part_vi_phase2_slim.py` |
| README 6-step lattice + Part links | **Done** — `volume-ii/civ-29`–`34` |
| Validator Part VI README checks | **Done** — `volume_i_parts.py` Part VI block |
| GB stub routing (`gb-09`/`gb-10` from Part doorway) | **Done** — mirror `gb-02` pattern |
| `gb-07`→`gb-08`→Part VI synthesis | **Done** — Part III § anti-Homer→Aeneid |
| `gb-10` transcript section rails + ASR spot-check | **Done** — 10 `#anchor` sections |
| `gb-11` mirror promotion | **Done** — `scripts/promote_gb_11_mirror.py` |
| `gb-12` mirror promotion | **Done** — `scripts/promote_gb_12_mirror.py` (YouTube ASR) |

---

## Cross-Part ingress (from Part V `civ-28`)

| Prediction | Strength | Status (2026-06-09) | Part VI test |
|------------|----------|---------------------|--------------|
| Dante/medieval arc follows Islamic + Augustinian field | C | **Pending** | `civ-29` Augustine rebuttal |
| Sacred legitimacy → poetic/imagination architecture | C | **Pending** | `civ-29`–`30` + `gb-09` |
| Eastward dissent / imperial whitewashing carries to Rome–Byzantium split | E | **Partial** (Part V) | `civ-33`–`34` |

---

## Medieval imagination grammar spine (draft)

1. **Epic → pilgrimage** — Commedia structure; apocalyptic overturn; human agency (`civ-29`)
2. **Homer/Virgil displacement** — unreliable guide; love without possession; poetic surgery (`civ-30`, `gb-09`/`gb-10`)
3. **Oceanic currents** — second-semester model; borderlands; prediction grammar (`civ-31`)
4. **Roman inheritance** — republic/empire citizenship; America analogy (`civ-32`)
5. **Byzantine survival** — east Roman continuity; Nicaea; stagnation (`civ-33`)
6. **Holy Roman fiction** — Charlemagne legitimacy; Augustine blueprint; useful fiction close (`civ-34`)

**Cross-links:** Part V [`civ-28`](./part-05-christianity-and-islam-commentary.md#civ-28); forward [Part VII](./part-07-world-after-rome.md) (`civ-35` world orders; `civ-41` Dante close).

---

## Implementation phases

### Phase 0 — Inventory — **Done** (2026-06-09)

### Phase 1 — Author only (~1–2 sessions) — **Done** (2026-06-09)

- Create `part-06-medieval-imagination-commentary.md` + `-bibliography.md` ✓
- Wire `volume-i-parts.json` paths + doorway Apparatus block ✓
- Seed prediction ledger + `gb-09`/`gb-10` pointer sections ✓
- Stub-route `gb-09`/`gb-10` commentaries ✓

### Phase 2 — Reader reshape (~1–2 sessions) — **Done** (2026-06-09)

- Pin-cite prep script for `civ-29`–`34` ✓ (prior pass)
- Slim chapters to Layer 0–2 + Part pointer ✓
- Update `volume-ii/` READMEs (6-step lattice) ✓
- Part commentary chapter sections (`civ-29`–`34`) ✓

### Phase 3 — Validator + docs (~half session) — **Done** (2026-06-09)

- Extend `volume_i_parts.py` Part VI checks (mirror Part V) ✓
- Update `parts/README.md`, `docs/methodology/commentary-canvas.md`, `docs/methodology/source-lattice.md` ✓
- Promote `gb-12` from YouTube ASR (`scripts/promote_gb_12_mirror.py`) ✓

---

## Risks / counter-readings to front-load

| Topic | Note |
|-------|------|
| Dante vs Augustine (`civ-29`) | Patristic vs Commedia theology — keep source-layer discipline |
| Renaissance/Reformation/Science seeds (`civ-29`) | Lecture chain ≠ historical causation |
| Paul-as-spy / Virgil unreliable narrator (`civ-30`) | Literary reading vs biographical claim |
| Live geopolitics in `civ-31` | Date-stamp L3; separate model from news |
| America–Rome analogy (`civ-32`) | Structural analogy ≠ prediction proof |
| Byzantine refutation frame (`civ-33`) | Scholarly consensus vs lecture dissent |
| Holy Roman “fiction” (`civ-34`) | Voltaire quip vs institutional history |
| Duplicate `gb-09` anchors | Registry lists two rows — one Part `### gb-09` section |
| Homer-to-Dante bookend | Do not treat `civ-34` as corridor **close** — `civ-41` owns close |

---

## GB-11/12 corridor extension inventory

Dante continuation beyond public mirror step `gb-10`. Extended Dante source archive lives outside this public mirror until promoted.

| GB | Title | YouTube | Archive file | Body | Promotion blockers |
|----|-------|---------|--------------|------|-------------------|
| `gb-11` | Dante's Revolution (Purgatory) | `otyUpKhpTYM` | `lectures/great-books/gb-11/` | **Promoted** (2026-06-09) | 10 section rails; Part VI § `gb-11` |
| `gb-12` | Dante in Paradise | `FspDllFoiDE` | `lectures/great-books/gb-12/` | **Promoted** (2026-06-09) | YouTube ASR; 10 section rails; Part VI § `gb-12` |

**Load-bearing themes (gb-11 archive):** Virgil/Augustine **human nature bad** vs Dante **divine spark + love**; Purgatory terrace sins (inverse Inferno); two-part lecture series (Purgatory then Paradise).

**Load-bearing themes (gb-12):** Paradise spheres; Beatrice moon-spots; Trinity vision; closing *love moves the sun and stars*.

**Corridor:** [homer-to-dante](../../../data/corridors/homer-to-dante.md) steps 12–13 **live**. **Do not** treat as Apocalypse reroute.

---

## Out of scope (Part VI pilot)

- Parts VII–X full apparatus · `civ-41` Dante close (Part VII) · SH companions · `gb-10`/`gb-12` audio re-align (optional)

---

## Next operator pick

**Commit** local batch · **push** · Part VII apparatus inventory · `gb-10` audio re-align (optional).
