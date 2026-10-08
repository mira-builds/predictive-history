# Pin-cite manifest index

**SSOT:** [`data/pin-cite/volume-i-anchors.yaml`](../data/pin-cite/volume-i-anchors.yaml)

| Tool | Role |
|------|------|
| `scripts/sync_all_parts_to_manifest.py` | Refresh **all** Parts I–X in one pass (or `--part NN` for one Part) |
| `scripts/part_pin_cite_from_manifest.py --part NN` | Apply `###` rails + refresh L2 refs from manifest |
| `scripts/validate_pin_cite.py` | Every manifest slug has transcript `###`; phrases unique in lecture order |
| `scripts/part_vii_pin_cite_prep.py` … `part_x_pin_cite_prep.py` | Part-specific wrappers (delegate to manifest where wired) |

## Coverage (2026-06-12)

| Part | Chapters in manifest | Prep script |
|------|----------------------|-------------|
| I | `civ-01`–`06` | `sync_part_i_to_manifest.py` (SSOT: `part_i_pin_cite_prep`) |
| II | `civ-07`–`13` | `sync_part_ii_to_manifest.py` (SSOT: `part_ii_tier_b_uplift` + `part_ii_iii_pin_cite_sweep`) |
| III | `civ-14`–`17` | `sync_part_iii_to_manifest.py` (SSOT: `part_ii_iii_pin_cite_sweep`) |
| IV | `civ-18`–`23` | `sync_part_iv_to_manifest.py` (SSOT: `part_iv_pin_cite_prep`) |
| V | `civ-24`–`28` | `sync_part_v_to_manifest.py` (SSOT: `part_v_pin_cite_prep`) |
| VI | `civ-29`–`34` | `sync_part_vi_to_manifest.py` (SSOT: `part_vi_pin_cite_prep`) |
| VII | `civ-35`–`41` | `sync_part_vii_to_manifest.py` (SSOT: `part_vii_pin_cite_prep`) |
| VIII | `civ-42`–`50` | `sync_part_viii_to_manifest.py` (sections SSOT: manifest; refresh L2 refs) |
| IX | `civ-51`–`53` | `sync_part_ix_to_manifest.py` (sections SSOT: manifest; refresh L2 refs) |
| X | `civ-54`–`60` | `sync_part_x_to_manifest.py` (sections SSOT: manifest; refresh L2 refs) |

All Parts I–X sync via `sync_part_*` (prep SSOT or manifest sections + commentary L2 refresh).

**Discipline:** [`PIN-CITE-DISCIPLINE.md`](./PIN-CITE-DISCIPLINE.md)
