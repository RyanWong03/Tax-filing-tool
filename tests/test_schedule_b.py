import tax_context
import federal.forms.schedule_b as schedule_b
import federal.tax_years.y_2025 as y_2025

def test_aggregate_zero_interest_entries():
    context = tax_context.tax_context(2025)
    context.constants = y_2025
    schedule_b.aggregate_schedule_b(context)
    assert context.schedule_b.taxable_interest == 0

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
        "payer": "Capital One", "amount": 1000.98, "bond_interest": 300,
        "early_withdrawal_penalty": 0, "fed_tax_withheld": 0, "tax_exempt_interest": 0
    })
    context.schedule_b.interest_entries.append({
        "payer": "JP Morgan Chase", "amount": 500.19, "bond_interest": 57.15,
        "early_withdrawal_penalty": 0, "fed_tax_withheld": 0, "tax_exempt_interest": 0
    })

    schedule_b.aggregate_schedule_b(context)

    assert context.schedule_b.taxable_interest == 1858
    assert context.schedule_b.interest_on_savings_bonds == 357

def test_schedule_b_interest_over_threshold():
    context = tax_context.tax_context(2025)
    context.constants = y_2025
    context.schedule_b.interest_entries.append({
        "payer": "Bank of America",
        "amount": 5234.99,
        "bond_interest": 0,
        "early_withdrawal_penalty": 0,
        "fed_tax_withheld": 0,
        "tax_exempt_interest": 0
    })
    
    schedule_b.aggregate_schedule_b(context)
    assert schedule_b.is_filing_schedule_b(context) == True

def test_schedule_b_required_for_any_bond_interest():
    context = tax_context.tax_context(2025)
    context.constants = y_2025
    context.schedule_b.interest_entries.append({
        "payer": "Chase Bank",
        "amount": 50,
        "bond_interest": 50,
        "early_withdrawal_penalty": 0,
        "fed_tax_withheld": 0,
        "tax_exempt_interest": 0
    })
    
    schedule_b.aggregate_schedule_b(context)
    assert schedule_b.is_filing_schedule_b(context) == True

def test_aggregate_zero_dividend_entries():
    context = tax_context.tax_context(2025)
    schedule_b.aggregate_schedule_b(context)
    assert context.schedule_b.ordinary_dividends == 0
    assert context.schedule_b.qualified_dividends == 0

def test_aggregate_single_dividend_entry():
    context = tax_context.tax_context(2025)
    context.schedule_b.dividend_entries.append({
        "payer": "Fidelity",
        "ordinary_dividends": 400,
        "qualified_dividends": 250,
        "cap_gain_distributions": 0,
        "unrecaptured_sec_1250_gain": 0,
        "fed_tax_withheld": 0,
        "section_199a_dividends": 0,
    })

    schedule_b.aggregate_schedule_b(context)
    assert context.schedule_b.ordinary_dividends == 400
    assert context.schedule_b.qualified_dividends == 250

def test_aggregate_multiple_dividend_entries():
    context = tax_context.tax_context(2025)
    context.schedule_b.dividend_entries.append({
        "payer": "Fidelity", "ordinary_dividends": 1000, "qualified_dividends": 0,
        "cap_gain_distributions": 0, "unrecaptured_sec_1250_gain": 0, "fed_tax_withheld": 0,
        "section_199a_dividends": 0
    })
    context.schedule_b.dividend_entries.append({
        "payer": "Vanguard", "ordinary_dividends": 3000, "qualified_dividends": 2500,
        "cap_gain_distributions": 0, "unrecaptured_sec_1250_gain": 0, "fed_tax_withheld": 0,
        "section_199a_dividends": 0
    })

    schedule_b.aggregate_schedule_b(context)
    assert context.schedule_b.ordinary_dividends == 4000
    assert context.schedule_b.qualified_dividends == 2500

def test_schedule_b_dividend_over_threshold():
    context = tax_context.tax_context(2025)
    context.constants = y_2025
    context.schedule_b.dividend_entries.append({
        "payer": "Fidelity",
        "ordinary_dividends": 25000.73,
        "qualified_dividends": 18424.30,
        "cap_gain_distributions": 0,
        "unrecaptured_sec_1250_gain": 0,
        "fed_tax_withheld": 0,
        "section_199a_dividends": 0,
    })

    schedule_b.aggregate_schedule_b(context)
    assert schedule_b.is_filing_schedule_b(context) == True

def test_schedule_b_not_required_when_all_thresholds_unmet():
    context = tax_context.tax_context(2025)
    context.constants = y_2025
    context.schedule_b.interest_entries.append({
        "payer": "Chase Bank", "amount": 500, "bond_interest": 0,
        "early_withdrawal_penalty": 0, "fed_tax_withheld": 0, "tax_exempt_interest": 0
    })

    context.schedule_b.dividend_entries.append({
        "payer": "Fidelity", "ordinary_dividends": 300, "qualified_dividends": 200,
        "cap_gain_distributions": 0, "unrecaptured_sec_1250_gain": 0,
        "fed_tax_withheld": 0, "section_199a_dividends": 0
    })

    schedule_b.aggregate_schedule_b(context)
    assert schedule_b.is_filing_schedule_b(context) == False

def test_aggregate_all_schedule_b_fields():
    context = tax_context.tax_context(2025)
    context.schedule_b.interest_entries.append({
        "payer": "Chase Bank",
        "amount": 1000,
        "bond_interest": 200,
        "early_withdrawal_penalty": 50,
        "fed_tax_withheld": 75,
        "tax_exempt_interest": 25
    })
    context.schedule_b.dividend_entries.append({
        "payer": "Fidelity",
        "ordinary_dividends": 800,
        "qualified_dividends": 600,
        "cap_gain_distributions": 150,
        "unrecaptured_sec_1250_gain": 40,
        "fed_tax_withheld": 30,
        "section_199a_dividends": 20
    })

    schedule_b.aggregate_schedule_b(context)

    assert context.schedule_b.taxable_interest == 1200 # 1000 + 200
    assert context.schedule_b.interest_on_savings_bonds == 200
    assert context.schedule_b.early_withdrawal_penalty == 50
    assert context.schedule_b.federal_tax_withheld_interest == 75
    assert context.schedule_b.tax_exempt_interest == 25

    assert context.schedule_b.ordinary_dividends == 800
    assert context.schedule_b.qualified_dividends == 600
    assert context.schedule_b.cap_gain_distributions == 150
    assert context.schedule_b.unrecaptured_sec_1250_gain == 40
    assert context.schedule_b.federal_tax_withheld_dividends == 30
    assert context.schedule_b.section_199a_dividends == 20