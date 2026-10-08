# Runbook: chapter study readiness

## Purpose

Bring one chapter folder to a trustworthy public study doorway: transcript source floor, open commentary canvas, card lattice, and folder README markers.

## Trigger

- New or refreshed chapter folder
- `NEEDS_SOURCE_FLOOR` or README marker failures in `predictive-history validate`
- Curator wants a shareable GitHub folder link

## Inputs

- `source_id` and paths from `data/cards.jsonl`
- Transcript under `lectures/` or chapter folder
- Companion `*-commentary.md`

## Steps

1. Confirm transcript file exists and frontmatter includes `source_url` when a public video exists.
2. Open or regen commentary per [commentary-canvas-upgrade.md](commentary-canvas-upgrade.md).
3. Verify card sections: Where This Sits, Reading Posture, Historical Pressure Points, Limits of the Frame, Return Path.
4. Ensure folder `README.md` includes study doorway markers and source video block when applicable.
5. Run `predictive-history link <source_id>` for paste-ready packet.
6. Regen `predictive-history index` and `predictive-history surface-triage`.

## Validation

```bash
predictive-history validate
predictive-history surface-triage --verbose
```

## Stop conditions

- Missing transcript body or unverifiable video URL — stop; do not claim public_ready.
- Commentary still routes to Part apparatus — migrate to v2 first.

## Curator approval

Final judgment on whether the chapter deserves public folder links in distribution.

## Output

Chapter row moves toward `PUBLIC_READY` or `OPEN_CANVAS` in `data/public-surface-triage.json`.
