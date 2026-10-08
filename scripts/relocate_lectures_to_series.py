#!/usr/bin/env python3
"""PH-LECTURES: relocate all lecture packets to lectures/{series}/.

    python scripts/relocate_lectures_to_series.py
    python scripts/relocate_lectures_to_series.py --dry-run
    PYTHONPATH=src python -m civ_ph.cli index --force
    PYTHONPATH=src python -m civ_ph.cli validate
    pytest
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from civ_ph.ph_civ_index import LECTURE_SERIES  # noqa: E402

SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", "node_modules", "runtime"}
SKIP_FILES = {"relocate_lectures_to_series.py"}
SERIES_FOLDER = {
    "civilization": "civilization",
    "great-books": "great-books",
    "geo-strategy": "geo-strategy",
    "game-theory": "game-theory",
    "secret-history": "secret-history",
}


@dataclass
class MoveSpec:
    source_id: str
    series: str
    src_dir: Path
    dst_dir: Path
    legacy_dir: Path


def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    import yaml

    return yaml.safe_load(parts[1]) or {}


def rel_posix(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def discover_folder_moves(glob_pattern: str, series: str, legacy_parent: Path) -> list[MoveSpec]:
    moves: list[MoveSpec] = []
    folder = SERIES_FOLDER[series]
    for src in sorted(ROOT.glob(glob_pattern)):
        if not src.is_dir():
            continue
        sid = src.name
        dst = ROOT / "lectures" / folder / sid
        legacy = legacy_parent / sid
        moves.append(MoveSpec(sid, series, src, dst, legacy))
    return moves


def discover_gt_moves() -> list[MoveSpec]:
    moves: list[MoveSpec] = []
    for src in sorted((ROOT / "lectures" / "game-theory").glob("gt-*")):
        if not src.is_dir():
            continue
        sid = src.name
        moves.append(MoveSpec(sid, "game-theory", src, src, src))
    return moves


def discover_geo_moves() -> list[MoveSpec]:
    moves: list[MoveSpec] = []
    for transcript in sorted(ROOT.glob("book/volume-i/geo-*-transcript.md")):
        sid = transcript.name.replace("-transcript.md", "")
        dst = ROOT / "lectures" / "geo-strategy" / sid
        legacy = ROOT / "book" / "volume-i" / sid
        moves.append(MoveSpec(sid, "geo-strategy", ROOT / "book" / "volume-i", dst, legacy))
    return moves


def collect_moves() -> list[MoveSpec]:
    moves: list[MoveSpec] = []
    moves.extend(discover_folder_moves("book/volume-ii/civ-*", "civilization", ROOT / "book" / "volume-ii"))
    moves.extend(discover_folder_moves("book/volume-v/gb-*", "great-books", ROOT / "book" / "volume-v"))
    moves.extend(discover_folder_moves("book/volume-vi/sh-*", "secret-history", ROOT / "book" / "volume-vi"))
    moves.extend(discover_gt_moves())
    moves.extend(discover_geo_moves())
    return moves


def geo_flat_files(source_id: str) -> list[Path]:
    base = ROOT / "book" / "volume-i" / source_id
    vol = ROOT / "book" / "volume-i"
    names = [
        f"{source_id}-transcript.md",
        f"{source_id}-commentary.md",
        f"{source_id}-orientation.yaml",
        f"{source_id}-media.yaml",
    ]
    return [vol / name for name in names if (vol / name).is_file()]


def geo_readme(source_id: str, title: str, source_url: str, review_status: str) -> str:
    return f"""# {title}

This chapter folder is a public study doorway for `{source_id}`.

## Start Here

Use this folder when someone shares the GitHub chapter link in a YouTube comment or an LLM chat. Start with the transcript, then use the commentary canvas and orientation card to keep the reading bounded.

## Source-Lattice Reading Order

Treat this chapter folder as a small source-lattice:

1. `Doorway` - this README tells you what the packet is and what limits apply.
2. `Primary source floor` - read the transcript and public source capture first.
3. `Secondary support` - use the commentary canvas, orientation payload, and public card only after the source floor is open.
4. `Widened interpretation` - draw comparisons or broader claims only after keeping the review status in view.

## Source Video

- YouTube: {source_url}

## Files

- [Transcript]({source_id}-transcript.md)
- [Commentary canvas]({source_id}-commentary.md)
- [Orientation payload]({source_id}-orientation.yaml)
- [Public card](../../../data/cards/{source_id}.md)

## Review Status

`{review_status}`. Do not treat provisional transcript text, named claims, quotations, or current-event predictions as final until review is complete.

## LLM Prompt

Paste this folder link into ChatGPT, Claude, or Grok and ask:

