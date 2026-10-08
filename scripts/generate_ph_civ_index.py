#!/usr/bin/env python3
"""Generate chapter catalogs from data/cards.jsonl (full hub + namespace slices)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from civ_ph.data import load_cards  # noqa: E402
from civ_ph.ph_civ_index import ensure_all_indexes  # noqa: E402


def main() -> int:
    cards = load_cards()
    written = ensure_all_indexes(cards, repo_root=ROOT, force=True)
    action = "wrote" if written else "unchanged"
    print(f"{action} chapter catalogs for {len(cards)} cards (hub + namespace slices)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
