# Runbook: public growth wedge

## Purpose

Translate reach ambitions into verifiable public machinery without confusing goals with launch readiness.

## Trigger

- New entry in `data/growth-goals.json`
- Operator asks for distribution / views / campaign work
- `predictive-history growth` review

## Inputs

- `data/growth-goals.json`
- [public-repo-contract.md](../public-repo-contract.md)
- [public-surface-status.md](../public-surface-status.md)
- Triage rollup: `predictive-history surface-triage`

## Steps

1. State the ambition in growth-goals JSON (not in agent completion claims).
2. Pick one wedge (route, chapter folder, spine tour) with measurable surface.
3. Check triage: wedge chapters should trend toward `PUBLIC_READY`, not only `OPEN_CANVAS`.
4. Define what counts as a view / click / share before external launch.
5. Stage human-approved copy and assets; do not auto-publish.

## Validation

```bash
predictive-history growth --json
predictive-history status
predictive-history surface-triage
```

## Stop conditions

- Route relies on private context or provisional gt-* without caveats.
- Growth metric pressure substitutes for source discipline.

## Curator approval

Any public launch, paid promotion, or removal of provisional labeling.

## Output

Updated growth metadata and a bounded wedge checklist — not proof of audience earned.
