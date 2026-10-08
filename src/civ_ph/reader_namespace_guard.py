from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path

from civ_ph.data import PACKAGE_ROOT, load_cards, load_llm_experience
from civ_ph.volume_i_parts import load_volume_i_parts_registry

BOOK_PATH_PREFIX = "book/"
PH_CIV_PATH_PREFIX = "ph-civ/"
PH_APO_PATH_PREFIX = "ph-apo/"

READER_NAMESPACE_PREFIXES = (
    BOOK_PATH_PREFIX,
    PH_CIV_PATH_PREFIX,
    PH_APO_PATH_PREFIX,
)

FORBIDDEN_TOMBSTONE_PHRASES = (
    "canonical public reader root",
    "canonical two-volume reader",
)

PARTS_PATH_KEYS = (
    "doorway_shelf",
    "spine_ssot",
    "doorway_path",
    "commentary_path",
    "bibliography_path",
)

CATALOG_INDEX_REL = "docs/predictive-history-index.json"
ROUTES_DIR_REL = "data/routes"

TOMBSTONE_DIRS = (
    ("book", BOOK_PATH_PREFIX),
    ("ph-civ", PH_CIV_PATH_PREFIX),
    ("ph-apo", PH_APO_PATH_PREFIX),
)


def _is_reader_namespace_repo_path(value: str, prefix: str) -> bool:
    if not value.startswith(prefix):
        return False
    rest = value[len(prefix) :]
    return bool(rest) and not rest[0].isspace() and (
        "/" in rest or rest.endswith((".md", ".json", ".yaml", ".yml"))
    )


def _is_book_repo_path(value: str) -> bool:
    return _is_reader_namespace_repo_path(value, BOOK_PATH_PREFIX)


def _is_ph_civ_repo_path(value: str) -> bool:
    return _is_reader_namespace_repo_path(value, PH_CIV_PATH_PREFIX)


def _is_ph_apo_repo_path(value: str) -> bool:
    return _is_reader_namespace_repo_path(value, PH_APO_PATH_PREFIX)


def _reader_namespace_path_strings(obj: object, *, prefix: str) -> list[str]:
    found: list[str] = []
    if isinstance(obj, str):
        if _is_reader_namespace_repo_path(obj, prefix):
            found.append(obj)
    elif isinstance(obj, dict):
        for value in obj.values():
            found.extend(_reader_namespace_path_strings(value, prefix=prefix))
    elif isinstance(obj, list):
        for item in obj:
            found.extend(_reader_namespace_path_strings(item, prefix=prefix))
    return found


def _book_path_strings(obj: object) -> list[str]:
    return _reader_namespace_path_strings(obj, prefix=BOOK_PATH_PREFIX)


def _ph_civ_path_strings(obj: object) -> list[str]:
    return _reader_namespace_path_strings(obj, prefix=PH_CIV_PATH_PREFIX)


def _ph_apo_path_strings(obj: object) -> list[str]:
    return _reader_namespace_path_strings(obj, prefix=PH_APO_PATH_PREFIX)


def validate_reader_tombstone(namespace: str, *, repo_root: Path | None = None) -> list[str]:
    root = repo_root or PACKAGE_ROOT
    errors: list[str] = []
    ns_dir = root / namespace
    if not ns_dir.exists():
        errors.append(f"{namespace}/ tombstone directory missing")
        return errors

    for path in ns_dir.rglob("*"):
        if path.is_dir():
            continue
        rel = path.relative_to(ns_dir).as_posix()
        if rel != "README.md":
            errors.append(f"{namespace}/ must contain only README.md tombstone; found: {namespace}/{rel}")

    readme = ns_dir / "README.md"
    if not readme.is_file():
        errors.append(f"{namespace}/README.md tombstone missing")
        return errors

    text = readme.read_text(encoding="utf-8").lower()
    for phrase in FORBIDDEN_TOMBSTONE_PHRASES:
        if phrase in text:
            errors.append(
                f"{namespace}/README.md must not claim deprecated canonical status: contains {phrase!r}"
            )
    return errors


def validate_book_tombstone(*, repo_root: Path | None = None) -> list[str]:
    return validate_reader_tombstone("book", repo_root=repo_root)


def validate_ph_civ_tombstone(*, repo_root: Path | None = None) -> list[str]:
    return validate_reader_tombstone("ph-civ", repo_root=repo_root)


def validate_ph_apo_tombstone(*, repo_root: Path | None = None) -> list[str]:
    return validate_reader_tombstone("ph-apo", repo_root=repo_root)


def _validate_namespace_paths_in_cards(
    *,
    repo_root: Path,
    is_path: Callable[[str], bool],
    label: str,
) -> list[str]:
    errors: list[str] = []
    for card in load_cards():
        source_id = card.get("source_id", "?")
        for key, value in card.get("source_paths", {}).items():
            if isinstance(value, str) and is_path(value):
                errors.append(f"{source_id} source_paths.{key} must not use {label}: {value}")
    return errors


def _validate_namespace_paths_in_catalog(
    *,
    repo_root: Path,
    path_strings_fn: Callable[[object], list[str]],
    label: str,
) -> list[str]:
    errors: list[str] = []
    catalog_path = repo_root / CATALOG_INDEX_REL
    if catalog_path.is_file():
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        for path in path_strings_fn(catalog):
            errors.append(f"{CATALOG_INDEX_REL} must not reference {label}: {path}")
    return errors


