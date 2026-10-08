---
part_id: part-09-age-of-conscience
plan_status: phase2_slimmed
scaffold_version: ph_civ_part_commentary_v1
template_from: part-08-birth-of-modernity (hybrid pilot complete)
inventory_date: 2026-06-10
---

# Part IX Hybrid Apparatus — Readiness Inventory

Planning doc for extending the **Part II–VIII hybrid model** (thin chapter + thick Part commentary/bibliography) to **Part IX — The Age of Conscience** (`civ-51`–`civ-53` + `sh-16` hinge @ `civ-53`).

**Law-discovery question (registry):** How do theater, democracy, and the Russian novel name conscience at the Tolstoy hinge?

**Spine note:** `spine_slice_warning: false` — contiguous block (`civ-51`→`civ-53`). Opens after Part VIII Anglo-American close (`civ-50`); closes before Part X nation-state arc (`civ-54`).

**Cross-Part ingress:** [Part VIII `civ-50`](./part-08-birth-of-modernity-commentary.md#civ-50) Rule Britannia → [`civ-51`](#civ-51) Shakespeare language-of-empire open; [homer-to-tolstoy](../../../data/corridors/homer-to-tolstoy.md) steps 4–5 land here.

**Corridors:** [homer-to-tolstoy](../../../data/corridors/homer-to-tolstoy.md) · [civilization-to-apocalypse](../../docs/routes/civilization-to-apocalypse.md) ingress @ conscience hinge.

---

## Maturity gate (when to implement)

| Gate | Threshold | Current (2026-06-10) |
|------|-----------|----------------------|
| Chapter Layer 0–2 | All three chapters have transcript-anchored claims + `#anchor` refs | **Done** — 6 L2 claims each; pin-cite manifest + prep script |
| Chapter slimming | Willing to move Layers 3–6 to Part apparatus | **Not met** — full Layers 0–6 on packets (deferred Slice 9) |
| SH companion | `sh-16` @ `civ-53` hinge documented | **Done** — pointer + delta in Part commentary; body in `volume-vi/sh-16/` |
| Cross-Part bridge | Part VIII `civ-50` → Part IX `civ-51` egress | **Partially supported** — ingress row live; ledger test **Partially supported** |
| Validator | `volume_i_parts.py` Part IX README checks | **Done** — `civ-51`–`53` 6-step lattice + Part links |
| Corridor synthesis | homer-to-tolstoy + civ-to-apocalypse in commentary | **Done** — Phase 3 synthesis close |
| High-risk guardrails | Bibliography + counter-readings (race, Civil War, Ukraine) | **Partial** — wedge bib; deepen in Phase 4 |

**Recommendation:** Phase 0 inventory **done** (this doc). Phase 3 **complete** — pin-cite `civ-51`–`53`; Part sections live; `sh-16` pointer wired.

---

## Chapter inventory (`volume-ii/` packets)

| Chapter | Core thesis (Layer 0) | L2 claims | L3 | analysis_depth | Part section weight |
|---------|----------------------|-----------|-----|----------------|---------------------|
| `civ-51` | Shakespeare as language-of-empire; diction, pentameter, theater | 6 | yes | layer2_drafted | **Thick** — Part IX open; homer-to-tolstoy step 4 |
| `civ-52` | America as anti-civilization / empire of democracy | 6 | yes | layer2_drafted | **Thick** — democratic imperial arc |
| `civ-53` | Dostoevsky + Russian heart; Putin/Ukraine frame | 6 | yes | layer2_drafted | **Thick** — Part IX close; pairs `sh-16` |

**Pin-cite debt:** **Cleared** (2026-06-10) — `scripts/part_ix_pin_cite_prep.py` + `volume-i-anchors.yaml`.

---

## Companion weave

| Companion | Anchor | Role | Packet state | Part IX placement |
|-----------|--------|------|--------------|-------------------|
| `sh-16` | `civ-53` | hinge | seed in `volume-vi/sh-16/`; wrapper in `secret-history-support/` | **`### sh-16`** pointer + delta (parallel Part V `sh-18`) |

**Law:** Civilization lecture (`civ-53`) owns Dostoevsky/Russia spine; `sh-16` cross-links Tolstoy/literary-endpoint lane — do not duplicate SH body in Part file.

---

## Part IX artifacts

| Artifact | Status (2026-06-10) |
|----------|---------------------|
| `part-09-age-of-conscience-commentary.md` | **Created** — Phase 3 (`civ-51`–`53` live + `sh-16` pointer) |
| `part-09-age-of-conscience-bibliography.md` | **Created** — wedge stub |
| `volume-i-parts.json` `commentary_path` / `bibliography_path` | **Wired** |
| `part-09-age-of-conscience.md` Apparatus block | **Wired** |
| `PART-09-HYBRID-READINESS.md` | **Done** — this inventory |
| `volume-ii/` READMEs (6-step lattice) | **Done** — Phase 3 |
| `scripts/part_ix_pin_cite_prep.py` | **Done** |

---

## Cross-Part ingress (from Part VIII `civ-50`)

| Prediction | Strength | Status (2026-06-10) | Part IX test |
|------------|----------|---------------------|--------------|
| Britannia institutional close → Shakespeare cultural-linguistic open | C | **Partially supported** | § `civ-51` `#language-of-empire-question` after `civ-50` egress |
| Anglo-American arc continues through American democratic empire | C | **Partially supported** | § `civ-52` `#empire-of-democracy-lincoln` |
| homer-to-tolstoy step 4–5 complete before Part X | C | **Partially supported** | § `civ-51`/`civ-53` + `sh-16` Tolstoy route |

---

## Conscience grammar spine (draft)

1. **Language of empire** — four modern civs map; Shakespeare diction/pentameter/theater (`civ-51`)
2. **Empire of democracy** — anti-civilization design; Founders; Lincoln synthesis (`civ-52`)
3. **Russian heart** — Dostoevsky; reason vs heart; Ukraine frame (`civ-53`, pairs `sh-16`)

**Cross-links:** Part VIII [`civ-50`](./part-08-birth-of-modernity-commentary.md#civ-50); forward [Part X](./part-10-rise-of-the-nation-state.md) (`civ-54`).

---

## Implementation phases

### Phase 0 — Inventory — **Done** (2026-06-10)

### Phase 1 — Author only — **Done** (2026-06-10)

- Part commentary wedge + bibliography + registry paths

### Phase 2 — Reader reshape — **Deferred** (Slice 9)

- Slim `civ-51`–`53` to Layer 0–2 + Part pointer (Volume I final pass)

### Phase 3 — Validator + docs — **Done** (2026-06-10)

- Pin-cite `civ-51`–`53`; README 6-step lattice; synthesis close

---

## Risks / counter-readings to front-load

| Topic | Note |
|-------|------|
| White man's burden / Othello (`civ-51`) | Imperial ideology — representation_not_endorsement |
| Shakespeare-as-founder (`civ-51`) | Literary causation vs empire — bounded |
| Anti-civilization frame (`civ-52`) | Course frame — not full US history |
| Civil War / slavery causation (`civ-52`) | Lecture compression — external review |
| Putin/Ukraine (`civ-53`) | Live-current — not settled diagnosis |
| Dostoevsky as Russia key (`civ-53`) | Literary vs geopolitical — Tolstoy Lens guardrail |
| `sh-16` duplication | Pointer only; Tolstoy via SH not civ lecture |

---

## Next operator pick

**External-verify** Part IX bibliography (Civil War, Ukraine, Shakespeare scholarship) · **Part X** readiness inventory · **Slice 9** slimming pass.

| Slim `part-09-age-of-conscience` chapters | **Done** — `scripts/part_hybrid_slim.py --part 09` (2026-06-10) |
