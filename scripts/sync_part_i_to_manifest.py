#!/usr/bin/env python3
"""Merge Part I (civ-01..06) pin-cite SSOT into volume-i-anchors.yaml."""

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
    ordered_chapters,
)


def main() -> int:
    if yaml is None:
        print("PyYAML required", file=sys.stderr)
        return 1
    spec = PART_SPECS["01"]
    part_id = str(spec["part_id"])
    chapter_ids = list(spec["chapters"])  # type: ignore[arg-type]

    data = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    chapters = data.setdefault("chapters", {})
    for cid in chapter_ids:
        chapters[cid] = build_entry(cid, part_id)
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
    print(f"sync_part_i_to_manifest: wrote {MANIFEST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
