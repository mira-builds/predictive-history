# Runbook: source lattice review

## Purpose

Review a chapter or card using source-floor-first discipline for LLM and human readers.

## Trigger

- LLM reader pasted a chapter URL
- `NEEDS_SOURCE_FLOOR` in triage
- Strategy-facing cite needs public `source_id` grounding

## Inputs

- [source-lattice.md](../source-lattice.md)
- Transcript (canonical source floor)
- Card (`data/cards/<source_id>.md`)
- Commentary canvas
- Optional `pattern_id` bridges

## Steps

1. Read transcript before commentary or card synthesis.
2. Classify claims: transcript-backed vs orientation frame vs open canvas TBD.
3. Check pin-cite Layer 2 table when `layer2_drafted` or maturity ≥ `l2_pinned`.
4. Use patterns as orientation aids only — pair with `source_id` and limits.
5. Record falsifiers in Layer 3 when upgrading maturity.

## Validation

- No unsupported live-event claims from seed commentary alone
- `predictive-history show <source_id>` sections present
- `predictive-history bridge <source_id>` if pattern routing applies

## Stop conditions

- Transcript missing or empty — do not synthesize from card alone for proof claims.

## Curator approval

Upgrading public copy that implies scholarly finality.

## Output

Source-disciplined reading notes; optional commentary maturity bump after pin-cite pass.
