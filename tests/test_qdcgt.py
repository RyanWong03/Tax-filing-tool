import json
from types import SimpleNamespace
import tax_context
import federal.forms.f1040 as f1040
from conftest import YEAR, TAX_YEAR

# Made-up constants so the math is easy to check by hand and doesn't depend on any tax year.
# 0% rate up to 100,000. 15% rate up to 400,000. 20% above that.
# Ordinary tax: 10% to 100,000, 20% to 500,000, 30% above.
FAKE = SimpleNamespace(
    QDCGT_ZERO_RATE_MAX={"single": 100000},
    QDCGT_FIFTEEN_RATE_MAX={"single": 400000},
    TAX_BRACKETS={"single": [(0, 100000, 0.10), (100000, 500000, 0.20), (500000, float("inf"), 0.30)]},
)

def make_context(taxable_income, qualified_dividends=0, line_7a=0, constants=FAKE):
    context = tax_context.tax_context(YEAR)
    context.constants = constants
    context.filing_status = "single"
    context.form_1040.line_15 = taxable_income
    context.form_1040.line_3a = qualified_dividends
    context.form_1040.line_7a = line_7a
    return context

def add_long_term_sale(context):
    context.form_8949.long_term_entries["D"].append({
        "description": "test", "date_acquired": "01/01/2024", "date_sold": "06/01/2025",
        "proceeds": 8000, "cost_basis": 3000, "adjustments": 0, "adjustment_code": None,
        "gain": 5000, "federal_tax_withheld": 0, "state_tax_withheld": 0
    })

def read_saved(tmp_path):
    with open(tmp_path / f"qualified_dividends_and_capital_gain_tax_worksheet_{YEAR}.json") as f:
        return json.load(f)

# ---------- Made-up constants: how the worksheet works ----------

def test_no_gains_or_dividends_equals_regular_tax():
    # Nothing is taxed at the lower rates, so the answer is the regular tax on 150000.
    # Regular tax: 10000 + 20% of 50000 = 20000
    context = make_context(150000)
    assert f1040.compute_qualified_dividends_and_capital_gain_tax_worksheet(context) == 20000

def test_qualified_dividends_entirely_in_zero_percent_zone():
    # Income 80000, of which 5000 is qualified dividends. All of it falls under the 100000 zero-rate line.
    # Tax on the other 75000: slot midpoint 75025, 10% = 7502.50 -> 7503
    # Regular tax on 80000: slot midpoint 80025, 10% = 8002.50 -> 8003. Smaller is 7503.
    context = make_context(80000, qualified_dividends=5000)
    assert f1040.compute_qualified_dividends_and_capital_gain_tax_worksheet(context) == 7503

def test_qualified_dividends_straddle_zero_and_fifteen_percent():
    # Income 130000, of which 50000 is qualified dividends. Ordinary part is 80000.
    # The first 20000 of dividends fills the zero-rate zone (80000 -> 100000). The other 30000 is at 15% = 4500.
    # Tax on the ordinary 80000: 8003. Total 4500 + 8003 = 12503. Regular tax on 130000 is 16000.
    context = make_context(130000, qualified_dividends=50000)
    assert f1040.compute_qualified_dividends_and_capital_gain_tax_worksheet(context) == 12503

def test_gains_reach_twenty_percent_zone():
    # Income 600000, of which 300000 is qualified dividends. Ordinary part is 300000.
    # Nothing at 0% (ordinary income already past 100000). 15% zone runs 300000 -> 400000 = 100000 * 15% = 15000.
    # The remaining 200000 is at 20% = 40000. Tax on ordinary 300000: 10000 + 20% of 200000 = 50000.
    # Total 15000 + 40000 + 50000 = 105000. Regular tax on 600000 is 120000.
    context = make_context(600000, qualified_dividends=300000)
    assert f1040.compute_qualified_dividends_and_capital_gain_tax_worksheet(context) == 105000

def test_not_filing_schedule_d_uses_form_1040_line_7a(tmp_path):
    # No Schedule D, but 1040 line 7a has 2000 (capital gain distributions). Line 3 picks it up.
    # Ordinary part 128000: tax 10000 + 20% of 28000 = 15600. The 2000 is at 15% = 300. Total 15900.
    context = make_context(130000, line_7a=2000)
    result = f1040.compute_qualified_dividends_and_capital_gain_tax_worksheet(context)
    assert result == 15900
    assert read_saved(tmp_path)["line_3"] == 2000

def test_filing_schedule_d_uses_smaller_of_long_term_net_and_total(tmp_path):
    # Schedule D: net long-term 30000, Schedule D line 16 total 20000. Line 3 = smaller = 20000.
    # Income 130000, qualified dividends 10000. Gains and dividends total 30000, ordinary part 100000.
    # Ordinary part is right at the zero-rate line, so all 30000 is at 15% = 4500.
    # Tax on 100000 (no slot): 10000. Total 14500. Regular tax on 130000 is 16000.
    context = make_context(130000, qualified_dividends=10000)
    add_long_term_sale(context)
    context.schedule_d.net_long_term_gain_loss = 30000
    context.schedule_d.line_16 = 20000
    assert f1040.compute_qualified_dividends_and_capital_gain_tax_worksheet(context) == 14500
    assert read_saved(tmp_path)["line_3"] == 20000

