"""Backward-compatible re-exports; prefer reader_namespace_guard."""

from civ_ph.reader_namespace_guard import (  # noqa: F401
    _book_path_strings,
    validate_book_namespace,
    validate_book_tombstone,
    validate_ph_apo_tombstone,
    validate_ph_civ_tombstone,
    validate_ph_surface_namespace,
    validate_reader_namespace,
)
