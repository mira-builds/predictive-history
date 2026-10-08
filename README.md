# Predictive History Public Repository

**Publisher:** **Statecraft Intelligence Desk**

For AI agents and new chats: start with `START-HERE.md`, then `AGENTS.md` and `llms.txt`. If a user pastes `https://github.com/mira-builds/predictive-history` into an LLM chat, use `START-HERE.md`, `data/llm-experience.json`, and `llms-full.txt` as the unfolding map and one-shot context packet. Do not stop at a generic repository summary or "what would you like to do next?" response; begin the `first_tour` through the 10-route spine seed unless the reader chooses another mode. If a user pastes a direct chapter-folder URL, treat that folder as `study` mode: open its `README.md`, transcript, commentary canvas, and public card. This repo is the public Predictive History distribution layer, not the private editorial workshop.

## Primary reader model: namespace catalog hub

**Primary artifact:** `namespace_catalog` — full hub at [`docs/predictive-history-index.md`](docs/predictive-history-index.md) and [`docs/predictive-history-index.json`](docs/predictive-history-index.json) (**216** public chapters).

| Slice | Index | Count |
| --- | --- | ---: |
| Lectures | [`lectures/predictive-history-lecture-index.md`](lectures/predictive-history-lecture-index.md) | 150 |
| Essays | [`essays/predictive-history-essay-index.md`](essays/predictive-history-essay-index.md) | 43 |
| Interviews | [`interviews/predictive-history-interview-index.md`](interviews/predictive-history-interview-index.md) | 23 |

SSOT: [`data/cards.jsonl`](data/cards.jsonl). Regenerate indexes: `predictive-history index`.

**Deprecated (metadata only):** two-volume **ph-civ / ph-apo** reader frame — see [`docs/archive/two-volume-ph-civ-apo-deprecated.md`](docs/archive/two-volume-ph-civ-apo-deprecated.md). Card `part` and route `surface` remain for historical routing; the supported CLI is `predictive-history`.

**Root layout:** [`docs/onboarding/root-directory-map.md`](docs/onboarding/root-directory-map.md)

It also contains the chapter body for each source item. In this repo, one chapter consists of the lecture transcript, companion commentary, and public orientation/navigation metadata. The package lets students and AI systems explore historical placement, reading posture, pressure points, limits, return paths, and guided prompts alongside the chapter text.

This package is independent educational infrastructure. It is not official course material, not endorsement, and not a substitute for the source lectures, transcripts, commentary, or external verification.

The repo also carries a trilingual civilizational bridge ambition: English, Chinese, and Russian readerships can reinforce each other by reading the Western canon, historical pattern, and modern crisis through the same source-bounded route system. This is ambition metadata, not a Chinese or Russian translation launch. Both `ph-civ-zh` and `ph-civ-ru` would be downstream mirrors of canonical `ph-civ`, not sibling sources of truth; see `docs/localization/bilingual-civilizational-bridge.md`.

## Repository Role

This repo is the public distribution layer. It should contain public cards, public navigation, schemas, prompts, contribution instructions, generated manifests, and small text metadata.

It should not become the large-media vault. Large media archives stay outside Git; this repo tracks transcripts, commentaries, cards, routes, and study navigation.

## Root Chapter Corpora

Medium-first chapter namespaces at the repository root (with deprecated `book/`, `ph-civ/`, and `ph-apo/` tombstones retained only for migration orientation):

- [`essays/`](essays/README.md) — flat Substack essay bodies (`essay-YYYY-MM-DD-{slug}.md`)
- [`commentaries/`](commentaries/README.md) — essay commentary canvases (`essay-*-commentary.md`; lectures/interviews unchanged)
- [`lectures/`](lectures/README.md) — canonical lecture chapter packets under `lectures/<series>/` (150)
- [`interviews/`](interviews/README.md) — 23 public interview provenance packets (`interview-YYYY-MM-DD-{host-slug}`); catalog in the interview slice index

## What Is Included

- 216 public cards in `data/cards.jsonl` — 150 lectures, 43 Substack essays (`essay-2025-08-06-vision-mission-goals` … `essay-2026-06-19-peace-in-our-time`), and 23 provenance interviews.
- 216 public source chapters under canonical root namespaces (`lectures/`, `essays/`, `interviews/`).
- 216 chapter commentaries attached to those canonical homes, each seeded as an open commentary canvas.
- Chapter-folder `README.md` doorways for folder-backed chapters, designed for direct GitHub links in YouTube comments and LLM chats.
- Full lecture transcripts under `lectures/` so the repo can function independently of outside workshop storage.
- Chapter catalog and source URLs: [`docs/predictive-history-index.md`](docs/predictive-history-index.md) and [`docs/predictive-history-index.json`](docs/predictive-history-index.json) (`source_video_url` per chapter).
- A full chapter catalog at `docs/predictive-history-index.md` (human) and `docs/predictive-history-index.json` (machine) listing all 216 public chapters (lectures, essays, and provenance interviews) with transcript, commentary, folder, and source URLs (regenerate: `predictive-history index`; auto-sync during `predictive-history validate` and publish).
- Two conceptual volumes (deprecated reader frame): Volume I / `ph-civ` and Volume II / `ph-apo` — see [`docs/archive/two-volume-ph-civ-apo-deprecated.md`](docs/archive/two-volume-ph-civ-apo-deprecated.md).
- Historical two-volume reader map archived under [`docs/archive/`](docs/archive/two-volume-reader-order.md); see [From The Old Seven Volumes To The Current Two](docs/archive/seven-volume-to-two-volume.md).
- Series coverage: Civilization, Great Books, Geo-Strategy, Game Theory, Secret History, and Essays.
- The Homer-to-Tolstoy literary spine as the Volume I literary spine with cross-volume routing exposure.
- The Plato-to-Hegel theological-philosophical spine as a secondary Volume I route through reality, sacred order, imagination, and philosophy of history.
- The `ph-apo` pressure spine as the Volume II public application spine: geography, incentives, causation hinge, and infrastructure/sacred systems.
- A compact externalization of the reader-facing restructuring at [Two Volumes, One Reader Map](docs/archive/two-volumes-one-reader-map.md).
- Provider-neutral prompt templates.
- Eight public civilizational pattern IDs for downstream strategy-facing reference.
- 
- 

