#!/usr/bin/env python3
"""Commentary completeness report — delegates to predictive-history commentary-status."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from civ_ph.commentary_v2 import commentary_status_report  # noqa: E402
from civ_ph.data import DATA_ROOT, load_cards  # noqa: E402


def main() -> int:
    cards = load_cards()
    report = commentary_status_report(cards, DATA_ROOT.parent)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
