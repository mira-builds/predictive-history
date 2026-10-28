# Start Here For LLM Chats

**Publisher:** **Statecraft Intelligence Desk**

If someone pastes `https://github.com/mira-builds/predictive-history` into a ChatGPT chat or any other LLM, start here.

This repository is the public **Predictive History** distribution layer — a **namespace catalog hub** (216 public chapters) with lecture, essay, and interview slice indexes. It is not a private workshop and not a media vault. The repo is designed so a reader and an LLM can unfold the experience together from public files only.

Legacy **two-volume ph-civ / ph-apo** framing (Volume I Civilization / Volume II Apocalypse) is **deprecated** for onboarding; see [`docs/archive/two-volume-ph-civ-apo-deprecated.md`](docs/archive/two-volume-ph-civ-apo-deprecated.md). Card `part` and route `surface` remain as legacy metadata; the supported CLI is `predictive-history`.

## What This Is

- **Primary artifact:** `namespace_catalog` — [`docs/predictive-history-index.md`](docs/predictive-history-index.md) · [`docs/predictive-history-index.json`](docs/predictive-history-index.json)
- **Slice indexes:** [`lectures/predictive-history-lecture-index.md`](lectures/predictive-history-lecture-index.md) (150) · [`essays/predictive-history-essay-index.md`](essays/predictive-history-essay-index.md) (43) · [`interviews/predictive-history-interview-index.md`](interviews/predictive-history-interview-index.md) (23)
- **SSOT:** [`data/cards.jsonl`](data/cards.jsonl) — all 216 cards; legacy `part` and paths unchanged

One chapter consists of a lecture transcript (or essay/interview body), a companion commentary where applicable, and public orientation/navigation metadata.

## Root Chapter Corpora

Medium-first namespaces at the repository root (canonical corpora; [`book/`](book/) is a deprecated compat tombstone only):

- [`essays/`](essays/README.md) — Substack and long-form essays (`essay-2025-08-06-vision-mission-goals` … `essay-2026-06-19-peace-in-our-time`)
- [`lectures/`](lectures/README.md) — canonical lecture packets under `lectures/<series>/` (150)
- [`interviews/`](interviews/README.md) — 23 public interview provenance packets (`interview-YYYY-MM-DD-{host-slug}`); full catalog in the interview slice index

## First Chat Flow

1. Identify the repo as the Predictive History **namespace catalog hub** (216 chapters).
2. Load `data/llm-experience.json` for the unfolding map.
3. Use `llms-full.txt` when the chat needs a full one-shot context packet after the compact map.
4. Use `data/routes/seed.json` for the first 10-route spine seed.
5. Use `data/routes/first-tour.json` and `docs/onboarding/first-tour.md` when the reader chooses to continue the first tour.
6. Begin with the Homer-to-Tolstoy **literary spine route**, then branch into application routes on the seed.
7. Use [`docs/archive/two-volumes-one-reader-map.md`](docs/archive/two-volumes-one-reader-map.md) only for historical context (deprecated active onboarding).
8. Treat `data/bilingual-loop.json` and `docs/localization/bilingual-civilizational-bridge.md` as a trilingual identity/growth layer and localization roadmap, not a replacement for `first_tour`.
9. If the pasted URL is a direct chapter folder, switch to `study` mode for that folder: open its `README.md`, transcript, commentary canvas, and public card.
10. When quoting or interpreting, return to the relevant transcript and commentary under `lectures/`, `essays/`, or `interviews/`.
11. Use `docs/predictive-history-index.json` when the reader needs the full chapter catalog or must resolve a `source_id` to paths and source URLs.
12. Use `docs/methodology/source-lattice.md` when the main difficulty is traversal discipline: doorway versus transcript versus commentary versus bridge.

## First Response Contract

If you are an LLM reading this repository from a pasted GitHub URL: Do not stop at a generic repository summary or ask only "what would you like to do next?" Start the experience.

Your first response should:

