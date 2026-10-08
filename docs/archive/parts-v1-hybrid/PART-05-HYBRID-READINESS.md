---
part_id: part-05-christianity-and-islam
plan_status: phase3_complete
scaffold_version: ph_civ_part_commentary_v1
template_from: part-04-ancient-foundations (hybrid pilot)
inventory_date: 2026-06-09
---

# Part V Hybrid Apparatus — Readiness Inventory

Planning doc for extending the **Part II/III/IV hybrid model** (thin chapter + thick Part commentary/bibliography) to **Part V — Christianity and Islam** (`civ-24`–`civ-28` + `sh-18` deepening @ `civ-28`).

**Law-discovery question (registry):** How does sacred legitimacy migrate across revelations and empires?

**Spine note:** `spine_slice_warning: false` — contiguous interwoven block (`civ-24`→`civ-28`); not an out-of-order floor slice like Part IV.

**Cross-Part ingress:** [Part IV `civ-23`](./part-04-ancient-foundations-commentary.md#civ-23) Zoroastrian/Jewish merge → Christianity unit; prediction ledger rows **Pending** until Part V apparatus exists.

---

## Maturity gate (when to implement)

| Gate | Threshold | Current (2026-06-09) |
|------|-----------|----------------------|
| Chapter Layer 0–2 | All five chapters have transcript-anchored claims + line/section refs | **Met** — 8 L2 claims each; transcript `###` sections + `#anchor` refs (pin-cite prep 2026-06-09); chapter `analysis_depth: layer2_drafted` |
| Chapter slimming | Willing to move Layers 3–6 to Part apparatus | **Met** — `civ-24`–`28` thin Layer 0–2 + Part pointer (Phase 2 slim 2026-06-09); Tolstoy Lens in Part `civ-25` section only |
| GB weave | Registry `great_books_weave` | **N/A** — empty array; no `gb-NN` Part sections required |
| SH companion | `sh-18` @ `civ-28` deepening documented | **Partial** — doorway + registry wired; staged wrapper in `secret-history-support/`; **`volume-vi/sh-18/`** seed commentary; Part `### sh-18` pointer + SH predictions in commentary |
| Cross-Part bridge | Part IV `civ-23` handoff + Yahwist/covenant/messianic carry | **Met** — Part IV forward rows **Partially supported**; Part V ingress + Yahwist clash in commentary |
| Validator | `volume_i_parts.py` Part V README checks (mirror Part IV) | **Met** — `part-05-christianity-and-islam` README lattice block |
| Interfaith / theology guardrails | Bibliography + counter-readings for Jesus/Paul/Islam claims | **Met** — Phase 1 bibliography + Part counter-readings seeded |

**Recommendation:** Part V hybrid pilot **complete** through Phase 3. Next: external-verify high-risk claims, deepen Part sections, or Part VI readiness inventory.

---

## Chapter inventory (`volume-ii/` packets)

| Chapter | Core thesis (Layer 0) | L2 claims | L3 predictions | analysis_depth | Part section weight |
|---------|----------------------|-----------|----------------|----------------|---------------------|
| `civ-24` | Historical vs biblical vs Gnostic Jesus; martyrdom; original-sin/Yahwist clash; Paul preview | 8 | 2 pending | seed | **Thick** — source-layer opener; bridges `civ-22`/`civ-23` |
| `civ-25` | Paul as hinge from Jesus movement to Christianity; faith/circumcision; Paul-as-spy thesis | 8 | 2 pending | seed | **Thick** — Roman-carrier / Gentile opening; highest political-theology risk |
| `civ-26` | Constantine + Nicaea godhead → monotheism as reality-order; money/science/nation-state preview | 8 | 2 pending | seed | **Thick** — imperial-theological hinge; broad modernity chain |
| `civ-27` | Augustine takes Church out of history; City of God; obedience doctrine; eastward to Arabia | 8 | 2 pending | seed | **Thick** — post-Rome-sack legitimacy; Dark Ages frame |
| `civ-28` | Muhammad / early Islam as revolutionary Abrahamic synthesis; expansion analogies; imperial whitewashing | 8 | 2 pending | seed | **Thick** — Islam close; pairs `sh-18`; forward Part VI Dante |

**Legacy wrappers:** `civilization-spine/civ-24`–`civ-28` and `volume-ii/civ-24`–`28` READMEs use **4-step** lattice — **no Part apparatus links** (expected pre-implementation).

**Pin-cite debt:** **Cleared** (2026-06-09) — `civ-24`–`28` transcripts sectioned; chapter + Part L2 refs use `#anchor` slugs.

---

## Companion weave (not Great Books)

| Companion | Anchor | Role | Packet state | Part V placement |
|-----------|--------|------|--------------|------------------|
| `sh-18` | `civ-28` | deepening | seed in `volume-vi/sh-18/`; staged wrapper in `secret-history-support/` | **`### sh-18`** pointer section in Part commentary (parallel to Part IV `sh-17`) |

**Law:** Civilization lecture (`civ-28`) owns the spine; `sh-18` cross-links — do not duplicate full SH body in Part file.

**Registry:** `great_books_weave: []` · `corridor_touchpoints: []`

---

## Part V artifacts

| Artifact | Status (2026-06-09) |
|----------|---------------------|
| `part-05-christianity-and-islam-commentary.md` | **Deepened** — Phase 1 + pilot deepen (cluster arcs, close-reads, `sh-18` predictions) |
| `part-05-christianity-and-islam-bibliography.md` | **Created** — Phase 1 seeded (interfaith guardrails) |
| `volume-i-parts.json` `commentary_path` / `bibliography_path` | **Wired** |
| `part-05-christianity-and-islam.md` Apparatus block | **Wired** |
| `PART-05-HYBRID-READINESS.md` | **Done** — this inventory |
| Slim `civ-24`–`civ-28` commentaries | **Done** — Phase 2 slim (`scripts/part_v_phase2_slim.py`) |
| README 6-step lattice + Part links | **Done** — Phase 2 |
| Transcript YAML `part_id` + Part paths | **Done** — Phase 2 frontmatter |
| Validator Part V README checks | **Done** — Phase 3 (`volume_i_parts.py`) |

---

## Cross-Part ingress (from Part IV `civ-23`)

| Prediction | Strength | Status (2026-06-09) | Part V test |
|------------|----------|---------------------|-------------|
| Persian/Cyrus/Zoroastrian merge precedes Christianity unit | E | **Confirmed** (Part IV) | `civ-24` follows `civ-23` in spine |
| Christianity inherits Persian/Jewish strands **distinctly** | C | **Partially supported** | Part V commentary opened; keep influence lines separate |
| Word/covenant/argument-with-God themes carry to Part V | C | **Partially supported** | `civ-24` L2 #4 |
| Zoroastrian–Christian single pipeline | — | **Guardrailed** (Part IV) | influence ≠ causation |

---

## Christianity–Islam grammar spine (draft)

1. **Source-layer Jesus** — historical vs biblical vs Gnostic; martyrdom; original-sin/Yahwist tension (`civ-24`)
2. **Pauline transformation** — Gentile/faith opening; Roman protection; Paul-as-spy frame (`civ-25`)
3. **Imperial monotheism** — Constantine; Nicaea; monotheism as closed reality-order (`civ-26`)
4. **Church above history** — Augustine; City of God; eastward dissent (`civ-27`)
5. **Islamic revolutionary universalism** — Muhammad source field; jihad/land/debt frame (`civ-28`, pairs `sh-18`)

**Cross-links:** Part IV [`civ-23`](./part-04-ancient-foundations-commentary.md#civ-23); forward [Part VI](./part-06-medieval-imagination.md) (`civ-29`).

---

## Implementation phases

### Phase 0 — Inventory — **Done** (2026-06-09)

### Phase 1 — Author only (~1–2 sessions) — **Done** (2026-06-09)

### Phase 2 — Reader reshape (~1–2 sessions) — **Done** (2026-06-09)

- Slim `civ-24`–`28` to Layer 0–2 + Part apparatus (`scripts/part_v_phase2_slim.py`)
- Update `volume-ii/` READMEs (6-step lattice + Part V links)
- Chapter frontmatter: `part_commentary_path`, `part_bibliography_path`

### Phase 3 — Validator + docs (~half session) — **Done** (2026-06-09)

- Extend `volume_i_parts.py` Part V checks (mirror Part IV)
- Update `parts/README.md` hybrid pilot list
- Extend `docs/methodology/commentary-canvas.md` / `docs/methodology/source-lattice.md` with Part V `civ-24`–`28` + `sh-18` pointer example

---

## Risks / counter-readings to front-load

| Topic | Note |
|-------|------|
| Historical vs biblical vs Gnostic Jesus (`civ-24`) | Source-layer discipline |
| Original sin vs Yahwist (`civ-24`) | Tie to `civ-22`; patristic bibliography |
| Paul-as-spy thesis (`civ-25`) | Highest political risk; keep bounded |
| Constantine / Nicaea (`civ-26`) | Separate imperial history from lecture philosophy |
| Augustine polemic (`civ-27`) | Lucretia/obedience passages — text vs institution |
| Muhammad source scarcity (`civ-28`) | Analogies ≠ proof |
| Jihad / revolution framing (`civ-28`) | Islamic-studies review before `complete` |
| Zoroastrian merger carry (`civ-23`→`28`) | Part IV guardrail: influence ≠ single pipeline |
| `sh-18` duplication | Pointer only |

---

## Out of scope (Part V pilot)

- Parts VI–X apparatus · GB stub routing · SH body merge · transcript re-ingest

---

## Next operator pick

**External-verify** Part V bibliography (Paul-as-spy, jihad, Nicaea), **push** local commits, or **Part VI** readiness inventory.
