import json

from civ_ph.reader_namespace_guard import (
    _book_path_strings,
    validate_book_namespace,
    validate_book_tombstone,
    validate_ph_apo_tombstone,
    validate_ph_civ_tombstone,
    validate_reader_namespace,
)


def test_reader_namespace_guard_clean_repo():
    assert validate_reader_namespace() == []


def test_book_namespace_guard_clean_repo():
    assert validate_book_namespace() == []


def test_book_path_strings_collects_nested_values():
    payload = {
        "entries": [{"path": "lectures/civ-01/README.md"}, {"path": "book/volume-i/civ-01/README.md"}],
        "note": "book/ mentioned in prose is not a path key",
    }
    assert _book_path_strings(payload) == ["book/volume-i/civ-01/README.md"]


def test_tombstone_rejects_extra_book_files(tmp_path):
    book_dir = tmp_path / "book"
    book_dir.mkdir()
    (book_dir / "README.md").write_text("# Book\n", encoding="utf-8")
    (book_dir / "volume-iii" / "gt-01").mkdir(parents=True)
    (book_dir / "volume-iii" / "gt-01" / "README.md").write_text("redirect\n", encoding="utf-8")

    errors = validate_book_tombstone(repo_root=tmp_path)
    assert any("must contain only README.md" in error for error in errors)


def test_ph_civ_tombstone_rejects_extra_files(tmp_path):
    ns_dir = tmp_path / "ph-civ"
    ns_dir.mkdir()
    (ns_dir / "README.md").write_text("# ph-civ\n", encoding="utf-8")
    (ns_dir / "chapters" / "gt-01").mkdir(parents=True)
    (ns_dir / "chapters" / "gt-01" / "README.md").write_text("stub\n", encoding="utf-8")

    errors = validate_ph_civ_tombstone(repo_root=tmp_path)
    assert any("ph-civ/" in error and "must contain only README.md" in error for error in errors)


def test_ph_apo_tombstone_rejects_extra_files(tmp_path):
    ns_dir = tmp_path / "ph-apo"
    ns_dir.mkdir()
    (ns_dir / "README.md").write_text("# ph-apo\n", encoding="utf-8")
    (ns_dir / "chapters").mkdir()
    (ns_dir / "chapters" / "README.md").write_text("stub\n", encoding="utf-8")

    errors = validate_ph_apo_tombstone(repo_root=tmp_path)
    assert any("ph-apo/" in error and "must contain only README.md" in error for error in errors)


def test_tombstone_rejects_forbidden_canonical_phrase(tmp_path):
    book_dir = tmp_path / "book"
    book_dir.mkdir()
    (book_dir / "README.md").write_text(
        "This is the canonical public reader root.\n",
        encoding="utf-8",
    )

    errors = validate_book_tombstone(repo_root=tmp_path)
    assert any("canonical public reader root" in error for error in errors)


def test_validate_detects_catalog_book_path(tmp_path, monkeypatch):
    book_dir = tmp_path / "book"
    book_dir.mkdir()
    (book_dir / "README.md").write_text("# Deprecated\n", encoding="utf-8")
    (tmp_path / "ph-civ").mkdir()
    (tmp_path / "ph-civ" / "README.md").write_text("# Deprecated\n", encoding="utf-8")
    (tmp_path / "ph-apo").mkdir()
    (tmp_path / "ph-apo" / "README.md").write_text("# Deprecated\n", encoding="utf-8")

    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "predictive-history-index.json").write_text(
        json.dumps({"chapters": [{"folder": "book/volume-i/civ-01"}]}),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "civ_ph.reader_namespace_guard.load_cards",
        lambda: [],
    )
    monkeypatch.setattr(
        "civ_ph.reader_namespace_guard.load_volume_i_parts_registry",
        lambda: {"parts": [], "doorway_shelf": "docs/routes/volume-i-parts/", "spine_ssot": "docs/archive/x.md"},
    )

    errors = validate_reader_namespace(repo_root=tmp_path)
    assert any("predictive-history-index.json" in error and "book/" in error for error in errors)


def test_derived_corpus_rejects_ph_civ(monkeypatch):
    monkeypatch.setattr(
        "civ_ph.reader_namespace_guard.load_cards",
        lambda: [{"source_id": "civ-01", "derived_corpus": "ph-civ", "source_paths": {}}],
    )
    monkeypatch.setattr(
        "civ_ph.reader_namespace_guard.load_llm_experience",
        lambda: {"chapter_catalog": {"cli": "predictive-history index"}, "chapter_folder_links": {"cli": "predictive-history link x"}},
    )
    monkeypatch.setattr(
        "civ_ph.reader_namespace_guard.validate_book_namespace",
        lambda **kwargs: [],
    )
    monkeypatch.setattr(
        "civ_ph.reader_namespace_guard.validate_ph_surface_namespace",
        lambda **kwargs: [],
    )
    errors = validate_reader_namespace()
    assert any("derived_corpus" in error and "ph-civ" in error for error in errors)
