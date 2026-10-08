#!/usr/bin/env python3
"""Verify commentary pin-cites resolve against transcript heading anchors."""
from __future__ import annotations

import argparse
import sys

from lecture_rails_lib import list_transcript_paths, verify_pin_cites_for_packet


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-id")
    args = parser.parse_args()

    if args.source_id:
        ids = [args.source_id]
    else:
        ids = sorted(
            p.name.replace("-transcript.md", "") for p in list_transcript_paths()
        )

    all_errors: list[str] = []
    for source_id in ids:
        all_errors.extend(verify_pin_cites_for_packet(source_id))

    if all_errors:
        for err in all_errors:
            print(err, file=sys.stderr)
        print(f"pin-cite verify FAIL: {len(all_errors)} errors", file=sys.stderr)
        return 1

    print(f"pin-cite verify OK ({len(ids)} packets checked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