## What Is Excluded

- Private notes or private workspace paths.
- External-source bibliography claims beyond the orientation cards.
- LLM provider integrations, API calls, or hidden model dependencies.
- Large image, audio, video, document, or scan archives.
- URL-only artifact submissions treated as complete chapter work.

## Install For Local Development

```bash
python -m pip install -e .
```

## CLI

```bash
predictive-history list
predictive-history list --series game-theory --json
predictive-history show civ-41 --format json
predictive-history search Dante
predictive-history prompt gb-01 --mode creative
predictive-history spark gt-16 --count 5
predictive-history spine
predictive-history path homer-to-tolstoy
predictive-history validate
predictive-history index
predictive-history index --check
predictive-history status
predictive-history start --json
predictive-history tour --json
predictive-history trilingual --json
predictive-history growth
predictive-history route civ-07 --json
predictive-history link gt-24 --json
predictive-history patterns
predictive-history pattern civ-chokepoint-pressure --format json
predictive-history bridge civ-07 --format markdown
```

All prompt and spark commands are template-only. They do not call an AI provider. Pattern commands expose public civilizational frames for downstream strategy analysis; they do not import live strategy workspace material. Use **`predictive-history`** as the public CLI (`python -m civ_ph.cli …` invokes the same code when running from source).

## Commentary Canvas

The chapter commentaries are the project canvas. They are seeded for all chapters, but they are not treated as complete analysis. Each commentary has a shared `Project Canvas` scaffold for later chapter-by-chapter development: project leverage, laws and patterns, volume role, strategy application, counter-readings, open questions, and build notes.

See `docs/methodology/commentary-canvas.md`.

## Public Growth

Large reach targets, such as one million public views by the end of 2026, are strategic ambitions rather than directly executable agent tasks. Treat them as campaign pressure: convert the ambition into one live publishing wedge, then ship only human-approved assets with clear metrics.

The first live wedge is the Volume I literary spine: make the Homer-to-Tolstoy route shareable, connect it to the two-volume ph-civ narrative, pair it with one publishable chapter/commentary path sample, and define what counts as a view before public distribution.

This wedge is defined, not automatically launch-ready. The unresolved tension is whether the route has enough source-disciplined educational trust to deserve audience growth, not only whether the CLI can render it.

The canonical growth guardrail lives in `data/growth-goals.json` and is exposed with:

```bash
predictive-history growth --json
```

For a compact doorway into Jiang-facing interpretive notes on teaching, spread, rhetoric, platform fit, and cross-volume continuity, see [Jiang Analysis Index](docs/methodology/jiang-analysis-index.md).

## Literary Spine

```text
Homer -> Virgil -> Dante -> Shakespeare -> Dostoevsky -> Tolstoy
```

Homer to Tolstoy is the Volume I literary spine, not a side corridor. It uses cross-volume routing exposure where needed. Tolstoy is routed through `sh-16`, where *Anna Karenina* appears as a source-backed coda rather than a dedicated Tolstoy lecture.

The route now also has a public [support ring](data/corridors/homer-to-tolstoy-support-ring.md), which names the nearby Volume I materials that strengthen the spine without changing its canonical author sequence or first-tour order.

Tolstoy also functions as the bridge into Volume II. The public handoff lives in [From Civilization To Apocalypse](docs/routes/civilization-to-apocalypse.md), [Predictive History After Tolstoy](docs/routes/predictive-history-after-tolstoy.md), and [The Tolstoy Question](corpus/cross-volume/tolstoy-question.md).

If the question is not only "what is the route?" but "why did the old seven become two?", open [Two Volumes, One Reader Map](docs/archive/two-volumes-one-reader-map.md).

## Theological-Philosophical Spine

Volume I now also has a secondary theological-philosophical route: [Plato to Hegel](data/corridors/plato-to-hegel.md). It is parallel to the literary spine rather than a replacement for it, and it gives readers a second stable entrance into Civilization through Plato, Genesis, Augustine, Dante, Kant, and Hegel.

## Application Pressure Spine

The archived two-volume architecture includes a pressure spine rather than an author spine. Use [ph-apo Pressure Spine](data/corridors/ph-apo-pressure-spine.md) as a legacy-named compact application route; it does not restore `ph-apo` as a reader root.

Retired museum layer orientation: `docs/archive/ph-mus-retired.md`.

## License

License is pending. See `LICENSE-PENDING.md`.

## Portable project skills

Repository-local skills use public files and the existing provider-neutral CLI:

- [Chapter reading](.agents/skills/predictive-history-read/SKILL.md) — bounded source-grounded reading.
- [Learning practice](.agents/skills/predictive-history-learn/SKILL.md) — explanations, seminar work, and optional exercises.
- [Repository maintenance](.agents/skills/predictive-history-maintain/SKILL.md) — scoped validation and authorized publication.

They require no private runtime or automatic saving and are not installed globally.
