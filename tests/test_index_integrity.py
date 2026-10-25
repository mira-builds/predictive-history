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
