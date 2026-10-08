# Deprecated reader namespaces

These top-level folders are **tombstone-only** compatibility namespaces. They are not active public reader roots.

| Namespace | Retired | Replacement |
|---|---|---|
| [`book/`](../../book/README.md) | 2026-06 | Namespace catalog hub — [`docs/predictive-history-index.md`](../predictive-history-index.md) |
| [`ph-civ/`](../../ph-civ/README.md) | 2026-06 | Same hub + [`lectures/`](../lectures/README.md) · [`essays/`](../essays/README.md) · [`interviews/`](../interviews/README.md) |
| [`ph-apo/`](../../ph-apo/README.md) | 2026-06 | Same hub + root corpora |

## What moved where

- **Chapter bodies** — `lectures/<series>/`, `essays/`, `interviews/`
- **Public orientation** — `data/cards.jsonl`, `data/cards/*.md`, slice indexes under each corpus
- **Volume I part apparatus** — [`docs/routes/volume-i-parts/`](../routes/volume-i-parts/README.md) (not the same as deprecated card `part` filters)
- **Two-volume reader order (archive)** — [`two-volume-reader-order.md`](two-volume-reader-order.md), [`two-volume-ph-civ-apo-deprecated.md`](two-volume-ph-civ-apo-deprecated.md)

## Migration program

Full CLI/metadata/Pages cutover: [`../migrations/PH-SURFACE-RETIREMENT.md`](../migrations/PH-SURFACE-RETIREMENT.md).

## Do not

- Add new canonical paths under `book/`, `ph-civ/`, or `ph-apo/` (except tombstone README updates)
- Treat GitHub tree links to old stub paths as current architecture — use the catalog hub or lectures packet README
