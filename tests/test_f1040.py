import json
from types import SimpleNamespace
import tax_context
import federal.forms.f1040 as f1040
from conftest import YEAR, TAX_YEAR
import library

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
        "gain": 5000, "w2_federal_tax_withheld": 0, "state_tax_withheld": 0
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
    assert read_saved(tmp_path)["line_3"] == [False, 2000]

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
    assert read_saved(tmp_path)["line_3"] == [True, 20000]

def test_filing_schedule_d_with_total_loss_counts_no_gain(tmp_path):
    # Net long-term gain 5000, but Schedule D line 16 is a loss (-1000). Either one zero or less means line 3 = 0.
    # So this is the same as having no gains: regular tax on 150000 = 20000.
    context = make_context(150000)
    add_long_term_sale(context)
    context.schedule_d.net_long_term_gain_loss = 5000
    context.schedule_d.line_16 = -1000
    assert f1040.compute_qualified_dividends_and_capital_gain_tax_worksheet(context) == 20000
    assert read_saved(tmp_path)["line_3"] == [True, 0]

def test_filing_schedule_d_with_long_term_loss_counts_no_gain(tmp_path):
    # Net long-term is a loss (-2000) even though Schedule D line 16 is positive. Line 3 = 0.
    context = make_context(150000)
    add_long_term_sale(context)
    context.schedule_d.net_long_term_gain_loss = -2000
    context.schedule_d.line_16 = 3000
    assert f1040.compute_qualified_dividends_and_capital_gain_tax_worksheet(context) == 20000
    assert read_saved(tmp_path)["line_3"] == [True, 0]

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
        "line_3": [False, 0],        # no capital gains
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

# Simple made-up brackets so the math is easy to check by hand and doesn't depend on any tax year.
BRACKETS = [
    (0, 10000, 0.10),
    (10000, 40000, 0.20),
    (40000, float("inf"), 0.30),
]

def test_zero_income_owes_no_tax():
    assert library.calculate_income_tax(0, BRACKETS) == 0

def test_negative_income_owes_no_tax():
    assert library.calculate_income_tax(-500, BRACKETS) == 0

def test_under_3000_uses_25_dollar_slot():
    # 1000 is in the 1000-1025 slot, midpoint 1012.50. 10% of 1012.50 = 101.25 -> 101
    assert library.calculate_income_tax(1000, BRACKETS) == 101

def test_just_under_3000_uses_25_dollar_slot():
    # 2999 is in the 2975-3000 slot, midpoint 2987.50. 10% = 298.75 -> 299
    assert library.calculate_income_tax(2999, BRACKETS) == 299

def test_exactly_3000_switches_to_50_dollar_slot():
    # 3000 is in the 3000-3050 slot, midpoint 3025. 10% = 302.50 -> 303
    assert library.calculate_income_tax(3000, BRACKETS) == 303

def test_income_just_over_first_bracket_edge():
    # 10000 is in the 10000-10050 slot, midpoint 10025.
    # 10% of 10000 = 1000, plus 20% of 25 = 5 -> 1005
    assert library.calculate_income_tax(10000, BRACKETS) == 1005

def test_income_from_code_comment_example():
    # 15019 is in the 15000-15050 slot, midpoint 15025.
    # 10% of 10000 = 1000, plus 20% of 5025 = 1005 -> 2005
    assert library.calculate_income_tax(15019, BRACKETS) == 2005

def test_just_under_100000_still_uses_slot():
    # 99999 is in the 99950-100000 slot, midpoint 99975.
    # 1000 + 20% of 30000 (6000) + 30% of 59975 (17992.50) = 24992.50 -> 24993
    assert library.calculate_income_tax(99999, BRACKETS) == 24993

def test_exactly_100000_uses_no_slot():
    # No slot at 100000 or above. 1000 + 6000 + 30% of 60000 (18000) = 25000
    assert library.calculate_income_tax(100000, BRACKETS) == 25000

def test_large_income_no_slot():
    # 1000 + 6000 + 30% of 460000 (138000) = 145000
    assert library.calculate_income_tax(500000, BRACKETS) == 145000

# ---- Real brackets from the year file. Expected values are for 2025 and must be redone for 2026. ----

