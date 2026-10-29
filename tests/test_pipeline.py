import tax_context
import federal.forms.schedule_b as schedule_b
import federal.forms.form_8949 as form_8949
import federal.forms.schedule_d as schedule_d
from conftest import YEAR
import main
import library

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

    assert context.schedule_d.line_17 is True
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

# ======================= Whole program: main.main() from typed answers =======================
def run_main(monkeypatch, answers):
    library.save_tax_return(YEAR - 1, ZERO_PRIOR)
    type_answers(monkeypatch, answers)
    main.main()


def saved_return():
    return library.load_prior_year_return(YEAR + 1)    # reads tax_return_<YEAR>.json


def test_main_wages_only_refund_all_sent_to_taxpayer(monkeypatch):
    # 60000 wages, 6000 withheld. Tax 5075, refund 925. All of it sent to the taxpayer.
    run_main(monkeypatch, [
        "2025", "single",
        "60000", "6000", "no",     # W-2
        "n", "n",                  # no 1099-INT, no 1099-DIV
        "X", "X",                  # no short-term, no long-term sales
        "925", "0",                # refund sent to taxpayer, applied to next year's estimated tax
    ])

    saved = saved_return()
    assert saved["form_1040_line_15"] == 44250
    assert saved["schedule_d_line_7"] == 0
    assert saved["schedule_d_line_15"] == 0
    assert saved["schedule_d_line_16"] == 0
    assert saved["schedule_d_line_21"] == 0


def test_main_refund_split_after_a_wrong_first_attempt(monkeypatch, capsys):
    # First pair adds to 1025, not 925, so the program asks again. Second pair is 625 + 300 = 925.
    run_main(monkeypatch, [
        "2025", "single",
        "60000", "6000", "no",
        "n", "n", "X", "X",
        "925", "100",
        "625", "300",
    ])

    assert "must add up to $925" in capsys.readouterr().out


def test_main_amount_owed_asks_no_refund_questions(monkeypatch):
    # 60000 wages, 3000 withheld. Tax 5075, owes 2075. There are no refund prompts, so no extra answers are given.
    # If the program asked anything more, type_answers would run out and raise StopIteration.
    run_main(monkeypatch, [
        "2025", "single",
        "60000", "3000", "no",
        "n", "n", "X", "X",
    ])

    assert saved_return()["form_1040_line_15"] == 44250


def test_main_with_interest_dividends_and_a_sale_reaches_the_form(monkeypatch):
    # Wages 60000 (5000 withheld), interest 1000 (20 withheld), dividends 500 of which 300 qualified (10 withheld),
    # one long-term sale with a 5000 gain.
    # Income 66500, taxable 50750. Qualified Dividends worksheet gives tax 5579 (the tax table would be 6085).
    # Paid in: 5000 + 20 + 10 = 5030. Owes 549 -> no refund questions.
    run_main(monkeypatch, [
        "2025", "single",
        "60000", "5000", "no",
        "",  "Chase", "1000", "0", "0", "20", "0", "no",                          # 1099-INT
        "",  "Fidelity", "500", "300", "0", "0", "10", "0", "no",                 # 1099-DIV
        "X",                                                                      # no short-term
        "D", "Fidelity", "MSFT", "01/01/2023", "06/01/2025", "8000", "3000", "0", "0", "0", "0", "no",
    ])

    saved = saved_return()
    assert saved["form_1040_line_15"] == 50750
    assert saved["schedule_d_line_7"] == 0
    assert saved["schedule_d_line_15"] == 5000
    assert saved["schedule_d_line_16"] == 5000
    assert saved["schedule_d_line_21"] == 0


def test_main_unsupported_year_asks_again(monkeypatch):
    run_main(monkeypatch, [
        "1999", "2025", "single",
        "60000", "3000", "no",
        "n", "n", "X", "X",
    ])

    assert saved_return()["form_1040_line_15"] == 44250


def test_main_saves_negative_taxable_income_for_next_years_carryover_worksheet(monkeypatch):
    # 10000 wages is 5750 less than the standard deduction. The form shows 0 on line 15, but next year's carryover
    # worksheet needs the real figure (-5750). schedule_d.py checks form_1040_line_15 < 0, which can never happen
    # if the floored line 15 is what gets saved. Withheld 500 -> refund 500, all sent to the taxpayer.
    run_main(monkeypatch, [
        "2025", "single",
        "10000", "500", "no",
        "n", "n", "X", "X",
        "500", "0",
    ])

    assert saved_return()["form_1040_line_15"] == -5750

def test_main_with_interest_and_dividends_over_1500_each(monkeypatch):
    # Interest 2000 and ordinary dividends 1800 are both over 1500, so Schedule B is filed along with the 1040.
    # Income: 60000 + 2000 + 1800 = 63800. Taxable income: 63800 - 15750 = 48050. Nothing withheld, so tax is owed
    # and there are no refund questions.
    run_main(monkeypatch, [
        "2025", "single",
        "60000", "0", "no",                                        # W-2
        "", "Chase", "2000", "0", "0", "0", "0", "yes",            # 1099-INT: box 1 = 2000
        "Capital One", "4452.32", "0", "0", "0", "0", "no",        # 1099-INT: box 1 = 4452.32
        "", "Fidelity", "1800", "0", "0", "0", "0", "0", "yes",    # 1099-DIV: box 1a = 1800
        "Vanguard", "15000", "0", "0", "0", "0", "0", "no",        # 1099-DIV: box 1a = 15000
        "X", "X",                                                  # no sales
    ])

    saved = saved_return()
    assert saved["form_1040_line_15"] == 67502
    assert saved["schedule_d_line_16"] == 0