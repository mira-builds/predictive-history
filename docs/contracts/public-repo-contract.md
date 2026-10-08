# Public Repository Contract

This repository is the public-facing distribution layer for **Predictive History**: a namespace catalog hub over lecture, essay, and interview corpora.

If a reader pastes the GitHub URL into an LLM chat, the repo should unfold from `START-HERE.md` and `data/llm-experience.json`. Those files define the provider-neutral first-tour flow, reader modes, 10-route spine seed, and guardrails for using public transcripts, commentaries, routes, and patterns.

## Public Surfaces

- **Catalog hub** — `docs/predictive-history-index.md` / `.json` (full public chapter index)
- **Corpora** — `lectures/`, `essays/`, `interviews/` (canonical chapter bodies + slice indexes)
- **Study edition** — GitHub Pages under `/predictive-history/` (see `docs/onboarding/study-edition.md`)

Legacy two-volume folders **`ph-civ/`**, **`ph-apo/`**, and **`book/`** are tombstone-only compat namespaces — not active reader roots. See [`docs/archive/deprecated-reader-namespaces.md`](../archive/deprecated-reader-namespaces.md).

## Source Of Truth Boundary

This repo publishes public-facing material, including chapter transcripts, chapter commentaries, public cards, routes, prompts, schemas, and manifests. It is not a private notes workspace and not the large artifact archive.

Canonical lecture transcripts live under `lectures/` so the public reader remains independently usable without any outside workshop storage. Chapter packets preserve the full transcript body inside the repo, even when folder READMEs render as lighter public study doorways.

The current chapter corpus was imported from the maintained Predictive History workspace and keeps that snapshot as provenance. Physical source series and folder labels are provenance metadata; the public reader architecture is the **namespace catalog hub**.

Each public chapter consists of:

- lecture transcript (or essay/interview body)
- companion commentary as an open project canvas
- public orientation/navigation metadata

Commentaries are not presumed complete at seed time. Each commentary must carry the shared Project Canvas scaffold so the chapter can be enhanced one by one without losing its role in the larger project.

## Public Growth Goals

Public reach goals belong in this repository only as strategy-facing ambitions and planning metadata. They are not proof that attention has been earned, and they are not directly completable by an agent.

When a public-growth ambition is stated, convert it into measurable project machinery:

- repo narrative and first-screen clarity
- shareable volume, chapter, spine, and route surfaces
- transcript/commentary/card readiness
- chapter study readiness
- analytics definitions and view-count boundaries
- distribution calendar and weekly review loop
- launch copy or assets staged for human approval

The canonical growth guardrail is `data/growth-goals.json`.

Surface-readiness vocabulary and triage buckets: [public-surface-status.md](public-surface-status.md) · machine rollup [`data/public-surface-triage.json`](../data/public-surface-triage.json).

Defined public-growth machinery is not the same as launch readiness. A route is launch-ready only when it can serve a first public reader without relying on private context, unsupported scholarly claims, or metric pressure to supply meaning.

The current public choreography export is `data/routes/choreography.json`. The LLM-native unfolding map is `data/llm-experience.json`; it must stay aligned with `data/routes/seed.json`, `data/cards.jsonl`, `data/patterns.json`, and `data/routes/choreography.json`.

Retired museum layer: `docs/archive/ph-mus-retired.md`.

## Human Curator Role

Human curators provide judgment that cannot be automated away: selection taste, cultural and historical balance, rights prudence, emotional calibration, representative caution, and final responsibility for why a chapter study path belongs in the public artifact.