def test_real_brackets_single_50000():
    # 50000 is in the 50000-50050 slot, midpoint 50025.
    # 10% of 11925 = 1192.50; 12% of 36550 = 4386; 22% of 1550 = 341 -> 5919.50 -> 5920
    assert library.calculate_income_tax(50000, TAX_YEAR.TAX_BRACKETS["single"]) == 5920

def test_real_brackets_single_150000():
    # No slot. 1192.50 + 4386 + 22% of 54875 (12072.50) + 24% of 46650 (11196) = 28847
    assert library.calculate_income_tax(150000, TAX_YEAR.TAX_BRACKETS["single"]) == 28847

def test_real_brackets_single_700000_reaches_top_bracket():
    # 1192.50 + 4386 + 12072.50 + 22548 + 17032 + 131538.75 + 37% of 73650 (27250.50) = 216020.25 -> 216020
    assert library.calculate_income_tax(700000, TAX_YEAR.TAX_BRACKETS["single"]) == 216020

def test_real_brackets_married_filing_jointly_120000():
    # No slot. 2385 + 12% of 73100 (8772) + 22% of 23050 (5071) = 16228
    assert library.calculate_income_tax(120000, TAX_YEAR.TAX_BRACKETS["married_filing_jointly"]) == 16228

def type_answers(monkeypatch, answers):
    """Makes input() return these answers one at a time, in order."""
    remaining = iter(answers)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(remaining))

def test_single_w2(monkeypatch):
    type_answers(monkeypatch, ["50000", "6000", "no"])
    assert f1040.collect_w2() == {"wages": 50000, "w2_federal_tax_withheld": 6000}

def test_two_w2s_are_added_together(monkeypatch):
    type_answers(monkeypatch, ["50000", "6000", "yes", "20000", "2500", "no"])
    assert f1040.collect_w2() == {"wages": 70000, "w2_federal_tax_withheld": 8500}

def test_three_w2s_are_added_together(monkeypatch):
    type_answers(monkeypatch, ["10000", "1000", "yes", "20000", "2000", "yes", "30000", "3000", "no"])
    assert f1040.collect_w2() == {"wages": 60000, "w2_federal_tax_withheld": 6000}

def test_totals_are_rounded_to_whole_dollars(monkeypatch):
    # Wages 1000.50 rounds up to 1001. Withholding 100.49 rounds down to 100.
    type_answers(monkeypatch, ["1000.50", "100.49", "no"])
    assert f1040.collect_w2() == {"wages": 1001, "w2_federal_tax_withheld": 100}

def test_rounding_happens_on_the_total_not_each_form(monkeypatch):
    # 0.40 + 0.40 = 0.80 rounds to 1. If each were rounded first, both would round to 0 and the total would be 0.
    type_answers(monkeypatch, ["10000.40", "0", "yes", "20000.40", "0", "no"])
    assert f1040.collect_w2() == {"wages": 30001, "w2_federal_tax_withheld": 0}

def test_zero_withholding(monkeypatch):
    type_answers(monkeypatch, ["30000", "0", "no"])
    assert f1040.collect_w2() == {"wages": 30000, "w2_federal_tax_withheld": 0}

def test_non_numeric_wages_asks_again(monkeypatch):
    type_answers(monkeypatch, ["abc", "50000", "6000", "no"])
    assert f1040.collect_w2() == {"wages": 50000, "w2_federal_tax_withheld": 6000}

def test_non_numeric_withholding_asks_again_without_double_counting(monkeypatch):
    # Wages are typed, then the withholding is bad. The form restarts, and the wages must not be counted twice.
    type_answers(monkeypatch, ["50000", "xyz", "50000", "6000", "no"])
    assert f1040.collect_w2() == {"wages": 50000, "w2_federal_tax_withheld": 6000}

def test_invalid_yes_no_answer_asks_again(monkeypatch):
    type_answers(monkeypatch, ["50000", "6000", "maybe", "no"])
    assert f1040.collect_w2() == {"wages": 50000, "w2_federal_tax_withheld": 6000}

def test_yes_no_answer_ignores_spaces_and_capitals(monkeypatch):
    type_answers(monkeypatch, ["50000", "6000", "  YES ", "10000", "1000", "No"])
    assert f1040.collect_w2() == {"wages": 60000, "w2_federal_tax_withheld": 7000}

# Tests for Form 1040 lines 1-15 as produced by f1040.calculate(filing_data).
 
