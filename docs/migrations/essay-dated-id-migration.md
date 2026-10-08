# Essay dated-ID migration (2026-06-26)

## Summary

All 43 public essay packets migrated from sequential **`essay-NN`** to **`essay-YYYY-MM-DD-{substack-slug}`**, matching the interview namespace pattern.

## Hard cut

- **Canonical `source_id`:** dated pattern only.
- **Legacy `essay-NN`:** crosswalk in [`data/essays/manifest.json`](../data/essays/manifest.json) only — no CLI aliases, no redirect stubs.
- **Old GitHub folder URLs** such as `https://github.com/mira-builds/predictive-history/tree/main/essays/essay-07` **404** after this change.
- **Substack URLs** (`predictivehistory.substack.com/p/{slug}`) are unchanged.

## Operator commands

```bash
python scripts/rename_essays_to_dated_ids.py   # one-time; already applied
PYTHONPATH=src python -m civ_ph.cli index --force
PYTHONPATH=src python -m civ_ph.cli validate
```

## New intakes

[`scripts/intake_essays_phase2.py`](../scripts/intake_essays_phase2.py) emits dated IDs from `publication_date` + `substack_slug`. Check manifest for same-day collisions before landing.

## Flat layout (2026-06-26)

Essay bodies and commentaries split across two root namespaces (no per-essay subfolders):

| Artifact | Path |
| --- | --- |
| Essay body | `essays/{source_id}.md` |
| Commentary | `commentaries/{source_id}-commentary.md` |

```bash
python scripts/flatten_essays_layout.py   # one-time; already applied
```

Old GitHub tree URLs `…/essays/{source_id}/` **404** after this cut. Use blob URLs from `ph-civ link {source_id}` for essays.