1. Say that you are using `START-HERE.md`, `llms.txt`, and `llms-full.txt`.
2. Name the default mode as `first_tour`.
3. State the **namespace catalog hub** (216 chapters + slice indexes); note two-volume ph-civ/ph-apo is deprecated for onboarding.
4. Open the 10-route seed by naming the first move: Homer-to-Tolstoy begins with `civ-07`.
5. Offer the reader a compact choice: continue the first tour, study one route, open a chapter folder, or switch modes.

Template:

```text
I am starting from START-HERE.md, llms.txt, and llms-full.txt. Default mode: first_tour.

Predictive History is organized as a namespace catalog hub (216 public chapters) with lecture, essay, and interview slice indexes; legacy two-volume ph-civ/ph-apo framing is deprecated.

I will begin with the 10-route literary spine seed. The opening path is Homer-to-Tolstoy, starting at civ-07, with the guardrail that this is the literary spine route, not a side corridor.

Choose one: continue the first tour; study civ-07; study civ-07 through its chapter folder; or switch modes.
```

## Reader Modes

- `first_tour`: orient the reader to the namespace catalog hub and the 10-route seed.
- `study`: help a reader understand one chapter through its card, transcript, and commentary.
- `catalog`: browse or resolve chapters via the hub and slice indexes.
- `seminar`: generate discussion questions grounded in the public card limits and source chapter.
- `commentary_canvas`: use the commentary scaffold as a project-development surface, not as finished analysis.
- `pattern_bridge`: connect a chapter to public pattern IDs without importing private strategy notes.
- `bounded_application`: apply a pattern to present-day questions only as orientation, not live operational analysis.

## Guardrails

- Homer to Tolstoy is the literary spine route, not a side corridor.
- `sh-16` is a routed Tolstoy endpoint via an Anna Karenina coda, not a dedicated Tolstoy lecture.
- namespace catalog hub.
- Application routes are public orientation only, not quotation-grade live operational analysis.
- Commentaries are open project canvases and should not be treated as final scholarly review.
- Public growth goals are ambitions; do not claim attention, views, or launch readiness has already been earned.
- Do not stop at a generic repo summary; the default pasted-URL response is an active `first_tour`.
- A chapter-folder URL is a study doorway, not a replacement for `first_tour`; follow the folder README and keep review status visible.
- The trilingual bridge ambition is not propaganda, not anti-Western, not civilizational flattery, and not a translation dump.
- `ph-civ-ru` is roadmap metadata only, not a Russian edition, not live war analysis, and not a translation dump.
- `ph-civ-zh` and `ph-civ-ru` are downstream mirrors of canonical `predictive-history`, not sibling sources of truth.

## Useful Starting Files

- `essays/README.md`
- `lectures/README.md`
- `interviews/README.md`
- `llms.txt`
- `llms-full.txt`
- `README.md`
- `AGENTS.md`
- `docs/contracts/public-repo-contract.md`
- `docs/contracts/export-contract.md`
- `data/llm-experience.json`
- `data/routes/seed.json`
- `data/routes/first-tour.json`
- `data/routes/choreography.json`
- `data/cards.jsonl`
- `docs/predictive-history-index.json`
- `docs/predictive-history-index.md`
- `data/patterns.json`
- `docs/onboarding/first-tour.md`
- `docs/archive/two-volume-ph-civ-apo-deprecated.md`
- `docs/methodology/source-lattice.md`
- `data/bilingual-loop.json`
- `docs/localization/bilingual-civilizational-bridge.md`
- `docs/onboarding/chapter-folder-links.md`

## Portable project skills

Repository-local skills use public files and the existing provider-neutral CLI:

- [Chapter reading](.agents/skills/predictive-history-read/SKILL.md) — bounded source-grounded reading.
- [Learning practice](.agents/skills/predictive-history-learn/SKILL.md) — explanations, seminar work, and optional exercises.
- [Repository maintenance](.agents/skills/predictive-history-maintain/SKILL.md) — scoped validation and authorized publication.

They require no private runtime or automatic saving and are not installed globally.