def _validate_namespace_paths_in_routes(
    *,
    repo_root: Path,
    path_strings_fn: Callable[[object], list[str]],
    label: str,
) -> list[str]:
    errors: list[str] = []
    routes_dir = repo_root / ROUTES_DIR_REL
    if routes_dir.is_dir():
        for route_file in sorted(routes_dir.glob("*.json")):
            payload = json.loads(route_file.read_text(encoding="utf-8"))
            for path in path_strings_fn(payload):
                rel = route_file.relative_to(repo_root).as_posix()
                errors.append(f"{rel} must not reference {label}: {path}")
    return errors


def validate_book_namespace(*, repo_root: Path | None = None) -> list[str]:
    root = repo_root or PACKAGE_ROOT
    errors: list[str] = []
    errors.extend(validate_book_tombstone(repo_root=root))
    errors.extend(
        _validate_namespace_paths_in_cards(
            repo_root=root,
            is_path=_is_book_repo_path,
            label="book/",
        )
    )
    errors.extend(
        _validate_namespace_paths_in_catalog(
            repo_root=root,
            path_strings_fn=_book_path_strings,
            label="book/",
        )
    )

    registry = load_volume_i_parts_registry()
    for key in ("doorway_shelf", "spine_ssot"):
        value = registry.get(key, "")
        if isinstance(value, str) and _is_book_repo_path(value):
            errors.append(f"volume-i-parts.json {key} must not use book/: {value}")
    for part in registry.get("parts", []):
        part_id = part.get("part_id", "?")
        for key in PARTS_PATH_KEYS:
            if key in {"doorway_shelf", "spine_ssot"}:
                continue
            value = part.get(key, "")
            if isinstance(value, str) and _is_book_repo_path(value):
                errors.append(f"volume-i-parts.json {part_id}.{key} must not use book/: {value}")

    errors.extend(
        _validate_namespace_paths_in_routes(
            repo_root=root,
            path_strings_fn=_book_path_strings,
            label="book/",
        )
    )
    return errors


def validate_ph_surface_namespace(*, repo_root: Path | None = None) -> list[str]:
    root = repo_root or PACKAGE_ROOT
    errors: list[str] = []
    errors.extend(validate_ph_civ_tombstone(repo_root=root))
    errors.extend(validate_ph_apo_tombstone(repo_root=root))
    errors.extend(
        _validate_namespace_paths_in_cards(
            repo_root=root,
            is_path=_is_ph_civ_repo_path,
            label="ph-civ/",
        )
    )
    errors.extend(
        _validate_namespace_paths_in_cards(
            repo_root=root,
            is_path=_is_ph_apo_repo_path,
            label="ph-apo/",
        )
    )
    errors.extend(
        _validate_namespace_paths_in_catalog(
            repo_root=root,
            path_strings_fn=_ph_civ_path_strings,
            label="ph-civ/",
        )
    )
    errors.extend(
        _validate_namespace_paths_in_catalog(
            repo_root=root,
            path_strings_fn=_ph_apo_path_strings,
            label="ph-apo/",
        )
    )
    errors.extend(
        _validate_namespace_paths_in_routes(
            repo_root=root,
            path_strings_fn=_ph_civ_path_strings,
            label="ph-civ/",
        )
    )
    errors.extend(
        _validate_namespace_paths_in_routes(
            repo_root=root,
            path_strings_fn=_ph_apo_path_strings,
            label="ph-apo/",
        )
    )
    return errors


def validate_derived_corpus_metadata(*, repo_root: Path | None = None) -> list[str]:
    errors: list[str] = []
    for card in load_cards():
        corpus = card.get("derived_corpus")
        if corpus in {"ph-civ", "ph-apo"}:
            errors.append(
                f"{card.get('source_id', '?')} derived_corpus must not use retired surface id: {corpus}"
            )
    return errors


def validate_llm_experience_surface_retirement(*, repo_root: Path | None = None) -> list[str]:
    errors: list[str] = []
    llm = load_llm_experience()
    blob = json.dumps(llm, ensure_ascii=False)
    if "--part world-war" in blob:
        errors.append("llm-experience.json must not document --part world-war as primary onboarding")
    chapter_catalog = llm.get("chapter_catalog", {})
    cli_hint = chapter_catalog.get("cli", "")
    if cli_hint.startswith("ph-civ "):
        errors.append("llm-experience chapter_catalog cli must not use ph-civ as primary command")
    folder_links = llm.get("chapter_folder_links", {})
    if folder_links.get("cli", "").startswith("ph-civ "):
        errors.append("llm-experience chapter_folder_links cli must not use ph-civ as primary command")
    return errors


def validate_reader_namespace(*, repo_root: Path | None = None) -> list[str]:
    errors: list[str] = []
    errors.extend(validate_book_namespace(repo_root=repo_root))
    errors.extend(validate_ph_surface_namespace(repo_root=repo_root))
    errors.extend(validate_derived_corpus_metadata(repo_root=repo_root))
    errors.extend(validate_llm_experience_surface_retirement(repo_root=repo_root))
    return errors
