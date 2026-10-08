# Strategy-Codex Bridge

This repository (`mira-builds/predictive-history`) is the **canonical public** Predictive History corpus. `strategy-codex` is the operator workshop for statecraft synthesis, source archive, and review — not a second edit surface for this corpus.

The bridge between them is intentionally small: strategy-codex may cite public `pattern_id` values, public `source_id` cards, and public chapter bodies from this repository. It should not import private notes, raw inputs, or live strategy workspace paths into the public tree.

## How To Use Patterns

- Cite a stable `pattern_id` when a strategy page needs a reusable civilizational frame.
- Pair the `pattern_id` with the relevant public `source_id` when possible.
- Treat pattern records as orientation aids, not proof of a live claim.
- Use current primary evidence for live events, forecasts, military claims, and attribution.

Example:

```text
pattern:civ-chokepoint-pressure
sources: geo-14, gt-16
use: public frame for Hormuz / shipping / energy pressure
```

## Boundary

Do not use this repo as a strategy inbox or private editorial workspace. Public lecture transcripts for released chapters live under `lectures/`.

**Authoring loop:** edit and push **this repository** directly. strategy-codex keeps an **inbound-only read snapshot** at `public/predictive-history/` refreshed via `sync_predictive_history_mirror.py` — do not author corpus files there.

Workshop essay intake reads frozen `codex/predictive-history/` in strategy-codex and lands captures here only.
