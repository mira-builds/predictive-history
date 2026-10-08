# Runbook: commentary canvas upgrade (v2)

## Purpose

Migrate or refresh chapter commentaries to methodology v2 (chapter-only L0–6 + Project Canvas).

## Trigger

- `NEEDS_COMMENTARY_REVIEW` bucket
- `predictive-history commentary-status` wave queue (`migrate_from_part`, `regen_seed`, `upgrade_l2_pinned`)
- Part apparatus or v1 scaffold detected

## Inputs

- [commentary-methodology-v2.md](../commentary-methodology-v2.md)
- Scripts under `scripts/`:
  - `extract_part_section_to_chapter.py`
  - `regenerate_commentary_v2_scaffold.py`
  - `migrate_gb_stubs_to_v2.py`

## Steps

1. Read v2 SSOT and pilot chapters (`civ-07`, `gb-02`, etc.).
2. For GB stubs: `python scripts/migrate_gb_stubs_to_v2.py` (or per-id flags).
3. For Part-sourced prose: `python scripts/extract_part_section_to_chapter.py --source-id …`.
4. For seed regen wave: `python scripts/regenerate_commentary_v2_scaffold.py --wave civ` (or `--source-id`).
5. Pin-cite Layer 2 before claiming `l2_pinned` or higher maturity.
6. Run `predictive-history validate` and `predictive-history commentary-status --verbose`.

## Validation

- `scaffold_version: ph_civ_commentary_canvas_v2`
- No active `## Part apparatus` or `part_commentary_path` frontmatter
- `predictive-history validate` passes commentary canvas checks

## Stop conditions

- Transcript fidelity not reviewed — keep maturity at `scaffold`.
- Operator has not approved lifting `commentary_maturity` past scaffold.

## Curator approval

Required before marking `in_review` or `calibration` maturity.

## Output

Updated `*-commentary.md`; triage bucket shifts from `NEEDS_COMMENTARY_REVIEW` toward `OPEN_CANVAS` or `PUBLIC_READY`.
