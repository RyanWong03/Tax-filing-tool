import pytest
import library
import federal.tax_years.y_2025 as y_2025

YEAR = 2025 #Will change every year, is the year prior to current year, matches TAX_YEAR below
TAX_YEAR = y_2025

@pytest.fixture(autouse=True)
def temp_data_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(library, "get_data_dir", lambda: str(tmp_path))