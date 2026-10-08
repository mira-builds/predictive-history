# PH-LECTURES — lecture packet recanonicalization

**Date:** 2026-06-26  
**Script:** [`scripts/relocate_lectures_to_series.py`](../scripts/relocate_lectures_to_series.py)

## What moved

All lecture chapter packets (transcript + commentary + orientation where present) now live under:

| Series | Path |
| --- | --- |
| `civilization` | `lectures/civilization/civ-*` |
| `great-books` | `lectures/great-books/gb-*` |
| `geo-strategy` | `lectures/geo-strategy/geo-*` (normalized from flat `book/volume-i/` files) |
| `game-theory` | `lectures/game-theory/gt-*` |
| `secret-history` | `lectures/secret-history/sh-*` |

**147** cataloged lecture cards in `data/cards.jsonl` point at `lectures/` (including **gt-29**). Total public card count: **206**.

**Catalog:** lectures slice [`lectures/predictive-history-lecture-index.md`](../lectures/predictive-history-lecture-index.md) · full hub [`docs/predictive-history-index.md`](predictive-history-index.md) (machine JSON colocated in `docs/`).

## Legacy compat

Redirect README stubs remain at:

- `book/volume-ii/civ-*`, `book/volume-v/gb-*`, `book/volume-vi/sh-*`
- `book/volume-i/geo-*` (folder redirect per chapter)
- `book/volume-iii/gt-*` (duplicate dedupe)
- `ph-civ/chapters/gt-*`, `ph-apo/chapters/gt-*`

Staged book wrappers under `lectures/` and `lectures/` now link to `lectures/` as the canonical packet.

## Verify

```bash
python scripts/relocate_lectures_to_series.py --dry-run   # no-op check
PYTHONPATH=src python -m civ_ph.cli index --force
PYTHONPATH=src python -m civ_ph.cli validate
python -m pytest
```
