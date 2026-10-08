from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

from civ_ph.data import PACKAGE_ROOT

REGISTRY_PATH = PACKAGE_ROOT / "data" / "parts" / "volume-i-parts.json"
INTERWOVEN_PATH = (
    PACKAGE_ROOT / "docs" / "archive" / "two-volume-reader-order-interwoven.md"
)

CIV_LINE = re.compile(
    r"^- \[(civ-\d+)\]\([^)]+\) - Civilization #\d+: (.+)$"
)
COMPANION_LINE = re.compile(
    r"^- companion(?: \(([^)]+)\))?: \[(gb-\d+|sh-\d+)\]"
)


def civ_number(civ_id: str) -> int:
    return int(civ_id.split("-")[1])


@lru_cache(maxsize=1)
def load_volume_i_parts_registry() -> dict:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def parse_interwoven_spine(path: Path | None = None) -> list[dict]:
    """Return ordered spine entries: civ rows and companion rows with anchor_civ."""
    text = (path or INTERWOVEN_PATH).read_text(encoding="utf-8")
    entries: list[dict] = []
    current_civ: str | None = None
    for line in text.splitlines():
        civ_match = CIV_LINE.match(line)
        if civ_match:
            current_civ = civ_match.group(1)
            entries.append(
                {
                    "kind": "civ",
                    "entry_id": current_civ,
                    "anchor_civ": current_civ,
                    "title": civ_match.group(2).strip(),
                }
            )
            continue
        companion_match = COMPANION_LINE.match(line)
        if companion_match and current_civ:
            role_hint = companion_match.group(1) or "companion"
            entry_id = companion_match.group(2)
            kind = "gb" if entry_id.startswith("gb-") else "sh"
            entries.append(
                {
                    "kind": kind,
                    "entry_id": entry_id,
                    "anchor_civ": current_civ,
                    "role_hint": role_hint,
                }
            )
    return entries


def _interwoven_civ_order(entries: list[dict]) -> list[str]:
    return [entry["entry_id"] for entry in entries if entry["kind"] == "civ"]


def _interwoven_weave(entries: list[dict]) -> tuple[set[tuple[str, str]], set[tuple[str, str]]]:
    gb_pairs: set[tuple[str, str]] = set()
    sh_pairs: set[tuple[str, str]] = set()
    for entry in entries:
        if entry["kind"] == "gb":
            gb_pairs.add((entry["entry_id"], entry["anchor_civ"]))
        elif entry["kind"] == "sh":
            sh_pairs.add((entry["entry_id"], entry["anchor_civ"]))
    return gb_pairs, sh_pairs


def _title_word_count(title: str) -> int:
    return len(title.split())


