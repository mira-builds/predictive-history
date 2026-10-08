# Runbook: PH transcript curation

**Repo SSOT:** this file lives in `mira-builds/predictive-history` only. A separate copy may exist in private operator workspaces; **edit here** for public transcript curation policy on **interviews** and **lectures**.

**Activations:** `PH transcript pass` · `interview section pass` · `interview turn pass` · `lecture transcript pass` · `lecture section pass` · `lecture turn pass` · `PH-TRANSCRIPT-EDIT`

## Purpose

Curate public transcript bodies under:

- **Interviews:** `interviews/interview-YYYY-MM-DD-{host-slug}/`
- **Lectures:** `lectures/{series}/{source_id}/` (150 packets across five series — see [`lectures/README.md`](../../lectures/README.md))

Shared work:

- **Title Case section rails** under `## Part I: Full transcript`
- **Named speaker / turn labels** where dialogue exists
- Light **ASR / entity** repair in touched blocks only
- **README pass notes** + validate before push

**Transcript-logic only** — not audio-verified verbatim unless operator supplies caption SSOT.

## Trigger

- New or refreshed transcript body after promote / verbatim paste
- `>>` markers or merged speaker paragraphs remain
- Operator names a packet (`vi-11`, `ext-doac-01`, `gt-29`, `civ-59`, …) or asks for pass **A / B / C / D**

## Out of scope

| Out | Route |
| --- | --- |
| First promote (card, manifest, intake) | `scripts/intake_interview_external.py` (interviews) — separate commit |
| Commentary canvas rewrites | [`commentary-canvas-upgrade.md`](commentary-canvas-upgrade.md) |
| **Essay** bodies | `essays/` — separate workflow |
| Private workshop notes | not in this repo |

