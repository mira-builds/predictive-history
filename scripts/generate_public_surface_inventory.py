#!/usr/bin/env python3
"""Generate data/public-surface-inventory.json and runtime summary."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from civ_ph.data import load_cards  # noqa: E402
from civ_ph.public_surface_inventory import ensure_public_surface_inventory  # noqa: E402


def main() -> int:
    cards = load_cards()
    json_path, md_path, written = ensure_public_surface_inventory(cards, repo_root=ROOT, force=True)
    action = "wrote" if written else "unchanged"
    print(f"{action} {json_path.relative_to(ROOT)} and {md_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