def test_filing_schedule_d_with_total_loss_counts_no_gain(tmp_path):
    # Net long-term gain 5000, but Schedule D line 16 is a loss (-1000). Either one zero or less means line 3 = 0.
    # So this is the same as having no gains: regular tax on 150000 = 20000.
    context = make_context(150000)
    add_long_term_sale(context)
    context.schedule_d.net_long_term_gain_loss = 5000
    context.schedule_d.line_16 = -1000
    assert f1040.compute_qualified_dividends_and_capital_gain_tax_worksheet(context) == 20000
    assert read_saved(tmp_path)["line_3"] == 0

def test_filing_schedule_d_with_long_term_loss_counts_no_gain(tmp_path):
    # Net long-term is a loss (-2000) even though Schedule D line 16 is positive. Line 3 = 0.
    context = make_context(150000)
    add_long_term_sale(context)
    context.schedule_d.net_long_term_gain_loss = -2000
    context.schedule_d.line_16 = 3000
    assert f1040.compute_qualified_dividends_and_capital_gain_tax_worksheet(context) == 20000
    assert read_saved(tmp_path)["line_3"] == 0

def test_result_is_never_more_than_regular_tax():
    # Zero-rate zone only goes to 10000 here, so most of the 100000 of dividends is taxed at 15%,
    # which is more than the 10% ordinary rate. The worksheet's last line takes the smaller of the two.
    # Worksheet method: 15% of 100000 = 15000, plus tax on ordinary 20000 (midpoint 20025, 10% = 2002.50 -> 2003) = 17003.
    # Regular tax on 120000: 10000 + 20% of 20000 = 14000. Smaller is 14000.
    low_zero_zone = SimpleNamespace(
        QDCGT_ZERO_RATE_MAX={"single": 10000},
        QDCGT_FIFTEEN_RATE_MAX={"single": 400000},
        TAX_BRACKETS=FAKE.TAX_BRACKETS,
    )
    context = make_context(120000, qualified_dividends=100000, constants=low_zero_zone)
    assert f1040.compute_qualified_dividends_and_capital_gain_tax_worksheet(context) == 14000

def test_saved_worksheet_every_line(tmp_path):
    # Same situation as the zero/fifteen straddle test, every line checked.
    context = make_context(130000, qualified_dividends=50000)
    f1040.compute_qualified_dividends_and_capital_gain_tax_worksheet(context)

    assert read_saved(tmp_path) == {
        "tax_year": YEAR,
        "line_1": 130000,   # taxable income
        "line_2": 50000,    # qualified dividends
        "line_3": 0,        # no capital gains
        "line_4": 50000,    # 50000 + 0
        "line_5": 80000,    # 130000 - 50000 = ordinary part
        "line_6": 100000,   # zero-rate limit
        "line_7": 100000,   # smaller of 130000 and 100000
        "line_8": 80000,    # smaller of 80000 and 100000
        "line_9": 20000,    # 100000 - 80000 = room left at 0%
        "line_10": 50000,   # smaller of 130000 and 50000
        "line_11": 20000,   # same as line 9
        "line_12": 30000,   # 50000 - 20000
        "line_13": 400000,  # fifteen-rate limit
        "line_14": 130000,  # smaller of 130000 and 400000
        "line_15": 100000,  # 80000 + 20000
        "line_16": 30000,   # 130000 - 100000
        "line_17": 30000,   # smaller of 30000 and 30000 = amount at 15%
        "line_18": 4500,    # 30000 * 15%
        "line_19": 50000,   # 20000 + 30000
        "line_20": 0,       # 50000 - 50000 = amount at 20%
        "line_21": 0,       # 0 * 20%
        "line_22": 8003,    # tax on ordinary 80000
        "line_23": 12503,   # 4500 + 0 + 8003
        "line_24": 16000,   # regular tax on 130000
        "line_25": 12503,   # smaller of 12503 and 16000
    }

# ---------- Real 2025 constants. Expected values are for 2025 and must be redone for 2026. ----------

def test_real_constants_dividends_straddle_zero_and_fifteen_percent():
    # Single, income 100000, qualified dividends 20000. Ordinary part is 80000.
    # 0% zone ends at 48350, so all 80000 is already past it: dividends all at 15% = 3000.
    # Tax on ordinary 80000 (midpoint 80025): 1192.50 + 4386 + 22% of 31550 (6941) = 12519.50 -> 12520
    # Total 3000 + 12520 = 15520. Regular tax on 100000 is 16914.
    context = make_context(100000, qualified_dividends=20000, constants=TAX_YEAR)
    assert f1040.compute_qualified_dividends_and_capital_gain_tax_worksheet(context) == 15520

def test_real_constants_dividends_entirely_in_zero_percent_zone():
    # Single, income 45000, qualified dividends 10000. Ordinary part is 35000, under the 48350 line.
    # All 10000 of dividends fits under the line, so 0% on it. Tax is only on the ordinary 35000.
    # Midpoint 35025: 1192.50 + 12% of 23100 (2772) = 3964.50 -> 3965
    context = make_context(45000, qualified_dividends=10000, constants=TAX_YEAR)
    assert f1040.compute_qualified_dividends_and_capital_gain_tax_worksheet(context) == 3965