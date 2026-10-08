import json
from pathlib import Path

from civ_ph.cli import main
from civ_ph.data import (
    load_bilingual_loop,
    load_cards,
    load_choreography,
    load_course_architecture,
    load_first_tour,
    load_growth_goals,
    load_llm_experience,
    load_route_seed,
    load_spine,
)

ROOT = Path(__file__).resolve().parents[1]


def test_loads_all_seeded_cards():
    cards = load_cards()
    assert len(cards) == 216
    assert {"civilization", "world-war"} <= {card["part"] for card in cards}


def test_all_cards_have_local_transcript_and_commentary():
    cards = load_cards()
    transcript_paths = []
    commentary_paths = []
    for card in cards:
        transcript_path = ROOT / card["source_paths"]["source_chapter_path"]
        commentary_path = ROOT / card["source_paths"]["commentary_path"]
        assert transcript_path.exists(), card["source_id"]
        assert commentary_path.exists(), card["source_id"]
        transcript_paths.append(transcript_path)
        commentary_paths.append(commentary_path)

    assert len(set(transcript_paths)) == 216
    assert len(set(commentary_paths)) == 216


def test_all_commentaries_have_open_project_canvas():
    from civ_ph.cli import validate_commentary_canvas

    for card in load_cards():
        commentary_path = ROOT / card["source_paths"]["commentary_path"]
        errors = validate_commentary_canvas(card["source_id"], commentary_path)
        assert not errors, f"{card['source_id']}: " + "; ".join(errors)


def test_folder_backed_chapters_have_reader_doorways():
    for card in load_cards():
        transcript_path = card["source_paths"]["source_chapter_path"]
        commentary_path = card["source_paths"]["commentary_path"]
        folder = Path(transcript_path).parent
        if folder.name != card["source_id"]:
            continue
        readme = ROOT / folder / "README.md"
        assert readme.exists(), card["source_id"]
        text = readme.read_text(encoding="utf-8")
        assert "public study doorway" in text
        assert "Paste this folder link into ChatGPT, Claude, or Grok" in text
        assert Path(transcript_path).name in text
        assert Path(commentary_path).name in text
        transcript_text = (ROOT / transcript_path).read_text(encoding="utf-8")
        if "source_url:" in transcript_text:
            source_url = next(
                line.split(":", 1)[1].strip().strip('"')
                for line in transcript_text.splitlines()
                if line.startswith("source_url:")
            )
            assert ("## Source Video" in text or "## Source" in text)
            assert source_url in text


def test_all_lecture_cards_under_lectures_namespace():
    series_folder = {
        "civilization": "civilization",
        "great-books": "great-books",
        "geo-strategy": "geo-strategy",
        "game-theory": "game-theory",
        "secret-history": "secret-history",
    }
    for card in load_cards():
        series = card.get("series")
        if series not in series_folder:
            continue
        transcript = card["source_paths"]["source_chapter_path"]
        assert transcript.startswith(f"lectures/{series_folder[series]}/"), card["source_id"]


