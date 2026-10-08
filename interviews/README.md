# Interviews

Public provenance packets for Predictive History interview-form source material.

Repo path: **`interviews/`** at the repository root (sibling to [`essays/`](../essays/README.md), [`lectures/`](../lectures/README.md); deprecated [`book/`](../book/) tombstone; [`ph-civ/`](../ph-civ/README.md)).

## Public ID scheme

**Pattern:** `interview-YYYY-MM-DD-{host-slug}`

Examples: `interview-2025-11-24-glenn-diesen`, `interview-2026-05-07-diary-of-a-ceo`.

| Field | Detail |
| --- | --- |
| **Date** | YouTube upload date (pinned in [`data/interviews/manifest.json`](../data/interviews/manifest.json)) |
| **Host slug** | Lowercase hyphenated host or show name |
| **Folder** | `interviews/{source_id}/` with transcript, commentary canvas, and README |
| **Catalog** | [`predictive-history-interview-index.md`](predictive-history-interview-index.md) · full hub [`docs/predictive-history-index.md`](../docs/predictive-history-index.md) |

**Public today:** 23 interview chapter packets (`interview-2025-10-30-cyrus-janssen` … `interview-2026-08-11-glenn-diesen`).

## Workshop crosswalk (`vi-*` and external)

| Workshop | Public `source_id` | Upload date |
| --- | --- | --- |
| `vi-01` | `interview-2025-10-30-cyrus-janssen` | 2025-10-30 |
| `vi-02` | `interview-2025-11-24-glenn-diesen` | 2025-11-24 |
| `vi-03` | `interview-2026-01-05-glenn-diesen` | 2026-01-05 |
| `vi-04` | `interview-2026-01-18-danny-haiphong` | 2026-01-18 |
| `vi-05` | `interview-2026-01-22-dimitri-lascaris` | 2026-01-22 |
| `vi-06` | `interview-2026-01-26-glenn-diesen` | 2026-01-26 |
| `vi-07` | `interview-2026-03-02-breaking-points` | 2026-03-02 |
| `vi-08` | `interview-2026-03-07-dialogue-works` | 2026-03-07 |
| `vi-09` | `interview-2026-03-09-sneako` | 2026-03-09 |
| `vi-10` | `interview-2026-03-16-endgame` | 2026-03-16 |
| `vi-11` | `interview-2026-03-20-tucker-carlson` | 2026-03-20 |
| `vi-12` | `interview-2026-04-01-jay-shapiro` | 2026-04-01 |
| `vi-13` | `interview-2026-04-07-patrick-bet-david` | 2026-04-07 |
| `vi-14` | `interview-2026-04-13-glenn-diesen` | 2026-04-13 |
| `vi-15` | `interview-2026-04-13-sneako-dugin` | 2026-04-13 |

### External (not in workshop `vi-*`)