> Guide me through this chapter folder as a public study packet. Start with the transcript, then use the commentary canvas and orientation/card guardrails. Keep provisional claims bounded and separate lecture representation from verification.
>
> Use a source-lattice reading order: README first, transcript and source capture second, commentary/orientation/card third, and broader interpretation only after the source floor is stable.

## Guardrails

This folder represents the public lecture material and companion study apparatus. It is not a private note dump, not an endorsement layer, and not a substitute for source review.
"""


def legacy_redirect_readme(source_id: str, canonical_rel: str, legacy_label: str) -> str:
    return f"""# {source_id} — legacy redirect

The canonical lecture packet for `{source_id}` now lives under [`lectures/`](../../lectures/README.md).

## Canonical packet

- [{canonical_rel}](../../{canonical_rel}/README.md)

## Staged status

This {legacy_label} path is a **compat redirect** after PH-LECTURES recanonicalization. Do not add new transcript or commentary files here.
"""


def move_folder_packet(spec: MoveSpec, *, dry_run: bool) -> None:
    if spec.series == "geo-strategy":
        move_geo_packet(spec, dry_run=dry_run)
        return
    if spec.dst_dir.exists() and not spec.src_dir.samefile(spec.dst_dir):
        if any(spec.dst_dir.iterdir()):
            if not dry_run:
                print(f"skip move (target exists): {rel_posix(spec.dst_dir)}")
            return
    spec.dst_dir.parent.mkdir(parents=True, exist_ok=True)
    if dry_run:
        print(f"move {rel_posix(spec.src_dir)} -> {rel_posix(spec.dst_dir)}")
        return
    if spec.src_dir.exists():
        shutil.move(str(spec.src_dir), str(spec.dst_dir))
        print(f"moved {spec.source_id} -> {rel_posix(spec.dst_dir)}")


def move_geo_packet(spec: MoveSpec, *, dry_run: bool) -> None:
    dst = spec.dst_dir
    if dst.exists() and any(dst.iterdir()):
        if not dry_run:
            print(f"skip geo (target exists): {rel_posix(dst)}")
        return
    files = geo_flat_files(spec.source_id)
    if not files and not dst.exists():
        return
    transcript = ROOT / "book" / "volume-i" / f"{spec.source_id}-transcript.md"
    if not transcript.is_file() and dst.exists():
        return
    meta = parse_frontmatter(transcript.read_text(encoding="utf-8")) if transcript.is_file() else {}
    title = str(meta.get("title") or spec.source_id)
    source_url = str(meta.get("canonical_url") or meta.get("source_url") or "")
    review_status = str(meta.get("review_status") or "provisional")
    if dry_run:
        print(f"geo assemble {spec.source_id} -> {rel_posix(dst)}")
        return
    dst.mkdir(parents=True, exist_ok=True)
    for path in files:
        shutil.move(str(path), str(dst / path.name))
    readme = dst / "README.md"
    if not readme.is_file():
        readme.write_text(
            geo_readme(spec.source_id, title, source_url, review_status),
            encoding="utf-8",
            newline="\n",
        )
    print(f"assembled geo {spec.source_id} -> {rel_posix(dst)}")


def write_legacy_stub(spec: MoveSpec, *, dry_run: bool) -> None:
    folder = SERIES_FOLDER[spec.series]
    canonical = f"lectures/{folder}/{spec.source_id}"
    if spec.series == "geo-strategy":
        stub_dir = ROOT / "book" / "volume-i" / spec.source_id
        legacy_label = "`book/volume-i` flat-file"
    elif spec.series == "game-theory":
        return
    else:
        stub_dir = spec.legacy_dir
        legacy_label = f"`book/{spec.legacy_dir.parent.name}`"
    if dry_run:
        print(f"stub {rel_posix(stub_dir)}")
        return
    stub_dir.mkdir(parents=True, exist_ok=True)
    for child in stub_dir.iterdir():
        if child.name == "README.md":
            continue
        if child.is_file():
            child.unlink()
        elif child.is_dir():
            shutil.rmtree(child)
    (stub_dir / "README.md").write_text(
        legacy_redirect_readme(spec.source_id, canonical, legacy_label),
        encoding="utf-8",
        newline="\n",
    )


def dedupe_volume_iii_gt(moves: list[MoveSpec], *, dry_run: bool) -> None:
    gt_ids = {m.source_id for m in moves if m.series == "game-theory"}
    for sid in sorted(gt_ids):
        stub_dir = ROOT / "book" / "volume-iii" / sid
        if not stub_dir.is_dir():
            continue
        canonical = f"lectures/game-theory/{sid}"
        if dry_run:
            print(f"volume-iii stub {sid}")
            continue
        for child in stub_dir.iterdir():
            if child.name == "README.md":
                continue
            if child.is_file():
                child.unlink()
            elif child.is_dir():
                shutil.rmtree(child)
        (stub_dir / "README.md").write_text(
            legacy_redirect_readme(sid, canonical, "`book/volume-iii` duplicate"),
            encoding="utf-8",
            newline="\n",
        )


def build_replacements(moves: list[MoveSpec]) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for spec in moves:
        folder = SERIES_FOLDER[spec.series]
        sid = spec.source_id
        if spec.series == "geo-strategy":
            old_base = f"book/volume-i/{sid}"
            new_base = f"lectures/geo-strategy/{sid}"
            for suffix in ("-transcript.md", "-commentary.md", "-orientation.yaml", "-media.yaml"):
                pairs.append((f"{old_base}{suffix}", f"{new_base}/{sid}{suffix}"))
            pairs.append((f"{old_base}/", f"{new_base}/"))
            continue
        if spec.series == "game-theory":
            for prefix in ("ph-civ/chapters", "ph-apo/chapters"):
                old_base = f"{prefix}/{sid}"
                new_base = f"lectures/game-theory/{sid}"
                pairs.append((f"{old_base}/{sid}-transcript.md", f"{new_base}/{sid}-transcript.md"))
                pairs.append((f"{old_base}/{sid}-commentary.md", f"{new_base}/{sid}-commentary.md"))
                pairs.append(
                    (f"{old_base}/{sid}-orientation.yaml", f"{new_base}/{sid}-orientation.yaml")
                )
                pairs.append((f"{old_base}/{sid}-media.yaml", f"{new_base}/{sid}-media.yaml"))
                pairs.append((f"{old_base}/README.md", f"{new_base}/README.md"))
                pairs.append((f"{old_base}/", f"{new_base}/"))
                pairs.append((f"`{old_base}`", f"`{new_base}`"))
                pairs.append((f"Return through `{old_base}/`", f"Return through `{new_base}/`"))
            continue
        legacy_vol = {
            "civilization": "book/volume-ii",
            "great-books": "book/volume-v",
            "secret-history": "book/volume-vi",
        }[spec.series]
        old_base = f"{legacy_vol}/{sid}"
        new_base = f"lectures/{folder}/{sid}"
        for suffix in ("-transcript.md", "-commentary.md", "-orientation.yaml", "-media.yaml"):
            pairs.append((f"{old_base}/{sid}{suffix}", f"{new_base}/{sid}{suffix}"))
        pairs.append((f"{old_base}/README.md", f"{new_base}/README.md"))
        pairs.append((f"{old_base}/", f"{new_base}/"))
    pairs = list(dict.fromkeys(pairs))
    pairs.sort(key=lambda p: len(p[0]), reverse=True)
    return pairs


def rewrite_text(text: str, pairs: list[tuple[str, str]]) -> str:
    for old, new in pairs:
        text = text.replace(old, new)
    return text


def fix_civ_readme_links(text: str) -> str:
    text = text.replace("../../volume-v/", "../../great-books/")
    text = text.replace("../../volume-vi/", "../../secret-history/")
    text = text.replace(
        "../../volume-i-civilization/",
        "../../../lectures/",
    )
    return text


def patch_moved_readmes(moves: list[MoveSpec], *, dry_run: bool) -> None:
    for spec in moves:
        if spec.series != "civilization":
            continue
        readme = spec.dst_dir / "README.md"
        if not readme.is_file():
            continue
        text = readme.read_text(encoding="utf-8")
        patched = fix_civ_readme_links(text)
        if patched != text and not dry_run:
            readme.write_text(patched, encoding="utf-8", newline="\n")


def refresh_staged_wrappers(moves: list[MoveSpec], *, dry_run: bool) -> None:
    by_id = {m.source_id: m for m in moves}
    wrapper_map = [
        ("lectures/civilization-spine", "civ-", "civilization", "../../../volume-ii"),
        ("lectures/great-books-evidence", "gb-", "great-books", "../../../volume-v"),
        ("lectures/secret-history-support", "sh-", "secret-history", "../../../volume-vi"),
        ("lectures/geo", "geo-", "geo-strategy", "../../../volume-i"),
        ("lectures/gt", "gt-", "game-theory", None),
        ("lectures/sh", "sh-", "secret-history", "../../../volume-vi"),
    ]
    for base, prefix, series, legacy_vol in wrapper_map:
        folder = SERIES_FOLDER[series]
        for path in sorted(ROOT.glob(f"{base}/{prefix}*/README.md")):
            sid = path.parent.name
            if sid not in by_id and not (ROOT / "lectures" / folder / sid).is_dir():
                continue
            canonical = f"lectures/{folder}/{sid}"
            text = path.read_text(encoding="utf-8")
            new_block = (
                f"- [Canonical packet](../../../../{canonical}/README.md)\n"
            )
            if legacy_vol and series != "geo-strategy":
                new_block += f"- [Legacy redirect]({legacy_vol}/{sid}/README.md)\n"
            elif series == "geo-strategy":
                new_block += f"- [Legacy redirect](../../../volume-i/{sid}/README.md)\n"
            elif series == "game-theory":
                pass
            if "## Current Source Packet" in text:
                text = re.sub(
                    r"## Current Source Packet\n\n.*?(?=\n## |\Z)",
                    "## Current Source Packet\n\n" + new_block + "\n",
                    text,
                    count=1,
                    flags=re.DOTALL,
                )
            elif "Legacy source packet" in text:
                text = re.sub(
                    r"- \[Legacy source packet\]\([^)]+\)\n",
                    new_block,
                    text,
                    count=1,
                )
            if "until a later move pass" in text:
                text = text.replace(
                    "until a later move pass",
                    "after PH-LECTURES recanonicalization (legacy paths are redirect stubs)",
                )
            if not dry_run and text != path.read_text(encoding="utf-8"):
                path.write_text(text, encoding="utf-8", newline="\n")


def patch_tree(pairs: list[tuple[str, str]], *, dry_run: bool) -> int:
    needles = [p[0] for p in pairs if len(p[0]) > 8]
    changed = 0
    for path in ROOT.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if not path.is_file():
            continue
        if path.name in SKIP_FILES:
            continue
        if path.suffix not in {".md", ".json", ".jsonl", ".yaml", ".yml", ".py", ".txt"}:
            continue
        if path.parts[0] == "runtime":
            continue
        text = path.read_text(encoding="utf-8")
        if not any(n in text for n in needles):
            continue
        patched = rewrite_text(text, pairs)
        if patched != text:
            changed += 1
            if not dry_run:
                path.write_text(patched, encoding="utf-8", newline="\n")
    return changed


def update_namespace_readmes(*, dry_run: bool) -> None:
    lectures_readme = ROOT / "lectures" / "README.md"
    if lectures_readme.is_file():
        text = lectures_readme.read_text(encoding="utf-8")
        old = "Most lecture chapters still live under [`book/`](../book/) during recanonicalization."
        new = "Canonical lecture packets live under `lectures/<series>/`; legacy `book/volume-*` paths are compat redirect stubs."
        if old in text:
            text = text.replace(old, new)
            if not dry_run:
                lectures_readme.write_text(text, encoding="utf-8", newline="\n")
    for series, blurb in [
        ("civilization", "Volume I civilization spine (`civ-*`)."),
        ("great-books", "Great Books evidence lectures (`gb-*`)."),
        ("geo-strategy", "Geo-strategy lectures (`geo-*`)."),
        ("game-theory", "Game Theory lectures (`gt-*`)."),
        ("secret-history", "Secret History lectures (`sh-*`)."),
    ]:
        path = ROOT / "lectures" / series / "README.md"
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if "during recanonicalization" in text:
            text = re.sub(
                r" during recanonicalization\.[^\n]*",
                f". {blurb} Legacy book paths redirect here.",
                text,
            )
            if not dry_run:
                path.write_text(text, encoding="utf-8", newline="\n")


def verify_moves(moves: list[MoveSpec]) -> None:
    for spec in moves:
        transcript = spec.dst_dir / f"{spec.source_id}-transcript.md"
        commentary = spec.dst_dir / f"{spec.source_id}-commentary.md"
        if not transcript.is_file():
            raise SystemExit(f"missing transcript after move: {transcript}")
        if not commentary.is_file():
            raise SystemExit(f"missing commentary after move: {commentary}")
        if spec.series != "geo-strategy":
            readme = spec.dst_dir / "README.md"
            if not readme.is_file():
                raise SystemExit(f"missing README after move: {readme}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Relocate lecture packets to lectures/{series}/")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    moves = collect_moves()
    if not moves:
        print("no lecture packets discovered")
        return 0
    print(f"discovered {len(moves)} lecture packets")
    folder_moves = [m for m in moves if m.series != "geo-strategy"]
    geo_moves = [m for m in moves if m.series == "geo-strategy"]
    for spec in folder_moves:
        move_folder_packet(spec, dry_run=args.dry_run)
    for spec in geo_moves:
        move_folder_packet(spec, dry_run=args.dry_run)
    if not args.dry_run:
        for spec in moves:
            write_legacy_stub(spec, dry_run=False)
        dedupe_volume_iii_gt(moves, dry_run=False)
        patch_moved_readmes(moves, dry_run=False)
    pairs = build_replacements(moves)
    changed = patch_tree(pairs, dry_run=args.dry_run)
    print(f"patched {changed} files")
    refresh_staged_wrappers(moves, dry_run=args.dry_run)
    update_namespace_readmes(dry_run=args.dry_run)
    if not args.dry_run:
        verify_moves(moves)
        print("PH-LECTURES relocation complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
