#!/usr/bin/env python3
"""Validate study-edition bundles: anchor integrity and required outputs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE_DATA = ROOT / "site" / "_data" / "chapters"
SITE_DIST = ROOT / "site" / "dist" / "study"

PART_CHAPTERS: dict[str, list[str]] = {
    "01": [f"civ-{n:02d}" for n in range(1, 7)],
    "02": [f"civ-{n:02d}" for n in range(7, 14)],
    "03": [f"civ-{n:02d}" for n in range(14, 18)],
    "04": [f"civ-{n:02d}" for n in range(18, 24)],
    "05": [f"civ-{n:02d}" for n in range(24, 29)],
    "06": [f"civ-{n:02d}" for n in range(29, 35)],
    "07": [f"civ-{n:02d}" for n in range(35, 42)],
    "08": [f"civ-{n:02d}" for n in range(42, 51)],
    "09": [f"civ-{n:02d}" for n in range(51, 54)],
    "10": [f"civ-{n:02d}" for n in range(54, 61)],
}


def validate_phase1(bundle: dict, html: str) -> list[str]:
    errors: list[str] = []
    source_id = bundle.get("source_id", "")
    if not bundle.get("phase1"):
        return errors
    phase1 = bundle["phase1"]
    if "contrast_split" not in phase1:
        errors.append(f"{source_id}: phase1 missing contrast_split")
    elif "contrast-split" not in html:
        errors.append(f"{source_id}: HTML missing contrast split")
    if "claim-morph-view" not in html:
        errors.append(f"{source_id}: HTML missing claim morph view")
    aids = phase1.get("claim_aids") or {}
    for claim in bundle.get("claims", []):
        key = str(claim.get("n"))
        if key not in aids:
            errors.append(f"{source_id}: phase1 missing claim aid {key}")
    for slug in phase1.get("seminar_slugs") or []:
        if f'data-slug="{slug}"' not in html and f"seminar-strip" not in html:
            errors.append(f"{source_id}: HTML missing seminar strip for {slug}")
    return errors


def validate_bundle(path: Path) -> list[str]:
    errors: list[str] = []
    bundle = json.loads(path.read_text(encoding="utf-8"))
    source_id = bundle.get("source_id", path.stem)
    sections = {row["slug"] for row in bundle.get("sections", [])}
    for claim in bundle.get("claims", []):
        anchor = claim.get("anchor")
        if anchor not in sections:
            errors.append(f"{source_id}: claim {claim.get('n')} missing section #{anchor}")
    html_path = SITE_DIST / source_id / "index.html"
    if not html_path.is_file():
        errors.append(f"{source_id}: missing HTML output {html_path.relative_to(ROOT)}")
    else:
        html = html_path.read_text(encoding="utf-8")
        for slug in sections:
            if f'id="{slug}"' not in html:
                errors.append(f"{source_id}: HTML missing section id={slug}")
        for claim in bundle.get("claims", []):
            n = claim.get("n")
            if f'id="claim-{n}"' not in html:
                errors.append(f"{source_id}: HTML missing claim-{n}")
        errors.extend(validate_phase1(bundle, html))
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate study-edition outputs.")
    parser.add_argument("--chapter", help="single source_id")
    parser.add_argument("--part", choices=sorted(PART_CHAPTERS), help="validate all Part chapters")
    parser.add_argument("--from-chapter", help="first chapter when using --part")
    args = parser.parse_args(argv)

    if args.part:
        chapter_ids = list(PART_CHAPTERS[args.part])
        if args.from_chapter:
            if args.from_chapter not in chapter_ids:
                print(f"validate_study_edition: {args.from_chapter} not in Part {args.part}", file=sys.stderr)
                return 1
            chapter_ids = chapter_ids[chapter_ids.index(args.from_chapter) :]
    elif args.chapter:
        chapter_ids = [args.chapter]
    else:
        chapter_ids = ["civ-07"]

    all_errors: list[str] = []
    for cid in chapter_ids:
        json_path = SITE_DATA / f"{cid}.json"
        if not json_path.is_file():
            all_errors.append(f"missing bundle {json_path.relative_to(ROOT)}")
            continue
        all_errors.extend(validate_bundle(json_path))

    if all_errors:
        for err in all_errors:
            print(err, file=sys.stderr)
        print(f"validate_study_edition: {len(all_errors)} error(s)", file=sys.stderr)
        return 1
    label = f"Part {args.part}" if args.part else chapter_ids[0]
    print(f"validate_study_edition: ok ({label}, {len(chapter_ids)} chapter(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
