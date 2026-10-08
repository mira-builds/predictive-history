---
part_id: part-03-roman-imperium
plan_status: phase3_complete
scaffold_version: ph_civ_part_commentary_v1
template_from: part-02-hellenic-world (hybrid pilot)
inventory_date: 2026-06-09
---

# Part III Hybrid Apparatus — Readiness Inventory

Planning doc for extending the **Part II hybrid model** (thin chapter + thick Part commentary/bibliography) to **Part III — The Roman Imperium** (`civ-14`–`civ-17` + `gb-08`).

**Law-discovery question (registry):** How does imperial machinery acquire a literary soul?

**Spine note:** `spine_slice_warning: true` — Rome block appears before Part IV ancient-worlds floor in interwoven order.

---

## Maturity gate (when to implement)

| Gate | Threshold | Current (2026-06-09) |
|------|-----------|----------------------|
| Chapter Layer 0–2 | All four chapters have transcript-anchored claims + line/section refs | **Met** — 8 L2 claims each; transcript `###` sections + `#anchor` refs (pin-cite sweep 2026-06-09); chapter `analysis_depth: layer2_drafted` |
| Pin-cite (Tier A) | L2 rows use `#anchor`, not blanket `:32` | **Cleared** — `civ-14`–`17` via `part_ii_iii_pin_cite_sweep.py`; discipline: [`docs/methodology/PIN-CITE-DISCIPLINE.md`](../../../docs/methodology/PIN-CITE-DISCIPLINE.md) |
| Chapter slimming | Willing to move Layers 3–6 to Part apparatus | **Met** — civ-14–17 thin Layer 0–2 + Part pointer |
| GB weave | `gb-08` @ `civ-17` interwoven; `gb-07` anti-Homer lecture matures Part link | **Met** — gb-08 Part section + transcript anchors; gb-07 Part II stub |
| Cross-Part bridge | Part II Homer grammar ↔ Part III Virgil inversion documented | **Met** — gb-07 pointer in Part II; civ-17 ↔ Part III gb-08 |
| Validator | `volume_i_parts.py` Part III checks (mirror Part II) | **Met** |
| ASR | civ-14–17 in normalization scope if needed | **Out of scope** until operator extends pilot |

**Recommendation:** Part III hybrid pilot **complete** through Phase 3 + pin-cite **Cleared**. Next work: external-verify claims, deepen Part sections, or Part II `civ-07`–`10`/`civ-12` Tier-B uplift.

---

## Chapter inventory (`volume-ii/` packets)

| Chapter | Core thesis (Layer 0) | L2 claims | L3 predictions | analysis_depth | Part section weight |
|---------|----------------------|-----------|----------------|----------------|---------------------|
| `civ-14` | Rome rises via manpower, citizenship, cohesion — Hannibal/Cannae crisis | 8 | 2 pending | seed | **Thick** — republican machinery + Punic arc |
| `civ-15` | Caesar as mythmaker; narrative + action; assassination as identity threat | 8 | 2+ pending | seed | **Thick** — late republic narrative weapon |
| `civ-16` | Caesar's will → Octavian settlement; Augustan republican theater | 8 | 2+ pending | seed | **Thick** — empire birth mechanics |
| `civ-17` | Homer vs Virgil; literature as Roman soul / state epic | 8 | 2 pending | seed | **Thick** — literary soul capstone; pairs `gb-08` |

**Legacy wrappers:** `civilization-spine/civ-14`–`civ-17` READMEs point at `volume-ii/` packets with Part apparatus links.

---

## Great Books weave

| GB | Anchor | Role | Commentary state | Part placement |
|----|--------|------|------------------|-------------------|
| `gb-08` | `civ-17` | interwoven | stub → Part III | **`### gb-08`** canonical section; transcript section anchors |
| `gb-07` | `civ-07` (Part II) | interwoven | stub → Part II | **Cross-part pointer** — anti-Homer frame; forward to Part III `gb-08` |