ZERO_PRIOR = {"form_1040_line_15": 0, "schedule_d_line_7": 0, "schedule_d_line_15": 0,
              "schedule_d_line_16": 0, "schedule_d_line_21": 0}
 
 
def make_1040_context(filing_status="single"):
    context = tax_context.tax_context(YEAR)
    context.constants = TAX_YEAR
    context.filing_status = filing_status
    return context
 
 
def run_calculate(context, wages):
    # Saved so the prior-year lookup does not stop to ask questions.
    library.save_tax_return(YEAR - 1, ZERO_PRIOR)
    f1040.calculate({"year": YEAR, "wages": wages, "w2_federal_tax_withheld": 0, "context": context})
 
 
def form_lines(context):
    f = context.form_1040
    return {
        "1a": f.line_1a, "1z": f.line_1z, "2a": f.line_2a, "2b": f.line_2b,
        "3a": f.line_3a, "3b": f.line_3b, "7a": f.line_7a, "8": f.line_8,
        "9": f.line_9, "10": f.line_10, "11a": f.line_11a, "11b": f.line_11b,
        "12e": f.line_12e, "13a": f.line_13a, "13b": f.line_13b, "14": f.line_14,
        "15": f.line_15,
    }
 
 
def interest_entry(amount, bond_interest=0, tax_exempt_interest=0):
    return {"payer": "Test Bank", "amount": amount, "bond_interest": bond_interest,
            "early_withdrawal_penalty": 0, "fed_tax_withheld": 0, "tax_exempt_interest": tax_exempt_interest}
 
 
def dividend_entry(ordinary=0, qualified=0, cap_gain_distributions=0):
    return {"payer": "Fidelity", "ordinary_dividends": ordinary, "qualified_dividends": qualified,
            "cap_gain_distributions": cap_gain_distributions, "unrecaptured_sec_1250_gain": 0,
            "fed_tax_withheld": 0, "section_199a_dividends": 0}
 
 
def sale(gain):
    return {"description": "test", "date_acquired": "01/01/2024", "date_sold": "06/01/2025",
            "proceeds": 10000 + gain, "cost_basis": 10000, "adjustments": 0, "adjustment_code": None,
            "gain": gain, "w2_federal_tax_withheld": 0, "state_tax_withheld": 0}
 
 
def test_wages_only():
    context = make_1040_context()
 
    run_calculate(context, 60000)
 
    assert form_lines(context) == {
        "1a": 60000, "1z": 60000,
        "2a": 0, "2b": 0, "3a": 0, "3b": 0,
        "7a": 0, "8": 0,
        "9": 60000,       # wages only
        "10": 0,
        "11a": 60000,      # 60000 - 0
        "11b": 60000,
        "12e": 15750,      # single standard deduction
        "13a": 0, "13b": 0,
        "14": 15750,
        "15": 44250,      # 60000 - 15750
    }
 
 
def test_interest_and_dividends_are_added_and_tax_exempt_interest_is_not():
    context = make_1040_context()
    # Interest 1000.60 + savings bond interest 300 = 1300.60 -> 1301. Tax-exempt interest 200 is shown on 2a only.
    context.schedule_b.interest_entries.append(interest_entry(1000.60, bond_interest=300, tax_exempt_interest=200))
    context.schedule_b.dividend_entries.append(dividend_entry(ordinary=400, qualified=250))
 
    run_calculate(context, 60000)
 
    assert form_lines(context) == {
        "1a": 60000, "1z": 60000,
        "2a": 200,        # tax-exempt interest, not part of income
        "2b": 1301,
        "3a": 250,        # qualified dividends, not added again
        "3b": 400,
        "7a": 0, "8": 0,
        "9": 61701,       # 60000 + 1301 + 400
        "10": 0,
        "11a": 61701,
        "11b": 61701,
        "12e": 15750,
        "13a": 0, "13b": 0,
        "14": 15750,
        "15": 45951,      # 61701 - 15750
    }
 
 
