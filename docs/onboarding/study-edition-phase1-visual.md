# Study Edition — Phase 1 visual spec (`civ-07`)

**Status:** specification (2026-06-10)  
**Scope:** One chapter only — `civ-07` (Homer / Hellenic World entry)  
**Builds on:** Phase 0 three-pane (`site/dist/study/civ-07/`)  
**Parent:** [`study-edition.md`](./study-edition.md)

Phase 1 adds **three anchor-locked enhancements** chosen for `civ-07` content and the existing pin-cite apparatus. No open-ended chat. No site-wide rollout until `civ-07` passes acceptance below.

---

## Selected features (2–3)

| # | Feature | Brainstorm source | Why `civ-07` |
| --- | --- | --- | --- |
| **1** | **Claim-card morph** | Parallel panes / study cards | 16 L2 claims already mapped 1:1 to sections |
| **2** | **Greece–China contrast split** | Comparison lens | Chapter climax at `#greece-china-contrast`; encodes oral vs literacy monopoly thesis |
| **3** | **Section seminar strip** | Question garden | Homer/oral/polis sections invite discussion; matches `START-HERE` `seminar` mode |

**Deferred from brainstorm (not Phase 1):** route cinema scroll, living margin illustrations, TTS oral mode, large off-repo media vaults, full concept constellation graph.

---

## Design system (Phase 1 extensions)

Extend Phase 0 tokens in `site/assets/study-edition.css`:

| Token | Value | Use |
| --- | --- | --- |
| `--greek` | `#2c5282` | Greece column, Hellenic accents |
| `--china` | `#8b2942` | China column (muted, not flag literal) |
| `--seminar` | `#3d5c45` | Seminar strip border / labels |
| `--card-shadow` | `0 2px 12px rgba(31, 26, 20, 0.08)` | Morphed claim cards |
| `--font-display` | `Palatino Linotype`, `Book Antiqua`, Georgia, serif | Section titles, card headers |

**Typography law**

- Transcript floor: unchanged serif body (lecture is primary).
- UI chrome: sans (`--font-ui`).
- Claim cards: display serif for claim number + one-line thesis line only.

**Motion law**

- Transitions ≤ 220ms; `prefers-reduced-motion` disables morph and split animations.
- All motion triggered by user selection of a `#slug` or claim `n` — no autoplay carousels.

**Trust chrome (unchanged, always visible)**

- Top bar: `source_reviewed` + `curated_transcript`.
- Footer on gen-AI blocks: *Generated study aid · not new evidence · verify in transcript.*

---

## Feature 1 — Claim-card morph

### Reader experience

When the reader selects a claim (notes panel) or a `[n]` marker (transcript):

1. Right rail **morphs** the flat claim list into a **focused study card** for claim `n`.
2. Card shows: claim text, strength/confidence, **one-line thesis** (generated or templated), **2–3 bullet “notice in passage”** lines, button **↗ Return to passage**.
3. Outline rail highlights the matching `#slug`.
4. Secondary control: **View all claims** restores the list.

### Visual layout

```
┌─ Notes panel ─────────────────────┐
│  ◉ Claim 12 · Iliad empathy     │
│  ─────────────────────────────  │
│  Thesis (one line, display)     │
│  • Notice …                     │
│  • Notice …                     │
│  Explicit · High                │
│  [↗ Passage] [All claims]       │
└─────────────────────────────────┘
```

### Data / gen-AI

| Field | Source | Gen-AI allowed? |
| --- | --- | --- |
| Claim text | Layer 2 table | No |
| Anchor | L2 ref | No |
| Thesis line | Compress claim ≤ 120 chars | Yes, **must be entailed by claim row** |
| Notice bullets | Transcript section body for `#anchor` | Yes, **quote fragments or paraphrase with “lecture says”** |
| Strength / confidence | L2 table | No |

**Cache key:** `civ-07:claim:{n}:{transcript_sha256_prefix}` in `site/_data/generated/civ-07-claims.json` (committed after human spot-check OR built at deploy).

**Offline fallback:** If no generated file, show claim row only (Phase 0 behavior).

---

## Feature 2 — Greece–China contrast split

### Reader experience

When the reader opens section `#greece-china-contrast` (outline click or scroll):

1. Center floor **switches layout** for this section only: **two columns**.
2. **Left (Greece):** clauses tagged in builder as `greece` (alphabet openness, Homer/poet priority, decentralization).
3. **Right (China):** clauses tagged `china` (literacy monopoly, scholar-officials, censorship, no Homer).
4. Center divider label: *Structural contrast · lecture representation*.
5. Claims **15–16** pin to this section; notes panel auto-focuses claim 16 when split opens.

### Visual layout

```
┌──────────────────┬──────────────────┐
│ Greece           │ China            │
│ (blue accent)    │ (wine accent)    │
│ transcript cols  │ transcript cols  │
└──────────────────┴──────────────────┘
```

