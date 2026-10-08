from pathlib import Path

from civ_ph.cli import validate_public_boundary


ROOT = Path(__file__).resolve().parents[1]


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_agent_identity_contract_exists():
    text = read_text("AGENTS.md")

    assert "mira-builds/predictive-history" in text
    assert "namespace catalog hub" in text
    assert "Compatibility" in text
    assert "two-volume ph-civ artifact" not in text
    assert "companion commentary" in text
    assert "transcript" in text
    assert "Repository-origin identifiers are omitted" in text
    assert "generic coffee greeting" in text


def test_llms_load_contract_names_boundaries():
    text = read_text("llms.txt")

    assert "public consumption layer" in text
    assert "public lecture transcript bodies" in text
    assert "public companion commentary bodies" in text
    assert "private workspace paths" in text


def test_readme_points_new_chats_to_identity_contract():
    text = read_text("README.md")

    assert "AGENTS.md" in text
    assert "llms.txt" in text


def test_public_exports_do_not_leak_private_workspace_boundary():
    assert validate_public_boundary() == []


def test_ph_civ_name_stays_lowercase():
    checked_suffixes = {".json", ".jsonl", ".md", ".py", ".txt", ".yaml"}
    forbidden = tuple(
        left + "-" + right
        for left, right in (
            ("PH", "CIV"),
            ("Ph", "Civ"),
            ("Ph", "civ"),
            ("ph", "CIV"),
        )
    )
    offenders = []

    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in checked_suffixes:
            continue
        if any(part in {".git", ".pytest_cache", "__pycache__"} for part in path.parts):
            continue
        if path.name.endswith("-transcript.md"):
            continue
        text = path.read_text(encoding="utf-8")
        if any(token in text for token in forbidden):
            offenders.append(str(path.relative_to(ROOT)))

    assert offenders == []