**Pass A patch scripts** for interviews live under `scripts/patch_*_sections_asr.py` (16 curated interview packets; Interviews #17–#23 await pass A). **Lecture pass A** uses [`scripts/lecture_section_pass.py`](../../scripts/lecture_section_pass.py) + [`scripts/verify_transcript_pin_cites.py`](../../scripts/verify_transcript_pin_cites.py) — see **Rails everywhere** below.

## Edit surface

| Corpus | Transcript + YAML | Provenance |
| --- | --- | --- |
| Interview | `interviews/{source_id}/{source_id}.md` | `interviews/{source_id}/README.md` |
| Lecture | `lectures/{series}/{source_id}/{source_id}-transcript.md` | `lectures/{series}/{source_id}/README.md` |

| Shared | Path |
| --- | --- |
| Section helpers | [`scripts/interview_transcript_sections.py`](../../scripts/interview_transcript_sections.py) |
| Indexes (generated) | `docs/predictive-history-index.*`, slice indexes — via `validate` |

## Lecture shapes

| Shape | Where | Typical passes | Notes |
| --- | --- | --- | --- |
| **Monologue + slug rails** | Most `civ-*`, many `gb-*` | A (Title Case retitle), D | `### stalin-greatest-man-thesis` style; pass C usually N/A |
| **Flat monologue** | Most `geo-*`, many `gt-*` | A (insert rails from anchors / README timestamp map) | e.g. [`geo-01`](../../lectures/geo-strategy/geo-01/geo-01-transcript.md) — preface timestamps, flat body |
| **Classroom Q&A (`>>`)** | `gt-29`, many `gb-*` / `sh-*` | B, C | Alan reads questions; Jiang answers — same mechanics as interview pass B/C |
| **Hybrid (interview)** | DOAC sections | B, C | “Lecture + interjections” pattern in pass-C table below |

## Exemplars

### Interviews

| Interview | Shape | Reference |
| --- | --- | --- |
| Tucker `vi-11` | Clean promote — sections + turns in one pass | [`interview-2026-03-20-tucker-carlson`](../../interviews/interview-2026-03-20-tucker-carlson/) · `d475974` |
| DOAC `ext-doac-01` | ASR/paste — **incremental pass ladder**; **14/14 section rails pass C complete** | [`interview-2026-05-07-diary-of-a-ceo`](../../interviews/interview-2026-05-07-diary-of-a-ceo/) · sections `ddeeff7`; pass 13 `a6f86e8` |

### Lectures

| Lecture | Shape | Reference |
| --- | --- | --- |
| `gt-29` | Flat body · classroom Q&A · 57 `>>` | [`lectures/game-theory/gt-29/`](../../lectures/game-theory/gt-29/) — priority pilot for pass B/C |
| `civ-59` | Monologue · slug section rails | [`lectures/civilization/civ-59/`](../../lectures/civilization/civ-59/) — Title Case retitle via `apply_slug_to_title_headings` / `write_slug_retitle_transcript()` |

### DOAC pass ladder (reference)

Read packet `README.md` **Transcript pass N** notes. **Pass C complete** on all 14 Part I rails; sponsor/read blocks and Cold Open montage stay **unlabeled by design**.

| Pass | Date | Scope | Notes |
| --- | --- | --- | --- |
| 2 | 2026-06-25 | **A + B** | 14 Title Case rails; `>>` → **Steven Bartlett:** |
| 3 | 2026-06-26 | **B** | Batch `>>` / cold-open tags |
| 4–6 | 2026-06-26 | **C** | Iran Topography · NDS Western Hemisphere · War Phases |
| 7 | 2026-06-26 | **C** (batch) | 11 sections mechanical — superseded by 8–13 where listed |
| 8 | 2026-06-26 | **C** (hand) | Chess — lecture + Mhm/Okay interjections |
| 9 | 2026-06-26 | **C** (hand) | Eight Predictions — Q&A chain |
| 10 | 2026-06-26 | **C** (hand) | Global Chokepoints — wire-read insert |
| 11 | 2026-06-26 | **C** (hand) | Interview Open + Timeline |
| 12 | 2026-06-26 | **C** (hand) | Israel · East Asia (NK game-theory) · Community · Hermetic |
| 13 | 2026-06-26 | **C** (hand) | Plato Cave |

### DOAC section rails × pass-C status

| # | Section rail | Pass-C | Pattern |
| ---: | --- | --- | --- |
| 1 | Cold Open — Predictions Teaser | Partial | Teaser montage |
| 2 | Interview Open — Predictions and Petrodollar | 11 | Q&A + petrodollar monologue |
| 3 | Iran Topography, Attrition, and Hormuz | 4 | Map lecture |
| 4 | National Defense Strategy — Western Hemisphere | 5 | Map + NDS |
| 5 | War Phases — Ground Troops and IRGC | 6 | Phased war |
| 6 | Chess Grand Strategies and WWIII Players | 8 | Lecture + interjections |
| 7 | Global Chokepoints — Russia Shadow Fleet | 10 | Seizure Q&A + wire read |
| 8 | Timeline — Trump Term Limits and Forever War | 11 | Timeline Q&A |
| 9 | Eight Predictions — Trump Third Term and AI State | 9 | Prediction box Q&A |
| 10 | Israel — Greater Israel, NATO, and Odessa | 12 | Odessa map |
| 11 | East Asia Flashpoints — North Korea | 12 | NK game-theory roleplay |
| 12 | Community, Hope, and Bronze Age Collapse | 12 | Bronze Age / Steve Keen |
| 13 | Plato Cave — Reality and Financial Elite | 13 | Allegory + media Q&A |
| 14 | Hermetic Philosophy, Life Advice, and Closing Tradition | 12 | Closing + wife story |

**Unlabeled by design:** Shopify / Pipedrive / DOAC Circle reads; YouTube algorithm outro; README unresolved (e.g. Araghchi title).

### Pass-C hand-fix patterns

| Pattern | When | Technique |
| --- | --- | --- |
| **Q&A chain** | Prediction box, constitution | One host question per label; guest answer blocks |
| **Lecture + interjections** | Chess, Plato, chokepoints | Pull **Mhm**, **Okay**, **Right?**, **Exactly** to host; rhetorical teaching pivots stay on guest |
| **Game-theory roleplay** | East Asia NK | Guest as NK voice; host as interlocutor |
| **Wire read** | Global Chokepoints seizures | Host reads verified facts; guest frames |
| **Host monologue** | Plato / independent media | Long host blocks stay on host |
| **Classroom question read** | gt-29, gb-* | `>>` → **Alan:** (or named reader); answer blocks → **Jiang Xueqin:** |
| **Stop rule** | Low confidence | README unresolved — do not guess |

## Pass ladder

Run the **lowest pass still needed**. One commit slice per pass when practical. Increment **Transcript pass N** in packet README.

| Pass | Stub | Work | Lectures |
| --- | --- | --- | --- |
| **A** | `interview section pass` · `lecture section pass` | `### Title Case` rails; light dedup; optional `scripts/patch_*_sections_asr.py` (interviews) or `write_sectioned_transcript` / `write_slug_retitle_transcript` | Slug → Title Case retitle; flat → anchor split; geo timestamps may stay in README until promoted |
| **B** | `PH transcript pass` · `lecture transcript pass` | `>>` → named speaker; cold-open tags; obvious inline splits | When `>>` or merged Q&A blocks exist |
| **C** | `interview turn pass` · `lecture turn pass` | Named turns in **scoped section(s)**; light ASR in touched blocks | Classroom Q&A; seminar dialogue — skip for pure monologue |
| **D** | (with B/C) | Places, names, acronyms; unresolved → README | ASR in touched blocks only |

**Stop rule:** ambiguous merged paragraphs → README unresolved.

Do **not** block pass A ship on full-file turn labeling for long ASR bodies (~900 lines).

## Steps

1. Read packet README pass notes + first half of transcript — note shape, labels, sponsor boundaries.
2. Pick pass **A**, **B**, **C**, or scoped **C** on named sections.
3. Edit transcript + README; update frontmatter when curation lands:
   - `transcript_curation: curated_sectioned` (or existing lecture curation values when retitle-only)
   - `transcript_fidelity: curated_pass` (interviews) or preserve lecture fidelity fields when appropriate
   - `fidelity_reviewed_at: YYYY-MM-DD`
4. Validate from repo root:

```bash
PYTHONPATH=src python -m civ_ph.cli validate
python -m pytest -q
```

5. Commit: prefix **`PH-TRANSCRIPT-EDIT:`** · pass + section in subject for pass C.
6. Push `main` when operator directs.

## Section headings

- **Title Case** ASCII (`### Iran Topography, Attrition, and Hormuz`)
- Under `## Part I: Full transcript` only
- Topic pivot, not timestamps (geo README timestamp lists are optional preface until promoted to rails)
- Count is **per packet** (Tucker 7; DOAC 14; civ-* typically 6–8 slug rails today)

## Turn labeling

### Interviews

- Use names from packet README (DOAC: **Steven Bartlett** / **Jiang Xueqin**; Tucker: **Tucker Carlson** / guest)
- Labels: `**Host:**` / `**Guest:**` or named speakers
- **Sponsor/read blocks:** omit labels (DOAC) or `[Sponsor segment omitted.]` (Tucker)

### Lectures

- Default monologue: **`**Jiang Xueqin:**`** when labeling helps (optional for uninterrupted teaching blocks)
- Classroom packets: **`**Alan:**`** (question reader), **`**Vincent:**`** / **`**Student:**`** when named
- Do **not** force Host/Guest vocabulary on lectures
- One label per turn; blank line between long turns

## Verification

Do not call a pass complete unless:

- `source_id` + packet path named
- pass letter(s) + section scope stated
- pass C: approximate exchange count or labeled section name
- unresolved entities in README
- `validate` + `pytest` exit codes reported
- commit hash + push status (or explicit defer)

## Rails everywhere (lecture pass A program)

**Goal:** Title Case `###` section rails under `## Part I: Full transcript` on all lecture packets.

**CLI:**

```bash
python scripts/lecture_section_pass.py audit [--strict]
python scripts/lecture_section_pass.py slug-retitle --series civilization
python scripts/verify_transcript_pin_cites.py
python scripts/lecture_section_pass.py draft-map --series geo-strategy --template geo-flat
python scripts/lecture_section_pass.py geo-from-timestamps
python scripts/lecture_section_pass.py geo-upgrade --from-id 4 --to-id 20
python scripts/lecture_section_pass.py apply --series geo-strategy
python scripts/lecture_section_pass.py auto-section --series game-theory --template gt-monologue
```

**Pin-cite rule (T1):** slug → Title Case words only (`stalin-greatest-man-thesis` → `### Stalin Greatest Man Thesis`) — preserves commentary `#fragment` links.

**Anchor semantics (insert-tier):** YAML `anchor` on a section marks where **that section’s body starts** (boundary after the prior rail). Opening has no boundary anchor — Part I text from the top through the next pivot belongs under `### Opening`.

**Insert-tier maps:** [`data/lectures/section-maps/`](../../data/lectures/section-maps/) · templates in `_templates/`.

**Commit prefix:** `PH-TRANSCRIPT-EDIT: lecture pass A {series} batch N`

## Related

- [`interviews/README.md`](../../interviews/README.md) — interview patch script table, DOAC verbatim swap
- [`lectures/README.md`](../../lectures/README.md) — series partitions, transcript pass ladder
- [`scripts/interview_transcript_sections.py`](../../scripts/interview_transcript_sections.py) — shared section helpers (interviews + lectures)
- [`source-lattice-review.md`](source-lattice-review.md) — reader traversal discipline
