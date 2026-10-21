import json
import os
import pytest
import library

# Saved now, before conftest's temporary folder is swapped in for each test.
original_get_data_dir = library.get_data_dir

def type_answers(monkeypatch, answers):
    """Makes input() return these answers one at a time, in order."""
    remaining = iter(answers)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(remaining))

def saved_file(tmp_path, year):
    with open(tmp_path / f"tax_return_{year}.json") as f:
        return json.load(f)

DEFAULT_2025 = {
    "tax_year": 2025,
    "form_1040_line_15": 0,
    "schedule_d_line_7": 0,
    "schedule_d_line_15": 0,
    "schedule_d_line_16": 0,
    "schedule_d_line_21": 0,
    "short_term_carryover_to_next_year": 0,
    "long_term_carryover_to_next_year": 0,
}

# ---------- Where the files live ----------

def test_data_folder_is_outside_the_project_folder():
    # Tax data must never end up inside the git repository.
    data_dir = os.path.abspath(original_get_data_dir())
    project_dir = os.path.abspath(os.getcwd())
    assert not data_dir.startswith(project_dir)

def test_data_folder_is_in_the_users_app_data(monkeypatch, tmp_path):
    if os.name == "nt":
        monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
        assert original_get_data_dir() == os.path.join(str(tmp_path), "Tax_filing_tool")
    else:
        monkeypatch.setenv("HOME", str(tmp_path))
        assert original_get_data_dir() == os.path.join(str(tmp_path), ".taxtool")

# ---------- Saving ----------

def test_save_tax_return_writes_a_readable_file(tmp_path):
    library.save_tax_return(2025, {"tax_year": 2025, "form_1040_line_15": 50000})

    assert saved_file(tmp_path, 2025) == {"tax_year": 2025, "form_1040_line_15": 50000}

def test_save_tax_return_creates_the_folder_if_missing(monkeypatch, tmp_path):
    # First time the tool runs, the data folder doesn't exist yet.
    new_folder = tmp_path / "does_not_exist_yet"
    monkeypatch.setattr(library, "get_data_dir", lambda: str(new_folder))

    library.save_tax_return(2025, {"tax_year": 2025})

    assert (new_folder / "tax_return_2025.json").exists()

def test_default_prior_year_return_is_all_zeros():
    assert library.default_prior_year_return(2026) == DEFAULT_2025

# ---------- Loading ----------

def test_load_prior_year_return_reads_the_saved_file(tmp_path):
    saved = dict(DEFAULT_2025, form_1040_line_15=50000, schedule_d_line_21=-3000)
    (tmp_path / "tax_return_2025.json").write_text(json.dumps(saved))

    assert library.load_prior_year_return(2026) == saved

def test_load_prior_year_return_reads_the_year_before_not_the_current_year(tmp_path):
    (tmp_path / "tax_return_2025.json").write_text(json.dumps(dict(DEFAULT_2025, form_1040_line_15=111)))
    (tmp_path / "tax_return_2026.json").write_text(json.dumps(dict(DEFAULT_2025, form_1040_line_15=222)))

    assert library.load_prior_year_return(2026)["form_1040_line_15"] == 111

# ---------- Missing file: asks you to type it in from your paper return ----------

def test_missing_file_and_no_prior_return_gives_zeros_and_saves_them(monkeypatch, tmp_path):
    type_answers(monkeypatch, ["no"])

    result = library.load_prior_year_return(2026)

    assert result == DEFAULT_2025
    assert saved_file(tmp_path, 2025) == DEFAULT_2025

def test_missing_file_with_prior_return_but_no_schedule_d(monkeypatch, tmp_path):
    type_answers(monkeypatch, ["yes", "50000", "no"])

    result = library.load_prior_year_return(2026)

    assert result == dict(DEFAULT_2025, form_1040_line_15=50000)
    assert saved_file(tmp_path, 2025) == result

def test_missing_file_with_prior_return_and_schedule_d(monkeypatch, tmp_path):
    # Answers: yes, 1040 line 15, yes (Schedule D), lines 7, 15, 16, 21, then the two carryover amounts.
    type_answers(monkeypatch, ["yes", "50000", "yes", "-8000", "0", "-8000", "-3000", "5000", "0"])

    result = library.load_prior_year_return(2026)

    assert result == {
        "tax_year": 2025,
        "form_1040_line_15": 50000,
        "schedule_d_line_7": -8000,
        "schedule_d_line_15": 0,
        "schedule_d_line_16": -8000,
        "schedule_d_line_21": -3000,
        "short_term_carryover_to_next_year": 5000,
        "long_term_carryover_to_next_year": 0,
    }
    assert saved_file(tmp_path, 2025) == result

def test_typed_in_return_is_remembered_next_time(monkeypatch, tmp_path):
    # After typing it in once, loading again reads the saved file and asks nothing.
    type_answers(monkeypatch, ["yes", "50000", "no"])
    first = library.load_prior_year_return(2026)

    type_answers(monkeypatch, [])   # any question now would fail the test
    second = library.load_prior_year_return(2026)

    assert second == first

def test_first_run_with_no_data_folder_at_all(monkeypatch, tmp_path):
    # Brand new computer: no data folder, no saved returns.
    new_folder = tmp_path / "does_not_exist_yet"
    monkeypatch.setattr(library, "get_data_dir", lambda: str(new_folder))
    type_answers(monkeypatch, ["no"])

    assert library.load_prior_year_return(2026) == DEFAULT_2025

# ---------- Corrupt file ----------

def test_corrupt_file_is_replaced_after_asking_again(monkeypatch, tmp_path):
    (tmp_path / "tax_return_2025.json").write_text("{this is not valid json")
    type_answers(monkeypatch, ["yes", "50000", "no"])

    result = library.load_prior_year_return(2026)

    assert result == dict(DEFAULT_2025, form_1040_line_15=50000)
    assert saved_file(tmp_path, 2025) == result