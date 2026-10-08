# Parts v1 hybrid — deprecated

**Status:** Retired (2026-06). Do not extend the Volume I Part apparatus under Commentary Methodology v2.

## What was deprecated

- Ten Part doorways (`part-01` … `part-10`) under [`docs/routes/volume-i-parts/`](../docs/routes/volume-i-parts/)
- Three-file apparatus per Part: doorway, **thick commentary**, bibliography
- Hybrid law: chapter L0–2 thin + Part L3–6 thick
- Machine surfaces: [`data/parts/volume-i-parts.json`](../data/parts/volume-i-parts.json) → [`volume-i-parts.deprecated.json`](../data/parts/volume-i-parts.deprecated.json)
- [`data/routes/part-boundary-tour.json`](../data/routes/part-boundary-tour.json) → [`volume-i-spine-tour.json`](../data/routes/volume-i-spine-tour.json)
- LLM `part_tour` mode → `spine_tour`
- `stub_routed_to_part` GB/SH routing

## Replacement SSOT

| Need | v2 surface |
|------|------------|
| Reading order | [`interwoven-reader/README.md`](../docs/archive/two-volume-reader-order-interwoven.md) |
| gb/sh weave | [`data/weave/volume-i-companions.json`](../data/weave/volume-i-companions.json) |
| Structured tour | [`data/routes/volume-i-spine-tour.json`](../data/routes/volume-i-spine-tour.json) |
| Interpretation | Per-chapter `*-commentary.md` L0–6 |

## Migration law

1. **Extract** load-bearing Part sections into chapter commentaries ([`commentary-methodology-v2.md`](../commentary-methodology-v2.md) §10).
2. **Freeze** Part thick files (no new edits).
3. **Archive** copies under `docs/archive/parts-v1-hybrid/` when extract acceptance passes per chapter.
4. **Strip** live Part apparatus links from chapter READMEs and frontmatter.

## Archive copies

Frozen snapshots of Part thick commentaries and hybrid readiness docs live in:

[`docs/archive/parts-v1-hybrid/`](parts-v1-hybrid/)

Original paths under `docs/routes/volume-i-parts/` remain as redirect stubs until physical removal in a later slice.

## Doctrine

**SSOT:** [commentary-methodology-v2.md](../commentary-methodology-v2.md)
