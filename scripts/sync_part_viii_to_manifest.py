#!/usr/bin/env python3
"""Refresh Part VIII (civ-42..50) manifest entries from volume-i-anchors sections SSOT."""

from __future__ import annotations

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


def main() -> int:
    if yaml is None:
        print("PyYAML required", file=sys.stderr)
        return 1
    spec = PART_SPECS["08"]
    part_id = str(spec["part_id"])
    chapter_ids = list(spec["chapters"])  # type: ignore[arg-type]

    existing = load_manifest_chapters()
    data = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    chapters = data.setdefault("chapters", {})
    for cid in chapter_ids:
        prior = existing.get(cid) or chapters.get(cid)
        if not prior or not prior.get("sections"):
            print(f"missing manifest sections for {cid}", file=sys.stderr)
            return 1
        chapters[cid] = build_entry(
            cid,
            part_id,
            sections=prior["sections"],
        )
        print(
            f"synced {cid}: {len(chapters[cid]['sections'])} sections, "
            f"{len(chapters[cid]['claim_refs'])} claim_refs"
        )
    data["chapters"] = ordered_chapters(chapters)
    MANIFEST.write_text(
        yaml.dump(data, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
        newline="\n",
    )
    print(f"sync_part_viii_to_manifest: wrote {MANIFEST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
