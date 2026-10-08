# Essays

**Canonical public home** for Predictive History **Substack essay bodies** (verbatim text).

Repo path: **`essays/`** at the repository root (sibling to [`commentaries/`](../commentaries/README.md), [`interviews/`](../interviews/README.md), [`lectures/`](../lectures/README.md), [`ph-civ/`](../ph-civ/README.md); deprecated [`book/`](../book/) tombstone).

## Public ID scheme

**Pattern:** `essay-YYYY-MM-DD-{substack-slug}`

Examples: `essay-2025-08-06-vision-mission-goals`, `essay-2025-09-27-the-empire-goes-to-war`.

| Field | Detail |
| --- | --- |
| **Date** | Substack `publication_date` (pinned in [`data/essays/manifest.json`](../data/essays/manifest.json)) |
| **Slug** | `substack_slug` from packet frontmatter |
| **Essay body** | `essays/{source_id}.md` (flat file, no subfolder) |
| **Commentary** | [`commentaries/{source_id}-commentary.md`](../commentaries/README.md) |
| **Catalog** | [`predictive-history-essay-index.md`](predictive-history-essay-index.md) · full hub [`docs/predictive-history-index.md`](../docs/predictive-history-index.md) |

**Public today:** 43 essay bodies (`essay-2025-08-06-vision-mission-goals` … `essay-2026-06-19-peace-in-our-time`).

### Workshop crosswalk (`es-*`)

Full legacy ↔ dated crosswalk: [`data/essays/manifest.json`](../data/essays/manifest.json).

**Deprecated paths:**

- Sequential `essay-NN` folder URLs (2026-06-26 dated-ID cut)
- Per-essay subfolder URLs `…/essays/{source_id}/` (2026-06-26 flat layout cut) — use `essays/{source_id}.md` instead

Substack canonical URLs unchanged. See [`docs/migrations/essay-dated-id-migration.md`](../docs/migrations/essay-dated-id-migration.md).

## Packet shape

| Artifact | Path |
| --- | --- |
| Essay body | `essays/{source_id}.md` |
| Commentary canvas | `commentaries/{source_id}-commentary.md` |
| Orientation card | `data/cards/{source_id}.md` |

No per-essay README doorway — study entry is essay body + commentary + card. Share link: `ph-civ link {source_id}` (essays emit transcript blob URL).

Intake: [`scripts/intake_essays_phase2.py`](../scripts/intake_essays_phase2.py)
