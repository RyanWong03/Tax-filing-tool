import tax_context
import federal.forms.schedule_b as schedule_b
import federal.forms.form_8949 as form_8949
import federal.forms.schedule_d as schedule_d
from conftest import YEAR

# These tests run the whole path: typed answers -> stored entries -> Schedule B and D totals.
# They catch a mismatch between what the entry code stores and what the math code reads.

def type_answers(monkeypatch, answers):
    """Makes input() return these answers one at a time, in order."""
    remaining = iter(answers)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(remaining))

ZERO_PRIOR = {"form_1040_line_15": 0, "schedule_d_line_7": 0, "schedule_d_line_15": 0,
              "schedule_d_line_16": 0, "schedule_d_line_21": 0}

def test_typed_interest_and_dividends_reach_the_schedule_b_totals(monkeypatch):
    context = tax_context.tax_context(YEAR)
    type_answers(monkeypatch, [
        "",   "Chase", "1000.60", "0", "300", "0", "0", "no",          # 1099-INT
        "",   "Fidelity", "400", "250", "100", "50", "0", "0", "no",   # 1099-DIV
    ])

    schedule_b.collect_1099_int(context)
    schedule_b.collect_1099_div(context)
    schedule_b.aggregate_schedule_b(context)

    assert context.schedule_b.taxable_interest == 1301      # 1000.60 + 300 = 1300.60
    assert context.schedule_b.interest_on_savings_bonds == 300
    assert context.schedule_b.ordinary_dividends == 400
    assert context.schedule_b.qualified_dividends == 250
    assert context.schedule_b.cap_gain_distributions == 100
    assert context.schedule_b.unrecaptured_sec_1250_gain == 50

def test_typed_sales_reach_schedule_d(monkeypatch):
    # Short-term sale with a 1000 gain, long-term sale with a 3000 gain, 200 of capital gain distributions.
    context = tax_context.tax_context(YEAR)
    type_answers(monkeypatch, [
        "A", "Fidelity", "AAPL", "01/01/2025", "06/01/2025", "3000", "2000", "0", "0", "0", "0", "no",
        "D", "Fidelity", "MSFT", "01/01/2023", "06/01/2025", "8000", "5000", "0", "0", "0", "0", "no",
        "",  "Fidelity", "0", "0", "200", "0", "0", "0", "no",
    ])

    form_8949.collect_1099_b_short_term(context)
    form_8949.collect_1099_b_long_term(context)
    schedule_b.collect_1099_div(context)
    schedule_b.aggregate_schedule_b(context)
    schedule_d.aggregate_schedule_d(context, ZERO_PRIOR)

    assert context.schedule_d.net_short_term_gain_loss == 1000
    assert context.schedule_d.capital_gain_distributions == 200
    assert context.schedule_d.net_long_term_gain_loss == 3200     # 3000 + 200
    assert context.schedule_d.line_16 == 4200
    assert context.form_1040.line_7a == 4200
    assert context.schedule_d.line_20 is True

def test_typed_box_2b_reaches_the_1250_worksheet(monkeypatch):
    # A 5000 long-term gain, and a 1099-DIV with 500 in box 2b (unrecaptured section 1250 gain).
    context = tax_context.tax_context(YEAR)
    type_answers(monkeypatch, [
        "D", "Fidelity", "VNQ", "01/01/2023", "06/01/2025", "8000", "3000", "0", "0", "0", "0", "no",
        "",  "Fidelity", "0", "0", "0", "500", "0", "0", "no",
    ])

    form_8949.collect_1099_b_long_term(context)
    schedule_b.collect_1099_div(context)
    schedule_b.aggregate_schedule_b(context)
    schedule_d.aggregate_schedule_d(context, ZERO_PRIOR)

    assert context.schedule_d.unrecaptured_section_1250_gain == 500
    assert context.schedule_d.line_20 is False

def test_typed_accrued_market_discount_reaches_schedule_b_interest(monkeypatch):
    context = tax_context.tax_context(YEAR)
    type_answers(monkeypatch, [
        "A", "Fidelity", "BOND", "01/01/2025", "06/01/2025", "3000", "2000", "125.50", "0", "0", "0", "no",
    ])

    form_8949.collect_1099_b_short_term(context)
    schedule_b.aggregate_schedule_b(context)

    assert context.schedule_b.taxable_interest == 126      # 125.50 rounds to 126