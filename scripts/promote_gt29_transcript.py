"""Refresh gt-29 lecture transcript frontmatter (lectures/ is canonical SSOT)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEC = ROOT / "lectures/game-theory/gt-29/gt-29-transcript.md"

FRONTMATTER = """---
source_id: "gt-29"
title: "Game Theory #29: Final Examination"
source_series: "Game Theory"
publication_date: "2026-06-04"
source_url: "https://www.youtube.com/watch?v=RE2UribEFIo"
video_id: "RE2UribEFIo"
transcript_status: "public_transcript"
transcript_fidelity: "exact_body_match"
transcript_source: "user_pasted_public_transcript"
representation_not_endorsement: true
review_status: "provisional"
source_captured_at: "2026-06-04"
fidelity_review_note: "Lecture transcript body aligned 2026-06-26. External YouTube ASR compare not completed in CI (bot-check); run scripts/verify_gt29_youtube_asr.py locally. See artifacts/gt-29-asr-verify.md."
part: "world-war"
part_role: "world-war"
date_inference_note: "Publication date inferred from lecture references to 'next Sunday, June 7' and 'tomorrow will be my last class'."
---

# Game Theory #29: Final Examination

## Part I: Full transcript

"""

SELF_LINK = re.compile(
    r"^Canonical public source capture:\n"
    r"\[sources/predictive-history/game-theory/gt-29\.md\]\([^\)]+\)\n\n",
    re.MULTILINE,
)


def extract_transcript_body(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        text = text[end + 5 :]
    marker = "## Part I: Full transcript"
    idx = text.find(marker)
    body = text[idx + len(marker) :].lstrip("\n")
    return SELF_LINK.sub("", body, count=1)


def main() -> None:
    if not LEC.exists():
        raise SystemExit(f"missing canonical transcript: {LEC}")
    body = extract_transcript_body(LEC.read_text(encoding="utf-8"))
    payload = FRONTMATTER + body
    LEC.write_text(payload, encoding="utf-8")
    print(f"wrote {LEC.relative_to(ROOT)} ({len(payload)} chars)")


if __name__ == "__main__":
    main()
