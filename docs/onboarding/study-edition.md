# Study Edition — public reader externalization

**Status:** specification (2026-06-10)  
**Pilot:** Homer-to-Tolstoy route · first chapter `civ-07`  
**Companion:** [`PIN-CITE-DISCIPLINE.md`](./PIN-CITE-DISCIPLINE.md) · [`public-repo-contract.md`](./public-repo-contract.md) · [`source-lattice.md`](./source-lattice.md)

---

## Purpose

Deliver a **Bible-study-style reading experience** for Predictive History: navigable outlines, click-through footnotes, and bidirectional jumps between lecture text and study notes — without forking the corpus away from git markdown SSOT.

The study edition is a **rendered skin** on existing apparatus:

| Bible-study layer | ph-civ SSOT |
| --- | --- |
| Book / chapter outline | Interwoven spine, Parts I–X, route spines |
| Verse-addressable text | Transcript `### kebab-slug` rails |
| Footnotes | Layer 2 claim tables (`*-transcript.md#slug`) |
| Cross-references | Part commentary, corridors, bibliography `supports:` |
| Study guide | Layer 0–1 chapter packet; thick notes in Part apparatus |

**Invariant:** Verbatim transcript bodies are not rewritten at render time. The builder only reads, indexes, and links.

---

## Reader promise

A human reader should be able to:

1. Open a **route or Part outline** (left rail).
2. Read the **lecture floor** (center panel) with stable section handles.
3. Click a **claim or section** and see the matching note (right rail or drawer).
4. Jump **note → passage** and **passage → note** without hunting separate markdown files.
5. See **review status** and source-video link before trusting provisional material.

LLM paste flows (`START-HERE.md`, chapter-folder URLs) remain parallel — not replaced.

---

## Page model

### Site levels

| Level | Example URL (GitHub Pages) | Source |
| --- | --- | --- |
| Home | `/` | Two-volume frame + first-tour CTA |
| Route | `/routes/homer-to-tolstoy/` | `data/spines/homer-to-tolstoy.json` |
| Part | `/parts/part-02-hellenic-world/` | `data/parts/volume-i-parts.json` + doorway md |
| Chapter | `/study/civ-07/` | Chapter packet (three-pane) |

