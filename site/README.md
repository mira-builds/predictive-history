# Study edition site (Phase 0)

Generated static reader skin for Predictive History. SSOT remains markdown under `lectures/`, `essays/`, `interviews/`, and `docs/`.

## Build

```bash
# Single chapter
python scripts/build_study_edition.py --chapter civ-07

# Part I batch (civ-01..06)
python scripts/build_study_edition.py --part 01

# Part II batch (civ-07..13; use --from-chapter civ-08 to skip civ-07 if already built)
python scripts/build_study_edition.py --part 02 --from-chapter civ-08

# Part III batch (civ-14..17)
python scripts/build_study_edition.py --part 03

# Part IV batch (civ-18..23)
python scripts/build_study_edition.py --part 04

# Part V batch (civ-24..28)
python scripts/build_study_edition.py --part 05

# Part VI batch (civ-29..34)
python scripts/build_study_edition.py --part 06

# Part VII batch (civ-35..41)
python scripts/build_study_edition.py --part 07

# Part VIII batch (civ-42..50)
python scripts/build_study_edition.py --part 08

# Part IX batch (civ-51..53)
python scripts/build_study_edition.py --part 09

# Part X batch (civ-54..60)
python scripts/build_study_edition.py --part 10

# Full site (Parts 01–10 + assets + index) — GitHub Pages artifact
python scripts/build_study_edition.py --all-parts

python scripts/validate_study_edition.py --part 01
python scripts/validate_study_edition.py --part 02 --from-chapter civ-08
python scripts/validate_study_edition.py --part 03
python scripts/validate_study_edition.py --part 04
python scripts/validate_study_edition.py --part 05
python scripts/validate_study_edition.py --part 06
python scripts/validate_study_edition.py --part 07
python scripts/validate_study_edition.py --part 08
python scripts/validate_study_edition.py --part 09
python scripts/validate_study_edition.py --part 10
python scripts/validate_study_edition.py --chapter civ-07
```

## Preview locally

- Site home: `site/dist/index.html`
- Part I index: `site/dist/study/part-01/index.html`
- Part II index: `site/dist/study/part-02/index.html`
- Part III index: `site/dist/study/part-03/index.html`
- Part IV index: `site/dist/study/part-04/index.html`
- Part V index: `site/dist/study/part-05/index.html`
- Part VI index: `site/dist/study/part-06/index.html`
- Part VII index: `site/dist/study/part-07/index.html`
- Part VIII index: `site/dist/study/part-08/index.html`
- Part IX index: `site/dist/study/part-09/index.html`
- Part X index: `site/dist/study/part-10/index.html`
- Phase 1 pilot: `site/dist/study/civ-07/index.html`

## GitHub Pages

Workflow: [`.github/workflows/study-edition-pages.yml`](../.github/workflows/study-edition-pages.yml)

- **URL:** `https://mira-builds.github.io/predictive-history/` (project site)
- **Publish dir:** `site/dist` (Actions artifact)
- Enable **Settings → Pages → GitHub Actions** on first deploy.

## Layout

- `site/_data/chapters/` — JSON bundles (build output)
- `site/dist/study/<source_id>/` — HTML study pages
- `site/assets/` — shared CSS/JS

Spec: [`docs/onboarding/study-edition.md`](../docs/onboarding/study-edition.md)

Hosting note: URLs in this document describe a prospective Pages destination. Publication of the repository alone does not enable or verify a Pages deployment.
