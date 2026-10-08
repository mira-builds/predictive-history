# Root Directory Map

This repository is the public **Predictive History namespace catalog hub** (`namespace_catalog`).

**Root policy:** A file or folder belongs at repository root only if it is a GitHub convention file, an LLM/agent entrypoint, a canonical corpus namespace, a machine SSOT namespace, project tooling, or an active compatibility namespace. Everything else belongs under `docs/`.

## Root entrypoints

| Path | Role |
| --- | --- |
| [`README.md`](../../README.md) | GitHub landing page |
| [`START-HERE.md`](../../START-HERE.md) | LLM/chat entrypoint (pasted GitHub URLs) |
| [`AGENTS.md`](../../AGENTS.md) | Agent/operator guardrails |
| [`llms.txt`](../../llms.txt) / [`llms-full.txt`](../../llms-full.txt) | LLM context packets |
| [`CONTRIBUTING.md`](../../CONTRIBUTING.md) | Contribution guide (GitHub convention) |
| [`LICENSE-PENDING.md`](../../LICENSE-PENDING.md) | License status note |
| [`pyproject.toml`](../../pyproject.toml) | Python project metadata |

## Canonical public corpus (do not move into `docs/`)

| Path | Role |
| --- | --- |
| [`lectures/`](../../lectures/README.md) | Video-sourced lecture chapter packets (150) |
| [`essays/`](../../essays/README.md) | Flat Substack essay bodies (43) |
| [`commentaries/`](../../commentaries/README.md) | Essay commentary canvases |
| [`interviews/`](../../interviews/README.md) | Interview provenance packets (23) |

Lecture transcripts canonicalize under `lectures/<series>/`. [`book/`](../../book/) is a deprecated compat tombstone only.

## Catalog hub

| Path | Role |
| --- | --- |
| [`docs/predictive-history-index.md`](../predictive-history-index.md) | Full human-readable catalog |
| [`docs/predictive-history-index.json`](../predictive-history-index.json) | Machine-readable catalog |

Slice indexes: [`lectures/predictive-history-lecture-index.md`](../../lectures/predictive-history-lecture-index.md) · [`essays/predictive-history-essay-index.md`](../../essays/predictive-history-essay-index.md) · [`interviews/predictive-history-interview-index.md`](../../interviews/predictive-history-interview-index.md).

## Machine source of truth

| Path | Role |
| --- | --- |
| [`data/cards.jsonl`](../../data/cards.jsonl) | Public card SSOT (216 chapters) |
| [`data/routes/`](../../data/routes/) | Route seed, first tour, choreography |
| [`data/patterns.json`](../../data/patterns.json) | Public pattern IDs |
| [`data/llm-experience.json`](../../data/llm-experience.json) | LLM unfolding map |

## Documentation tree

See [`docs/README.md`](../README.md) for contracts, methodology, migrations, onboarding, routes, localization, catalogs, archive, and runbooks.

## Reader architecture and compatibility

| Path | Role |
| --- | --- |
| [`book/`](../../book/) | Deprecated compat tombstone (no active reader root) |
| [`ph-civ/`](../../ph-civ/README.md) / [`ph-apo/`](../../ph-apo/README.md) | Deprecated reader surfaces; CLI/card compat only |

Two-volume onboarding is deprecated — [`docs/archive/two-volume-ph-civ-apo-deprecated.md`](../archive/two-volume-ph-civ-apo-deprecated.md).

## Tooling

| Path | Role |
| --- | --- |
| [`scripts/`](../../scripts/) | Intake, patch, and maintenance scripts |
| [`src/`](../../src/) | Supported `predictive-history` CLI implementation (Python package: `civ_ph`) |
| [`tests/`](../../tests/) | Pytest suite |
| [`site/`](../../site/) | Public/static site output (if active) |

Regenerate catalog: `PYTHONPATH=src python -m civ_ph.cli index` · validate: `python -m civ_ph.cli validate`.