def test_capital_gains_reach_line_7a_and_total_income():
    context = make_1040_context()
    context.form_8949.short_term_entries["A"].append(sale(1000))
    context.form_8949.long_term_entries["D"].append(sale(5000))
    # 200 of capital gain distributions: part of the long-term total, not part of ordinary dividends (3b).
    context.schedule_b.dividend_entries.append(dividend_entry(ordinary=0, qualified=0, cap_gain_distributions=200))
 
    run_calculate(context, 60000)
 
    assert form_lines(context) == {
        "1a": 60000, "1z": 60000,
        "2a": 0, "2b": 0, "3a": 0, "3b": 0,
        "7a": 6200,       # short-term 1000 + long-term 5000 + distributions 200
        "8": 0,
        "9": 66200,       # 60000 + 6200
        "10": 0,
        "11a": 66200,
        "11b": 66200,
        "12e": 15750,
        "13a": 0, "13b": 0,
        "14": 15750,
        "15": 50450,      # 66200 - 15750
    }
 
 
def test_capital_loss_is_limited_to_3000_on_line_7a():
    context = make_1040_context()
    context.form_8949.long_term_entries["D"].append(sale(-5000))
 
    run_calculate(context, 60000)
 
    assert context.form_1040.line_7a == -3000     # loss of 5000, but only 3000 can be deducted
    assert context.form_1040.line_9 == 57000      # 60000 - 3000
    assert context.form_1040.line_11a == 57000
    assert context.form_1040.line_11b == 57000
    assert context.form_1040.line_15 == 41250     # 57000 - 15750
 
 
def test_qualified_dividends_are_on_line_3a_before_schedule_d_runs():
    # A 6000 short-term gain and a 2000 long-term loss: net gain 4000 but no long-term gain, so Schedule D line 17
    # is No and line 22 asks "do you have qualified dividends on 1040 line 3a?". That only works if line 3a was
    # filled in before Schedule D ran.
    context = make_1040_context()
    context.form_8949.short_term_entries["A"].append(sale(6000))
    context.form_8949.long_term_entries["D"].append(sale(-2000))
    context.schedule_b.dividend_entries.append(dividend_entry(ordinary=400, qualified=250))
 
    run_calculate(context, 60000)
 
    assert context.form_1040.line_3a == 250
    assert context.schedule_d.line_17 is False
    assert context.schedule_d.line_22 is True
    assert context.form_1040.line_7a == 4000
    assert context.form_1040.line_9 == 64400      # 60000 + 400 + 4000
    assert context.form_1040.line_15 == 48650     # 64400 - 15750
 
 
def test_schedule_d_line_22_is_false_without_qualified_dividends():
    context = make_1040_context()
    context.form_8949.short_term_entries["A"].append(sale(6000))
    context.form_8949.long_term_entries["D"].append(sale(-2000))
    context.schedule_b.dividend_entries.append(dividend_entry(ordinary=400, qualified=0))
 
    run_calculate(context, 60000)
 
    assert context.form_1040.line_3a == 0
    assert context.schedule_d.line_22 is False
 
 
def test_taxable_income_is_never_negative():
    context = make_1040_context()
 
    run_calculate(context, 10000)
 
    assert context.form_1040.line_11a == 10000
    assert context.form_1040.line_11b == 10000
    assert context.form_1040.line_14 == 15750
    assert context.form_1040.line_15 == 0         # 10000 - 15750 would be -5750, so it is 0
 
 
def test_married_filing_jointly_uses_the_joint_standard_deduction():
    context = make_1040_context("married_filing_jointly")
 
    run_calculate(context, 100000)
 
    assert context.form_1040.line_12e == 31500
    assert context.form_1040.line_14 == 31500
    assert context.form_1040.line_15 == 68500     # 100000 - 31500
 
 
def test_no_income_at_all():
    context = make_1040_context()
 
    run_calculate(context, 0)
 
    assert context.form_1040.line_9 == 0
    assert context.form_1040.line_11a == 0
    assert context.form_1040.line_11b == 0
    assert context.form_1040.line_15 == 0

# ======================= Form 1040 lines 16-24 =======================

def test_tax_on_wages_only_uses_the_tax_table():
    # Taxable income 44250 (60000 - 15750). Slot 44250-44300, midpoint 44275.
    # 10% of 11925 = 1192.50; 12% of 32350 = 3882 -> 5074.50 -> 5075
    context = make_1040_context()

    run_calculate(context, 60000)

    assert context.form_1040.line_15 == 44250
    assert context.form_1040.line_16_amt == 5075
    assert context.form_1040.line_16_form_8814 is False
    assert context.form_1040.line_16_form_4972 is False
    assert context.form_1040.line_16_form_misc is False
    assert context.form_1040.line_16_form_misc_value == ""
    assert context.form_1040.line_24 == 5075


