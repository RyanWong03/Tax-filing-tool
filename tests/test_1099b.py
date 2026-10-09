import tax_context
import federal.forms.form_8949 as form_8949
from conftest import YEAR

def type_answers(monkeypatch, answers):
    """Makes input() return these answers one at a time, in order."""
    remaining = iter(answers)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(remaining))

def sale(proceeds, cost_basis, accrued_discount="0", wash_sale="0", fed="0", state="0",
         payer="Fidelity", description="5 shares of AAPL", acquired="01/01/2025", sold="06/01/2025"):
    """The ten answers for one sale, in the order the program asks for them."""
    return [payer, description, acquired, sold, proceeds, cost_basis, accrued_discount, wash_sale, fed, state]

# ---------- Short-term (codes A, B, C) ----------

def test_short_term_single_sale_with_gain(monkeypatch):
    context = tax_context.tax_context(YEAR)
    type_answers(monkeypatch, ["A"] + sale("3000", "2000") + ["no"])

    form_8949.collect_1099_b_short_term(context)

    assert context.form_8949.short_term_entries["A"] == [{
        "description": "5 shares of AAPL",
        "date_acquired": "01/01/2025",
        "date_sold": "06/01/2025",
        "proceeds": 3000,
        "cost_basis": 2000,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": 1000,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0,
    }]
    assert context.schedule_b.interest_entries == []

def test_short_term_sale_with_loss(monkeypatch):
    context = tax_context.tax_context(YEAR)
    type_answers(monkeypatch, ["A"] + sale("2000", "5000") + ["no"])

    form_8949.collect_1099_b_short_term(context)

    assert context.form_8949.short_term_entries["A"][0]["gain"] == -3000

def test_short_term_wash_sale_adds_back_the_disallowed_loss(monkeypatch):
    # Sold for 3000, bought for 4000 (loss of 1000), but 150 of the loss is a wash sale and not allowed.
    # Gain = 3000 - 4000 + 150 = -850. The 150 is the adjustment, with code W.
    context = tax_context.tax_context(YEAR)
    type_answers(monkeypatch, ["A"] + sale("3000", "4000", wash_sale="150") + ["no"])

    form_8949.collect_1099_b_short_term(context)

    entry = context.form_8949.short_term_entries["A"][0]
    assert entry["gain"] == -850
    assert entry["adjustments"] == 150
    assert entry["adjustment_code"] == "W"

def test_short_term_gain_is_rounded_to_cents(monkeypatch):
    # 3394.24 - 5003.39 is -1609.1499999999996 in floating point. It should be stored as -1609.15.
    context = tax_context.tax_context(YEAR)
    type_answers(monkeypatch, ["A"] + sale("3394.24", "5003.39") + ["no"])

    form_8949.collect_1099_b_short_term(context)

    assert context.form_8949.short_term_entries["A"][0]["gain"] == -1609.15

def test_short_term_tax_withheld_is_stored(monkeypatch):
    context = tax_context.tax_context(YEAR)
    type_answers(monkeypatch, ["A"] + sale("3000", "2000", fed="120.50", state="45") + ["no"])

    form_8949.collect_1099_b_short_term(context)

    entry = context.form_8949.short_term_entries["A"][0]
    assert entry["federal_tax_withheld"] == 120.50
    assert entry["state_tax_withheld"] == 45

def test_short_term_two_sales_same_code(monkeypatch):
    context = tax_context.tax_context(YEAR)
    type_answers(monkeypatch, ["A"] + sale("3000", "2000") + ["yes"] + sale("1000", "1500") + ["no"])

    form_8949.collect_1099_b_short_term(context)

    entries = context.form_8949.short_term_entries["A"]
    assert [e["gain"] for e in entries] == [1000, -500]

def test_short_term_two_codes_go_to_the_right_buckets(monkeypatch):
    context = tax_context.tax_context(YEAR)
    type_answers(monkeypatch, ["A B"] + sale("3000", "2000") + ["no"] + sale("1000", "400") + ["no"])

    form_8949.collect_1099_b_short_term(context)

    assert [e["gain"] for e in context.form_8949.short_term_entries["A"]] == [1000]
    assert [e["gain"] for e in context.form_8949.short_term_entries["B"]] == [600]
    assert context.form_8949.short_term_entries["C"] == []

def test_short_term_no_transactions(monkeypatch):
    # Typing X means none. Nothing else is asked, so there are no further answers to give.
    context = tax_context.tax_context(YEAR)
    type_answers(monkeypatch, ["X"])

    form_8949.collect_1099_b_short_term(context)

    assert context.form_8949.short_term_entries == {"A": [], "B": [], "C": []}

