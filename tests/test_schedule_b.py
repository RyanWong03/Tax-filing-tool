import tax_context
import federal.forms.schedule_b as schedule_b

def test_aggregate_single_interest_entry():
    context = tax_context.tax_context(2025)
    context.schedule_b.interest_entries.append({
        "payer": "Capital One",
        "amount": 4000,
        "bond_interest": 0,
        "early_withdrawal_penalty": 0,
        "fed_tax_withheld": 0,
        "tax_exempt_interest": 0
    })

    schedule_b.aggregate_schedule_b(context)

    assert context.schedule_b.taxable_interest == 4000
    assert context.schedule_b.interest_on_savings_bonds == 0

def test_aggregate_multiple_interest_entries():
    context = tax_context.tax_context(2025)
    context.schedule_b.interest_entries.append({
        "payer": "Capital One", "amount": 1000, "bond_interest": 0,
        "early_withdrawal_penalty": 0, "fed_tax_withheld": 0, "tax_exempt_interest": 0
    })
    context.schedule_b.interest_entries.append({
        "payer": "JP Morgan Chase", "amount": 500, "bond_interest": 0,
        "early_withdrawal_penalty": 0, "fed_tax_withheld": 0, "tax_exempt_interest": 0
    })

    schedule_b.aggregate_schedule_b(context)

    assert context.schedule_b.taxable_interest == 1500

def test_aggregate_single_dividend_entry():
    context = tax_context.tax_context(2025)
    context.schedule_b.dividend_entries.append({
        "payer": "Capital One",
        "ordinary_dividends": 400,
        "qualified_dividends": 250,
        "cap_gain_distributions": 0,
        "unrecpatured_sec_1250_gain": 0,
        "fed_tax_withheld": 0,
        "section_199a_dividends": 0,
    })

    schedule_b.aggregate_schedule_b(context)
    assert context.schedule_b.ordinary_dividends == 4000

def test_aggregate_multiple_dividend_entries():
    context = tax_context.tax_context(2025)
    context.schedule_b.divide_entries.append({
        "payer": "Capital One", "amount": 1000.0, "bond_interest": 0.0,
        "early_withdrawal_penalty": 0, "fed_tax_withheld": 0, "tax_exempt_interest": 0
    })
    context.schedule_b.dividend_entries.append({
        "payer": "JP Morgan Chase", "amount": 500.0, "bond_interest": 0.0,
        "early_withdrawal_penalty": 0, "fed_tax_withheld": 0, "tax_exempt_interest": 0
    })

    schedule_b.aggregate_schedule_b(context)

   # assert context.schedule_b.taxable_interest == 1500