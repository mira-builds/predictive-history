---
part_id: part-01-dawn-of-civilization
plan_status: phase2_slimmed
scaffold_version: ph_civ_part_commentary_v1
template_from: part-08-birth-of-modernity (hybrid pilot complete)
inventory_date: 2026-06-10
---

# Part I Hybrid Apparatus — Readiness Inventory

Planning doc for extending the **Part II–VIII hybrid model** (thin chapter + thick Part commentary/bibliography) to **Part I — The Dawn of Civilization** (`civ-01`–`civ-06` + `gb-01`/`gb-03`/`gb-04` weave + `sh-11` prologue @ `civ-01`).

**Law-discovery question (registry):** How do form, religion, and destruction precede empire?

**Spine note:** `spine_slice_warning: false` — contiguous block (`civ-01`→`civ-06`). **No corridor touchpoints** in registry (origin arc precedes Homer-to-Tolstoy spine @ `civ-07`).

**Cross-Part egress:** [`civ-06`](#civ-06) collapse/generative close → [Part II `civ-07`](./part-02-hellenic-world-commentary.md#civ-07) Homer rebirth.

---

## Maturity gate (when to implement)

| Gate | Threshold | Current (2026-06-10) |
|------|-----------|----------------------|
| Chapter Layer 0–2 | All six chapters have transcript-anchored claims + `#anchor` refs | **Done** — 6 L2 claims each; pin-cite cleared |
| Chapter slimming | Willing to move Layers 3–6 to Part apparatus | **Not met** — full Layers 0–6 on all packets |
| GB weave | Registry `great_books_weave` + Part `### gb-NN` stub-route sections | **Done** — `gb-01`/`gb-03`/`gb-04`; `gb-03` dual-placement documented |
| SH prologue | `sh-11` @ `civ-01` pointer in Part commentary | **Done** — `### sh-11` pointer only |
| Validator | `volume_i_parts.py` Part I README checks | **Done** — all `civ-01`–`06` 6-step lattice |
| Part II ingress | Load-bearing back-links to Part I apparatus | **Done** — doorway + `gb-03` dual-route |

**Recommendation:** Phase 3 **complete**. Slimming deferred to Volume I final pass (Slice 9).

---

## Chapter inventory (`volume-ii/` packets)

| Chapter | Core thesis (Layer 0) | L2 claims | analysis_depth | Part section weight |
|---------|----------------------|-----------|----------------|---------------------|
| `civ-01` | Agriculture not progress; religion-led sedentism | 6 | layer2_drafted | **Thick** — opens Part law question |
| `civ-02` | Religious impulse before farming; cave/animism | 6 | layer2_drafted | **Thick** — symbolic life floor |
| `civ-03` | Peaceful/egalitarian/artistic default; animist model | 6 | layer2_drafted | **Thick** — religious imagination |
| `civ-04` | Gimbutas Old Europe; conquest vs diffusion | 6 | layer2_drafted | **Thick** — paradise-lost hinge |
| `civ-05` | Yamnaya pastoral conquest; sky-father religion | 6 | layer2_drafted | **Thick** — patriarchy/war turn |
| `civ-06` | Bronze Age collapse; elite overproduction | 6 | layer2_drafted | **Thick** — generative destruction close |

**Pin-cite debt:** **Cleared** (2026-06-10) — `scripts/part_i_pin_cite_prep.py`; all six chapters sectioned.

---

## Great Books weave

| GB | Anchor(s) | Role | Part I placement |
|----|-----------|------|------------------|
| `gb-01` | `civ-01` | interwoven | **`### gb-01` stub-route** — Secrets of the Universe threshold |
| `gb-03` | `civ-02` (Part I); `civ-07` (Part II support_ring) | interwoven + support_ring_optional | **`### gb-03` stub-route** — dual-placement documented |
| `gb-04` | `civ-03` | interwoven | **`### gb-04` stub-route** — Conscious Universe @ religious imagination |

**Dual-placement law (`gb-03`):** Part I interwoven @ `civ-02` (religion/dawn weave); Part II `support_ring_optional` @ `civ-07` (Homer trilogy closer). Canonical close-read lives in [Part II `### gb-03`](./part-02-hellenic-world-commentary.md#gb-03); Part I section is **pointer + origin-context delta**, not a second apparatus.

---

## Secret History companion

| SH | Anchor | Role | Part I placement |
|----|--------|------|------------------|
| `sh-11` | `civ-01` | prologue | **`### sh-11` pointer** — prologue companion; full packet under `lectures/secret-history/sh-11/` |

---

## Part I artifacts

| Artifact | Status (2026-06-10) |
|----------|---------------------|
| `part-01-dawn-of-civilization-commentary.md` | **Phase 3 complete** — `civ-01`–`06` + gb/sh pointers |
| `part-01-dawn-of-civilization-bibliography.md` | **Phase 3** — `supports:`/`counters:` for `civ-01`–`06` |
| `volume-i-parts.json` `commentary_path` / `bibliography_path` | **Wired** |
| `part-01-dawn-of-civilization.md` Apparatus block | **Done** |
| `PART-01-HYBRID-READINESS.md` | **Done** — this inventory |
| Pin-cite `civ-01`–`06` | **Done** — `scripts/part_i_pin_cite_prep.py` |
| README 6-step lattice + Part links | **Done** — all `civ-01`–`06` |
| Part II ingress back-links | **Done** |
| `volume-i-anchors.yaml` `civ-01`–`06` | **Done** |

---

## Cross-Part egress (to Part II)

| Prediction | Strength | Status (2026-06-10) | Part II test |
|------------|----------|---------------------|--------------|
| Religion-first origin arc carries into Homer rebirth | C | **Partially supported** | `civ-07` post-collapse creativity |
| Yamnaya/conquest turn sets up Indo-European epic inheritance | C | **Partially supported** | `civ-07`/`gb-02` grammar |
| Collapse generative → Greek civilization rebirth | C | **Partially supported** | `civ-07` Bronze Age collapse recap |
| `gb-03` Part I anchor @ `civ-02` pairs Part II support ring @ `civ-07` | E | **Partially supported** | dual-placement cross-link |
| Part II has no corridor requiring Part I corridor (none) | E | **Confirmed** | registry `corridor_touchpoints: []` |

---

## Phased rollout

### Phase 0 — Inventory — **Done** (2026-06-10)

### Phase 1 — Apparatus seed — **Done**

### Phase 2 — Pin-cite + README lattice — **Done** (2026-06-10)

### Phase 3 — Validator + synthesis close — **Done** (2026-06-10)

- Ledger, bibliography, Part II link reconcile (no Part I corridor)

---

## Risks / counter-readings to front-load

| Topic | Note |
|-------|------|
| Religion-first agriculture (`civ-01`) | Scholarly debate; coercion/war families named but rejected in lecture |
| Gimbutas Old Europe (`civ-04`) | Contested; DNA update ≠ full ideological vindication |
| Conquest/genocide framing (`civ-04`/`civ-05`) | Sensitive; representation_not_endorsement |
| Elite overproduction (`civ-06`) | Turchin/Piketty borrow — lecture hypothesis |
| `gb-03` dual placement | Avoid duplicate Poets/Prophets apparatus in Part I |

---

## Out of scope (Part I pilot)

- Part I corridor rows (none in registry) · full GB close-read in Part I (stub-route only) · `sh-11` thick section · slim chapter commentaries

| Slim `part-01-dawn-of-civilization` chapters | **Done** — `scripts/part_hybrid_slim.py --part 01` (2026-06-10) |
