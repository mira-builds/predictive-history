<!-- public-surface-inventory-fingerprint: c7de39f1f38c5387 -->
# Public surface inventory

- **Surfaces:** 26
- **Generated:** 2026-10-08T17:27:48Z
- **Machine SSOT:** [`data/public-surface-inventory.json`](../../data/public-surface-inventory.json)
- **Regenerate:** `predictive-history surface-inventory`

Per-surface status vocabulary: [public-surface-status.md](../../docs/catalogs/public-surface-status.md).

| Surface | Class | Status | Path | Validation |
| --- | --- | --- | --- | --- |
| `parts_v1_hybrid_archive` | archive_retired | deprecated | docs/archive/parts-v1-hybrid.md | validate:volume-i-parts-deprecated |
| `volume_i_parts_deprecated_json` | archive_retired | deprecated | data/parts/volume-i-parts.deprecated.json | manual |
| `agents_guardrails` | bootloader | canonical | AGENTS.md | validate:public-boundary |
| `start_here` | bootloader | canonical | START-HERE.md | validate:llm-experience |
| `strategy_codex_bridge` | bridge | active | docs/methodology/strategy-codex-bridge.md | manual |
| `cards_dataset` | card_dataset | active | data/cards.jsonl | validate:cards |
| `predictive_history_index` | chapter_catalog | generated | docs/predictive-history-index.json | validate:predictive-history-index |
| `chapter_folders` | chapter_folder | active | lectures/* | validate:cards |
| `ph_apo_volume_ii_chapters` | chapter_folder | active | lectures/*  | docs/predictive-history-index.json |
| `ph_civ_volume_i_chapters` | chapter_folder | active | lectures/*  | docs/predictive-history-index.json |
| `commentary_methodology_v2` | doctrine_doc | canonical | docs/methodology/commentary-methodology-v2.md | validate:commentary-canvas |
| `public_repo_contract` | doctrine_doc | canonical | docs/contracts/public-repo-contract.md | manual |
| `public_surface_status` | doctrine_doc | active | docs/catalogs/public-surface-status.md | manual |
| `source_lattice` | doctrine_doc | canonical | docs/methodology/source-lattice.md | manual |
| `growth_goals` | growth_surface | active | data/growth-goals.json | manual |
| `llm_experience` | llm_context | active | data/llm-experience.json | validate:llm-experience |
| `llms_full` | llm_context | active | llms-full.txt | validate:llm-experience |
| `llms_txt` | llm_context | active | llms.txt | validate:llm-experience |
| `patterns_dataset` | pattern_dataset | active | data/patterns.json | validate:patterns |
| `choreography_routes` | route_dataset | active | data/routes/choreography.json | validate:choreography |
| `first_tour` | route_dataset | active | data/routes/first-tour.json | validate:first-tour |
| `route_seed` | route_dataset | active | data/routes/seed.json | validate:choreography |
| `spine_tour` | route_dataset | active | data/routes/volume-i-spine-tour.json | manual |
| `public_surface_inventory` | schema_prompt | generated | data/public-surface-inventory.json | manual |
| `public_surface_triage` | schema_prompt | generated | data/public-surface-triage.json | manual |
| `transcript_commentary_chapters` | transcript | canonical | (per docs/predictive-history-index.json chapters[].paths) | docs/predictive-history-index.json |
