"""Catalog navigation and stale-content regressions; never regenerate the real tree."""

import json
import re
from pathlib import Path

import pytest

from civ_ph import ph_civ_index as index

ROOT = Path(__file__).resolve().parents[1]
SCOPES = [None, *index.NAMESPACE_SCOPES]


def paths(scope, root=ROOT):
    if scope is None:
        return index.index_markdown_path(root), index.index_json_path(root)
    return index.namespace_markdown_path(scope, root), index.namespace_json_path(scope, root)


def validate(scope):
    if scope is None:
        return index.validate_ph_civ_index(repo_root=ROOT)
    return index.validate_namespace_index(scope, repo_root=ROOT)


@pytest.mark.parametrize("scope", SCOPES)
def test_catalog_is_current_and_all_generated_file_links_resolve(scope):
    assert validate(scope) == []


@pytest.mark.parametrize("scope", SCOPES)
@pytest.mark.parametrize("kind", ["markdown", "json"])
def test_read_only_check_rejects_changed_content_with_unchanged_fingerprint(monkeypatch, scope, kind):
    md_path, json_path = paths(scope)
    target = md_path if kind == "markdown" else json_path
    original = Path.read_text
    before = {p: p.read_bytes() for p in paths(scope)}

    def changed(path, *args, **kwargs):
        text = original(path, *args, **kwargs)
        if path == target:
            if kind == "markdown":
                text = re.sub(r"\]\(\.\./[^)]+\)", "](../missing-index-target.md)", text, count=1)
            else:
                payload = json.loads(text)
                payload["chapters"][0]["title"] = "Changed without updating fingerprint"
                text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
        return text

    monkeypatch.setattr(Path, "read_text", changed)
    errors = validate(scope)
    assert any("stale index content" in error for error in errors)
    if kind == "markdown":
        assert any("broken local index link" in error for error in errors)
    assert {p: p.read_bytes() for p in paths(scope)} == before


def test_missing_local_target_fails_even_when_rendered_content_matches(tmp_path):
    md = tmp_path / "index.md"
    data = tmp_path / "index.json"
    content = "[missing](missing.md)\n[web](https://example.com)\n[section](#section)\n"
    md.write_text(content, encoding="utf-8")
    data.write_text("{}\n", encoding="utf-8")
    errors = index.validate_rendered_index(md, data, content, "{}\n", repo_root=tmp_path)
    assert len(errors) == 1
    assert "broken local index link" in errors[0]
    assert "missing.md" in errors[0]


@pytest.mark.parametrize("scope", SCOPES)
def test_normal_generation_repairs_content_without_force(scope, tmp_path):
    def generate():
        if scope is None:
            return index.ensure_ph_civ_index([], repo_root=tmp_path)
        return index.ensure_namespace_index(scope, [], repo_root=tmp_path)

    md, data, written = generate()
    assert written
    expected = (md.read_text(encoding="utf-8"), data.read_text(encoding="utf-8"))
    md.write_text(expected[0] + "\nUnexpected stale body\n", encoding="utf-8")
    payload = json.loads(expected[1])
    payload["transcript_word_total"] = 999
    data.write_text(json.dumps(payload), encoding="utf-8")
    assert generate()[2]
    assert (md.read_text(encoding="utf-8"), data.read_text(encoding="utf-8")) == expected
    assert not generate()[2]


@pytest.mark.parametrize("scope", SCOPES)
def test_every_catalog_row_exposes_existing_commentary_stage(scope):
    md, data = paths(scope)
    payload = json.loads(data.read_text(encoding="utf-8"))
    labels = {
        "scaffold": "Scaffold",
        "l2_pinned": "Source-linked draft",
        "l3_falsifiers": "Falsifier layer",
        "l6_drafted": "Expanded draft",
        "in_review": "Awaiting review",
        "calibration": "Calibration pilot",
    }
    expected = {entry["source_id"]: labels.get(entry.get("commentary_maturity"), "Unclassified")
                for entry in payload["chapters"]}
    text = md.read_text(encoding="utf-8")
    assert text.count("## Reading commentary stages") == 1
    assert "legacy structure-based inference" in text
    assert "not a new assessment" in text
    seen = set()
    for line in text.splitlines():
        if not line.startswith("| `"):
            continue
        cells = re.split(r"(?<!\\)\|", line)[1:-1]
        source_id = cells[0].strip().strip("`")
        assert cells[3].strip() == expected[source_id]
        seen.add(source_id)
    assert seen == set(expected)


def test_secret_history_placeholder_is_distinct_from_developed_commentary():
    text = (ROOT / index.INDEX_MD_REL).read_text(encoding="utf-8")
    scaffold_rows = [line for line in text.splitlines() if line.startswith("| `sh-01` |")]
    developed_rows = [line for line in text.splitlines() if line.startswith("| `civ-01` |")]
    assert scaffold_rows and all("| Scaffold |" in line for line in scaffold_rows)
    assert developed_rows and all("| Source-linked draft |" in line for line in developed_rows)