def test_short_term_lowercase_code_is_accepted(monkeypatch):
    context = tax_context.tax_context(YEAR)
    type_answers(monkeypatch, ["a"] + sale("3000", "2000") + ["no"])

    form_8949.collect_1099_b_short_term(context)

    assert len(context.form_8949.short_term_entries["A"]) == 1

def test_short_term_bad_number_asks_the_sale_again(monkeypatch):
    # "abc" for proceeds restarts the sale. The program asks for everything again, and only one entry is stored.
    context = tax_context.tax_context(YEAR)
    bad_sale = ["Fidelity", "5 shares of AAPL", "01/01/2025", "06/01/2025", "abc"]
    type_answers(monkeypatch, ["A"] + bad_sale + sale("3000", "2000") + ["no"])

    form_8949.collect_1099_b_short_term(context)

    entries = context.form_8949.short_term_entries["A"]
    assert len(entries) == 1
    assert entries[0]["gain"] == 1000

def test_short_term_invalid_yes_no_asks_again(monkeypatch):
    context = tax_context.tax_context(YEAR)
    type_answers(monkeypatch, ["A"] + sale("3000", "2000") + ["maybe", "no"])

    form_8949.collect_1099_b_short_term(context)

    assert len(context.form_8949.short_term_entries["A"]) == 1

def test_short_term_accrued_market_discount_goes_to_schedule_b(monkeypatch):
    # Current behavior: accrued market discount is added to Schedule B as interest.
    context = tax_context.tax_context(YEAR)
    type_answers(monkeypatch, ["A"] + sale("3000", "2000", accrued_discount="125.50", payer="Fidelity") + ["no"])

    form_8949.collect_1099_b_short_term(context)

    assert context.schedule_b.interest_entries == [{
        "payer": "Fidelity",
        "amount": 125.50,
        "bond_interest": 0,
        "early_withdrawal_penalty": 0,
        "fed_tax_withheld": 0,
        "tax_exempt_interest": 0,
    }]
    assert len(context.form_8949.short_term_entries["A"]) == 1

# ---------- Long-term (codes D, E, F) ----------

def test_long_term_single_sale_with_gain(monkeypatch):
    context = tax_context.tax_context(YEAR)
    type_answers(monkeypatch, ["D"] + sale("5050", "2033", acquired="03/15/2023") + ["no"])

    form_8949.collect_1099_b_long_term(context)

    assert context.form_8949.long_term_entries["D"] == [{
        "description": "5 shares of AAPL",
        "date_acquired": "03/15/2023",
        "date_sold": "06/01/2025",
        "proceeds": 5050,
        "cost_basis": 2033,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": 3017,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0,
    }]
    assert context.form_8949.short_term_entries == {"A": [], "B": [], "C": []}

def test_long_term_wash_sale(monkeypatch):
    context = tax_context.tax_context(YEAR)
    type_answers(monkeypatch, ["E"] + sale("3000", "4000", wash_sale="150") + ["no"])

    form_8949.collect_1099_b_long_term(context)

    entry = context.form_8949.long_term_entries["E"][0]
    assert entry["gain"] == -850
    assert entry["adjustments"] == 150
    assert entry["adjustment_code"] == "W"

def test_long_term_three_codes_go_to_the_right_buckets(monkeypatch):
    context = tax_context.tax_context(YEAR)
    type_answers(monkeypatch,
        ["D E F"] + sale("3000", "2000") + ["no"] + sale("1000", "400") + ["no"] + sale("500", "800") + ["no"])

    form_8949.collect_1099_b_long_term(context)

    assert [e["gain"] for e in context.form_8949.long_term_entries["D"]] == [1000]
    assert [e["gain"] for e in context.form_8949.long_term_entries["E"]] == [600]
    assert [e["gain"] for e in context.form_8949.long_term_entries["F"]] == [-300]

def test_long_term_no_transactions(monkeypatch):
    context = tax_context.tax_context(YEAR)
    type_answers(monkeypatch, ["X"])

    form_8949.collect_1099_b_long_term(context)

    assert context.form_8949.long_term_entries == {"D": [], "E": [], "F": []}

def test_long_term_accrued_market_discount_goes_to_schedule_b(monkeypatch):
    context = tax_context.tax_context(YEAR)
    type_answers(monkeypatch, ["D"] + sale("3000", "2000", accrued_discount="80") + ["no"])

    form_8949.collect_1099_b_long_term(context)

    assert [e["amount"] for e in context.schedule_b.interest_entries] == [80]