**Stub targets:** `gb-08-commentary.md` → `part-03-roman-imperium-commentary.md#gb-08`; Part II `gb-02`/`gb-05`/`gb-07` mirror `gb-03` pattern.

---

## Part III artifacts

| Artifact | Status (2026-06-09) |
|----------|---------------------|
| `part-03-roman-imperium-commentary.md` | **Created** — Phase 1 draft; gb-08 claim refs use transcript anchors |
| `part-03-roman-imperium-bibliography.md` | **Created** — Phase 1 seeded |
| `volume-i-parts.json` commentary/bib paths | **Wired** |
| `part-03-roman-imperium.md` Apparatus block | **Wired** |
| Slim `civ-14`–`civ-17` commentaries | **Done** |
| README + transcript frontmatter Part links | **Done** |
| `gb-08-commentary.md` stub route | **Done** |
| Validator Part III README checks | **Done** |
| `gb-08-transcript` section anchors | **Done** — Phase 3 |
| `docs/methodology/commentary-canvas.md` / `docs/methodology/source-lattice.md` | **Done** — Part III + GB stub pattern |
| Part II `gb-02`/`gb-05`/`gb-07` stub route | **Done** — cross-part with Part II |

---

## Roman grammar spine (draft for Part commentary)

Working mechanism chain to validate against lectures:

1. **Citizenship-manpower** — open body, cohesion triad (`civ-14`)
2. **External crisis** — Hannibal, Cannae, Punic endgame (`civ-14`)
3. **Mythmaker** — Caesar narrates conquest into legitimacy (`civ-15`)
4. **Will-heir settlement** — Octavian converts assassination into empire (`civ-16`)
5. **Literary soul** — Aeneid / Homer-Virgil war for Roman identity (`civ-17`, `gb-08`)

**Cross-links:** Part II conquest-carrier (`civ-11`–`civ-13`) → Roman absorption; Homer corridor (`homer-to-dante`, `homer-to-tolstoy`).

---

## Implementation phases

### Phase 1 — Author only (~1 session) — **Done**

- Draft Part III commentary + bibliography from existing Layer 0–2
- Fold civ-14–17 Layer 3 predictions into Part ledger
- Wire registry + doorway apparatus links

### Phase 2 — Reader reshape (~1 session) — **Done**

- Slim civ-14–17 commentaries
- Stub `gb-08-commentary.md`
- Update civilization-spine READMEs (6-step lattice + Part links)
- Transcript YAML frontmatter only

### Phase 3 — Validator + docs (~half session) — **Done**

- Extend `volume_i_parts.py` Part III checks (mirror `part-02-hellenic-world` block)
- Update `docs/methodology/commentary-canvas.md` / `docs/methodology/source-lattice.md` with Part III example
- Section anchors on `gb-08-transcript.md`
- Stub-route Part II `gb-02`/`gb-05`/`gb-07`

---

## Risks / counter-readings to front-load

| Topic | Note |
|-------|------|
| Character typology (Greek/Carthaginian/Roman) | Lecture shorthand — bibliography must carry scholarship |
| Caesar myth-maker | Distinct from standard prosopography — label as lecture frame |
| Augustus-as-Virgil-author (gb-07) | Strong lecture claim; counter-read in Part bibliography |
| Homer vs Virgil binary (`civ-17`) | Medium counter-evidence already in Layer 4 — preserve in Part section |
| `spine_slice_warning` | Part commentary must explain interwoven order vs historical chronology |

---

## Out of scope (Part III pilot)

- Part I or Parts IV–X apparatus
- Moving `gb-07` canonical body from Part II to Part III (keep pointer)
- Museum room retargeting
- civ-14–17 transcript body / ASR edits

---

## Next operator pick

Commit Phase 2 + Phase 3 batch; parent submodule bump; or deepen Part III gb-08 / civ-17 claims with external verify.