Base path for project-site deploy: `/predictive-history/` (see [GitHub Pages](#github-pages-deploy)).

### Chapter study page (three-pane)

```
┌─────────────────┬────────────────────────────┬──────────────────┐
│ Outline rail    │ Transcript floor           │ Notes rail       │
│ Part + sections │ § greek-western-source     │ Claim 1 [↗]      │
│ ├ movement      │ …verbatim lecture…         │ Claim 2          │
│ ├ movement      │ inline markers [1][2]      │ Concepts         │
│ └ …             │                            │ Part § link      │
│ Route context   │ Source video · status ribbon │ Biblio stubs     │
└─────────────────┴────────────────────────────┴──────────────────┘
```

**Panels**

| Panel | Content | Max depth |
| --- | --- | --- |
| **Outline** | Part title, chapter title, ordered `###` slugs (human labels), route membership | From manifest or parsed transcript |
| **Floor** | Full transcript body; section boundaries = anchor targets | Verbatim only |
| **Notes** | Layer 2 claim rows keyed to `#slug`; Layer 1 summary (collapsible); link to Part apparatus | Thin chapter layers only |
| **Overflow** | Part commentary excerpt for active section; bibliography rows tagged `supports: civ-NN` | Link out, do not inline Layers 3–6 |

**Interactions (minimum viable)**

- Click outline slug → scroll floor to `#slug`
- Click claim row → scroll floor to matching slug; highlight section
- Click floor marker `[n]` → scroll notes to claim `n`
- Mobile: outline and notes collapse to drawers; floor stays primary

### Generated chapter bundle (internal)

Builder emits one JSON bundle per chapter (checked in under `site/_data/` or build cache only — **not** a second SSOT):

```json
{
  "source_id": "civ-07",
  "title": "Civilization #7: Homer's Iliad and the Birth of Greek Civilization",
  "part_id": "part-02-hellenic-world",
  "review_status": "in_review",
  "source_video": "https://www.youtube.com/watch?v=677rmlRgvLQ",
  "sections": [
    {"slug": "greek-western-source", "label": "Greek Western Source", "order": 1}
  ],
  "claims": [
    {
      "n": 1,
      "claim": "Greek civilization is framed as the creative source of Western civilization…",
      "anchor": "greek-western-source",
      "strength": "Explicit",
      "confidence": "High"
    }
  ],
  "paths": {
    "transcript": "lectures/civilization/civ-07/civ-07-transcript.md",
    "commentary": "lectures/civilization/civ-07/civ-07-commentary.md",
    "part_commentary": "docs/routes/volume-i-parts/part-02-hellenic-world-commentary.md"
  }
}
```

HTML pages are generated from bundles; markdown sources stay authoritative.

---

## Build inputs (read-only)

| Input | Role | Validator |
| --- | --- | --- |
| `book/**/**-transcript.md` | Text floor + `###` rails | `validate_pin_cite.py` (where manifest exists) |
| `book/**/**-commentary.md` | Layer 0–2 claims, metadata | Frontmatter + L2 table parse |
| `data/pin-cite/volume-i-anchors.yaml` | Section order + claim ref SSOT | `validate_pin_cite.py` |
| `data/parts/volume-i-parts.json` | Part ↔ chapter mapping | `validate_volume_i_parts.py` |
| `data/spines/homer-to-tolstoy.json` | Pilot route sequence | CLI / manual |
| `docs/routes/volume-i-parts/part-*-commentary.md` | Part notes cross-links | — |
| `docs/routes/volume-i-parts/part-*-bibliography.md` | Footnote bibliography | — |
| `docs/archive/two-volume-reader-order-interwoven.md` | Canonical chapter order | — |
| `data/cards/*.md` | Orientation card (footer) | — |

**Manifest gap (2026-06-12):** Part II (`civ-07`–`13`) is in the manifest. Parts III–VI chapters still parse transcript `###` + commentary L2 directly until manifest extension.

**Do not read:** `private operator workspace` paths, private notes, `artifacts/` scratch, raw VTT.

---

## Build pipeline (planned)

| Step | Script (planned) | Output |
| --- | --- | --- |
| 1. Resolve chapter paths | `scripts/study_edition_resolve.py` | `source_id` → on-disk packet |
| 2. Parse + validate | `scripts/build_study_edition.py` | `site/_data/chapters/{id}.json` |
| 3. Render HTML | stack-specific (see below) | `site/dist/` |
| 4. Verify links | `scripts/validate_study_edition.py` | exit 0 = all anchors resolve |

**CLI (planned):**

```bash
python scripts/build_study_edition.py --chapter civ-07
python scripts/build_study_edition.py --route homer-to-tolstoy
predictive-history study civ-07          # proposed: opens local preview path
predictive-history study --build         # proposed: full pilot route
```

**CI (planned):** GitHub Actions on `main` → build → deploy `site/dist` to GitHub Pages.

---

## Static-site stack comparison (GitHub Pages fit)

Requirements specific to Predictive History:

- **Python-first repo** — validators, pin-cite prep, and CLI already in Python; no Node toolchain today.
- **Custom three-pane UX** — outline | verbatim floor | bidirectional footnotes; not standard docs-sidebar markdown.
- **Large verbatim transcripts** — pages can be long; need anchor scroll, not full SPA re-fetch per chapter.
- **Project-site hosting** — `https://mira-builds.github.io/predictive-history/` (repo name = Pages path prefix).
- **Dual skin** — git markdown for LLMs; static HTML for humans. Builder must not fork content.

### Comparison

| Criterion | VitePress | Eleventy (11ty) | Custom (Python → HTML) |
| --- | --- | --- | --- |
| **GitHub Pages** | Good; `base: '/predictive-history/'` in config | Excellent; `_site` → `gh-pages` | Excellent; output folder only |
| **Repo alignment** | Adds Node/npm CI lane | Adds Node/npm CI lane | Matches existing Python stack |
| **Three-pane layout** | Needs custom Vue theme components | Full control via Nunjucks/Liquid + light JS | Full control; vanilla JS for panels |
| **Bidirectional footnotes** | Custom Vue components | Alpine.js or small module | Tailored JS in generated pages |
| **Transcript pages** | MD import OK; long pages heavy in Vite bundle | Static HTML per chapter; fast | One HTML file per chapter; fast |
| **Search** | Built-in local search plugin | Add Pagefind or lunr.js | Defer; route index sufficient for pilot |
| **Nav from JSON/ YAML** | Sidebar config generation | Data cascade native fit | Python emits nav JSON → template |
| **Maintenance** | Vue + Vite upgrades | Moderate template debt | You own all UI/a11y/mobile |
| **Time to pilot `civ-07`** | Slower (theme + components) | Medium | Fastest |

### Recommendation (phased)

| Phase | Stack | Rationale |
| --- | --- | --- |
| **0 — Prove data** | **Custom Python builder** → self-contained `civ-07.html` + shared CSS/JS | Validates manifest parse, L2 join, anchor map without CI/toolchain debate |
| **1 — Pilot route site** | **Eleventy** wrapping Python-generated chapter data | Shared layouts for Homer route chapters; data files fit 11ty cascade; add Pagefind later |
| **2 — Scale / polish** | Re-evaluate **VitePress** only if search, i18n, or theme ecosystem outweigh custom layout cost | Not the pilot default |

**Default decision:** **Python SSOT builder + Eleventy render** for multi-chapter GitHub Pages. **Not** VitePress-first — the UX is study-bible panels, not VitePress doc sidebars.

**Custom-only fallback:** If Node in CI is unacceptable, stay on Python → static HTML for the full pilot route; revisit Eleventy when chapter count exceeds ~10 pages.

---

## GitHub Pages deploy

| Setting | Value |
| --- | --- |
| Repo | `mira-builds/predictive-history` |
| URL | `https://mira-builds.github.io/predictive-history/` |
| Publish dir | `site/dist` (or `docs/` only if using branch docs — prefer Actions artifact) |
| `base` / asset prefix | `/predictive-history/` |
| Branch | `gh-pages` (Actions) or Pages from Actions workflow |

**Link contract:** Chapter-folder GitHub links and study-edition URLs must stay aligned. `predictive-history link civ-07` should eventually emit **both** raw folder URL and study-edition URL.

---

## Pilot scope

### Wave 1 — single chapter

- **Chapter:** `civ-07` (Homer / Volume I literary spine entry)
- **Route context:** Step 1 of `homer-to-tolstoy`
- **Done when:** Three-pane page live on GitHub Pages; all 16 L2 claims bidirectionally linked to 16 transcript sections; review ribbon visible; source video linked

### Wave 2 — Homer route slice

- **Chapters:** `civ-07`, `gb-02`, `gb-05`, `gb-07` (per spine sequence step 1)
- **Done when:** Route outline page links all four study pages; interwoven order preserved

### Wave 3 — full Homer-to-Tolstoy

- Full `data/spines/homer-to-tolstoy.json` sequence
- Launch packet copy from `data/growth-goals.json` first_live_wedge
- Human approval before distribution push

**Out of pilot scope:** Volume II Apocalypse pressure spine, large media exhibit binaries, translation mirrors, upstream workshop imports.

---

## Relation to existing surfaces

| Surface | Role after study edition |
| --- | --- |
| `START-HERE.md` / `llm-experience.json` | LLM-first entry; links to study site as human alternative |
| Chapter-folder `README.md` | Agent doorway; add “Open study edition” link |
| `docs/onboarding/chapter-folder-links.md` | YouTube comments may point to study URL instead of raw folder |
| `PIN-CITE-DISCIPLINE.md` | Workshop authoring law; pin-cite also feeds public study edition |
| `docs/contracts/export-contract.md` | Study edition = exported navigation layer, not new corpus class |

**Pin-cite policy shift:** Anchors and L2 tables are no longer workshop-only when consumed by the study builder. Authoring discipline stays WORK; **rendered output** is public.

---

## Launch readiness gate

Do not claim `launch_ready` until:

1. Pilot chapter passes `validate_study_edition.py` (all anchors resolve).
2. `review_status` caveats render on every study page.
3. Human-approved launch blurb explains two-volume frame + why Homer spine first.
4. View-count definition documented (study page load? video click? — pick one for wedge).
5. `data/spines/homer-to-tolstoy.json` `launch_readiness` updated only after human sign-off.

---

## Implementation checklist

- [x] `docs/onboarding/study-edition.md` (this file)
- [ ] Extend `volume-i-anchors.yaml` with Part II (`civ-07`–`civ-13`) — **done** (`sync_part_ii_to_manifest.py`)
- [x] `scripts/build_study_edition.py` — parse + bundle
- [x] `scripts/validate_study_edition.py` — link integrity
- [x] `civ-07` static prototype (Phase 0 custom HTML) — `site/dist/study/civ-07/index.html`
- [ ] Eleventy layout + GitHub Actions deploy (Phase 1)
- [ ] `predictive-history study` CLI command
- [ ] `README.md` + `public-repo-contract.md` one-line study-edition pointer
- [ ] `predictive-history link` emits study URL

---

## See also

- [`study-edition-phase1-visual.md`](./study-edition-phase1-visual.md) — Phase 1 visual spec (`civ-07`: claim morph, Greece–China split, seminar strip)
- [`two-volumes-one-reader-map.md`](./two-volumes-one-reader-map.md)
- [`chapter-folder-links.md`](./chapter-folder-links.md)
- [`pin-cite-manifest-index.md`](./pin-cite-manifest-index.md)
- [`data/growth-goals.json`](../data/growth-goals.json) — first live wedge

Hosting note: URLs in this document describe a prospective Pages destination. Publication of the repository alone does not enable or verify a Pages deployment.