def validate_volume_i_parts(
    *,
    require_doorways: bool = False,
    require_chapter_anchors: bool = False,
    require_readme_part_links: bool = False,
) -> list[str]:
    errors: list[str] = []
    if not REGISTRY_PATH.exists():
        return ["missing registry: data/parts/volume-i-parts.json"]

    registry = load_volume_i_parts_registry()
    parts: list[dict] = registry.get("parts", [])
    part_count = registry.get("part_count")
    title_max = registry.get("title_max_words", 6)
    blocklist = set(registry.get("photocopy_blocklist", []))

    if part_count != len(parts):
        errors.append(f"part_count {part_count} != parts.length {len(parts)}")
    if part_count != 10:
        errors.append(f"expected 10 parts, got {part_count}")

    if not INTERWOVEN_PATH.exists():
        errors.append("missing interwoven spine SSOT")
        return errors

    spine_entries = parse_interwoven_spine()
    spine_civs = _interwoven_civ_order(spine_entries)
    spine_gb, spine_sh = _interwoven_weave(spine_entries)

    if spine_civs != [f"civ-{n:02d}" for n in range(1, 61)]:
        errors.append("interwoven spine must list civ-01 through civ-60 contiguously")

    birth_titles = 0
    medieval_titles = 0

    for index, part in enumerate(parts):
        part_id = part.get("part_id", f"part[{index}]")
        part_number = part.get("part_number")
        if part_number != index + 1:
            errors.append(f"{part_id} part_number {part_number} != expected {index + 1}")

        title = part.get("title", "")
        if _title_word_count(title) > title_max:
            errors.append(f"{part_id} title exceeds {title_max} words: {title!r}")
        if title in blocklist:
            errors.append(f"{part_id} title matches photocopy blocklist: {title!r}")
        if "Birth" in title:
            birth_titles += 1
        if "Medieval" in title:
            medieval_titles += 1

        chapters = part.get("chapters", [])
        if not chapters:
            errors.append(f"{part_id} missing chapters")
            continue

        start = part.get("spine_start")
        end = part.get("spine_end")
        if chapters[0] != start or chapters[-1] != end:
            errors.append(f"{part_id} chapters span mismatch with spine_start/spine_end")

        for left, right in zip(chapters, chapters[1:]):
            if civ_number(right) != civ_number(left) + 1:
                errors.append(f"{part_id} non-contiguous chapters: {left} -> {right}")

        if index == 0:
            if part.get("next_part_id") != parts[1]["part_id"]:
                errors.append("part I next_part_id must chain to part II")
        elif index == len(parts) - 1:
            if part.get("next_part_id") is not None:
                errors.append(f"{part_id} final part must have next_part_id null")
        else:
            if part.get("next_part_id") != parts[index + 1]["part_id"]:
                errors.append(f"{part_id} next_part_id must chain to next part")

        if index > 0 and part.get("previous_part_id") != parts[index - 1]["part_id"]:
            errors.append(f"{part_id} previous_part_id mismatch")

        if index == 0 and chapters[0] != "civ-01":
            errors.append("first part must start at civ-01")
        if index > 0:
            prev = parts[index - 1]["chapters"][-1]
            if civ_number(chapters[0]) != civ_number(prev) + 1:
                errors.append(f"{part_id} must follow {prev} immediately")

        registry_gb = {
            (row["gb_id"], row["anchor_civ"])
            for row in part.get("great_books_weave", [])
            if row.get("role") == "interwoven"
        }
        part_civ_set = set(chapters)
        spine_gb_in_part = {pair for pair in spine_gb if pair[1] in part_civ_set}
        if registry_gb != spine_gb_in_part:
            errors.append(
                f"{part_id} interwoven gb weave mismatch: "
                f"registry={sorted(registry_gb)} spine={sorted(spine_gb_in_part)}"
            )

        registry_sh = {
            (row["sh_id"], row["anchor_civ"])
            for row in part.get("secret_history_companions", [])
        }
        spine_sh_in_part = {pair for pair in spine_sh if pair[1] in part_civ_set}
        if registry_sh != spine_sh_in_part:
            errors.append(
                f"{part_id} sh companion mismatch: "
                f"registry={sorted(registry_sh)} spine={sorted(spine_sh_in_part)}"
            )

        doorway = PACKAGE_ROOT / part.get("doorway_path", "")
        if require_doorways and not doorway.exists():
            errors.append(f"{part_id} missing doorway: {part.get('doorway_path')}")

        commentary_path = part.get("commentary_path")
        bibliography_path = part.get("bibliography_path")
        if commentary_path:
            commentary_file = PACKAGE_ROOT / commentary_path
            if not commentary_file.is_file():
                errors.append(f"{part_id} missing commentary: {commentary_path}")
            if not bibliography_path:
                errors.append(f"{part_id} commentary_path set but bibliography_path missing")
            else:
                bibliography_file = PACKAGE_ROOT / bibliography_path
                if not bibliography_file.is_file():
                    errors.append(f"{part_id} missing bibliography: {bibliography_path}")

        if commentary_path and bibliography_path and require_readme_part_links:
            commentary_basename = Path(commentary_path).name
            bibliography_basename = Path(bibliography_path).name
            for civ_id in chapters:
                readme = PACKAGE_ROOT / "book" / "volume-ii" / civ_id / "README.md"
                if not readme.is_file():
                    errors.append(
                        f"{part_id} missing chapter README: "
                        f"{readme.relative_to(PACKAGE_ROOT)}"
                    )
                    continue
                readme_text = readme.read_text(encoding="utf-8")
                if commentary_basename not in readme_text:
                    errors.append(f"{civ_id} README missing commentary link ({commentary_basename})")
                if bibliography_basename not in readme_text:
                    errors.append(f"{civ_id} README missing bibliography link ({bibliography_basename})")

        if require_chapter_anchors and not part.get("chapter_anchors"):
            errors.append(f"{part_id} missing chapter_anchors")

    if birth_titles > 1:
        errors.append(f"at most one Birth title allowed, found {birth_titles}")
    if medieval_titles > 1:
        errors.append(f"at most one Medieval title allowed, found {medieval_titles}")

    part_ids = {part["part_id"] for part in parts}
    for part in parts:
        next_id = part.get("next_part_id")
        if next_id and next_id not in part_ids:
            errors.append(f"{part['part_id']} unknown next_part_id: {next_id}")

    return errors


def chapter_titles_from_spine() -> dict[str, str]:
    return {
        entry["entry_id"]: entry["title"]
        for entry in parse_interwoven_spine()
        if entry["kind"] == "civ"
    }
