# PH surface retirement — ph-civ / ph-apo namespace cutover

Program to retire **`ph-civ/`** and **`ph-apo/`** folder trees, migrate public identity to the **`predictive-history`** CLI, and deprecate two-volume **`--part`** filters.

## Scope

| In scope | Out of scope (this program) |
|---|---|
| Tombstone-only `ph-civ/` + `ph-apo/` | Rename `src/civ_ph/` Python package |
| `predictive-history` CLI + pyproject | GitHub repo rename (already `predictive-history`) |
| `derived_corpus` → `predictive-history` | Rename `ph-civ-zh` / `ph-civ-ru` mirror IDs |
| Deprecate `--part civilization\|world-war\|provenance` | Volume I `build_study_edition.py --part 01` … `10` |
| GitHub Pages `/ph-civ/` → `/predictive-history/` | Downstream mirror sync (separate commit lane) |

## Commit map (predictive-history)

1. **Hygiene** — tombstones, delete stub trees, unified `reader_namespace_guard`, archive hub, policy rewrite
2. **Identity** — CLI rename, metadata migration, cards prose, index regen (atomic)
3. **Pages** — study edition base path
4. **Guard final** — remove shims and `--part` flags; harden metadata guards

## CLI mapping

| Legacy | Target |
|---|---|
| `ph-civ list` / `ph-apo list` | `predictive-history list` (full catalog default) |
| `--part civilization` | `--series civilization` or full catalog |
| `--part world-war` | **removed** — use series/namespace filters |
| `--part provenance` | archive metadata only |
| `surface ph-civ` | deprecated; use namespace catalog hub |

Temporary **`ph-civ`** / **`ph-apo`** console shims may exist between commits 2–4; removed before final push.

## gh-pages cutover (commit 3)

1. Update `scripts/build_study_edition.py` base to `'/predictive-history/'`
2. Redeploy study edition to `https://mira-builds.github.io/predictive-history/`
3. Repo **Settings → Pages** — confirm publish root matches [`site/README.md`](../../site/README.md)
4. Old `/ph-civ/` URLs — expect 404; tombstones and this doc are the operator-facing redirect story

## Verification

```bash
PYTHONPATH=src python -m civ_ph.cli validate
python -m pytest -q
```

After identity commit:

```bash
predictive-history validate
predictive-history index --force
```

After Pages commit:

```bash
python scripts/validate_study_edition.py --part 01
```

## Related

- [`deprecated-reader-namespaces.md`](../archive/deprecated-reader-namespaces.md)
- [`two-volume-ph-civ-apo-deprecated.md`](../archive/two-volume-ph-civ-apo-deprecated.md)
- [`PH-LECTURES-RELOCATION.md`](PH-LECTURES-RELOCATION.md)
