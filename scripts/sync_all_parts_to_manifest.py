#!/usr/bin/env python3
"""Refresh volume-i-anchors.yaml from all Part sync sources (Parts I–X) in one pass."""

from __future__ import annotations

import argparse
import sys

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

from manifest_sync_common import (  # noqa: E402
    MANIFEST,
    PART_SPECS,
    ROOT,
    build_entry,
    load_manifest_chapters,
    ordered_chapters,
)

# Parts VIII–X: section rails live in manifest; sync refreshes L2 claim_refs only.
MANIFEST_SECTION_PARTS = frozenset({"08", "09", "10"})


def sync_parts(part_keys: list[str]) -> int:
    if yaml is None:
        print("PyYAML required", file=sys.stderr)
        return 1
    if not MANIFEST.is_file():
        print(f"missing manifest: {MANIFEST}", file=sys.stderr)
        return 1

    sections_ssot = load_manifest_chapters()
    data = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    chapters = data.setdefault("chapters", {})
    total = 0

    for part_key in part_keys:
        spec = PART_SPECS[part_key]
        part_id = str(spec["part_id"])
        chapter_ids = list(spec["chapters"])  # type: ignore[arg-type]
        print(f"sync_all_parts_to_manifest: Part {part_key} ({part_id})")
        for cid in chapter_ids:
            if part_key in MANIFEST_SECTION_PARTS:
                prior = sections_ssot.get(cid) or chapters.get(cid)
                if not prior or not prior.get("sections"):
                    print(f"missing manifest sections for {cid}", file=sys.stderr)
                    return 1
                chapters[cid] = build_entry(
                    cid,
                    part_id,
                    sections=prior["sections"],
                )
            else:
                chapters[cid] = build_entry(cid, part_id)
            total += 1
            print(
                f"  synced {cid}: {len(chapters[cid]['sections'])} sections, "
                f"{len(chapters[cid]['claim_refs'])} claim_refs"
            )

    data["chapters"] = ordered_chapters(chapters)
    MANIFEST.write_text(
        yaml.dump(data, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
        newline="\n",
    )
    print(
        f"sync_all_parts_to_manifest: wrote {MANIFEST.relative_to(ROOT)} "
        f"({total} chapters across {len(part_keys)} part(s))"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sync pin-cite manifest for Parts I–X (or one Part)",
    )
    parser.add_argument(
        "--part",
        choices=sorted(PART_SPECS),
        help="sync a single Part only (default: all Parts 01–10)",
    )
    args = parser.parse_args()
    part_keys = [args.part] if args.part else sorted(PART_SPECS)
    return sync_parts(part_keys)


if __name__ == "__main__":
    raise SystemExit(main())