| Registry | Public `source_id` | Upload date | Source |
| --- | --- | --- | --- |
| `ext-doac-01` | `interview-2026-05-07-diary-of-a-ceo` | 2026-05-07 | [Diary of a CEO / Steven Bartlett](https://www.youtube.com/watch?v=BTJGr78-zyw) |
| `ext-interview-02` | `interview-2026-03-09-glenn-diesen-iran-war` | 2026-03-09 | [Glenn Diesen](https://www.youtube.com/watch?v=6rTlI_Qwd1I) |
| `ext-interview-03` | `interview-2026-03-19-tom-bilyeu` | 2026-03-19 | [Tom Bilyeu](https://www.youtube.com/watch?v=uP9Fnq23lsA) |
| `ext-interview-04` | `interview-2026-04-22-redacted` | 2026-04-22 | [Redacted](https://www.youtube.com/watch?v=NidlGa9C0H8) |
| `ext-interview-05` | `interview-2026-06-01-glenn-diesen` | 2026-06-01 | [Glenn Diesen](https://www.youtube.com/watch?v=Pk15Ov0v98U) |
| `ext-interview-06` | `interview-2026-07-01-glenn-diesen` | 2026-07-01 | [Glenn Diesen](https://www.youtube.com/watch?v=Kygtd00Xbto) |
| `ext-interview-07` | `interview-2026-07-11-cyrus-janssen` | 2026-07-11 | [Cyrus Janssen](https://www.youtube.com/watch?v=NuumRbqItBg) |
| `ext-interview-08` | `interview-2026-08-11-glenn-diesen` | 2026-08-11 | [Glenn Diesen](https://www.youtube.com/watch?v=QEysVg7ftWk) |

Cards use `part: provenance`, `series: interviews`, `derived_corpus: provenance`, `placement_weight: light`. They appear in the **Provenance** section of the chapter catalog; they are not foreground Volume I/II spine routes.

Related: [`docs/archive/book-provenance-index.md`](../docs/archive/book-provenance-index.md) · interviews slice [`predictive-history-interview-index.md`](predictive-history-interview-index.md) · full hub [`docs/predictive-history-index.md`](../docs/predictive-history-index.md) · intake manifest [`data/interviews/manifest.json`](../data/interviews/manifest.json).

## DOAC #16 — verbatim swap + section restore

[`interview-2026-05-07-diary-of-a-ceo`](interview-2026-05-07-diary-of-a-ceo/) uses an **operator verbatim paste** body with **Title Case section headings** (not lowercase slug headers). After replacing the transcript body under `## Part I: Full transcript`, re-apply sections and light ASR cleanup with:

```bash
python scripts/patch_doac_sections_asr.py
python -m civ_ph.cli index --force
python -m civ_ph.cli validate
```

**What the script does**

- Splits the verbatim body at **14 anchor phrases** (see `SECTION_ANCHORS` in the script; section map pinned from commit `c01fe76`).
- Inserts `### Title Case — …` headings from `SECTION_TITLES`.
- Applies light ASR fixes (e.g. `Professor Dieng` → `Professor Jiang`, duplicate-word cleanup).
- Rewrites frontmatter: `transcript_source: operator_paste`, `transcript_curation: curated_sectioned`, `transcript_fidelity: exact_body_match`.

**Staging (optional):** operator paste can land in `data/interviews/_land_doac/body.txt` before manual or scripted merge into the packet transcript. Keep staging **UTF-8** only — files under `data/` are scanned by `ph-civ validate`; UTF-16 artifacts will fail the public-boundary read pass.

## Interview section headings (Title Case)

Curated interview transcripts use **`### Title Case — …`** section headings, not lowercase slug headers (`### iran-attrition-and-global-stakes`).

| Interview | Patch script |
| --- | --- |
| [`interview-2026-05-07-diary-of-a-ceo`](interview-2026-05-07-diary-of-a-ceo/) | `python scripts/patch_doac_sections_asr.py` |
| [`interview-2026-03-16-endgame`](interview-2026-03-16-endgame/) | `python scripts/patch_endgame_sections_asr.py` |
| [`interview-2026-03-20-tucker-carlson`](interview-2026-03-20-tucker-carlson/) | `python scripts/patch_tucker_sections_asr.py` |
| [`interview-2026-03-02-breaking-points`](interview-2026-03-02-breaking-points/) | `python scripts/patch_breaking_points_sections_asr.py` |
| [`interview-2026-04-07-patrick-bet-david`](interview-2026-04-07-patrick-bet-david/) | `python scripts/patch_pbd_sections_asr.py` |
| [`interview-2026-04-13-glenn-diesen`](interview-2026-04-13-glenn-diesen/) | `python scripts/patch_glenn_diesen_april_sections_asr.py` |
| [`interview-2026-04-13-sneako-dugin`](interview-2026-04-13-sneako-dugin/) | `python scripts/patch_sneako_dugin_sections_asr.py` |
| [`interview-2025-10-30-cyrus-janssen`](interview-2025-10-30-cyrus-janssen/) | `python scripts/patch_cyrus_janssen_sections_asr.py` |
| [`interview-2025-11-24-glenn-diesen`](interview-2025-11-24-glenn-diesen/) | `python scripts/patch_glenn_diesen_nov_sections_asr.py` |
| [`interview-2026-01-05-glenn-diesen`](interview-2026-01-05-glenn-diesen/) | `python scripts/patch_glenn_diesen_jan_sections_asr.py` |
| [`interview-2026-03-07-dialogue-works`](interview-2026-03-07-dialogue-works/) | `python scripts/patch_dialogue_works_sections_asr.py` |
| [`interview-2026-03-09-sneako`](interview-2026-03-09-sneako/) | `python scripts/patch_sneako_sections_asr.py` |
| [`interview-2026-01-18-danny-haiphong`](interview-2026-01-18-danny-haiphong/) | `python scripts/patch_danny_haiphong_sections_asr.py` |
| [`interview-2026-01-22-dimitri-lascaris`](interview-2026-01-22-dimitri-lascaris/) | `python scripts/patch_dimitri_lascaris_sections_asr.py` |
| [`interview-2026-01-26-glenn-diesen`](interview-2026-01-26-glenn-diesen/) | `python scripts/patch_glenn_diesen_jan26_sections_asr.py` |
| [`interview-2026-04-01-jay-shapiro`](interview-2026-04-01-jay-shapiro/) | `python scripts/patch_jay_shapiro_sections_asr.py` |

After any patch: `python -m civ_ph.cli index --force` and `python -m civ_ph.cli validate`.

Shared helpers (`insert_sections`, `write_sectioned_transcript`, `common_asr_cleanup`, …): [`scripts/interview_transcript_sections.py`](../scripts/interview_transcript_sections.py).

### Section audit (2026-06-25)

| Status | Interviews |
| --- | --- |
| **Curated Title Case sections** | Interviews #1–#16: Cyrus Janssen, Glenn Diesen (Nov/Jan/Jan 26/Apr), Danny Haiphong, Dimitri Lascaris, Breaking Points, Dialogue Works, Sneako, **Endgame (18 rails)**, Tucker, Jay Shapiro, PBD, Sneako–Dugin, DOAC |
| **No `###` sections** (operator paste; curation pending) | Interviews #17–#23 |

No lowercase slug headers remain. PH-TRANSCRIPT-EDIT Title Case pass is **complete** for all curated interview transcripts.

## Transcript pass ladder (sections + turn labeling)

After section rails exist (pass **A**, often via `scripts/patch_*_sections_asr.py`), use the repo-native runbook for host cleanup and turn labeling:

- **Runbook (SSOT):** [`docs/runbooks/ph-transcript-curation.md`](../docs/runbooks/ph-transcript-curation.md)
- **Cursor skill (this repo):** [`.cursor/skills/ph-transcript-curation/SKILL.md`](../.cursor/skills/ph-transcript-curation/SKILL.md) — not a strategy-codex junction

Passes **B / C / D:** `>>` → named host, scoped turn labels, light ASR, README **Transcript pass N** notes. Commit prefix **`PH-TRANSCRIPT-EDIT:`**. Reference exemplar: DOAC #16 pass ladder (14/14 section rails pass C · `a6f86e8`).
