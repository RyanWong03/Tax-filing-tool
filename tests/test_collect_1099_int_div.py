import tax_context
import federal.forms.schedule_b as schedule_b
from conftest import YEAR

def type_answers(monkeypatch, answers):
    """Makes input() return these answers one at a time, in order."""
    remaining = iter(answers)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(remaining))

def int_form(payer="Chase", box1="1000", box2="0", box3="0", box4="0", box8="0"):
    """The six answers for one 1099-INT, in the order the program asks."""
    return [payer, box1, box2, box3, box4, box8]

def div_form(payer="Fidelity", box1a="400", box1b="250", box2a="0", box2b="0", box4="0", box5="0"):
    """The seven answers for one 1099-DIV, in the order the program asks."""
    return [payer, box1a, box1b, box2a, box2b, box4, box5]

# ---------- 1099-INT ----------

def test_int_no_forms(monkeypatch):
    context = tax_context.tax_context(YEAR)
    type_answers(monkeypatch, ["n"])

    schedule_b.collect_1099_int(context)

    assert context.schedule_b.interest_entries == []

def test_int_single_form(monkeypatch):
    context = tax_context.tax_context(YEAR)
    type_answers(monkeypatch, [""] + int_form("Chase", "1000.50", "25", "300", "50", "10") + ["no"])

    schedule_b.collect_1099_int(context)

    assert context.schedule_b.interest_entries == [{
        "payer": "Chase",
        "amount": 1000.50,
        "bond_interest": 300,
        "early_withdrawal_penalty": 25,
        "fed_tax_withheld": 50,
        "tax_exempt_interest": 10,
    }]

def test_int_whole_dollar_boxes_are_rounded_and_interest_is_kept_exact(monkeypatch):
    # Boxes 2, 4 and 8 are rounded to whole dollars when typed in. Boxes 1 and 3 keep their cents
    # (they are added up and rounded once, later, on Schedule B).
    context = tax_context.tax_context(YEAR)
    type_answers(monkeypatch, [""] + int_form("Chase", "1000.55", "25.50", "300.25", "50.49", "10.5") + ["no"])

    schedule_b.collect_1099_int(context)

    entry = context.schedule_b.interest_entries[0]
    assert entry["amount"] == 1000.55
    assert entry["bond_interest"] == 300.25
    assert entry["early_withdrawal_penalty"] == 26
    assert entry["fed_tax_withheld"] == 50
    assert entry["tax_exempt_interest"] == 11

def test_int_payer_name_is_trimmed(monkeypatch):
    context = tax_context.tax_context(YEAR)
    type_answers(monkeypatch, [""] + int_form("  Chase  ") + ["no"])

    schedule_b.collect_1099_int(context)

    assert context.schedule_b.interest_entries[0]["payer"] == "Chase"

def test_int_two_forms(monkeypatch):
    context = tax_context.tax_context(YEAR)
    type_answers(monkeypatch, [""] + int_form("Chase", "1000") + ["yes"] + int_form("Ally", "500") + ["no"])

    schedule_b.collect_1099_int(context)

    entries = context.schedule_b.interest_entries
    assert [(e["payer"], e["amount"]) for e in entries] == [("Chase", 1000), ("Ally", 500)]

def test_int_bad_number_asks_the_form_again(monkeypatch):
    context = tax_context.tax_context(YEAR)
    type_answers(monkeypatch, [""] + ["Chase", "abc"] + int_form("Chase", "1000") + ["no"])

    schedule_b.collect_1099_int(context)

    assert len(context.schedule_b.interest_entries) == 1
    assert context.schedule_b.interest_entries[0]["amount"] == 1000

def test_int_invalid_yes_no_asks_again(monkeypatch):
    context = tax_context.tax_context(YEAR)
    type_answers(monkeypatch, [""] + int_form() + ["maybe", "no"])

    schedule_b.collect_1099_int(context)

    assert len(context.schedule_b.interest_entries) == 1

# ---------- 1099-DIV ----------

def test_div_no_forms(monkeypatch):
    context = tax_context.tax_context(YEAR)
    type_answers(monkeypatch, ["n"])

    schedule_b.collect_1099_div(context)

    assert context.schedule_b.dividend_entries == []

def test_div_single_form(monkeypatch):
    context = tax_context.tax_context(YEAR)
    type_answers(monkeypatch, [""] + div_form("Fidelity", "400", "250", "100", "50", "10", "20") + ["no"])

    schedule_b.collect_1099_div(context)

    assert context.schedule_b.dividend_entries == [{
        "payer": "Fidelity",
        "ordinary_dividends": 400,
        "qualified_dividends": 250,
        "cap_gain_distributions": 100,
        "unrecaptured_sec_1250_gain": 50,
        "fed_tax_withheld": 10,
        "section_199a_dividends": 20,
    }]

def test_div_every_box_is_rounded_to_whole_dollars(monkeypatch):
    context = tax_context.tax_context(YEAR)
    type_answers(monkeypatch, [""] + div_form("Fidelity", "400.50", "250.49", "100.5", "50.4", "10.6", "20.5") + ["no"])

    schedule_b.collect_1099_div(context)

    entry = context.schedule_b.dividend_entries[0]
    assert entry["ordinary_dividends"] == 401
    assert entry["qualified_dividends"] == 250
    assert entry["cap_gain_distributions"] == 101
    assert entry["unrecaptured_sec_1250_gain"] == 50
    assert entry["fed_tax_withheld"] == 11
    assert entry["section_199a_dividends"] == 21

def test_div_two_forms(monkeypatch):
    context = tax_context.tax_context(YEAR)
    type_answers(monkeypatch, [""] + div_form("Fidelity", "400") + ["yes"] + div_form("Vanguard", "3000") + ["no"])

    schedule_b.collect_1099_div(context)

    entries = context.schedule_b.dividend_entries
    assert [(e["payer"], e["ordinary_dividends"]) for e in entries] == [("Fidelity", 400), ("Vanguard", 3000)]

def test_div_bad_number_asks_the_form_again(monkeypatch):
    context = tax_context.tax_context(YEAR)
    type_answers(monkeypatch, [""] + ["Fidelity", "abc"] + div_form("Fidelity", "400") + ["no"])

    schedule_b.collect_1099_div(context)

    assert len(context.schedule_b.dividend_entries) == 1
    assert context.schedule_b.dividend_entries[0]["ordinary_dividends"] == 400

def test_div_invalid_yes_no_asks_again(monkeypatch):
    context = tax_context.tax_context(YEAR)
    type_answers(monkeypatch, [""] + div_form() + ["maybe", "no"])

    schedule_b.collect_1099_div(context)

    assert len(context.schedule_b.dividend_entries) == 1