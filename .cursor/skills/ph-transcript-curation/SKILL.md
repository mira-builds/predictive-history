---
name: ph-transcript-curation
description: "PH transcript curation — interviews + lectures — section rails, speaker/turn labeling, ASR repair, pass ladder, validate, PH-TRANSCRIPT-EDIT. Repo-native SSOT in docs/runbooks/."
activation: PH transcript pass
preferred_activation: PH transcript pass
repository: predictive-history
version: 1.1.0
status: active
---

# PH transcript curation (predictive-history)

**Repo SSOT:** [`docs/runbooks/ph-transcript-curation.md`](../../docs/runbooks/ph-transcript-curation.md)

Read and follow that runbook **in full** before editing. This skill file is the Cursor discovery entry for the **predictive-history** workspace only — not a strategy-codex junction mirror.

**Activations:** `PH transcript pass` · `interview section pass` · `interview turn pass` · `lecture transcript pass` · `lecture section pass` · `lecture turn pass` · `PH-TRANSCRIPT-EDIT`

**Edit surface (this repo):**

- `interviews/interview-YYYY-MM-DD-{host-slug}/`
- `lectures/{series}/{source_id}/` (`civilization` · `great-books` · `geo-strategy` · `game-theory` · `secret-history`)

**Validate:**

```bash
PYTHONPATH=src python -m civ_ph.cli validate
python -m pytest -q
```

**Exemplars:** Tucker `vi-11` (one-shot) · DOAC `ext-doac-01` (pass ladder 2–13; 14/14 pass C · `a6f86e8`) · `gt-29` (lecture Q&A pilot) · `civ-59` (monologue + slug rails).
