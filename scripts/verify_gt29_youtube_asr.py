#!/usr/bin/env python3
"""Compare gt-29 lecture transcript against YouTube auto-captions (local operator run).

Requires yt-dlp (`python -m pip install yt-dlp`) and network access that YouTube
does not block. If bot-check blocks the fetch, pass browser cookies:

  python scripts/verify_gt29_youtube_asr.py --cookies-from-browser chrome

Writes: artifacts/gt-29-asr-verify.md
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import date
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VIDEO_ID = "RE2UribEFIo"
VIDEO_URL = f"https://www.youtube.com/watch?v={VIDEO_ID}"
TRANSCRIPT = ROOT / "lectures/game-theory/gt-29/gt-29-transcript.md"
ARTIFACTS = ROOT / "artifacts"
REPORT = ARTIFACTS / "gt-29-asr-verify.md"

OPENING_ANCHORS = [
    "So, welcome to the final examination",
    "thank Alan and Vincent",
    "Substack community",
]
CLOSING_ANCHORS = [
    "almost two hours",
    "enjoy the rest of your life",
]


def strip_frontmatter(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            text = text[end + 5 :]
    return text


def transcript_body(text: str) -> str:
    text = strip_frontmatter(text)
    marker = "## Part I: Full transcript"
    idx = text.find(marker)
    if idx == -1:
        return text.strip()
    return text[idx + len(marker) :].strip()


def normalize_for_compare(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\[snorts\]", " ", text, flags=re.I)
    text = re.sub(r"\[clears throat\]", " ", text, flags=re.I)
    text = re.sub(r"\[laughter\]", " ", text, flags=re.I)
    text = re.sub(r"\[music\]", " ", text, flags=re.I)
    text = re.sub(r">>\s*", " ", text)
    text = re.sub(r"[^\w\s']", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def vtt_to_plain(vtt: str) -> str:
    blocks = re.split(r"\n\n+", vtt.replace("\r\n", "\n"))
    parts: list[str] = []
    prev: str | None = None
    for block in blocks:
        if "-->" not in block:
            continue
        lines: list[str] = []
        for line in block.splitlines():
            s = line.strip()
            if not s or "-->" in s or s.isdigit() or s.startswith("align:"):
                continue
            if s.startswith("Kind:") or s.startswith("Language:"):
                continue
            s = re.sub(r"<[^>]+>", "", s).strip()
            if s:
                lines.append(s)
        if not lines:
            continue
        best = max(lines, key=len)
        if best != prev:
            parts.append(best)
            prev = best
    return re.sub(r"\s+", " ", " ".join(parts)).strip()


def download_subs(out_stem: Path, cookies_from_browser: str | None) -> Path:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        "-m",
        "yt_dlp",
        "--write-auto-subs",
        "--write-subs",
        "--sub-lang",
        "en.*,en",
        "--convert-subs",
        "vtt",
        "--skip-download",
        f"--output={out_stem}",
        VIDEO_URL,
    ]
    if cookies_from_browser:
        cmd.insert(-1, f"--cookies-from-browser={cookies_from_browser}")
    subprocess.run(cmd, check=True, cwd=ROOT)
    matches = sorted(ARTIFACTS.glob("gt-29-subs*.vtt"))
    if not matches:
        raise FileNotFoundError("No VTT subtitle file produced under artifacts/")
    return matches[0]


def structural_checks(body: str) -> list[str]:
    lines: list[str] = []
    lines.append(f"- Transcript body length: **{len(body):,}** characters")
    lines.append(f"- `>>` Q&A markers: **{body.count('>>')}**")
    for phrase in OPENING_ANCHORS + CLOSING_ANCHORS:
        ok = phrase.lower() in body.lower()
        lines.append(f"- Anchor {phrase!r}: **{'pass' if ok else 'fail'}**")
    return lines


def compare_bodies(pasted: str, asr_plain: str) -> dict[str, str | float]:
    a = normalize_for_compare(pasted)
    b = normalize_for_compare(asr_plain)
    ratio = SequenceMatcher(None, a, b).ratio()
    a_words = a.split()
    b_words = b.split()
    overlap = len(set(a_words) & set(b_words)) / max(len(set(a_words)), 1)
    return {
        "sequence_ratio": ratio,
        "token_overlap": overlap,
        "pasted_words": len(a_words),
        "asr_words": len(b_words),
    }


def render_report(
    *,
    fetch_status: str,
    fetch_detail: str,
    structural: list[str],
    metrics: dict[str, str | float] | None,
    vtt_path: Path | None,
) -> str:
    today = date.today().isoformat()
    lines = [
        f"# gt-29 YouTube ASR verification ({today})",
        "",
        f"- **Video:** [{VIDEO_ID}]({VIDEO_URL})",
        f"- **Transcript:** `lectures/game-theory/gt-29/gt-29-transcript.md`",
        "",
        "## Fetch",
        "",
        f"- **Status:** {fetch_status}",
        f"- **Detail:** {fetch_detail}",
    ]
    if vtt_path:
        lines.append(f"- **VTT:** `{vtt_path.relative_to(ROOT).as_posix()}`")
    lines.extend(["", "## Structural spot-check (pasted body)", ""])
    lines.extend(structural)
    if metrics:
        lines.extend(
            [
                "",
                "## Normalized comparison (pasted vs YouTube ASR)",
                "",
                f"- Sequence similarity ratio: **{metrics['sequence_ratio']:.4f}**",
                f"- Token overlap: **{metrics['token_overlap']:.4f}**",
                f"- Pasted words: **{int(metrics['pasted_words']):,}**",
                f"- ASR words: **{int(metrics['asr_words']):,}**",
                "",
                "### Interpretation",
                "",
                "- **≥ 0.90** sequence ratio: strong ASR alignment; candidate for `fidelity_reviewed_at` + `transcript_source: youtube_auto_captions` after human spot-check.",
                "- **0.75–0.90**: partial alignment; keep `review_status: provisional`; note drift (paste curation vs auto-captions).",
                "- **< 0.75**: do not upgrade; re-ingest or manual reconcile.",
            ]
        )
    else:
        lines.extend(
            [
                "",
                "## ASR comparison",
                "",
                "Not run (subtitle fetch failed). Re-run locally:",
                "",
                "```powershell",
                "cd <predictive-history-checkout>",
                "python scripts/verify_gt29_youtube_asr.py --cookies-from-browser chrome",
                "```",
            ]
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify gt-29 transcript against YouTube ASR")
    parser.add_argument(
        "--cookies-from-browser",
        help="Browser for yt-dlp cookies (e.g. chrome, edge, firefox)",
    )
    parser.add_argument("--structural-only", action="store_true", help="Skip subtitle fetch")
    args = parser.parse_args()

    pasted = transcript_body(TRANSCRIPT.read_text(encoding="utf-8"))
    structural = structural_checks(pasted)

    vtt_path: Path | None = None
    metrics: dict[str, str | float] | None = None
    fetch_status = "skipped"
    fetch_detail = "--structural-only"

    if not args.structural_only:
        try:
            vtt_path = download_subs(ARTIFACTS / "gt-29-subs", args.cookies_from_browser)
            asr_plain = vtt_to_plain(vtt_path.read_text(encoding="utf-8"))
            metrics = compare_bodies(pasted, asr_plain)
            fetch_status = "ok"
            fetch_detail = "YouTube subtitles downloaded and compared"
        except subprocess.CalledProcessError as exc:
            fetch_status = "failed"
            fetch_detail = f"yt-dlp exit {exc.returncode} (often YouTube bot-check; try --cookies-from-browser)"
        except Exception as exc:  # noqa: BLE001 — CLI report surface
            fetch_status = "failed"
            fetch_detail = str(exc)

    REPORT.write_text(
        render_report(
            fetch_status=fetch_status,
            fetch_detail=fetch_detail,
            structural=structural,
            metrics=metrics,
            vtt_path=vtt_path,
        ),
        encoding="utf-8",
    )
    print(REPORT.read_text(encoding="utf-8"))
    return 0 if metrics and float(metrics["sequence_ratio"]) >= 0.90 else 1


if __name__ == "__main__":
    raise SystemExit(main())