def test_qualified_dividends_use_the_qualified_dividends_worksheet():
    # 5000 of ordinary dividends, all qualified. Taxable income 49250 (60000 + 5000 - 15750).
    # Ordinary part 44250. 4100 of the dividends fills the 0% band (44250 -> 48350), the other 900 is at 15% = 135.
    # Tax on the ordinary 44250 = 5075. Worksheet total 5210. Tax table on 49250 would be 5755.
    context = make_1040_context()
    context.schedule_b.dividend_entries.append(dividend_entry(ordinary=5000, qualified=5000))

    run_calculate(context, 60000)

    assert context.form_1040.line_15 == 49250
    assert context.form_1040.line_16_amt == 5210
    assert context.form_1040.line_16_form_8814 is False
    assert context.form_1040.line_16_form_4972 is False
    assert context.form_1040.line_16_form_misc is False
    assert context.form_1040.line_16_form_misc_value == ""
    assert context.form_1040.line_24 == 5210


def test_long_term_gain_with_line_20_yes_uses_the_qualified_dividends_worksheet():
    # 8000 long-term gain, no 1099-DIV, so Schedule D line 20 is Yes. Taxable income 52250 (68000 - 15750).
    # Ordinary part 44250 (tax 5075). 4100 of the gain is at 0%, 3900 at 15% = 585. Total 5660.
    # Tax table on 52250 would be 6415.
    context = make_1040_context()
    context.form_8949.long_term_entries["D"].append(sale(8000))

    run_calculate(context, 60000)

    assert context.schedule_d.line_20 is True
    assert context.form_1040.line_15 == 52250
    assert context.form_1040.line_16_amt == 5660
    assert context.form_1040.line_16_form_8814 is False
    assert context.form_1040.line_16_form_4972 is False
    assert context.form_1040.line_16_form_misc is False
    assert context.form_1040.line_16_form_misc_value == ""


def test_box_2b_gain_uses_the_schedule_d_tax_worksheet():
    # 9000 long-term sale + 1000 capital gain distributions (500 of it is unrecaptured section 1250 gain, box 2b).
    # Net long-term 10000 = 7a. Taxable income 54250 (70000 - 15750). Schedule D line 20 is No.
    # Schedule D Tax Worksheet: the 500 of 1250 gain is taxed as ordinary income, the other 9500 gets the 0%/15%
    # rates. Line 45 = 885 (15% part) + 5135 (ordinary 44750) = 6020. Tax table on 54250 would be 6855.
    # The Qualified Dividends worksheet would wrongly give 5960 (it taxes the 1250 gain at 15%).
    context = make_1040_context()
    context.form_8949.long_term_entries["D"].append(sale(9000))
    box_2b = dividend_entry(ordinary=0, qualified=0, cap_gain_distributions=1000)
    box_2b["unrecaptured_sec_1250_gain"] = 500
    context.schedule_b.dividend_entries.append(box_2b)

    run_calculate(context, 60000)

    assert context.schedule_d.line_20 is False
    assert context.form_1040.line_15 == 54250
    assert context.form_1040.line_16_amt == 6020
    assert context.form_1040.line_16_form_8814 is False
    assert context.form_1040.line_16_form_4972 is False
    assert context.form_1040.line_16_form_misc is False
    assert context.form_1040.line_16_form_misc_value == ""
    assert context.form_1040.line_24 == 6020


def test_box_2b_gain_absorbed_by_a_short_term_loss_uses_the_qualified_dividends_worksheet():
    # Same 1250 gain (500), but an 800 short-term loss wipes it out, so Schedule D line 20 is Yes.
    # Net long-term 10000, net short-term -800, line 16 = 9200 = 7a. Taxable income 53450 (69200 - 15750).
    # Worksheet line 3 = smaller of net long-term (10000) and line 16 (9200) = 9200. Result 5840.
    # Tax table would be 6679. The Schedule D Tax Worksheet would wrongly give 5900.
    context = make_1040_context()
    context.form_8949.long_term_entries["D"].append(sale(9000))
    context.form_8949.short_term_entries["A"].append(sale(-800))
    box_2b = dividend_entry(ordinary=0, qualified=0, cap_gain_distributions=1000)
    box_2b["unrecaptured_sec_1250_gain"] = 500
    context.schedule_b.dividend_entries.append(box_2b)

    run_calculate(context, 60000)

    assert context.schedule_d.line_20 is True
    assert context.form_1040.line_15 == 53450
    assert context.form_1040.line_16_amt == 5840
    assert context.form_1040.line_16_form_8814 is False
    assert context.form_1040.line_16_form_4972 is False
    assert context.form_1040.line_16_form_misc is False
    assert context.form_1040.line_16_form_misc_value == ""


