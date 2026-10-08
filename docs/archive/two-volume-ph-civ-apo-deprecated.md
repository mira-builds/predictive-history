# Two-volume ph-civ / ph-apo — deprecated reader frame

**Status:** Deprecated as the **primary public reader model** (2026-06).  
**Replaces:** Volume I / Volume II onboarding, `ph-civ` and `ph-apo` as foreground reader surfaces.

## What is deprecated

- **Volume I — Civilization (`ph-civ`)** and **Volume II — Apocalypse (`ph-apo`)** as the default way to introduce the repo
- Treating the repository as a **two-volume semester** (law discovery vs law application) in START-HERE, LLM bootloaders, and generated catalog intros
- Active use of [`docs/archive/two-volumes-one-reader-map.md`](./two-volumes-one-reader-map.md) for new-reader onboarding (document retained for history)

Historical chain: [`seven-volume-to-two-volume.md`](./seven-volume-to-two-volume.md) → [`two-volume-reader-order.md`](./two-volume-reader-order.md) → **namespace catalog hub** (this deprecation).

## What replaces it

**Namespace catalog hub** — primary artifact `namespace_catalog`:

| Catalog | Path |
| --- | --- |
| Full hub | [`docs/predictive-history-index.md`](../predictive-history-index.md) · [`docs/predictive-history-index.json`](../predictive-history-index.json) |
| Lectures (147) | [`lectures/predictive-history-lecture-index.md`](../../lectures/predictive-history-lecture-index.md) |
| Essays (43) | [`essays/predictive-history-essay-index.md`](../../essays/predictive-history-essay-index.md) |
| Interviews (23) | [`interviews/predictive-history-interview-index.md`](../../interviews/predictive-history-interview-index.md) |

SSOT remains [`data/cards.jsonl`](../../data/cards.jsonl). Regenerate: `ph-civ index`.

## Content retention (non-negotiable)

This deprecation changes **framing and index topology**, not corpus membership.

- All **206** public chapters remain in `cards.jsonl`, slice indexes, and the hub **full alphabetical index**
- Transcripts, commentaries, routes, Homer-to-Tolstoy spine, and first-tour content are **unchanged**
- [`docs/archive/two-volumes-one-reader-map.md`](./two-volumes-one-reader-map.md) stays available for readers who want the old law-discovery / law-application narrative

## What stays for compatibility

| Layer | Notes |
| --- | --- |
| `cards.jsonl` **`part`** | `civilization` / `world-war` / `provenance` — legacy routing metadata |
| Route **`surface`** fields | `ph-civ` / `ph-apo` on choreography and seed routes |
| **`ph-civ` CLI** | Command name unchanged (`ph-civ index`, `ph-civ link`, `ph-civ validate`) |
| **`ph-civ/` / `ph-apo/` folders** | Redirect stubs → hub + slices + this doc |
| Bilingual loop | `canonical_source: ph-civ`; zh/ru mirrors downstream |
| Generated JSON | `by_surface` and per-chapter `surface` / `volume_label` retained as **deprecated mirrors** in schema v4 |

## Out of scope (later ships)

- Removing `part` from cards
- Renaming the `ph-civ` CLI or Python package
- Deleting route surface fields