### Data / gen-AI

| Field | Source | Gen-AI allowed? |
| --- | --- | --- |
| Column assignment | Builder rules + optional `contrast_tags` in bundle JSON | **Human-reviewed once** for `civ-07`; gen-AI proposes tags, human approves |
| Column intro line | None or one sentence from Layer 1 summary | Optional, ≤ 80 chars |
| Row-level highlights | Keyword rules (`alphabet`, `Homer`, `scholar`, `censorship`) | Yes for **highlight spans only**, not new sentences |

**Builder addition:** `scripts/build_study_edition.py` emits `contrast_split` block on `greece-china-contrast` with `{left_paragraphs[], right_paragraphs[]}` split from section body (sentence-level heuristic; manual override file `site/_data/overrides/civ-07-contrast.json` if heuristic fails).

**No gen-AI** inventing historical facts outside the section text.

---

## Feature 3 — Section seminar strip

### Reader experience

Below each transcript section (or collapsible under section header):

1. **Seminar strip** — 2 prompts + 1 “pressure question”.
2. Prompts derived from claims touching that `#slug` (if any).
3. Clicking a prompt expands **one** follow-up question (accordion); no chat thread.
4. Strip collapsed by default on mobile; open on desktop for `#homer-poet-for-people`, `#iliad-empathy`, `#greece-china-contrast` only (3 flagship sections for Phase 1).

### Visual layout

```
┌─ Section: Homer poet for people ──────────────┐
│ …transcript…                                 │
├─ Seminar ────────────────────────────────────┤
│ ▸ How does “poet for the people” change who  │
│   founds a civilization?                     │
│ ▸ What would falsify the anti-propaganda read? │
│ ▾ Pressure: Where does the lecture overstate?  │
└──────────────────────────────────────────────┘
```

### Data / gen-AI

| Field | Source | Gen-AI allowed? |
| --- | --- | --- |
| Prompts | Claim rows + section slug | Yes — `seminar` mode per [`START-HERE.md`](../START-HERE.md) guardrails |
| Follow-up | Single step only | Yes — must say when answer not in transcript |
| Pressure question | Template + section theme | Yes |

**Output file:** `site/_data/generated/civ-07-seminar.json` keyed by `slug`.

**Pilot sections only:** `homer-poet-for-people`, `iliad-empathy`, `greece-china-contrast`.

---

## Page-level composition (`civ-07`)

```
Top bar (status + route + video)
├── Outline (16 sections + badges)
├── Floor
│   ├── opening
│   ├── sections 1–15 (standard + seminar strip on 3)
│   └── section 16: GREECE–CHINA SPLIT
└── Notes
    ├── Layer 1 summary (collapsible)
    ├── Claim morph OR list (Feature 1)
    └── Concepts (unchanged)
```

---

## Gen-AI policy (Phase 1)

1. **Inputs bounded** to: claim row, matching transcript section, Layer 1 summary, public card if present.
2. **Outputs are study aids**, not corpus edits — never write back to `book/` automatically.
3. **Cache + version** every generated artifact; regenerate only when transcript or claim table changes.
4. **Human approval** before first public GitHub Pages deploy with generated copy (operator spot-check 16 claims + 3 seminar blocks + contrast split).
5. **Abstention string** required in prompts: *If not supported by the section, say “not stated in this lecture passage.”*

Suggested offline generation script (Phase 1b): `scripts/generate_study_edition_aids.py --chapter civ-07` (provider-neutral prompt to stdout/file; no API key in repo).

---

## Acceptance criteria (`civ-07` done)

- [ ] Claim morph works for all 16 claims; fallback without generated JSON.
- [ ] Greece–China section renders split; both columns traceable to same section body.
- [ ] Seminar strips on 3 flagship sections; expand/collapse accessible.
- [ ] `validate_study_edition.py` extended for new bundle fields.
- [ ] Lighthouse: readable contrast, keyboard nav for outline/claims/split.
- [ ] One operator pass: no generated text contradicts Layer 2 claim for same `n`.

---

## Implementation order

| Step | Work | Owner |
| --- | --- | --- |
| 1 | Extend bundle JSON schema (`contrast_split`, `seminar`, `claim_aids`) | Builder |
| 2 | CSS: morph card + split columns + seminar strip | Front-end |
| 3 | JS: morph state machine; split section detector on scroll/click | Front-end |
| 4 | Manual `civ-07-contrast.json` override if heuristic split wrong | Content |
| 5 | Generate aids JSON (optional API or hand-authored pilot) | Operator |
| 6 | Extend validator + update Phase 0 checklist in `study-edition.md` | Tooling |

---

## See also

- [`study-edition.md`](./study-edition.md) — architecture + stack choice
- [`site/README.md`](../site/README.md) — build/preview
- [`START-HERE.md`](../START-HERE.md) — `seminar` reader mode guardrails
