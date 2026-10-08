#!/usr/bin/env python3
"""Pass B/C turn labeling for gt-29 classroom Q&A transcript.

Pass B: ``>>`` markers → **Alan:** / **Vincent:** (question reads and prompts).
Pass C: Answer blocks → **Jiang Xueqin:** in YouTube Questions + Closing sections.
Also re-anchors the four capstone section rails (template paragraph split was wrong).

    python scripts/patch_gt29_turns_asr.py
    PYTHONPATH=src python -m civ_ph.cli validate
    python -m pytest -q
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from interview_transcript_sections import (  # noqa: E402
    PART_I_MARKER,
    common_asr_cleanup,
    insert_sections,
    update_sectioned_frontmatter,
)

ROOT = Path(__file__).resolve().parents[1]
TRANSCRIPT_PATH = ROOT / "lectures" / "game-theory" / "gt-29" / "gt-29-transcript.md"
README_PATH = ROOT / "lectures" / "game-theory" / "gt-29" / "README.md"

SECTION_TITLES = [
    "Opening and Thanks",
    "Substack Questions",
    "YouTube Questions",
    "Closing",
]

SECTION_ANCHORS = [
    "so first of all what what i'm going to do is i'm going to read all the questions",
    "so um alan, can you help can you help me read this",
    "okay, guys. well, we've been all here for almost two hours",
]

SPEAKER_ALAN = "Alan"
SPEAKER_JIANG = "Jiang Xueqin"
SPEAKER_VINCENT = "Vincent"

LABEL_RE = re.compile(r"^\*\*(Alan|Jiang Xueqin|Vincent|Student):\*\*\s*", re.I)
CHEVRON_RE = re.compile(r"^>>\s*")

PASS_C_SECTIONS = frozenset({"YouTube Questions", "Closing"})


def flatten_sections(body: str) -> str:
    lines: list[str] = []
    for line in body.splitlines():
        if line.startswith("### "):
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def split_chevron_paragraphs(body: str) -> str:
    body = re.sub(r" >> Okay\.", r"\n\n>> Okay.", body)
    body = re.sub(r"\? >> ", "?\n\n>> ", body)
    body = re.sub(
        r"([^>\n]) >> (Wait|Uh|Okay\. So|Yeah\.|All right\.|Hello,|Hi professor)",
        r"\1\n\n>> \2",
        body,
        flags=re.IGNORECASE,
    )
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body


def explode_chevron_lines(body: str) -> str:
    """Each line starting with ``>>`` becomes its own paragraph."""
    out: list[str] = []
    for line in body.splitlines():
        if line.startswith(">>"):
            if out and out[-1] != "":
                out.append("")
            out.append(line)
            out.append("")
        else:
            out.append(line)
    text = "\n".join(out)
    return re.sub(r"\n{3,}", "\n\n", text)


def resection_body(flat: str) -> str:
    return insert_sections(flat, SECTION_TITLES, SECTION_ANCHORS)


def classify_chevron_speaker(text: str) -> str:
    t = text.strip()
    tl = t.lower()

    if re.search(r"why am i (asian|chinese)|why are we (born|ourselves)", tl):
        return SPEAKER_VINCENT
    if re.search(r"i think i have a final question", tl):
        return SPEAKER_VINCENT

    if re.search(
        r"^(wait,?\s+)?can you (just )?(read|go through|keep)|"
        r"^sorry\.?\s+c can you|^all right\.?\s+can you (read|keep|uh read)",
        tl,
    ):
        return SPEAKER_JIANG
    if re.search(r"^keep keep on going|^keep on going", tl):
        return SPEAKER_JIANG

    if re.search(
        r"^this is exactly correct|^this is a great question|"
        r"^yeah,?\s+this is a great (point|question)|"
        r"^(okay\.?\s+)?(uh\s+)?first of all,?\s+i (do believe|think)|"
        r"^great\.?\s+so (there are|yeah)|"
        r"^yes\.?\s+okay\.?\s+so why are you here|"
        r"^okay\.?\s+so (china's elite|my question is how do you think civilizations)|"
        r"^okay\.?\s+right\.?\s+so this is",
        tl,
    ):
        return SPEAKER_JIANG

    if re.search(
        r"^a question from |^hi professor|^hello,?\s+professor|"
        r"^professor,|^just just read this\.?\s*my question is|^yeah\.?\s*my question is|"
        r"^one thing i appreciate about your analysis|"
        r"^all right\.?\s+this is from |^okay\.?\s+hello,?\s+professor|"
        r"^thank you for your work\.?\s*professor,",
        tl,
    ):
        return SPEAKER_ALAN
    if re.search(
        r"^two,?\s+japan as a dominant|^also,?\s+honorable mention the youtube|"
        r"^great to be part of this\.?\s*i have several questions",
        tl,
    ):
        return SPEAKER_ALAN
    if re.search(r"^okay\.?\s+all right\.?\s+all right\.?\s+let me just pick", tl):
        return SPEAKER_JIANG

    if "?" in t and len(t) > 80 and not re.search(
        r"^(okay|yeah|so|the |if you|what makes|okay\. so my question is how)",
        tl,
    ):
        return SPEAKER_ALAN

    if len(t) < 45 and re.match(r"^(okay|yeah|all right|great)\.?$", tl, re.I):
        return SPEAKER_ALAN

    if "?" not in t and len(t) > 100:
        return SPEAKER_JIANG

    return SPEAKER_ALAN


def strip_speaker_label(paragraph: str) -> tuple[str | None, str]:
    m = LABEL_RE.match(paragraph)
    if not m:
        return None, paragraph
    return m.group(1), paragraph[m.end() :]


def format_turn(speaker: str, text: str) -> str:
    return f"**{speaker}:** {text.strip()}"


def apply_pass_b(paragraphs: list[str]) -> tuple[list[str], int]:
    out: list[str] = []
    converted = 0
    for para in paragraphs:
        if para.startswith("### "):
            out.append(para)
            continue
        if CHEVRON_RE.match(para):
            text = CHEVRON_RE.sub("", para, count=1).strip()
            speaker = classify_chevron_speaker(text)
            out.append(format_turn(speaker, text))
            converted += 1
            continue
        out.append(para)
    return out, converted


def looks_like_question_read(text: str) -> bool:
    tl = text.lower()
    if re.search(
        r"^a question from|^hi professor|^hello,?\s+professor|^thank you for your work|^"
        r"professor,|^my question is|^just just read this|^yeah\.?\s*my question is|"
        r"^one thing i appreciate|^great to be part of this|^the last question",
        tl,
    ):
        return True
    if "?" in text and len(text) > 60:
        if re.search(
            r"^(okay|yeah|so|the question is|if you|what makes|when i make|"
            r"i (do believe|think|would)|this is a|that's why|for example)",
            tl,
        ):
            return False
        return True
    return False


def looks_like_jiang_answer(text: str) -> bool:
    tl = text.lower()
    if LABEL_RE.match(text):
        return False
    if looks_like_question_read(text):
        return False
    return bool(
        re.search(
            r"^(okay|yeah|great|this is a really|this is from|so this is from|"
            r"um yes it is true|the monad is|i don't know enough|"
            r"trump is not playing|okay\. so this is from|well, you know, then i would)",
            tl,
        )
        or len(text) > 180
    )


def apply_pass_c(paragraphs: list[str]) -> tuple[list[str], int]:
    out: list[str] = []
    labeled = 0
    current_section: str | None = None
    prev_speaker: str | None = None

    for para in paragraphs:
        if para.startswith("### "):
            current_section = para.removeprefix("### ").strip()
            out.append(para)
            prev_speaker = None
            continue

        if current_section not in PASS_C_SECTIONS:
            out.append(para)
            _, bare = strip_speaker_label(para)
            if LABEL_RE.match(para):
                prev_speaker = LABEL_RE.match(para).group(1)  # type: ignore[union-attr]
            continue

        existing, bare = strip_speaker_label(para)
        if existing:
            out.append(para)
            prev_speaker = existing
            continue

        if prev_speaker in {SPEAKER_ALAN, SPEAKER_VINCENT} and looks_like_jiang_answer(
            bare
        ):
            out.append(format_turn(SPEAKER_JIANG, bare))
            labeled += 1
            prev_speaker = SPEAKER_JIANG
            continue

        out.append(para)
        if existing:
            prev_speaker = existing
        else:
            prev_speaker = None

    return out, labeled


def asr_cleanup(text: str) -> str:
    return common_asr_cleanup(
        text,
        replacements={
            "Professor John,": "Professor Jiang,",
            "Professor John ": "Professor Jiang ",
            "Miss Jiang.": "Professor Jiang.",
            "Shellyley": "Shelley",
            "sub substack": "Substack",
            "All right. Uh, John Zach": "All right. Uh, Jon Zach",
        },
    )


def paragraphs_from_body(body: str) -> list[str]:
    chunks: list[str] = []
    buf: list[str] = []
    for line in body.splitlines():
        if line.startswith("### "):
            if buf:
                chunks.append("\n".join(buf).strip())
                buf = []
            chunks.append(line.strip())
            continue
        if not line.strip():
            if buf:
                chunks.append("\n".join(buf).strip())
                buf = []
            continue
        buf.append(line)
    if buf:
        chunks.append("\n".join(buf).strip())
    return [c for c in chunks if c]


def body_from_paragraphs(paragraphs: list[str]) -> str:
    parts: list[str] = []
    for para in paragraphs:
        if para.startswith("### "):
            if parts:
                parts.append("")
            parts.append(para)
            parts.append("")
        else:
            parts.append(para)
            parts.append("")
    return "\n".join(parts).strip() + "\n"


def count_exchanges(body: str) -> int:
    return len(re.findall(r"\*\*(?:Alan|Jiang Xueqin|Vincent):\*\*", body))


def count_chevrons(body: str) -> int:
    return len(re.findall(r"^>>\s", body, flags=re.M))


def update_readme(pass_b: int, pass_c: int, exchanges: int, chevrons_left: int) -> None:
    note = (
        f"**Transcript pass 2 (2026-06-26):** Pass **A** section rails (gt-qa-capstone); "
        f"re-anchored Opening / Substack / YouTube / Closing (template paragraph split had "
        f"empty Opening and YouTube rails).\n\n"
        f"**Transcript pass 3 (2026-06-26):** Pass **B + C** classroom Q&A — "
        f"{pass_b} ``>>`` → named speaker; {pass_c} answer blocks labeled "
        f"**Jiang Xueqin:**; ~{exchanges} labeled turns in YouTube Questions + Closing. "
        f"Substack block stays mostly unlabeled (Jiang reads founding-member questions inline). "
        f"``>>`` remaining: {chevrons_left}. Unresolved: merged Alan/Jiang paragraphs; "
        f"some inline YouTube questions without ``>>``; ASR (Professor John → Jiang where touched)."
    )
    text = README_PATH.read_text(encoding="utf-8")
    marker = "## Review Status\n\n"
    if "Transcript pass 2" in text:
        text = re.sub(
            r"\*\*Transcript pass 2.*?(?=\n\n## |\Z)",
            note + "\n",
            text,
            count=1,
            flags=re.S,
        )
    else:
        text = text.replace(
            marker,
            marker + note + "\n\n",
            1,
        )
    README_PATH.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    doc = TRANSCRIPT_PATH.read_text(encoding="utf-8")
    if PART_I_MARKER not in doc:
        raise ValueError("missing Part I marker")

    head, body = doc.split(PART_I_MARKER, 1)
    flat = flatten_sections(body)
    flat = split_chevron_paragraphs(flat)
    flat = explode_chevron_lines(flat)
    flat = asr_cleanup(flat)
    body = resection_body(flat)

    paragraphs = paragraphs_from_body(body)
    paragraphs, pass_b = apply_pass_b(paragraphs)
    paragraphs, pass_c = apply_pass_c(paragraphs)
    body = body_from_paragraphs(paragraphs)

    head = update_sectioned_frontmatter(
        head,
        curation="curated_sectioned",
    )
    if "transcript_curation:" not in head:
        pass

    doc = f"{head}{PART_I_MARKER}\n\n{body}"
    TRANSCRIPT_PATH.write_text(doc, encoding="utf-8", newline="\n")

    exchanges = count_exchanges(body)
    chevrons_left = count_chevrons(body)
    update_readme(pass_b, pass_c, exchanges, chevrons_left)

    print(
        f"wrote {TRANSCRIPT_PATH} — pass B: {pass_b} chevrons, "
        f"pass C: {pass_c} answer labels, {exchanges} total turns, "
        f"{chevrons_left} >> remaining"
    )


if __name__ == "__main__":
    main()
