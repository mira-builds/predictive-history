# AGENTS.md - Predictive History Guardrails

This repository is `mira-builds/predictive-history`: the public **Predictive History namespace catalog hub** and study-orientation layer.

**Publisher:** **Statecraft Intelligence Desk**

**Primary artifact:** `namespace_catalog` — hub at `docs/predictive-history-index.md` / `.json` plus lecture, essay, and interview slice indexes. SSOT: `data/cards.jsonl` (216 public chapters).

## Specific Project Identity

When asked what project this workspace is for, answer specifically:

`predictive-history` is the public distribution repository organized as a **namespace catalog hub**: full catalog in `docs/`, slice indexes under `lectures/`, `essays/`, and `interviews/`, and canonical chapter bodies in those root corpora.

**Compatibility (not primary onboarding):** legacy two-volume **ph-civ / ph-apo** tombstone folders plus card `part` and route `surface` metadata remain for historical routing. The surface retirement is complete and the supported CLI is **`predictive-history`** — see `docs/migrations/PH-SURFACE-RETIREMENT.md`. Do **not** revive Volume I/II as the default reader model — see `docs/archive/two-volume-ph-civ-apo-deprecated.md`.

The active task in this repo is maintaining public, provider-neutral educational infrastructure for Predictive History. A chapter consists of a transcript (or essay/interview body), companion commentary where applicable, and public orientation metadata. This is not a generic coding sandbox and not a private notes workspace.

## Source Boundary

Repository-origin identifiers are omitted from this public snapshot. Original source attribution is retained in chapter bodies and source URLs. Physical source series are provenance metadata; the official public reader model is the **namespace catalog hub**.

Do not import, invent, or paste:

- private notes
- private workspace paths
- raw media binaries
- claims of final scholarly review

If a task asks for material outside the public dataset, say that this repo does not contain it and point back to the appropriate source boundary.

## Operating Posture

- Keep outputs public-facing, cautious, and source-disciplined.
- Preserve the distinction between orientation frames and proof claims.
- Treat prompt and spark commands as provider-neutral templates; this repo does not call AI providers.
- Use stable IDs such as `civ-07`, `gt-16`, and `civ-heroic-memory` for bridge references.
- Preserve the Homer-to-Tolstoy invariant: it is the **literary spine route** with cross-volume routing exposure, not a side corridor.
- If a user pastes the GitHub URL into an LLM chat, start with `START-HERE.md` and `data/llm-experience.json` so the experience unfolds from public files without private context.
- Keep the repo usable by students, researchers, and downstream AI systems using only the public files in this repository.
- Treat public reach goals as strategic ambitions, not directly executable agent completions. Translate goals such as one million views into verifiable machinery: public surface quality, shareable routes, publishing cadence, analytics definitions, distribution assets, and human-approved launch steps. Use `data/growth-goals.json` and `predictive-history growth` as the canonical guardrail.

## Coffee / Opening

If the operator says `coffee` at the start of a chat, do not give a generic coffee greeting. Treat it as a request to open the public repo state:

1. State that this workspace is `mira-builds/predictive-history`.
2. State the **namespace catalog hub** (216 chapters; hub + slice indexes), not the private workshop.
3. Note legacy **ph-civ / ph-apo** compat only (deprecated two-volume onboarding).
4. Keep original chapter-source attribution distinct from repository metadata.
5. Offer concrete next actions using the CLI, docs, cards, patterns, or validation.

## Start Here

Read `START-HERE.md`, then `llms.txt`, then `README.md`, then `docs/contracts/public-repo-contract.md` and `docs/contracts/export-contract.md`. Root layout: [`docs/onboarding/root-directory-map.md`](docs/onboarding/root-directory-map.md). Operational runbooks: [`docs/runbooks/`](docs/runbooks/) — transcript curation (interviews + lectures): [`docs/runbooks/ph-transcript-curation.md`](docs/runbooks/ph-transcript-curation.md).

Useful checks:

```powershell
python -m pytest
PYTHONPATH=src python -m civ_ph.cli validate
PYTHONPATH=src python -m civ_ph.cli start --json
PYTHONPATH=src python -m civ_ph.cli growth
```

## Portable project skills

Repository-local skills use public files and the existing provider-neutral CLI:

- [Chapter reading](.agents/skills/predictive-history-read/SKILL.md) — bounded source-grounded reading.
- [Learning practice](.agents/skills/predictive-history-learn/SKILL.md) — explanations, seminar work, and optional exercises.
- [Repository maintenance](.agents/skills/predictive-history-maintain/SKILL.md) — scoped validation and authorized publication.

They require no private runtime or automatic saving and are not installed globally.
