# PH / Jiang ASR blocklists

Machine-readable **residual mangling detectors** for transcript cleanup passes. Each blocklist lists `literal` strings that should not remain after normalization.

| File | Scope | SSOT | Regenerate |
| --- | --- | --- | --- |
| [`volume-ii-pilot.json`](volume-ii-pilot.json) | ph-civ Volume II `civ-01..18` transcript bodies | `ph-civ/scripts/_pilot_asr_normalize_civ01_civ07.py` | `python scripts/generate_ph_civ_asr_blocklist.py` |
| [`founding-members-pilot.json`](founding-members-pilot.json) | PH **Founding Members** livestreams in `source-archive/statecraft/` | `scripts/work_jiang/asr_transcript_replacements.py` → `FOUNDING_MEMBERS_REPLACEMENTS` | `python scripts/generate_founding_members_asr_blocklist.py` |

## Apply + validate (founding members)

```bash
python scripts/normalize_statecraft_source_asr.py \
  source-archive/statecraft/2026-06-10/source-predictive-history-founding-members-01-livestream-2026-06-10.md \
  --write

python scripts/validate_statecraft_asr_blocklist.py
```

## ph-civ Volume II

```bash
python scripts/validate_transcript_proper_nouns.py
```

**Not human-verified verbatim:** blocklists catch systematic ASR substitutions; they do not certify quote-grade accuracy.