def test_latest_game_theory_chapters_are_provisional_source_first(capsys):
    cards = {card["source_id"]: card for card in load_cards()}
    route_ids = set(load_route_seed()["route_ids"])
    for source_id in ["gt-23", "gt-24", "gt-25", "gt-26"]:
        card = cards[source_id]
        assert card["series"] == "game-theory"
        assert card["part"] == "world-war"
        assert card["review_status"] == "provisional"
        assert source_id not in route_ids
        folder = ROOT / "lectures" / "game-theory" / source_id
        assert (folder / f"{source_id}-transcript.md").exists()
        assert (folder / f"{source_id}-commentary.md").exists()
        assert (folder / f"{source_id}-orientation.yaml").exists()
        assert "public study doorway" in (folder / "README.md").read_text(encoding="utf-8")
        legacy = ROOT / "book" / "volume-iii" / source_id / "README.md"
        assert not legacy.exists(), source_id

    tombstone = ROOT / "book" / "README.md"
    assert tombstone.is_file()
    tombstone_text = tombstone.read_text(encoding="utf-8")
    assert "Deprecated Compatibility Namespace" in tombstone_text
    assert "docs/predictive-history-index.md" in tombstone_text

    assert main(["link", "gt-24", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["source_id"] == "gt-24"
    assert payload["folder_ready"] is True
    assert payload["github_folder_url"].endswith("/lectures/game-theory/gt-24")
    assert payload["source_video_url"] == "https://www.youtube.com/watch?v=8nsxuB3Vsts"
    assert "ChatGPT, Claude, or Grok" in payload["suggested_youtube_comment"]
    assert "provisional" in payload["suggested_youtube_comment"]

    assert main(["link", "gt-24"]) == 0
    out = capsys.readouterr().out
    assert "YouTube comment:" in out
    assert "source_video: https://www.youtube.com/watch?v=8nsxuB3Vsts" in out
    assert "https://github.com/mira-builds/predictive-history/tree/main/lectures/game-theory/gt-24" in out
    assert "Predictive History, a public LLM-native reader" in out


def test_link_essay_emits_transcript_url(capsys):
    essay_id = "essay-2025-09-27-the-empire-goes-to-war"
    assert main(["link", essay_id, "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["source_id"] == essay_id
    assert payload["series"] == "essays"
    assert payload["folder_ready"] is True
    assert payload["github_folder_url"] is None
    assert payload["github_transcript_url"].endswith(
        "/essays/essay-2025-09-27-the-empire-goes-to-war.md"
    )
    assert payload["commentary_path"] == "commentaries/essay-2025-09-27-the-empire-goes-to-war-commentary.md"
    assert "public essay packet" in payload["suggested_llm_prompt"]

    assert main(["link", essay_id]) == 0
    out = capsys.readouterr().out
    assert "essay: https://github.com/mira-builds/predictive-history/blob/main/essays/" in out


def test_show_known_card_json(capsys):
    assert main(["show", "civ-41", "--format", "json"]) == 0
    assert "\"source_id\": \"civ-41\"" in capsys.readouterr().out


def test_invalid_source_id_returns_nonzero(capsys):
    assert main(["show", "nope-99"]) == 2
    assert "Unknown source_id" in capsys.readouterr().err


def test_prompt_creative_contains_boundaries(capsys):
    assert main(["prompt", "gb-01", "--mode", "creative"]) == 0
    out = capsys.readouterr().out
    assert "Limits:" in out
    assert "gb-01" in out


def test_validate_passes(capsys):
    assert main(["validate"]) == 0
    assert "card_count: 216" in capsys.readouterr().out


def test_index_command_writes_fingerprinted_index():
    from civ_ph.ph_civ_index import (
        index_json_path,
        index_markdown_path,
        read_index_fingerprint,
        validate_ph_civ_index,
    )

    assert main(["index"]) == 0
    md_path = index_markdown_path()
    json_path = index_json_path()
    assert md_path.exists()
    assert json_path.exists()
    assert read_index_fingerprint(md_path)
    assert read_index_fingerprint(json_path)
    assert read_index_fingerprint(md_path) == read_index_fingerprint(json_path)
    assert md_path.read_text(encoding="utf-8").startswith("<!-- predictive-history-index-fingerprint:")
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["card_count"] == 216
    assert len(payload["chapters"]) == 216
    assert payload["schema_version"] == 5
    assert payload["primary_artifact"] == "namespace_catalog"
    assert payload["transcript_word_total"] > 1_000_000
    assert validate_ph_civ_index() == []


def test_index_check_reports_current_after_validate():
    assert main(["validate"]) == 0
    assert main(["index", "--check"]) == 0


def test_exported_source_repo_uses_public_capture():
    cards = load_cards()
    assert {card["source_snapshot"]["repo"] for card in cards} == {
        "public-source-capture",
        "operator-supplied-youtube-transcript",
        "mira-builds/predictive-history",
    }


def test_literary_spine_ends_with_tolstoy():
    spine = load_spine()
    assert spine["spine_id"] == "homer-to-tolstoy"
    assert spine["structural_role"] == "volume_i_literary_spine"
    assert spine["routing_role"] == "cross_volume_exposure"
    assert spine["launch_readiness"] == "defined_not_launch_ready"
    assert "first public reader" in spine["first_reader_gap"]
    assert spine["sequence"][-1]["author"] == "Tolstoy"
    assert spine["sequence"][-1]["source_ids"] == ["sh-16"]


def test_literary_spine_path_surfaces_launch_readiness(capsys):
    assert main(["path", "homer-to-tolstoy"]) == 0
    out = capsys.readouterr().out
    assert "launch_readiness: defined_not_launch_ready" in out
    assert "first_reader_gap:" in out
    assert "guardrail:" in out


def test_namespace_catalog_is_primary():
    architecture = load_course_architecture()
    assert architecture["primary_artifact"] == "namespace_catalog"
    assert architecture["repo_identity"] == "predictive-history"
    assert architecture["catalog_hub"]["markdown"] == "docs/predictive-history-index.md"
    assert "lectures" in architecture["namespace_slices"]
    deprecated = architecture["deprecated_two_volume"]
    assert deprecated["primary_artifact"] == "two_volume_ph_civ"
    assert architecture["volumes"]["volume_i"]["surface"] == "ph-civ"
    assert architecture["volumes"]["volume_i"]["role"] == "law_discovery"
    assert architecture["volumes"]["volume_ii"]["surface"] == "ph-apo"
    assert architecture["volumes"]["volume_ii"]["role"] == "law_application"
    assert "museum" not in architecture
    assert "ph-mus" not in {volume["surface"] for volume in architecture["volumes"].values()}
    assert architecture["bridge_support_nodes"] == ["sh-11", "sh-16", "sh-17", "sh-18"]


def test_public_surfaces_are_named(capsys):
    assert main(["surface", "ph-civ"]) == 2
    assert "retired" in capsys.readouterr().err
    assert main(["surface"]) == 0
    assert "PH-SURFACE-RETIREMENT" in capsys.readouterr().out


def test_status_leads_with_namespace_catalog(capsys):
    assert main(["status"]) == 0
    out = capsys.readouterr().out
    assert "namespace catalog hub" in out
    assert "primary_artifact: namespace_catalog" in out
    assert "predictive-history-index.md" in out
    assert "deprecated two-volume" in out


def test_llm_native_bootloader_contract(capsys):
    start_here = ROOT / "START-HERE.md"
    assert start_here.exists()
    start_text = start_here.read_text(encoding="utf-8")
    assert "pastes `https://github.com/mira-builds/predictive-history` into a ChatGPT chat or any other LLM" in start_text
    assert "First Response Contract" in start_text
    assert "Do not stop at a generic repository summary" in start_text
    assert "Default mode: first_tour" in start_text
    assert "literary spine route" in start_text
    assert "Anna Karenina coda" in start_text
    assert "namespace catalog hub" in start_text

    experience = load_llm_experience()
    assert experience["start_here"] == "START-HERE.md"
    assert experience["primary_artifact"] == "namespace_catalog"
    assert experience["full_context"]["path"] == "llms-full.txt"
    assert experience["full_context"]["purpose"] == "one_shot_llm_context_packet"
    assert experience["first_response_contract"]["default_mode"] == "first_tour"
    assert "generic repository summary" in experience["first_response_contract"]["anti_pattern"]
    assert experience["first_response_contract"]["required_opening_files"] == [
        "START-HERE.md",
        "llms.txt",
        "llms-full.txt",
    ]
    assert experience["first_response_contract"]["opening_route"] == "civ-07"
    assert experience["first_response_contract"]["opening_path"] == "homer-to-tolstoy"
    assert any("Choose one:" in line for line in experience["first_response_contract"]["template"])
    assert experience["first_tour"]["path"] == "data/routes/first-tour.json"
    assert experience["first_tour"]["reader_doc"] == "docs/onboarding/first-tour.md"
    assert experience["first_tour"]["opening_route"] == "civ-07"
    assert experience["bilingual_bridge"]["path"] == "data/bilingual-loop.json"
    assert experience["bilingual_bridge"]["reader_doc"] == "docs/localization/bilingual-civilizational-bridge.md"
    assert experience["bilingual_bridge"]["posture"] == "civilizational_bridge"
    assert experience["bilingual_bridge"]["bridge_id"] == "trilingual_civilizational_bridge"
    assert experience["bilingual_bridge"]["language_scope"] == "trilingual"
    assert experience["bilingual_bridge"]["status"] == "ambition_metadata"
    assert experience["bilingual_bridge"]["canonical_source"] == "predictive-history"
    assert experience["bilingual_bridge"]["primary_wedge"] == "homer_to_tolstoy_read_from_china"
    assert experience["bilingual_bridge"]["localization_roadmap"] == ["ph-civ-zh", "ph-civ-ru"]
    assert "downstream mirrors" in experience["bilingual_bridge"]["authority_model"]
    assert experience["chapter_folder_links"]["reader_doc"] == "docs/onboarding/chapter-folder-links.md"
    assert experience["chapter_folder_links"]["default_mode"] == "study"
    assert experience["chapter_folder_links"]["cli"] == "predictive-history link <source_id>"
    assert experience["chapter_catalog"]["json_path"] == "docs/predictive-history-index.json"
    assert experience["chapter_catalog"]["markdown_path"] == "docs/predictive-history-index.md"
    assert experience["chapter_catalog"]["not_replacement_for"] == "first_tour"
    assert "docs/predictive-history-index.json" in experience["unfolding_map"]
    study_mode = next(mode for mode in experience["modes"] if mode["mode"] == "study")
    assert "docs/predictive-history-index.json" in study_mode["start_files"]
    catalog_mode = next(mode for mode in experience["modes"] if mode["mode"] == "catalog")
    assert catalog_mode["start_files"] == ["docs/predictive-history-index.json", "docs/predictive-history-index.md"]
    assert "lectures" in experience["namespace_slices"]
    assert experience["catalog_hub"]["json"] == "docs/predictive-history-index.json"
    assert experience["deprecated_artifacts"]["two_volume_ph_civ"]["archive_doc"] == (
        "docs/archive/two-volume-ph-civ-apo-deprecated.md"
    )
    assert "museum" not in experience.get("namespace_slices", {})
    assert experience["first_seed"]["route_ids"] == load_route_seed()["route_ids"]
    guardrails = "\n".join(experience["guardrails"])
    assert "Homer to Tolstoy" in guardrails
    assert "Anna Karenina coda" in guardrails

    assert main(["start", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["experience_id"] == "ph_civ_llm_native_bootloader"
    assert payload["primary_artifact"] == "namespace_catalog"
    assert payload["full_context"]["path"] == "llms-full.txt"
    assert payload["first_response_contract"]["default_mode"] == "first_tour"
    assert payload["first_tour"]["path"] == "data/routes/first-tour.json"
    assert payload["bilingual_bridge"]["path"] == "data/bilingual-loop.json"
    assert payload["chapter_folder_links"]["reader_doc"] == "docs/onboarding/chapter-folder-links.md"
    assert payload["chapter_catalog"]["json_path"] == "docs/predictive-history-index.json"
    assert payload["first_seed"]["route_ids"] == load_route_seed()["route_ids"]


def test_llms_full_context_packet_exists():
    packet = ROOT / "llms-full.txt"
    assert packet.exists()
    text = packet.read_text(encoding="utf-8")
    assert "full one-shot LLM context packet" in text
    assert "https://github.com/mira-builds/predictive-history" in text
    assert "First Response Contract" in text
    assert "Do not stop at a generic repository summary" in text
    assert "Default mode: `first_tour`" in text
    assert "starting at civ-07" in text
    assert "literary spine route" in text
    assert "Anna Karenina coda" in text
    assert "namespace catalog hub" in text
    assert "Do not claim live geopolitical certainty" in text
    assert "Trilingual Civilizational Bridge" in text
    assert "canonical English `predictive-history`, downstream Chinese `ph-civ-zh`, and downstream Russian `ph-civ-ru`" in text
    assert "Homer to Tolstoy, read from China." in text
    assert "Default mode: `first_tour`" in text
    assert "not a translation dump" in text
    assert "ph-civ-ru" in text
    assert "Russian glossary" in text
    assert "not live war analysis" in text
    assert "Chapter-Folder Links" in text
    assert "not a replacement for `first_tour`" in text
    assert "docs/predictive-history-index.md" in text
    assert "docs/predictive-history-index.json" in text
    assert "Chapter Catalog" in text


def test_no_legacy_chapter_indexes():
    legacy_paths = [
        ROOT / "docs" / "ph-civ-index.md",
        ROOT / "data" / "ph-civ-index.json",
        ROOT / "docs" / "source-video-index.md",
        ROOT / "data" / "index.json",
        ROOT / "data" / "predictive-history-index.json",
    ]
    for path in legacy_paths:
        assert not path.exists(), f"legacy index must be removed: {path}"


def test_ph_civ_index_hub_links_namespace_slices():
    md = (ROOT / "docs" / "predictive-history-index.md").read_text(encoding="utf-8")
    assert "## Namespace slice indexes" in md
    assert "../lectures/predictive-history-lecture-index.md" in md
    assert "../essays/predictive-history-essay-index.md" in md
    assert "../interviews/predictive-history-interview-index.md" in md
    assert "| Lectures |" in md
    assert "| 150 |" in md
    assert "| 43 |" in md
    assert "| 23 |" in md
    assert "## Deprecated reader frame" in md
    assert "## Civilization" in md
    assert "archive/two-volume-ph-civ-apo-deprecated.md" in md


def test_ph_civ_index_provenance_section():
    payload = json.loads((ROOT / "docs" / "predictive-history-index.json").read_text(encoding="utf-8"))
    assert "provenance" in payload["by_surface"]
    assert payload.get("by_series")
    md = (ROOT / "docs" / "predictive-history-index.md").read_text(encoding="utf-8")
    assert "## Interviews / provenance" in md


def test_ph_civ_index_surfaces_youtube_urls():
    index = ROOT / "docs" / "predictive-history-index.md"
    assert index.exists()
    text = index.read_text(encoding="utf-8")
    assert "Predictive History Chapter Index" in text
    assert "| Words |" in text
    assert "https://www.youtube.com/watch?v=8nsxuB3Vsts" in text
    assert "lectures/game-theory/gt-24/gt-24-transcript.md" in text
    assert "https://www.youtube.com/watch?v=RG1clZlrfOo" in text


def test_ph_civ_index_transcript_word_counts():
    payload = json.loads((ROOT / "docs" / "predictive-history-index.json").read_text(encoding="utf-8"))
    chapters = payload["chapters"]
    assert payload["schema_version"] == 5
    assert payload["primary_artifact"] == "namespace_catalog"
    assert len(chapters) == 216
    assert all("transcript_word_count" in chapter for chapter in chapters)
    assert payload["transcript_word_total"] == sum(
        chapter["transcript_word_count"] for chapter in chapters
    )
    civ01 = next(chapter for chapter in chapters if chapter["source_id"] == "civ-01")
    assert civ01["transcript_word_count"] > 1000
    assert payload["transcript_word_total"] > 1_000_000


def test_lectures_index_exists_and_matches_cards():
    payload = json.loads(
        (ROOT / "lectures" / "predictive-history-lecture-index.json").read_text(encoding="utf-8")
    )
    assert payload["scope"] == "lectures"
    assert payload["hub_index"] == "docs/predictive-history-index.md"
    assert payload["card_count"] == 150
    assert len(payload["chapters"]) == 150
    md = (ROOT / "lectures" / "predictive-history-lecture-index.md").read_text(encoding="utf-8")
    assert md.startswith("<!-- predictive-history-lecture-index-fingerprint:")
    assert "civilization/civ-01/" in md


def test_essays_index_exists_and_matches_cards():
    payload = json.loads(
        (ROOT / "essays" / "predictive-history-essay-index.json").read_text(encoding="utf-8")
    )
    assert payload["scope"] == "essays"
    assert payload["hub_index"] == "docs/predictive-history-index.md"
    assert payload["card_count"] == 43
    assert len(payload["chapters"]) == 43
    md = (ROOT / "essays" / "predictive-history-essay-index.md").read_text(encoding="utf-8")
    assert md.startswith("<!-- predictive-history-essay-index-fingerprint:")
    assert "../commentaries/" in md


def test_interviews_index_exists_and_matches_cards():
    payload = json.loads(
        (ROOT / "interviews" / "predictive-history-interview-index.json").read_text(encoding="utf-8")
    )
    assert payload["scope"] == "interviews"
    assert payload["hub_index"] == "docs/predictive-history-index.md"
    assert payload["card_count"] == 23
    assert len(payload["chapters"]) == 23
    md = (ROOT / "interviews" / "predictive-history-interview-index.md").read_text(encoding="utf-8")
    assert md.startswith("<!-- predictive-history-interview-index-fingerprint:")
    assert "interview-2025-10-30-cyrus-janssen/" in md


def test_bilingual_bridge_contract(capsys):
    bridge = load_bilingual_loop()
    assert bridge["bridge_id"] == "trilingual_civilizational_bridge"
    assert bridge["loop_id"] == "english_chinese_civilizational_bridge"
    assert bridge["language_scope"] == "trilingual"
    assert bridge["posture"] == "civilizational_bridge"
    assert bridge["status"] == "ambition_metadata"
    assert bridge["canonical_source"] == "predictive-history"
    assert "English, Chinese, and Russian readerships" in bridge["identity"]
    assert bridge["canonical_language_surface"] == {
        "surface": "predictive-history",
        "locale": "en",
        "role": "canonical_source",
    }
    assert bridge["downstream_mirrors"] == ["ph-civ-zh", "ph-civ-ru"]
    assert [
        (item["surface"], item["locale"], item["role"])
        for item in bridge["downstream_language_surfaces"]
    ] == [
        ("ph-civ-zh", "zh", "downstream_localization_mirror"),
        ("ph-civ-ru", "ru", "downstream_localization_mirror"),
    ]
    assert "downstream localization mirrors" in bridge["authority_model"]
    assert "source of truth" in bridge["authority_model"]
    assert bridge["primary_wedge"] == "homer_to_tolstoy_read_from_china"
    assert "Chinese civilizational-history lens" in bridge["english_hook"]
    assert "without imitation or rejection" in bridge["chinese_hook"]
    assert any("Russian readers add a third reinforcement line" in item for item in bridge["reinforcement_loop"])
    assert any("Trilingual LLM chats" in item for item in bridge["reinforcement_loop"])
    guardrails = "\n".join(bridge["guardrails"])
    assert "not propaganda" in guardrails
    assert "not anti-Western" in guardrails
    assert "not a translation dump" in guardrails
    assert bridge["future_zh_wedge"]["first_steps"] == [
        "canonical glossary",
        "Chinese bootloader",
        "Chinese first-tour metadata",
    ]
    assert bridge["future_zh_wedge"]["upstream_source"] == "predictive-history"
    assert bridge["future_zh_wedge"]["dependency_role"] == "downstream_localization_mirror"
    assert "149 source chapters" in bridge["future_zh_wedge"]["defer"]
    assert bridge["future_zh_wedge"]["no_repo_scaffold_in_this_pass"] is True
    assert bridge["future_ru_wedge"]["future_surface"] == "ph-civ-ru"
    assert bridge["future_ru_wedge"]["status"] == "roadmap_candidate"
    assert bridge["future_ru_wedge"]["upstream_source"] == "predictive-history"
    assert bridge["future_ru_wedge"]["dependency_role"] == "downstream_localization_mirror"
    assert bridge["future_ru_wedge"]["first_steps"] == [
        "Russian glossary",
        "Russian bootloader",
        "Russian first-tour metadata",
    ]
    ru_guardrails = "\n".join(bridge["future_ru_wedge"]["guardrails"])
    assert "not Russian-state apologetics" in ru_guardrails
    assert "not anti-Ukrainian" in ru_guardrails
    assert "not live war analysis" in ru_guardrails
    assert "not a translation dump" in ru_guardrails
    assert "149 source chapters" in bridge["future_ru_wedge"]["defer"]
    assert "localization commands" in bridge["future_ru_wedge"]["defer"]
    assert bridge["future_ru_wedge"]["no_repo_scaffold_in_this_pass"] is True
    assert [item["future_surface"] for item in bridge["localization_roadmap"]] == [
        "ph-civ-zh",
        "ph-civ-ru",
    ]
    assert {item["upstream_source"] for item in bridge["localization_roadmap"]} == {"predictive-history"}
    assert {item["dependency_role"] for item in bridge["localization_roadmap"]} == {
        "downstream_localization_mirror"
    }

    doc = (ROOT / "docs" / "localization" / "bilingual-civilizational-bridge.md").read_text(encoding="utf-8")
    assert "Trilingual Civilizational Bridge" in doc
    assert "`predictive-history` / English / canonical public artifact" in doc
    assert "Homer to Tolstoy, read from China." in doc
    assert "Volume I literary spine" in doc
    assert "paired mirrors" in doc
    assert "not propaganda" in doc
    assert "not anti-Western" in doc
    assert "not a translation dump" in doc
    assert "ph-civ-ru" in doc
    assert "Russian glossary" in doc
    assert "not live war analysis" in doc
    assert "downstream of `predictive-history`" in doc
    assert "not become sibling authorities" in doc

    start_here = (ROOT / "START-HERE.md").read_text(encoding="utf-8")
    assert "Default mode: first_tour" in start_here
    assert "trilingual identity/growth layer" in start_here
    assert "not a replacement for `first_tour`" in start_here
    assert "downstream mirrors of canonical `predictive-history`" in start_here
    assert "chapter-folder URL is a study doorway" in start_here

    assert main(["bilingual", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["bridge_id"] == "trilingual_civilizational_bridge"
    assert payload["loop_id"] == "english_chinese_civilizational_bridge"
    assert payload["language_scope"] == "trilingual"
    assert payload["posture"] == "civilizational_bridge"
    assert payload["canonical_source"] == "predictive-history"
    assert payload["downstream_mirrors"] == ["ph-civ-zh", "ph-civ-ru"]
    assert payload["future_zh_wedge"]["first_steps"][0] == "canonical glossary"
    assert payload["future_ru_wedge"]["future_surface"] == "ph-civ-ru"
    assert payload["localization_roadmap"][1]["future_surface"] == "ph-civ-ru"

    assert main(["trilingual", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["bridge_id"] == "trilingual_civilizational_bridge"
    assert payload["downstream_mirrors"] == ["ph-civ-zh", "ph-civ-ru"]

    assert main(["bilingual"]) == 0
    out = capsys.readouterr().out
    assert "trilingual_civilizational_bridge: civilizational_bridge" in out
    assert "legacy_loop_id: english_chinese_civilizational_bridge" in out
    assert "language_scope: trilingual" in out
    assert "primary_wedge: homer_to_tolstoy_read_from_china" in out
    assert "canonical_source: predictive-history" in out
    assert "downstream_mirrors: ph-civ-zh, ph-civ-ru" in out
    assert "English hook:" in out
    assert "Chinese hook:" in out
    assert "not propaganda" in out
    assert "canonical glossary" in out
    assert "future_ru_wedge:" in out
    assert "future_surface: ph-civ-ru" in out
    assert "Russian glossary" in out

    assert main(["trilingual"]) == 0
    out = capsys.readouterr().out
    assert "trilingual_civilizational_bridge: civilizational_bridge" in out


def test_first_tour_contract(capsys):
    tour = load_first_tour()
    seed_ids = load_route_seed()["route_ids"]
    assert tour["tour_id"] == "first_tour_ten_route_spine"
    assert tour["mode"] == "first_tour"
    assert tour["seed_id"] == "ten_route_spine_seed"
    assert tour["opening_route"] == "civ-07"
    assert tour["opening_path"] == "homer-to-tolstoy"
    assert [stop["source_id"] for stop in tour["stops"]] == seed_ids
    assert [
        source_id
        for phase in tour["phases"]
        for source_id in phase["route_ids"]
    ] == seed_ids
    assert "Homeric memory system" in tour["continue_prompt"]
    assert "Anna Karenina coda" in "\n".join(tour["guardrails"])

    first_tour_doc = ROOT / "docs" / "onboarding" / "first-tour.md"
    text = first_tour_doc.read_text(encoding="utf-8")
    assert "First-Tour Response Shape" in text
    assert "First tour, stop 1: civ-07" in text
    assert "Continue to civ-17" in text
    assert "namespace catalog hub" in text

    assert main(["tour", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["opening_route"] == "civ-07"
    assert payload["stops"][0]["source_id"] == "civ-07"
    assert payload["stops"][0]["title"]
    assert payload["stops"][0]["transcript_path"].endswith("civ-07-transcript.md")

    assert main(["tour"]) == 0
    out = capsys.readouterr().out
    assert "First tour" not in out  # Keep command output compact and data-first.
    assert "opening_route: civ-07" in out
    assert "Continue" in out


def test_volumes_command_returns_architecture(capsys):
    assert main(["volumes", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["primary_artifact"] == "namespace_catalog"
    assert payload["volumes"]["volume_i"]["surface"] == "ph-civ"
    assert payload["volumes"]["volume_i"]["role"] == "law_discovery"
    assert payload["volumes"]["volume_ii"]["surface"] == "ph-apo"
    assert payload["volumes"]["volume_ii"]["role"] == "law_application"
    assert "museum" not in payload
    assert payload["unique_card_count"] == 216


def test_volume_command_lists_conceptual_membership(capsys):
    assert main(["volume", "volume-i", "--json"]) == 0
    volume_i = json.loads(capsys.readouterr().out)
    volume_i_ids = {card["source_id"] for card in volume_i["cards"]}
    assert {"civ-01", "gb-01", "sh-11", "sh-16", "sh-17", "sh-18"} <= volume_i_ids
    assert volume_i["role"] == "law_discovery"

    assert main(["volume", "volume-ii", "--json"]) == 0
    volume_ii = json.loads(capsys.readouterr().out)
    volume_ii_ids = {card["source_id"] for card in volume_ii["cards"]}
    assert {"geo-01", "gt-16", "sh-01", "sh-28"} <= volume_ii_ids
    assert volume_ii["role"] == "law_application"


def test_growth_goals_translate_outcomes_to_agent_machinery():
    growth_goals = load_growth_goals()
    assert growth_goals["goal_system"] == "ph_civ_public_growth"
    assert growth_goals["agent_goal_policy"]["must_translate_outcome_to_machinery"] is True
    campaign = growth_goals["campaigns"][0]
    assert campaign["campaign_id"] == "one_million_views_2026"
    assert campaign["status"] == "strategic_ambition"
    assert campaign["target_count"] == 1000000
    assert campaign["target_date"] == "2026-12-31"
    assert "source-disciplined educational trust" in campaign["unresolved_tension"]
    assert campaign["success_requires_external_audience_behavior"] is True
    assert campaign["human_approval_required_for_publication"] is True
    assert "achieved" not in campaign["status"]
    assert campaign["first_live_wedge"]["wedge_id"] == "launch_volume_i_spine"
    assert campaign["first_live_wedge"]["launch_readiness"] == "defined_not_launch_ready"
    assert "deserves audience growth" in campaign["first_live_wedge"]["readiness_question"]
    assert "Homer-to-Tolstoy route" in campaign["first_live_wedge"]["scope"]
    assert "without claiming views have already been earned" in campaign["first_live_wedge"]["done_when"]
    outputs = campaign["measurable_agent_outputs"]
    assert any("namespace catalog hub within one screen" in line for line in outputs)
    assert any("analytics plan defines what counts as a view across GitHub, web, video, social, and document surfaces" in line for line in outputs)
    assert any("distribution calendar converts the target into weekly and monthly milestones" in line for line in outputs)


def test_hub_catalog_completeness():
    cards = load_cards()
    payload = json.loads((ROOT / "docs" / "predictive-history-index.json").read_text(encoding="utf-8"))
    assert len(payload["chapters"]) == 216
    assert payload["card_count"] == 216
    assert payload.get("by_series")
    assert payload.get("by_surface")
    json_ids = {chapter["source_id"] for chapter in payload["chapters"]}
    card_ids = {card["source_id"] for card in cards}
    assert json_ids == card_ids


def test_hub_full_alphabetical_index():
    cards = load_cards()
    md = (ROOT / "docs" / "predictive-history-index.md").read_text(encoding="utf-8")
    alpha_start = md.index("## Full alphabetical index")
    alpha_section = md[alpha_start:]
    for card in cards:
        assert f"`{card['source_id']}`" in alpha_section


def test_two_volume_paths_deprecated():
    archive = ROOT / "docs" / "archive" / "two-volume-ph-civ-apo-deprecated.md"
    assert archive.exists()
    ph_civ_readme = (ROOT / "ph-civ" / "README.md").read_text(encoding="utf-8")
    assert "predictive-history-index.md" in ph_civ_readme
    hub_md = (ROOT / "docs" / "predictive-history-index.md").read_text(encoding="utf-8")
    assert "Volume I — Civilization" not in hub_md
    assert "Volume II — Apocalypse" not in hub_md


def test_growth_command_returns_agent_goal_policy(capsys):
    assert main(["growth", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["agent_goal_policy"]["must_translate_outcome_to_machinery"] is True
    assert payload["campaigns"][0]["campaign_id"] == "one_million_views_2026"
    assert payload["campaigns"][0]["first_live_wedge"]["wedge_id"] == "launch_volume_i_spine"
    assert payload["campaigns"][0]["first_live_wedge"]["launch_readiness"] == "defined_not_launch_ready"


def test_surface_scoped_commands(capsys):
    assert main(["list"]) == 0
    out = capsys.readouterr().out
    assert "civ-07" in out
    assert "gt-16" in out
    assert main(["list", "--namespace", "lectures", "--series", "game-theory"]) == 0
    out = capsys.readouterr().out
    assert "gt-16" in out
    assert "civ-07" not in out
    assert main(["status"]) == 0
    assert "deprecated two-volume" in capsys.readouterr().out


def test_public_routes(capsys):
    assert main(["route", "civ-07", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["route_type"] == "spine"
    assert "literature alone drives history" in payload["caveat"]
    assert "museum" not in payload
    assert main(["route", "civ-17", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["route_type"] == "spine"
    assert "Virgil and Rome" in payload["what_changes_here"]
    assert main(["route", "gt-16", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["route_type"] == "application"
    assert main(["route", "sh-16", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["surface"] == "ph-apo"
    assert payload["route_type"] == "coda"
    assert "Anna Karenina coda" in payload["caveat"]
    assert "not a dedicated Tolstoy lecture" in payload["caveat"]


def test_ten_route_spine_seed_guardrails():
    routes = load_choreography()
    route_ids = [route["source_id"] for route in routes]
    assert route_ids == [
        "civ-07",
        "civ-17",
        "civ-29",
        "civ-51",
        "gb-02",
        "gb-09",
        "geo-14",
        "gt-16",
        "sh-16",
        "sh-28",
    ]
    assert load_route_seed()["seed_id"] == "ten_route_spine_seed"
    assert load_route_seed()["route_ids"] == route_ids
    route_types = {route["source_id"]: route["route_type"] for route in routes}
    assert route_types["civ-17"] == "spine"
    assert route_types["gb-02"] == "paired_close_reading"
    assert route_types["gb-09"] == "paired_close_reading"
    assert route_types["geo-14"] == "application"
    assert route_types["gt-16"] == "application"
    assert route_types["sh-28"] == "application"
    assert route_types["sh-16"] == "coda"
    sh16 = next(route for route in routes if route["source_id"] == "sh-16")
    assert sh16["surface"] == "ph-apo"
    assert "Anna Karenina coda" in sh16["caveat"]
    assert "not a dedicated Tolstoy lecture" in sh16["caveat"]
