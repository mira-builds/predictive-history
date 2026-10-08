from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MOVED_DOC_REDIRECTS: dict[str, str] = {
    "docs/public-repo-contract.md": "docs/contracts/public-repo-contract.md",
    "docs/export-contract.md": "docs/contracts/export-contract.md",
    "docs/first-tour.md": "docs/onboarding/first-tour.md",
    "docs/chapter-folder-links.md": "docs/onboarding/chapter-folder-links.md",
    "docs/study-edition.md": "docs/onboarding/study-edition.md",
    "docs/study-edition-phase1-visual.md": "docs/onboarding/study-edition-phase1-visual.md",
    "docs/bilingual-civilizational-bridge.md": "docs/localization/bilingual-civilizational-bridge.md",
    "docs/public-surface-status.md": "docs/catalogs/public-surface-status.md",
    "docs/two-volumes-one-reader-map.md": "docs/archive/two-volumes-one-reader-map.md",
    "docs/source-lattice.md": "docs/methodology/source-lattice.md",
    "docs/commentary-methodology-v2.md": "docs/methodology/commentary-methodology-v2.md",
    "docs/commentary-canvas.md": "docs/methodology/commentary-canvas.md",
    "docs/pattern-calibration.md": "docs/methodology/pattern-calibration.md",
    "docs/PIN-CITE-DISCIPLINE.md": "docs/methodology/PIN-CITE-DISCIPLINE.md",
    "docs/pin-cite-manifest-index.md": "docs/methodology/pin-cite-manifest-index.md",
    "docs/ten-axioms-of-my-historical-method.md": "docs/methodology/ten-axioms-of-my-historical-method.md",
    "docs/worldview-teaching-platform-law.md": "docs/methodology/worldview-teaching-platform-law.md",
    "docs/jiang-analysis-index.md": "docs/methodology/jiang-analysis-index.md",
    "docs/jiang-classroom-rhetoric.md": "docs/methodology/jiang-classroom-rhetoric.md",
    "docs/jiang-pedagogy-and-virality.md": "docs/methodology/jiang-pedagogy-and-virality.md",
    "docs/strategy-codex-bridge.md": "docs/methodology/strategy-codex-bridge.md",
    "docs/hidden-doctrines-of-ph-civ.md": "docs/methodology/hidden-doctrines-of-ph-civ.md",
    "docs/gt-29-capstone-and-the-school-turn.md": "docs/methodology/gt-29-capstone-and-the-school-turn.md",
    "docs/game-theory-early-wave-placement-audit.md": "docs/methodology/game-theory-early-wave-placement-audit.md",
    "docs/future-ai-capability-roadmap.md": "docs/methodology/future-ai-capability-roadmap.md",
    "docs/essay-dated-id-migration.md": "docs/migrations/essay-dated-id-migration.md",
    "docs/PH-LECTURES-RELOCATION.md": "docs/migrations/PH-LECTURES-RELOCATION.md",
    "docs/repo-rename.md": "docs/migrations/repo-rename.md",
    "docs/civilization-to-apocalypse-bridge-lattice.md": "docs/routes/civilization-to-apocalypse-bridge-lattice.md",
    "docs/predictive-history-after-tolstoy.md": "docs/routes/predictive-history-after-tolstoy.md",
}


def load_llm_experience() -> dict:
    return json.loads((ROOT / "data" / "llm-experience.json").read_text(encoding="utf-8"))


def is_redirect_stub(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    return text.startswith("# Moved\n")


def test_moved_docs_have_redirect_stubs():
    for old_path, new_path in MOVED_DOC_REDIRECTS.items():
        stub = ROOT / old_path
        canonical = ROOT / new_path
        assert stub.exists(), f"missing redirect stub: {old_path}"
        assert canonical.exists(), f"missing canonical doc: {new_path}"
        assert is_redirect_stub(stub), f"{old_path} must be a redirect stub"
        assert not is_redirect_stub(canonical), f"{new_path} must not be a stub"


def test_llm_experience_reader_docs_are_canonical():
    experience = load_llm_experience()
    reader_paths = [
        experience["first_tour"]["reader_doc"],
        experience["bilingual_bridge"]["reader_doc"],
        experience["chapter_folder_links"]["reader_doc"],
        experience["deprecated_artifacts"]["two_volume_ph_civ"]["reader_map"],
    ]
    for rel in reader_paths:
        path = ROOT / rel
        assert path.exists(), rel
        assert not is_redirect_stub(path), rel


def test_llm_experience_unfolding_map_doc_paths_are_canonical():
    experience = load_llm_experience()
    doc_paths = [
        item
        for item in experience["unfolding_map"]
        if item.startswith("docs/") and (item.endswith(".md") or item.endswith(".json"))
    ]
    assert doc_paths, "expected docs paths in unfolding_map"
    for rel in doc_paths:
        path = ROOT / rel
        assert path.exists(), rel
        if rel.endswith(".md"):
            assert not is_redirect_stub(path), rel


def test_flat_docs_root_is_hub_plus_stubs():
    docs_root = ROOT / "docs"
    allowed_flat_names = {
        "README.md",
        "predictive-history-index.md",
        "predictive-history-index.json",
    } | {Path(old_path).name for old_path in MOVED_DOC_REDIRECTS}
    flat_files = {path.name for path in docs_root.iterdir() if path.is_file()}
    unexpected = flat_files - allowed_flat_names
    assert unexpected == set(), f"unexpected flat docs/: {sorted(unexpected)}"