def test_qualified_dividends_with_no_long_term_gain_use_the_qualified_dividends_worksheet():
    # Short-term gain 6000, long-term loss 2000: Schedule D line 17 is No, so line 22 asks about qualified dividends.
    # Dividends 400 (250 qualified). Taxable income 48650 (64400 - 15750). Worksheet line 3 = 0 (long-term is a loss).
    # Ordinary part is 48400, already past the 0% band (it ends at 48350), so all 250 of dividends is at 15% = 37.50.
    # Tax on ordinary 48400 = 5573. Total 5610.50 -> 5611. Tax table on 48650 would be 5623.
    context = make_1040_context()
    context.form_8949.short_term_entries["A"].append(sale(6000))
    context.form_8949.long_term_entries["D"].append(sale(-2000))
    context.schedule_b.dividend_entries.append(dividend_entry(ordinary=400, qualified=250))

    run_calculate(context, 60000)

    assert context.schedule_d.line_22 is True
    assert context.form_1040.line_15 == 48650
    assert context.form_1040.line_16_amt == 5611
    assert context.form_1040.line_16_form_8814 is False
    assert context.form_1040.line_16_form_4972 is False
    assert context.form_1040.line_16_form_misc is False
    assert context.form_1040.line_16_form_misc_value == ""


def test_same_sales_without_qualified_dividends_use_the_tax_table():
    # Same as above but none of the dividends are qualified, so Schedule D line 22 is No.
    # Tax table on 48650: slot 48650-48700, midpoint 48675. 1192.50 + 4386 + 22% of 200 (44) = 5622.50 -> 5623.
    context = make_1040_context()
    context.form_8949.short_term_entries["A"].append(sale(6000))
    context.form_8949.long_term_entries["D"].append(sale(-2000))
    context.schedule_b.dividend_entries.append(dividend_entry(ordinary=400, qualified=0))

    run_calculate(context, 60000)

    assert context.schedule_d.line_22 is False
    assert context.form_1040.line_15 == 48650
    assert context.form_1040.line_16_amt == 5623
    assert context.form_1040.line_16_form_8814 is False
    assert context.form_1040.line_16_form_4972 is False
    assert context.form_1040.line_16_form_misc is False
    assert context.form_1040.line_16_form_misc_value == ""


def test_no_taxable_income_means_no_tax():
    # 10000 wages + 1000 dividends (all qualified) is less than the 15750 standard deduction.
    context = make_1040_context()
    context.schedule_b.dividend_entries.append(dividend_entry(ordinary=1000, qualified=1000))

    run_calculate(context, 10000)

    assert context.form_1040.line_15 == 0
    assert context.form_1040.line_16_amt == 0
    assert context.form_1040.line_16_form_8814 is False
    assert context.form_1040.line_16_form_4972 is False
    assert context.form_1040.line_16_form_misc is False
    assert context.form_1040.line_16_form_misc_value == ""
    assert context.form_1040.line_24 == 0


def test_married_filing_jointly_uses_the_joint_brackets():
    # Taxable income 68500 (100000 - 31500). Slot 68500-68550, midpoint 68525.
    # 10% of 23850 = 2385; 12% of 44675 = 5361 -> 7746
    context = make_1040_context("married_filing_jointly")

    run_calculate(context, 100000)

    assert context.form_1040.line_15 == 68500
    assert context.form_1040.line_16_amt == 7746
    assert context.form_1040.line_16_form_8814 is False
    assert context.form_1040.line_16_form_4972 is False
    assert context.form_1040.line_16_form_misc is False
    assert context.form_1040.line_16_form_misc_value == ""
    assert context.form_1040.line_24 == 7746


