# Public surface status

Canonical public artifact: [`mira-builds/predictive-history`](https://github.com/mira-builds/predictive-history). This repository is the reader-facing distribution layer for the two-volume ph-civ artifact (`ph-civ` + `ph-apo`).

**Authoring:** edit and push **this repository** directly. strategy-codex keeps an inbound read-only snapshot at `public/predictive-history/`. See [strategy-codex-bridge.md](strategy-codex-bridge.md).

**Machine rollups:**

- Surface inventory: [`data/public-surface-inventory.json`](../../data/public-surface-inventory.json) · `predictive-history surface-inventory`
- Per-chapter triage: [`data/public-surface-triage.json`](../../data/public-surface-triage.json) · `predictive-history surface-triage`
- Human summaries: [`runtime/artifacts/`](../runtime/artifacts/)

**Related doctrine:**

- [source-lattice.md](source-lattice.md) — evidence types (transcript, card, route, pattern)
- [commentary-methodology-v2.md](commentary-methodology-v2.md) — `commentary_maturity` ladder
- [commentary-canvas.md](commentary-canvas.md) — v1 archive pointer only

## Status vocabulary

| Status | Typical surface | Maps from existing |
|--------|-----------------|-------------------|
| `canonical` | transcript, START-HERE | source floor |
| `active` | cards, routes, patterns | in use |
| `generated` | predictive-history-index, inventory/triage JSON | regen scripts |
| `seeded` / `open_canvas` | commentary | `analysis_depth: seed`, `canvas_status: open` |
| `provisional` | ph-apo gt-* | `review_status: provisional` |
| `public_ready` | curated chapter | composite gate (see triage) |
| `review_required` | in-review cards | `review_status: in_review` |
| `deprecated` / `archived` | Part apparatus, part_tour | [archive/parts-v1-hybrid.md](archive/parts-v1-hybrid.md) |

### Deprecated labels (do not use for new work)

| Label | Replacement |
|-------|-------------|
| `thin_receipt` / `thick_synthesis` | v2 chapter-only L0–6 per [commentary-methodology-v2.md](commentary-methodology-v2.md) |
| `stub_routed` | GB migration complete; expect zero `stub_routed_to_part` rows |

## Triage buckets (per chapter)

| Bucket | Meaning |
|--------|---------|
| `PUBLIC_READY` | Stable review status, commentary maturity ≥ `l3_falsifiers`, canvas validates, folder README markers pass |
| `OPEN_CANVAS` | Open canvas with seed/scaffold depth |
| `STUB_ROUTED` | Legacy `stub_routed_to_part` (expect 0) |
| `PROVISIONAL` | Card `review_status: provisional` |
| `NEEDS_ROUTE_REVIEW` | On ten-route choreography seed but still provisional |
| `NEEDS_SOURCE_FLOOR` | Missing transcript or pin-cite L2 where drafted |
| `NEEDS_CARD_LIMITS` | Card missing required orientation sections |
| `NEEDS_COMMENTARY_REVIEW` | Part apparatus, v1 scaffold, or deprecated part routing |
| `REVIEW_WITH_CURATOR` | `in_review` with placeholder-heavy commentary |
| `UNASSIGNED` | No higher-priority bucket matched |

`predictive-history commentary-status` remains the **rebuild wave queue**; `predictive-history surface-triage` is **curator readiness**.

## CLI

```bash
predictive-history surface-inventory
predictive-history surface-inventory --check
predictive-history surface-triage
predictive-history surface-triage --verbose
predictive-history status
predictive-history validate --surfaces --check
```
