from pathlib import Path
import re
import yaml
from civ_ph.cli import main

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents" / "skills"

def test_public_copy_contains_no_old_account_or_machine_paths():
    forbidden_account = "rb" + "tkhn"
    drive_path = re.compile(r"(?<![a-zA-Z0-9])[a-zA-Z]:[/\\]+[a-zA-Z0-9_]")
    offenders = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in {".git", "__pycache__", ".pytest_cache"} for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if forbidden_account in text.lower() or drive_path.search(text):
            offenders.append(path.relative_to(ROOT).as_posix())
    assert offenders == []

def test_portable_skills_have_valid_metadata_and_project_references():
    for name in ("predictive-history-read", "predictive-history-learn", "predictive-history-maintain"):
        path = SKILLS / name / "SKILL.md"
        text = path.read_text(encoding="utf-8")
        metadata = yaml.safe_load(text.split("---", 2)[1])
        assert metadata["name"] == name
        assert metadata["description"]
        for ref in re.findall(r"`((?:docs|data)/[^`]+\.(?:md|json))`", text):
            assert (ROOT / ref).is_file(), ref

def test_unavailable_chapter_returns_failure_without_fabricating_content(capsys):
    assert main(["show", "civ-99", "--format", "json"]) != 0
    assert "Homer" not in capsys.readouterr().out