def test_lines_17_to_24_add_up():
    # Whatever the individual lines are, the form's arithmetic must hold.
    context = make_1040_context()
    context.schedule_b.dividend_entries.append(dividend_entry(ordinary=5000, qualified=5000))

    run_calculate(context, 60000)

    f = context.form_1040
    assert f.line_18 == f.line_16_amt + f.line_17
    assert f.line_21 == f.line_19 + f.line_20
    assert f.line_22 == max(f.line_18 - f.line_21, 0)
    assert f.line_24 == f.line_22 + f.line_23

def test_lines_without_a_schedule_yet_are_zero():
    # Schedule 2 line 3 (17), Schedule 8812 (19), Schedule 3 line 8 (20) and Schedule 2 line 21 (23) are not
    # implemented, so they are 0 for now. Change this test when each schedule is built.
    context = make_1040_context()
    context.schedule_b.dividend_entries.append(dividend_entry(ordinary=5000, qualified=5000))

    run_calculate(context, 60000)

    f = context.form_1040
    assert f.line_17 == 0
    assert f.line_19 == 0
    assert f.line_20 == 0
    assert f.line_23 == 0
    assert f.line_21 == 0                  # 19 + 20
    assert f.line_18 == f.line_16_amt          # 16 + 17
    assert f.line_22 == f.line_16_amt          # nothing to subtract
    assert f.line_24 == f.line_16_amt          # 22 + 23

def test_income_lines_without_a_source_are_zero():
    context = make_1040_context()

    run_calculate(context, 60000)

    f = context.form_1040
    for name in ["line_1b", "line_1c", "line_1d", "line_1e", "line_1f", "line_1g", "line_1h", "line_1i",
                 "line_4a", "line_4b", "line_5a", "line_5b", "line_6a", "line_6b"]:
        assert getattr(f, name) == 0, name


def test_checkboxes_are_all_unchecked():
    # Assumed: not a dependent, not married filing separately, not dual-status, under 65, not blind, no children,
    # and we file Schedule D whenever there are sales, distributions or a carryover.
    context = make_1040_context()

    run_calculate(context, 60000)

    f = context.form_1040
    for name in ["line_3c_childs_dividends_included_in_line_3a", "line_3c_childs_dividends_included_in_line_3b",
                 "line_4c_rollover", "line_4c_qcd", "line_4c_misc", "line_5c_rollover", "line_5c_pso", "line_5c_misc",
                 "line_5c_misc_amt", "line_6c", "line_6d", "line_7b_schedule_d_not_required",
                 "line_7b_includes_childs_capital_gain_loss", "line_12a_you_are_claimed_as_dependent",
                 "line_12a_spouse_is_claimed_as_dependent", "line_12b", "line_12c", "line_12d_you_are_age_65_plus",
                 "line_12d_you_are_blind", "line_12d_spouse_is_age_65_plus", "line_12d_spouse_is_blind", "line_16_form_8814",
                 "line_16_form_4972", "line_16_form_misc", "line_27b", "line_27c", "line_28_reject_actc_claim"]:
        value = getattr(f, name)
        values = value if isinstance(value, list) else [value]
        assert not any(values), name


def test_line_11b_equals_line_11a():
    context = make_1040_context()

    run_calculate(context, 60000)

    assert context.form_1040.line_11b == context.form_1040.line_11a


def test_lines_1_to_15_arithmetic_holds():
    # A return with every kind of income, so each sum has several non-zero parts.
    context = make_1040_context()
    context.schedule_b.interest_entries.append(interest_entry(1000, tax_exempt_interest=200))
    context.schedule_b.dividend_entries.append(dividend_entry(ordinary=400, qualified=250, cap_gain_distributions=100))
    context.form_8949.long_term_entries["D"].append(sale(3000))

    run_calculate(context, 60000)

    f = context.form_1040
    assert f.line_1z == f.line_1a + f.line_1b + f.line_1c + f.line_1d + f.line_1e + f.line_1f + f.line_1g + f.line_1h
    assert f.line_9 == f.line_1z + f.line_2b + f.line_3b + f.line_4b + f.line_5b + f.line_6b + f.line_7a + f.line_8
    assert f.line_11a == f.line_9 - f.line_10
    assert f.line_14 == f.line_12e + f.line_13a + f.line_13b
    assert f.line_15 == max(f.line_11b - f.line_14, 0)