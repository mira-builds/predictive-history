# Volume I — Reading Parts

Volume I part apparatus (doorways, commentary, bibliographies). **Not the namespace catalog hub** — start at [`docs/predictive-history-index.md`](../../predictive-history-index.md).

Interwoven reader order (historical): [`two-volume-reader-order-interwoven.md`](../../archive/two-volume-reader-order-interwoven.md)

Ten **Part doorways** overlay the [interwoven civilization spine](../../archive/two-volume-reader-order-interwoven.md). Each Part is a contiguous spine slice (`civ-*` chapters plus woven companions) — not a reordering of the spine.

**Registry:** [`data/parts/volume-i-parts.json`](../../../data/parts/volume-i-parts.json)

**Scaffold:** `python scripts/scaffold_part_doorway.py` (from repo root)

**Validate:** `python scripts/validate_volume_i_parts.py`

**Pin-cite discipline:** [`docs/methodology/PIN-CITE-DISCIPLINE.md`](../../../docs/methodology/PIN-CITE-DISCIPLINE.md) — transcript `###` rails + Layer-2 `#anchor` refs (Parts II–VI sweep scripts).

## Parts I–X

| Part | Title | Chapters | Doorway |
|------|-------|----------|---------|
| I | The Dawn of Civilization | `civ-01`–`06` | [part-01-dawn-of-civilization.md](part-01-dawn-of-civilization.md) · [commentary](part-01-dawn-of-civilization-commentary.md) |
| II | The Hellenic World | `civ-07`–`13` | [part-02-hellenic-world.md](part-02-hellenic-world.md) |
| III | The Roman Imperium | `civ-14`–`17` | [part-03-roman-imperium.md](part-03-roman-imperium.md) |
| IV | The Ancient Foundations | `civ-18`–`23` | [part-04-ancient-foundations.md](part-04-ancient-foundations.md) |
| V | Christianity and Islam | `civ-24`–`28` | [part-05-christianity-and-islam.md](part-05-christianity-and-islam.md) |
| VI | The Medieval Imagination | `civ-29`–`34` | [part-06-medieval-imagination.md](part-06-medieval-imagination.md) |
| VII | The World After Rome | `civ-35`–`41` | [part-07-world-after-rome.md](part-07-world-after-rome.md) |
| VIII | The Birth of Modernity | `civ-42`–`50` | [part-08-birth-of-modernity.md](part-08-birth-of-modernity.md) |
| IX | The Age of Conscience | `civ-51`–`53` | [part-09-age-of-conscience.md](part-09-age-of-conscience.md) |
| X | The Rise of the Nation-State | `civ-54`–`60` | [part-10-rise-of-the-nation-state.md](part-10-rise-of-the-nation-state.md) |

### Index subtitles

| Part | Subtitle |
|------|----------|
| VI | Dante and Roman imagination through Holy Roman fiction |
| VII | Eurasian orders after Rome; Dante returns at close |
| VIII | Reformation through Britannia; plato-to-hegel modernity rupture |
| IX | Shakespeare through Dostoevsky; homer-to-tolstoy steps 4–5; civ-to-apocalypse ingress |
| X | Nation-state through American close; plato-to-hegel + Apocalypse exit |

## Reading law

- Open the **interwoven spine** for canonical order; use Part doorways for law-discovery questions, companion weave, and corridor links.
- **Part** here ≠ lecture transcript "Part I / Part II" ≠ CIV-STATE Part 1/2/3.

## Part apparatus (hybrid commentary pilot)

When a Part has thick synthesis, use three sibling files:

| File | Role |
|------|------|
| `part-NN-{slug}.md` | Doorway — navigation, weave, corridors |
| `part-NN-{slug}-commentary.md` | Thick synthesis — prediction ledger, gb sections, counter-readings |
| `part-NN-{slug}-bibliography.md` | External sources — tagged `supports: civ-NN` / `gb-NN` |

**Hybrid pilot:** Part I (`civ-01`–`06`, `gb-01`/`gb-03`/`gb-04`, `sh-11` @ `civ-01`) — **Phase 3 complete** (2026-06-10): all six chapters pin-cited; ledger/Part II ingress closed; `scripts/part_i_pin_cite_prep.py`; [part-01-dawn-of-civilization-commentary.md](part-01-dawn-of-civilization-commentary.md), [PART-01-HYBRID-READINESS.md](PART-01-HYBRID-READINESS.md). Part II + Part III + Part IV + Part V + Part VI — **complete** through Phase 3; Part II–III pin-cite **Cleared**. Part V — [PART-05-HYBRID-READINESS.md](PART-05-HYBRID-READINESS.md). Part VI (`civ-29`–`34`, `gb-09`–`gb-12`) — Phase 3 validator/docs **Done** (2026-06-09): [part-06-medieval-imagination-commentary.md](part-06-medieval-imagination-commentary.md), [PART-06-HYBRID-READINESS.md](PART-06-HYBRID-READINESS.md). Part VII (`civ-35`–`41`, `gb-10` @ `civ-41`) — **Phase 3 complete** (2026-06-09): all seven chapters pin-cited; ledger/corridor/bib synthesis closed; `scripts/part_vii_pin_cite_prep.py`; [part-07-world-after-rome-commentary.md](part-07-world-after-rome-commentary.md), [PART-07-HYBRID-READINESS.md](PART-07-HYBRID-READINESS.md). Part VIII (`civ-42`–`50`) — **Phase 3 complete** (2026-06-10): all nine chapters pin-cited; ledger/corridor/bib synthesis closed; `scripts/part_viii_pin_cite_prep.py`; [part-08-birth-of-modernity-commentary.md](part-08-birth-of-modernity-commentary.md), [PART-08-HYBRID-READINESS.md](PART-08-HYBRID-READINESS.md). Part IX (`civ-51`–`53`, `sh-16` @ `civ-53`) — **Phase 3 complete** (2026-06-10): all three chapters pin-cited; `sh-16` pointer; ledger/corridor/bib synthesis closed; `scripts/part_ix_pin_cite_prep.py`; [part-09-age-of-conscience-commentary.md](part-09-age-of-conscience-commentary.md), [PART-09-HYBRID-READINESS.md](PART-09-HYBRID-READINESS.md). Part X (`civ-54`–`60`) — **Phase 3 complete** (2026-06-10): all seven chapters pin-cited; plato-to-hegel + civilization-to-apocalypse exit closed; `scripts/part_x_pin_cite_prep.py`; [part-10-rise-of-the-nation-state-commentary.md](part-10-rise-of-the-nation-state-commentary.md), [PART-10-HYBRID-READINESS.md](PART-10-HYBRID-READINESS.md). **Volume I hybrid pilot (Parts I–X): complete** through Phase 3 + Phase 2 slim (2026-06-10). Pin-cite manifest: [`data/pin-cite/volume-i-anchors.yaml`](../../../data/pin-cite/volume-i-anchors.yaml) · [`docs/methodology/pin-cite-manifest-index.md`](../../../docs/methodology/pin-cite-manifest-index.md).

Registry fields (optional per part): `commentary_path`, `bibliography_path` in [`volume-i-parts.json`](../../../data/parts/volume-i-parts.json).

## Part boundary tour

Machine-readable ten-stop tour: [`data/routes/part-boundary-tour.json`](../../../data/routes/part-boundary-tour.json) (complements [`ten_route_spine_seed`](../../../data/routes/seed.json)).
