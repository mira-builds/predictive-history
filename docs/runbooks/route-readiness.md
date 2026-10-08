# Runbook: route readiness

## Purpose

Keep the ten-route spine seed, first tour, and spine tour aligned for LLM and human readers.

## Trigger

- Choreography or seed JSON edits
- `NEEDS_ROUTE_REVIEW` on provisional gt-* chapters in triage
- `predictive-history validate` route / first-tour / llm-experience errors

## Inputs

- `data/routes/choreography.json`
- `data/routes/seed.json`
- `data/routes/first-tour.json`
- `data/routes/volume-i-spine-tour.json`
- `data/llm-experience.json`
- `docs/onboarding/first-tour.md`

## Steps

1. Edit choreography only with matching seed route order (10 unique IDs).
2. Update `first-tour.json` stops and phases to mirror seed.
3. Sync `docs/onboarding/first-tour.md` markers required by validate.
4. Align `llm-experience.json` first_tour and first_response_contract fields.
5. For provisional game-theory routes: add caveats; do not remove `review_status: provisional` without curator sign-off.
6. Run `predictive-history tour --json` and `predictive-history validate`.

## Validation

```bash
predictive-history validate
predictive-history start --json
```

## Stop conditions

- Route count ≠ 10 or duplicate source IDs — fix before publish.
- Launch copy treats provisional routes as settled scholarship.

## Curator approval

Removing `provisional` from choreography seed chapters.

## Output

Route surfaces `active`; triage clears `NEEDS_ROUTE_REVIEW` when review status and caveats are honest.
