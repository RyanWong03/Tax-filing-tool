import tax_context
import federal.forms.schedule_d as schedule_d
import json
from conftest import YEAR, TAX_YEAR
import pytest

def read_saved(tmp_path, name):
    with open(tmp_path / f"{name}_{YEAR}.json") as f:
        return json.load(f)

def make_prior_year(line_15, line_7, sd_line_15, line_16, line_21):
    return {
        "form_1040_line_15": line_15,
        "schedule_d_line_7": line_7,
        "schedule_d_line_15": sd_line_15,
        "schedule_d_line_16": line_16,
        "schedule_d_line_21": line_21
    }

def test_aggregate_zero_entries():
    context = tax_context.tax_context(YEAR)
    prior_year_return = make_prior_year(0, 0, 0, 0, 0)

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    #Short term
    assert context.schedule_d.code_a_proceeds_total == 0
    assert context.schedule_d.code_a_cost_basis_total == 0
    assert context.schedule_d.code_a_adjustments_total == 0
    assert context.schedule_d.code_a_gain_loss_total == 0

    assert context.schedule_d.code_b_proceeds_total == 0
    assert context.schedule_d.code_b_cost_basis_total == 0
    assert context.schedule_d.code_b_adjustments_total == 0
    assert context.schedule_d.code_b_gain_loss_total == 0

    assert context.schedule_d.code_c_proceeds_total == 0
    assert context.schedule_d.code_c_cost_basis_total == 0
    assert context.schedule_d.code_c_adjustments_total == 0
    assert context.schedule_d.code_c_gain_loss_total == 0

    #Long term
    assert context.schedule_d.code_d_proceeds_total == 0
    assert context.schedule_d.code_d_cost_basis_total == 0
    assert context.schedule_d.code_d_adjustments_total == 0
    assert context.schedule_d.code_d_gain_loss_total == 0

    assert context.schedule_d.code_e_proceeds_total == 0
    assert context.schedule_d.code_e_cost_basis_total == 0
    assert context.schedule_d.code_e_adjustments_total == 0
    assert context.schedule_d.code_e_gain_loss_total == 0

    assert context.schedule_d.code_f_proceeds_total == 0
    assert context.schedule_d.code_f_cost_basis_total == 0
    assert context.schedule_d.code_f_adjustments_total == 0
    assert context.schedule_d.code_f_gain_loss_total == 0

    #Other Schedule D fields that should also default to zero
    assert context.schedule_d.net_short_term_gain_loss == 0
    assert context.schedule_d.net_long_term_gain_loss == 0
    assert context.schedule_d.capital_gain_distributions == 0
    assert context.schedule_d.short_term_capital_loss_carryover == 0
    assert context.schedule_d.long_term_capital_loss_carryover == 0

    #Part 3 - with zero activity, line_16 is 0, so none of the gain/loss branches should have run
    assert context.schedule_d.line_16 == 0
    assert context.schedule_d.line_17 is None
    assert context.schedule_d.rate_gain_28 == 0
    assert context.schedule_d.unrecaptured_section_1250_gain == 0
    assert context.schedule_d.line_20 is None
    assert context.schedule_d.line_21 == 0
    # line_22 depends on form_1040.line_3a, which also defaults to 0, so line_22 stays None too
    assert context.schedule_d.line_22 is False

def test_aggregate_single_code_a_entry():
    context = tax_context.tax_context(YEAR)
    context.form_8949.short_term_entries["A"].append({
        "description": "5 shares of AAPL",
        "date_acquired": "01/01/2025",
        "date_sold": "06/01/2025",
        "proceeds": 3000,
        "cost_basis": 2000,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": 1000,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })

    prior_year_return = make_prior_year(0, 0, 0, 0, 0)

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.code_a_proceeds_total == 3000
    assert context.schedule_d.code_a_cost_basis_total == 2000
    assert context.schedule_d.code_a_adjustments_total == 0
    assert context.schedule_d.code_a_gain_loss_total == 1000

def test_aggregate_multiple_code_a_entries():
    context = tax_context.tax_context(YEAR)
    context.form_8949.short_term_entries["A"].append({
        "description": "500 shares of TSLA",
        "date_acquired": "05/23/2025",
        "date_sold": "12/31/2025",
        "proceeds": 25382.45,
        "cost_basis": 20452,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": 4930.45,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })
    context.form_8949.short_term_entries["A"].append({
        "description": "138.13 shares of INTC",
        "date_acquired": "03/12/2025",
        "date_sold": "09/12/2025",
        "proceeds": 6000,
        "cost_basis": 4000,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": 2000,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })

    prior_year_return = make_prior_year(0, 0, 0, 0, 0)

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.code_a_proceeds_total == 31382
    assert context.schedule_d.code_a_cost_basis_total == 24452
    assert context.schedule_d.code_a_adjustments_total == 0
    assert context.schedule_d.code_a_gain_loss_total == 6930

def test_aggregate_single_code_b_entry():
    context = tax_context.tax_context(YEAR)
    context.form_8949.short_term_entries["B"].append({
        "description": "5 shares of AAPL",
        "date_acquired": "01/01/2025",
        "date_sold": "06/01/2025",
        "proceeds": 3000,
        "cost_basis": 2000,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": 1000,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })

    prior_year_return = make_prior_year(0, 0, 0, 0, 0)

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.code_b_proceeds_total == 3000
    assert context.schedule_d.code_b_cost_basis_total == 2000
    assert context.schedule_d.code_b_adjustments_total == 0
    assert context.schedule_d.code_b_gain_loss_total == 1000

def test_aggregate_multiple_code_b_entries():
    context = tax_context.tax_context(YEAR)
    context.form_8949.short_term_entries["B"].append({
        "description": "500 shares of TSLA",
        "date_acquired": "05/23/2025",
        "date_sold": "12/31/2025",
        "proceeds": 25382.45,
        "cost_basis": 20452,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": 4930.45,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })
    context.form_8949.short_term_entries["B"].append({
        "description": "138.13 shares of INTC",
        "date_acquired": "03/12/2025",
        "date_sold": "09/12/2025",
        "proceeds": 6000,
        "cost_basis": 4000,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": 2000,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })

    prior_year_return = make_prior_year(0, 0, 0, 0, 0)

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.code_b_proceeds_total == 31382
    assert context.schedule_d.code_b_cost_basis_total == 24452
    assert context.schedule_d.code_b_adjustments_total == 0
    assert context.schedule_d.code_b_gain_loss_total == 6930

def test_aggregate_single_code_c_entry():
    context = tax_context.tax_context(YEAR)
    context.form_8949.short_term_entries["C"].append({
        "description": "5 shares of AAPL",
        "date_acquired": "01/01/2025",
        "date_sold": "06/01/2025",
        "proceeds": 3000,
        "cost_basis": 2000,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": 1000,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })

    prior_year_return = make_prior_year(0, 0, 0, 0, 0)

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.code_c_proceeds_total == 3000
    assert context.schedule_d.code_c_cost_basis_total == 2000
    assert context.schedule_d.code_c_adjustments_total == 0
    assert context.schedule_d.code_c_gain_loss_total == 1000

def test_aggregate_multiple_code_c_entries():
    context = tax_context.tax_context(YEAR)
    context.form_8949.short_term_entries["C"].append({
        "description": "500 shares of TSLA",
        "date_acquired": "05/23/2025",
        "date_sold": "12/31/2025",
        "proceeds": 25382.45,
        "cost_basis": 20452,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": 4930.45,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })
    context.form_8949.short_term_entries["C"].append({
        "description": "138.13 shares of INTC",
        "date_acquired": "03/12/2025",
        "date_sold": "09/12/2025",
        "proceeds": 6000,
        "cost_basis": 4000,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": 2000,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })

    prior_year_return = make_prior_year(0, 0, 0, 0, 0)

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.code_c_proceeds_total == 31382
    assert context.schedule_d.code_c_cost_basis_total == 24452
    assert context.schedule_d.code_c_adjustments_total == 0
    assert context.schedule_d.code_c_gain_loss_total == 6930

def test_aggregate_single_code_d_entry():
    context = tax_context.tax_context(YEAR)
    context.form_8949.long_term_entries["D"].append({
        "description": "55 shares of AMD",
        "date_acquired": "03/15/2023",
        "date_sold": "06/01/2025",
        "proceeds": 5050,
        "cost_basis": 2033,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": 3017,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })

    prior_year_return = make_prior_year(0, 0, 0, 0, 0)

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.code_d_proceeds_total == 5050
    assert context.schedule_d.code_d_cost_basis_total == 2033
    assert context.schedule_d.code_d_adjustments_total == 0
    assert context.schedule_d.code_d_gain_loss_total == 3017

def test_aggregate_multiple_code_d_entries():
    context = tax_context.tax_context(YEAR)
    context.form_8949.long_term_entries["D"].append({
        "description": "500 shares of TSLA",
        "date_acquired": "05/23/2020",
        "date_sold": "12/31/2025",
        "proceeds": 25382.45,
        "cost_basis": 20452,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": 4930.45,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })
    context.form_8949.long_term_entries["D"].append({
        "description": "138.13 shares of INTC",
        "date_acquired": "03/12/2018",
        "date_sold": "09/12/2025",
        "proceeds": 60000,
        "cost_basis": 40000,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": 20000,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })

    prior_year_return = make_prior_year(0, 0, 0, 0, 0)

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.code_d_proceeds_total == 85382
    assert context.schedule_d.code_d_cost_basis_total == 60452
    assert context.schedule_d.code_d_adjustments_total == 0
    assert context.schedule_d.code_d_gain_loss_total == 24930

def test_aggregate_single_code_e_entry():
    context = tax_context.tax_context(YEAR)
    context.form_8949.long_term_entries["E"].append({
        "description": "55 shares of AMD",
        "date_acquired": "03/15/2023",
        "date_sold": "06/01/2025",
        "proceeds": 5050,
        "cost_basis": 2033,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": 3017,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })

    prior_year_return = make_prior_year(0, 0, 0, 0, 0)

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.code_e_proceeds_total == 5050
    assert context.schedule_d.code_e_cost_basis_total == 2033
    assert context.schedule_d.code_e_adjustments_total == 0
    assert context.schedule_d.code_e_gain_loss_total == 3017

def test_aggregate_multiple_code_e_entries():
    context = tax_context.tax_context(YEAR)
    context.form_8949.long_term_entries["E"].append({
        "description": "500 shares of TSLA",
        "date_acquired": "05/23/2020",
        "date_sold": "12/31/2025",
        "proceeds": 25382.45,
        "cost_basis": 20452,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": 4930.45,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })
    context.form_8949.long_term_entries["E"].append({
        "description": "138.13 shares of INTC",
        "date_acquired": "03/12/2018",
        "date_sold": "09/12/2025",
        "proceeds": 60000,
        "cost_basis": 40000,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": 20000,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })

    prior_year_return = make_prior_year(0, 0, 0, 0, 0)

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.code_e_proceeds_total == 85382
    assert context.schedule_d.code_e_cost_basis_total == 60452
    assert context.schedule_d.code_e_adjustments_total == 0
    assert context.schedule_d.code_e_gain_loss_total == 24930

def test_aggregate_single_code_f_entry():
    context = tax_context.tax_context(YEAR)
    context.form_8949.long_term_entries["F"].append({
        "description": "55 shares of AMD",
        "date_acquired": "03/15/2023",
        "date_sold": "06/01/2025",
        "proceeds": 5050,
        "cost_basis": 2033,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": 3017,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })

    prior_year_return = make_prior_year(0, 0, 0, 0, 0)

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.code_f_proceeds_total == 5050
    assert context.schedule_d.code_f_cost_basis_total == 2033
    assert context.schedule_d.code_f_adjustments_total == 0
    assert context.schedule_d.code_f_gain_loss_total == 3017

def test_aggregate_multiple_code_f_entries():
    context = tax_context.tax_context(YEAR)
    context.form_8949.long_term_entries["F"].append({
        "description": "500 shares of TSLA",
        "date_acquired": "05/23/2020",
        "date_sold": "12/31/2025",
        "proceeds": 25382.45,
        "cost_basis": 20452,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": 4930.45,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })
    context.form_8949.long_term_entries["F"].append({
        "description": "138.13 shares of INTC",
        "date_acquired": "03/12/2018",
        "date_sold": "09/12/2025",
        "proceeds": 60000,
        "cost_basis": 40000,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": 20000,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })

    prior_year_return = make_prior_year(0, 0, 0, 0, 0)

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.code_f_proceeds_total == 85382
    assert context.schedule_d.code_f_cost_basis_total == 60452
    assert context.schedule_d.code_f_adjustments_total == 0
    assert context.schedule_d.code_f_gain_loss_total == 24930

def test_net_short_term_gain_loss_without_loss_carryover():
    context = tax_context.tax_context(YEAR)
    context.constants = TAX_YEAR
    context.filing_status = "single"

    context.form_8949.short_term_entries["A"].append({
        "description": "5 shares of AAPL",
        "date_acquired": "01/01/2025",
        "date_sold": "06/01/2025",
        "proceeds": 3394.24,
        "cost_basis": 5003.39,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": -1609.15,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })

    context.form_8949.short_term_entries["B"].append({
        "description": "500 shares of TSLA",
        "date_acquired": "05/23/2025",
        "date_sold": "12/31/2025",
        "proceeds": 20452,
        "cost_basis": 20452,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": 0,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })

    context.form_8949.short_term_entries["C"].append({
        "description": "5 shares of AAPL",
        "date_acquired": "01/01/2025",
        "date_sold": "06/01/2025",
        "proceeds": 3000,
        "cost_basis": 2000,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": 1000,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })

    prior_year_return = make_prior_year(0, 0, 0, 0, 0)

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.net_short_term_gain_loss == -609

def test_net_short_term_gain_loss_with_loss_carryover():
    context = tax_context.tax_context(YEAR)
    context.constants = TAX_YEAR
    context.filing_status = "single"

    context.form_8949.short_term_entries["A"].append({
        "description": "5 shares of AAPL",
        "date_acquired": "01/01/2025",
        "date_sold": "06/01/2025",
        "proceeds": 3000,
        "cost_basis": 5000,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": -2000,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })

    context.form_8949.short_term_entries["B"].append({
        "description": "500 shares of TSLA",
        "date_acquired": "05/23/2025",
        "date_sold": "12/31/2025",
        "proceeds": 20452,
        "cost_basis": 20452,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": 0,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })

    context.form_8949.short_term_entries["C"].append({
        "description": "5 shares of AAPL",
        "date_acquired": "01/01/2025",
        "date_sold": "06/01/2025",
        "proceeds": 3000,
        "cost_basis": 2000,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": 1000,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })

    prior_year_return = make_prior_year(0, 0, 0, 0, 0)

    context.schedule_d.short_term_capital_loss_carryover = 5000

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.net_short_term_gain_loss == -6000

def test_net_long_term_gain_loss_without_loss_carryover():
    context = tax_context.tax_context(YEAR)
    context.constants = TAX_YEAR
    context.filing_status = "single"

    context.form_8949.long_term_entries["D"].append({
        "description": "5 shares of AAPL",
        "date_acquired": "01/01/2024",
        "date_sold": "06/01/2025",
        "proceeds": 3394.24,
        "cost_basis": 5003.39,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": -1609.15,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })

    context.form_8949.long_term_entries["E"].append({
        "description": "500 shares of TSLA",
        "date_acquired": "05/23/2024",
        "date_sold": "12/31/2025",
        "proceeds": 20452,
        "cost_basis": 20452,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": 0,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })

    context.form_8949.long_term_entries["F"].append({
        "description": "5 shares of AAPL",
        "date_acquired": "01/01/2024",
        "date_sold": "06/01/2025",
        "proceeds": 3000,
        "cost_basis": 2000,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": 1000,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })

    prior_year_return = make_prior_year(0, 0, 0, 0, 0)

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.net_long_term_gain_loss == -609

def test_net_long_term_gain_loss_with_loss_carryover():
    context = tax_context.tax_context(YEAR)
    context.constants = TAX_YEAR
    context.filing_status = "single"

    context.form_8949.long_term_entries["D"].append({
        "description": "5 shares of AAPL",
        "date_acquired": "01/01/2024",
        "date_sold": "06/01/2025",
        "proceeds": 3000,
        "cost_basis": 5000,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": -2000,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })

    context.form_8949.long_term_entries["E"].append({
        "description": "500 shares of TSLA",
        "date_acquired": "05/23/2024",
        "date_sold": "12/31/2025",
        "proceeds": 20452,
        "cost_basis": 20452,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": 0,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })

    context.form_8949.long_term_entries["F"].append({
        "description": "5 shares of AAPL",
        "date_acquired": "01/01/2024",
        "date_sold": "06/01/2025",
        "proceeds": 3000,
        "cost_basis": 2000,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": 1000,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })

    prior_year_return = make_prior_year(0, 0, 0, 0, 0)

    context.schedule_d.long_term_capital_loss_carryover = 5000

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.net_long_term_gain_loss == -6000

def test_net_long_term_gain_loss_includes_capital_gain_distributions():
    context = tax_context.tax_context(YEAR)
    context.constants = TAX_YEAR
    context.filing_status = "single"

    context.form_8949.long_term_entries["D"].append({
        "description": "5 shares of AAPL",
        "date_acquired": "01/01/2024",
        "date_sold": "06/01/2025",
        "proceeds": 3000,
        "cost_basis": 2000,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": 1000,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })

    context.schedule_b.dividend_entries.append({
        "payer": "Fidelity",
        "ordinary_dividends": 0,
        "qualified_dividends": 0,
        "cap_gain_distributions": 500,
        "unrecaptured_sec_1250_gain": 0,
        "fed_tax_withheld": 0,
        "section_199a_dividends": 0
    })

    prior_year_return = make_prior_year(0, 0, 0, 0, 0)

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.capital_gain_distributions == 500
    assert context.schedule_d.net_long_term_gain_loss == 1500  # 1000 gain + 500 cap gain distributions

def test_aggregate_adjustments_all_codes():
    context = tax_context.tax_context(YEAR)
    context.constants = TAX_YEAR          # needed because the net total is a loss,
    context.filing_status = "single"    # which reaches the loss-limit lookup

    def entry(proceeds, cost_basis, adjustments, gain):
        return {
            "description": "test", "date_acquired": "01/01/2024", "date_sold": "06/01/2025",
            "proceeds": proceeds, "cost_basis": cost_basis,
            "adjustments": adjustments, "adjustment_code": "W", "gain": gain,
            "federal_tax_withheld": 0, "state_tax_withheld": 0
        }

    context.form_8949.short_term_entries["A"].append(entry(800, 1000, 200, 0))
    context.form_8949.short_term_entries["B"].append(entry(900, 1100, 50, -150))
    context.form_8949.short_term_entries["C"].append(entry(500, 700, 120, -80))
    context.form_8949.long_term_entries["D"].append(entry(1000, 1500, 300, -200))
    context.form_8949.long_term_entries["E"].append(entry(2000, 2200, 75, -125))
    context.form_8949.long_term_entries["F"].append(entry(600, 900, 40, -260))

    prior_year_return = {
        "form_1040_line_15": 0, "schedule_d_line_7": 0, "schedule_d_line_15": 0,
        "schedule_d_line_16": 0, "schedule_d_line_21": 0
    }

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.code_a_adjustments_total == 200
    assert context.schedule_d.code_b_adjustments_total == 50
    assert context.schedule_d.code_c_adjustments_total == 120
    assert context.schedule_d.code_d_adjustments_total == 300
    assert context.schedule_d.code_e_adjustments_total == 75
    assert context.schedule_d.code_f_adjustments_total == 40

def test_net_loss_over_limit_is_capped():
    context = tax_context.tax_context(YEAR)
    context.constants = TAX_YEAR
    context.filing_status = "single"

    context.form_8949.short_term_entries["A"].append({
        "description": "100 shares of XYZ",
        "date_acquired": "01/01/2025",
        "date_sold": "06/01/2025",
        "proceeds": 2000,
        "cost_basis": 12000,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": -10000,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })

    prior_year_return = make_prior_year(0, 0, 0, 0, 0)

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.line_16 == -10000  # the real, uncapped loss
    assert context.schedule_d.line_21 == -3000   # capped at the $3,000 limit
    assert context.form_1040.line_7a == -3000    # what actually flows to the 1040

def test_net_loss_under_limit_is_not_capped():
    context = tax_context.tax_context(YEAR)
    context.constants = TAX_YEAR
    context.filing_status = "single"

    context.form_8949.short_term_entries["A"].append({
        "description": "100 shares of XYZ",
        "date_acquired": "01/01/2025",
        "date_sold": "06/01/2025",
        "proceeds": 3500,
        "cost_basis": 5000,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": -1500,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })

    prior_year_return = make_prior_year(0, 0, 0, 0, 0)

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.line_16 == -1500
    assert context.schedule_d.line_21 == -1500   # under the limit, so unchanged
    assert context.form_1040.line_7a == -1500

def test_net_gain_with_long_term_gain_takes_line_17_yes_path():
    context = tax_context.tax_context(YEAR)
    context.constants = TAX_YEAR
    context.filing_status = "single"

    context.form_8949.long_term_entries["D"].append({
        "description": "50 shares of XYZ",
        "date_acquired": "01/01/2024",
        "date_sold": "06/01/2025",
        "proceeds": 8000,
        "cost_basis": 3000,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": 5000,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })

    prior_year_return = make_prior_year(0, 0, 0, 0, 0)

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.net_long_term_gain_loss == 5000
    assert context.schedule_d.line_16 == 5000
    assert context.form_1040.line_7a == 5000
    assert context.schedule_d.line_17 is True
    assert context.schedule_d.rate_gain_28 == 0
    assert context.schedule_d.unrecaptured_section_1250_gain == 0
    assert context.schedule_d.line_20 is True
    # Returned early, so the loss-side lines were never reached
    assert context.schedule_d.line_21 == 0
    assert context.schedule_d.line_22 is None

def test_net_gain_with_long_term_loss_takes_line_17_no_path():
    context = tax_context.tax_context(YEAR)
    context.constants = TAX_YEAR
    context.filing_status = "single"

    context.form_8949.short_term_entries["A"].append({
        "description": "100 shares of ABC",
        "date_acquired": "01/01/2025",
        "date_sold": "06/01/2025",
        "proceeds": 9000,
        "cost_basis": 3000,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": 6000,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })
    context.form_8949.long_term_entries["D"].append({
        "description": "20 shares of XYZ",
        "date_acquired": "01/01/2024",
        "date_sold": "06/01/2025",
        "proceeds": 3000,
        "cost_basis": 5000,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": -2000,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })

    prior_year_return = make_prior_year(0, 0, 0, 0, 0)

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.net_short_term_gain_loss == 6000
    assert context.schedule_d.net_long_term_gain_loss == -2000
    assert context.schedule_d.line_16 == 4000      # total is still a gain...
    assert context.form_1040.line_7a == 4000
    assert context.schedule_d.line_17 is False     # ...but line 15 isn't, so line 17 is No
    assert context.schedule_d.line_20 is None      # never reached
    assert context.schedule_d.line_21 == 0
    assert context.schedule_d.line_22 is False     # line_3a defaults to 0

def test_line_17_no_path_line_22_yes_when_qualified_dividends():
    # Same setup as above, but with qualified dividends on the 1040
    context = tax_context.tax_context(YEAR)
    context.constants = TAX_YEAR
    context.filing_status = "single"
    context.form_1040.line_3a = 500

    context.form_8949.short_term_entries["A"].append({
        "description": "100 shares of ABC",
        "date_acquired": "01/01/2025",
        "date_sold": "06/01/2025",
        "proceeds": 9000,
        "cost_basis": 3000,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": 6000,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })
    context.form_8949.long_term_entries["D"].append({
        "description": "20 shares of XYZ",
        "date_acquired": "01/01/2024",
        "date_sold": "06/01/2025",
        "proceeds": 3000,
        "cost_basis": 5000,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": -2000,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })

    prior_year_return = make_prior_year(0, 0, 0, 0, 0)

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.line_17 is False
    assert context.schedule_d.line_22 is True

def test_filing_schedule_d_required_for_short_term_sale():
    context = tax_context.tax_context(YEAR)
    context.form_8949.short_term_entries["A"].append({
        "description": "100 shares of ABC",
        "date_acquired": "01/01/2025",
        "date_sold": "06/01/2025",
        "proceeds": 9000,
        "cost_basis": 3000,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": 6000,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })

    assert schedule_d.is_filing_schedule_d(context) == True

def test_filing_schedule_d_required_for_long_term_sale():
    context = tax_context.tax_context(YEAR)
    context.form_8949.long_term_entries["D"].append({
        "description": "20 shares of XYZ",
        "date_acquired": "01/01/2024",
        "date_sold": "06/01/2025",
        "proceeds": 3000,
        "cost_basis": 5000,
        "adjustments": 0,
        "adjustment_code": None,
        "gain": -2000,
        "federal_tax_withheld": 0,
        "state_tax_withheld": 0
    })

    assert schedule_d.is_filing_schedule_d(context) == True

def test_filing_schedule_d_required_for_capital_gain_distributions_only():
    context = tax_context.tax_context(YEAR)
    context.schedule_b.dividend_entries.append({
        "payer": "Fidelity",
        "ordinary_dividends": 0,
        "qualified_dividends": 0,
        "cap_gain_distributions": 500,
        "unrecaptured_sec_1250_gain": 0,
        "fed_tax_withheld": 0,
        "section_199a_dividends": 0
    })

    prior_year_return = make_prior_year(0, 0, 0, 0, 0)

    # capital_gain_distributions is only populated by aggregation
    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert schedule_d.is_filing_schedule_d(context) == True

def test_filing_schedule_d_required_for_short_term_carryover_only():
    context = tax_context.tax_context(YEAR)
    context.schedule_d.short_term_capital_loss_carryover = 2000

    assert schedule_d.is_filing_schedule_d(context) == True

def test_filing_schedule_d_required_for_long_term_carryover_only():
    context = tax_context.tax_context(YEAR)
    context.schedule_d.long_term_capital_loss_carryover = 2000

    assert schedule_d.is_filing_schedule_d(context) == True

def test_filing_schedule_d_not_required_with_no_activity():
    context = tax_context.tax_context(YEAR)

    assert schedule_d.is_filing_schedule_d(context) == False

def make_context():
    context = tax_context.tax_context(YEAR)
    context.constants = TAX_YEAR
    context.filing_status = "single"   # carryover makes line 16 a loss, which reads the loss limit
    return context

def test_carryover_worksheet_not_triggered_with_no_prior_loss(tmp_path):
    context = make_context()
    prior = make_prior_year(50000, 0, 0, 0, 0)

    schedule_d.aggregate_schedule_d(context, prior)

    assert context.schedule_d.short_term_capital_loss_carryover == 0
    assert context.schedule_d.long_term_capital_loss_carryover == 0
    assert not (tmp_path / "capital_loss_carryover_worksheet_2025.json").exists()

def test_carryover_worksheet_short_term_loss(tmp_path):
    context = make_context()
    # Last year: short-term loss of 8000, long-term 0, total 8000, only 3000 deducted
    prior = make_prior_year(50000, -8000, 0, -8000, -3000)

    schedule_d.aggregate_schedule_d(context, prior)

    # Worksheet by hand: l1=50000, l2=3000, l3=53000, l4=3000,
    # l5=8000, l6=0, l7=3000, l8=8000-3000=5000. Line 15 is not a loss, so it stops.
    assert context.schedule_d.short_term_capital_loss_carryover == 5000
    assert context.schedule_d.long_term_capital_loss_carryover == 0
    assert context.schedule_d.net_short_term_gain_loss == -5000   # carryover applied as a loss

    saved = json.loads((tmp_path / "capital_loss_carryover_worksheet_2025.json").read_text())
    assert saved == {
        "tax_year": 2025,
        "line_1": 50000, "line_2": 3000, "line_3": 53000, "line_4": 3000,
        "line_5": 8000, "line_6": 0, "line_7": 3000, "line_8": 5000
    }

def test_carryover_worksheet_long_term_loss():
    context = make_context()
    # Last year: short-term 0, long-term loss of 8000
    prior = make_prior_year(50000, 0, -8000, -8000, -3000)

    schedule_d.aggregate_schedule_d(context, prior)

    # Worksheet by hand: l4=3000, line 7 not a loss so l5=0.
    # l9=8000, l10=0, l11=3000-0=3000, l12=3000, l13=8000-3000=5000
    assert context.schedule_d.short_term_capital_loss_carryover == 0
    assert context.schedule_d.long_term_capital_loss_carryover == 5000
    assert context.schedule_d.net_long_term_gain_loss == -5000

def test_carryover_worksheet_short_and_long_term_losses():
    context = make_context()
    # Last year: short-term loss 5000, long-term loss 6000, total 11000, only 3000 deducted
    prior = make_prior_year(50000, -5000, -6000, -11000, -3000)

    schedule_d.aggregate_schedule_d(context, prior)

    # Short-term goes first: l4=3000, l5=5000, l6=0, l7=3000, l8=5000-3000=2000
    # Long-term: l9=6000, l10=0, l11=max(3000-5000,0)=0, l12=0, l13=6000
    # The 3000 deduction was used up by the short-term side, so 2000 + 6000 = 8000 carries over.
    assert context.schedule_d.short_term_capital_loss_carryover == 2000
    assert context.schedule_d.long_term_capital_loss_carryover == 6000

def test_carryover_triggered_by_negative_taxable_income():
    context = make_context()
    # Loss was under the cap (line 21 == line 16), but taxable income would have been negative
    prior = make_prior_year(-2000, -1500, 0, -1500, -1500)

    schedule_d.aggregate_schedule_d(context, prior)

    # l1=-2000, l2=1500, l3=max(-500,0)=0, l4=min(1500,0)=0
    # l5=1500, l6=0, l7=0, l8=1500
    assert context.schedule_d.short_term_capital_loss_carryover == 1500
    assert context.schedule_d.long_term_capital_loss_carryover == 0

def test_small_loss_fully_deducted_has_no_carryover(tmp_path):
    context = make_context()
    # Loss fully deducted (line 21 == line 16) and taxable income was positive
    prior = make_prior_year(40000, -1500, 0, -1500, -1500)

    schedule_d.aggregate_schedule_d(context, prior)

    assert context.schedule_d.short_term_capital_loss_carryover == 0
    assert context.schedule_d.long_term_capital_loss_carryover == 0
    assert not (tmp_path / "capital_loss_carryover_worksheet_2025.json").exists()

def test_1250_gain_kept_when_nothing_offsets_it():
    context = tax_context.tax_context(YEAR)
    context.constants = TAX_YEAR
    context.form_8949.long_term_entries["D"].append({
        "description": "test", "date_acquired": "01/01/2024", "date_sold": "06/01/2025",
        "proceeds": 10000, "cost_basis": 5000,
        "adjustments": 0, "adjustment_code": None, "gain": 5000,
        "federal_tax_withheld": 0, "state_tax_withheld": 0
    })

    context.schedule_b.unrecaptured_sec_1250_gain = 1000

    with pytest.raises(NotImplementedError, match="Schedule D Tax Worksheet"):
        schedule_d.aggregate_schedule_d(context, make_prior_year(0, 0, 0, 0, 0))

    assert context.schedule_d.line_17 is True
    assert context.schedule_d.unrecaptured_section_1250_gain == 1000
    assert context.schedule_d.line_20 is None #used to be false
    assert context.form_1040.line_7a == 5000

def test_1250_gain_reduced_by_short_term_loss():
    context = tax_context.tax_context(YEAR)
    context.constants = TAX_YEAR
    context.form_8949.long_term_entries["D"].append({
        "description": "test", "date_acquired": "01/01/2024", "date_sold": "06/01/2025",
        "proceeds": 10000, "cost_basis": 5000,
        "adjustments": 0, "adjustment_code": None, "gain": 5000,
        "federal_tax_withheld": 0, "state_tax_withheld": 0
    })
    context.form_8949.short_term_entries["A"].append({
        "description": "test", "date_acquired": "01/01/2025", "date_sold": "06/01/2025",
        "proceeds": 10000, "cost_basis": 10300,
        "adjustments": 0, "adjustment_code": None, "gain": -300,
        "federal_tax_withheld": 0, "state_tax_withheld": 0
    })
    context.schedule_b.unrecaptured_sec_1250_gain = 1000

    with pytest.raises(NotImplementedError, match="Schedule D Tax Worksheet"):
        schedule_d.aggregate_schedule_d(context, make_prior_year(0, 0, 0, 0, 0))

    assert context.schedule_d.line_16 == 4700
    assert context.schedule_d.unrecaptured_section_1250_gain == 700   # 1000 - 300
    assert context.schedule_d.line_20 is None

def test_1250_gain_wiped_out_by_larger_short_term_loss():
    context = tax_context.tax_context(YEAR)
    context.constants = TAX_YEAR
    context.form_8949.long_term_entries["D"].append({
        "description": "test", "date_acquired": "01/01/2024", "date_sold": "06/01/2025",
        "proceeds": 10000, "cost_basis": 5000,
        "adjustments": 0, "adjustment_code": None, "gain": 5000,
        "federal_tax_withheld": 0, "state_tax_withheld": 0
    })
    context.form_8949.short_term_entries["A"].append({
        "description": "test", "date_acquired": "01/01/2025", "date_sold": "06/01/2025",
        "proceeds": 10000, "cost_basis": 11500,
        "adjustments": 0, "adjustment_code": None, "gain": -1500,
        "federal_tax_withheld": 0, "state_tax_withheld": 0
    })
    context.schedule_b.unrecaptured_sec_1250_gain = 1000

    schedule_d.aggregate_schedule_d(context, make_prior_year(0, 0, 0, 0, 0))

    assert context.schedule_d.line_16 == 3500
    assert context.schedule_d.unrecaptured_section_1250_gain == 0     # 1000 - 1500, floored at 0
    assert context.schedule_d.line_20 is True

def test_1250_gain_reduced_by_long_term_carryover():
    context = tax_context.tax_context(YEAR)
    context.constants = TAX_YEAR
    context.form_8949.long_term_entries["D"].append({
        "description": "test", "date_acquired": "01/01/2024", "date_sold": "06/01/2025",
        "proceeds": 10000, "cost_basis": 5000,
        "adjustments": 0, "adjustment_code": None, "gain": 5000,
        "federal_tax_withheld": 0, "state_tax_withheld": 0
    })
    context.schedule_b.unrecaptured_sec_1250_gain = 1000
    context.schedule_d.long_term_capital_loss_carryover = 400

    with pytest.raises(NotImplementedError, match="Schedule D Tax Worksheet"):
        schedule_d.aggregate_schedule_d(context, make_prior_year(0, 0, 0, 0, 0))

    assert context.schedule_d.net_long_term_gain_loss == 4600
    assert context.schedule_d.unrecaptured_section_1250_gain == 600   # 1000 - 400
    assert context.schedule_d.line_20 is None # used to be false

def test_1250_worksheet_skipped_when_no_net_long_term_gain():
    context = tax_context.tax_context(YEAR)
    context.constants = TAX_YEAR
    context.form_8949.short_term_entries["A"].append({
        "description": "test", "date_acquired": "01/01/2025", "date_sold": "06/01/2025",
        "proceeds": 10000, "cost_basis": 5000,
        "adjustments": 0, "adjustment_code": None, "gain": 5000,
        "federal_tax_withheld": 0, "state_tax_withheld": 0
    })
    context.form_8949.long_term_entries["D"].append({
        "description": "test", "date_acquired": "01/01/2024", "date_sold": "06/01/2025",
        "proceeds": 10000, "cost_basis": 12000,
        "adjustments": 0, "adjustment_code": None, "gain": -2000,
        "federal_tax_withheld": 0, "state_tax_withheld": 0
    })
    context.schedule_b.unrecaptured_sec_1250_gain = 1000

    schedule_d.aggregate_schedule_d(context, make_prior_year(0, 0, 0, 0, 0))

    assert context.schedule_d.line_16 == 3000
    assert context.schedule_d.line_17 is False
    assert context.schedule_d.unrecaptured_section_1250_gain == 0
    assert context.schedule_d.line_20 is None

# ---------- Capital Loss Carryover Worksheet, called directly ----------

def test_carryover_worksheet_short_and_long_term_losses(tmp_path):
    # Last year: taxable income 50000, ST loss 5000, LT loss 6000, total loss 11000, deducted 3000
    context = tax_context.tax_context(YEAR)
    (context.schedule_d.short_term_capital_loss_carryover,
        context.schedule_d.long_term_capital_loss_carryover) \
            = schedule_d.compute_capital_loss_carryover_worksheet(context, make_prior_year(50000, -5000, -6000, -11000, -3000))

    assert context.schedule_d.short_term_capital_loss_carryover == 2000
    assert context.schedule_d.long_term_capital_loss_carryover == 6000
    assert read_saved(tmp_path, "capital_loss_carryover_worksheet") == {
        "tax_year": YEAR,
        "line_1": 50000,    # last year's taxable income
        "line_2": 3000,     # the loss deducted last year
        "line_3": 53000,    # 50000 + 3000
        "line_4": 3000,     # smaller of 3000 and 53000
        "line_5": 5000,     # short-term loss
        "line_6": 0,        # no long-term gain
        "line_7": 3000,     # 3000 + 0
        "line_8": 2000,     # 5000 - 3000 = short-term carryover
        "line_9": 6000,     # long-term loss
        "line_10": 0,       # no short-term gain
        "line_11": 0,       # 3000 - 5000, floored at 0 (deduction all used by short-term)
        "line_12": 0,       # 0 + 0
        "line_13": 6000,    # 6000 - 0 = long-term carryover
    }

def test_carryover_worksheet_long_term_loss_only(tmp_path):
    # Last year: LT loss 8000, nothing short-term, deducted 3000
    context = tax_context.tax_context(YEAR)
    (context.schedule_d.short_term_capital_loss_carryover,
         context.schedule_d.long_term_capital_loss_carryover) \
     = schedule_d.compute_capital_loss_carryover_worksheet(context, make_prior_year(50000, 0, -8000, -8000, -3000))

    assert context.schedule_d.short_term_capital_loss_carryover == 0
    assert context.schedule_d.long_term_capital_loss_carryover == 5000
    assert read_saved(tmp_path, "capital_loss_carryover_worksheet") == {
        "tax_year": YEAR,
        "line_1": 50000,
        "line_2": 3000,
        "line_3": 53000,
        "line_4": 3000,
        "line_5": 0,        # no short-term loss, so lines 6-8 are skipped
        "line_9": 8000,     # long-term loss
        "line_10": 0,
        "line_11": 3000,    # 3000 - 0: the whole deduction went against long-term
        "line_12": 3000,    # 0 + 3000
        "line_13": 5000,    # 8000 - 3000
    }

def test_carryover_worksheet_short_term_loss_only(tmp_path):
    # Last year: ST loss 8000, nothing long-term, deducted 3000. Worksheet stops after line 8.
    context = tax_context.tax_context(YEAR)
    (context.schedule_d.short_term_capital_loss_carryover,
             context.schedule_d.long_term_capital_loss_carryover) \
         = schedule_d.compute_capital_loss_carryover_worksheet(context, make_prior_year(50000, -8000, 0, -8000, -3000))

    assert context.schedule_d.short_term_capital_loss_carryover == 5000
    assert context.schedule_d.long_term_capital_loss_carryover == 0
    assert read_saved(tmp_path, "capital_loss_carryover_worksheet") == {
        "tax_year": YEAR,
        "line_1": 50000,
        "line_2": 3000,
        "line_3": 53000,
        "line_4": 3000,
        "line_5": 8000,
        "line_6": 0,
        "line_7": 3000,
        "line_8": 5000,     # 8000 - 3000
    }

# ---------- Unrecaptured Section 1250 Gain Worksheet, called directly ----------

def test_1250_worksheet_with_short_term_loss_and_carryover(tmp_path):
    context = tax_context.tax_context(YEAR)
    context.schedule_b.unrecaptured_sec_1250_gain = 1000
    context.schedule_d.net_short_term_gain_loss = -300
    context.schedule_d.long_term_capital_loss_carryover = 400

    context.schedule_d.unrecaptured_section_1250_gain = schedule_d.compute_unrecaptured_section_1250_gain_worksheet(context)

    assert context.schedule_d.unrecaptured_section_1250_gain == 300
    assert read_saved(tmp_path, "unrecaptured_section_1250_gain_worksheet") == {
        "tax_year": YEAR,
        "line_10": 0,
        "line_11": 1000,    # 1250 gain from the 1099-DIV
        "line_12": 0,
        "line_13": 1000,    # 0 + 1000 + 0
        "line_14": 0,
        "line_15": -300,    # short-term loss
        "line_16": -400,    # long-term carryover, as a loss
        "line_17": 700,     # losses combined: 300 + 400, entered as positive
        "line_18": 300,     # 1000 - 700
    }

def test_1250_worksheet_losses_larger_than_gain(tmp_path):
    context = tax_context.tax_context(YEAR)
    context.schedule_b.unrecaptured_sec_1250_gain = 1000
    context.schedule_d.net_short_term_gain_loss = -1500
    context.schedule_d.long_term_capital_loss_carryover = 0

    context.schedule_d.unrecaptured_section_1250_gain = schedule_d.compute_unrecaptured_section_1250_gain_worksheet(context)

    assert context.schedule_d.unrecaptured_section_1250_gain == 0
    assert read_saved(tmp_path, "unrecaptured_section_1250_gain_worksheet") == {
        "tax_year": YEAR,
        "line_10": 0,
        "line_11": 1000,
        "line_12": 0,
        "line_13": 1000,
        "line_14": 0,
        "line_15": -1500,
        "line_16": 0,
        "line_17": 1500,
        "line_18": 0,       # 1000 - 1500, floored at 0
    }

def test_1250_worksheet_short_term_gain_is_not_a_loss(tmp_path):
    context = tax_context.tax_context(YEAR)
    context.schedule_b.unrecaptured_sec_1250_gain = 1000
    context.schedule_d.net_short_term_gain_loss = 500    # a gain, so line 15 is 0
    context.schedule_d.long_term_capital_loss_carryover = 0

    context.schedule_d.unrecaptured_section_1250_gain = schedule_d.compute_unrecaptured_section_1250_gain_worksheet(context)

    assert context.schedule_d.unrecaptured_section_1250_gain == 1000
    assert read_saved(tmp_path, "unrecaptured_section_1250_gain_worksheet") == {
        "tax_year": YEAR,
        "line_10": 0,
        "line_11": 1000,
        "line_12": 0,
        "line_13": 1000,
        "line_14": 0,
        "line_15": 0,
        "line_16": 0,
        "line_17": 0,
        "line_18": 1000,
    }

# Tests for the Schedule D Tax Worksheet (compute_schedule_d_tax_worksheet).
def run_worksheet(taxable_income, qualified_dividends, net_long_term, net_short_term, section_1250, rate_gain_28=0):
    context = tax_context.tax_context(YEAR)
    context.constants = TAX_YEAR
    context.filing_status = "single"
    context.form_1040.line_15 = taxable_income
    context.form_1040.line_3a = qualified_dividends
    context.schedule_d.net_long_term_gain_loss = net_long_term
    context.schedule_d.net_short_term_gain_loss = net_short_term
    context.schedule_d.unrecaptured_section_1250_gain = section_1250
    context.schedule_d.rate_gain_28 = rate_gain_28
    return schedule_d.compute_schedule_d_tax_worksheet(context)

def check_lines(saved, expected, skipped=()):
    """Every expected line must match. Lines the worksheet says to skip must be blank/zero or absent."""
    for line, value in expected.items():
        assert saved[f"line_{line}"] == value, f"line {line}: expected {value}, got {saved[f'line_{line}']}"
    for line in skipped:
        assert not saved.get(f"line_{line}"), f"line {line} should have been skipped"

def test_a_typical_1250_with_qualified_dividends(tmp_path):
    # Typical case for you: 1250 gain, qualified dividends, income well above the 0% band.
    # 1250 gain lands entirely in the ordinary brackets (line 39 is 0), so no 25% tax.
    result = run_worksheet(80000, 2000, 10000, 0, 1000)

    assert result == 11750
    saved = read_saved(tmp_path, "schedule_d_tax_worksheet")
    check_lines(saved, {
        1: 80000,
        2: 2000,
        3: 0,
        4: 0,
        5: 0,
        6: 2000,   # qualified dividends, no 4952
        7: 10000,
        8: 0,
        9: 10000,   # min(LT 10000, line 16 10000)
        10: 12000,
        11: 1000,   # 28% gain 0 + 1250 gain 1000
        12: 1000,   # smaller of line 9 and line 11
        13: 11000,   # line 10 12000 - line 12 1000
        14: 69000,
        15: 48350,
        16: 48350,
        17: 48350,
        18: 68000,
        19: 80000,
        20: 69000,
        21: 69000,   # ordinary income, including the 1250 gain
        22: 0,
        23: 11000,
        24: 0,
        25: 11000,
        26: 533400,
        27: 80000,
        28: 69000,
        29: 11000,
        30: 11000,   # 15% band: 11000
        31: 1650,
        32: 11000,
        33: 0,
        34: 0,
        35: 1000,
        36: 81000,
        37: 80000,
        38: 1000,
        39: 0,   # 1250 gain fits under the ordinary brackets
        40: 0,
        44: 10100,   # tax on 69000 (slot 69000-69050, midpoint 69025): 10099.50 -> 10100
        45: 11750,
        46: 12520,   # tax on 80000 (midpoint 80025): 12519.50 -> 12520
        47: 11750,   # smaller of 45 and 46
    }, skipped=[41, 42, 43])

def test_b_1250_gain_taxed_at_25_percent(tmp_path):
    # High income: the 1250 gain is above the ordinary brackets that would tax it at less than 25%,
    # so line 39 is positive and line 40 (25%) is used.
    result = run_worksheet(250000, 0, 20000, 0, 5000)

    assert result == 54163
    saved = read_saved(tmp_path, "schedule_d_tax_worksheet")
    check_lines(saved, {
        1: 250000,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 20000,
        8: 0,
        9: 20000,
        10: 20000,
        11: 5000,
        12: 5000,
        13: 15000,
        14: 235000,
        15: 48350,
        16: 48350,
        17: 48350,
        18: 230000,
        19: 197300,   # smaller of 250000 and 197300
        20: 197300,
        21: 230000,
        22: 0,
        23: 15000,
        24: 0,
        25: 15000,
        26: 533400,
        27: 250000,
        28: 230000,
        29: 20000,
        30: 15000,
        31: 2250,   # 15% of 15000
        32: 15000,
        33: 0,
        34: 0,
        35: 5000,
        36: 250000,
        37: 250000,
        38: 0,
        39: 5000,   # all 5000 of the 1250 gain is taxed at 25%
        40: 1250,   # 25% of 5000
        44: 50663,   # tax on 230000, from the brackets (no slot over 100k)
        45: 54163,
        46: 57063,   # tax on 250000
        47: 54163,   # smaller of 45 and 46
    }, skipped=[41, 42, 43])

def test_c_gain_reaches_the_20_percent_band(tmp_path):
    # Income over $533,400: part of the gain is taxed at 20% (lines 33 and 34).
    result = run_worksheet(700000, 0, 100000, 0, 10000)

    assert result == 200047
    saved = read_saved(tmp_path, "schedule_d_tax_worksheet")
    check_lines(saved, {
        1: 700000,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 100000,
        8: 0,
        9: 100000,
        10: 100000,
        11: 10000,
        12: 10000,
        13: 90000,
        14: 610000,
        15: 48350,
        16: 48350,
        17: 48350,
        18: 600000,
        19: 197300,
        20: 197300,
        21: 600000,
        22: 0,
        23: 90000,
        24: 0,
        25: 90000,
        26: 533400,
        27: 533400,
        28: 600000,
        29: 0,   # 533400 - 600000, floored at 0, so nothing is left in the 15% band
        30: 0,
        31: 0,
        32: 0,
        33: 90000,   # all 90000 of the other gain is at 20%
        34: 18000,   # 20% of 90000
        35: 10000,
        36: 700000,
        37: 700000,
        38: 0,
        39: 10000,
        40: 2500,   # 25% of 10000
        44: 179547,   # tax on 600000: 179547.25 -> 179547
        45: 200047,
        46: 216020,   # tax on 700000: 216020.25 -> 216020
        47: 200047,   # smaller of 45 and 46
    }, skipped=[41, 42, 43])

def test_h_short_term_loss_reduces_line_7(tmp_path):
    # A short-term loss makes Schedule D line 16 smaller than line 15, so line 7 takes line 16.
    result = run_worksheet(80000, 0, 20000, -5000, 1000)

    assert result == 11540
    saved = read_saved(tmp_path, "schedule_d_tax_worksheet")
    check_lines(saved, {
        1: 80000,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 15000,   # min(LT 20000, line 16 = 15000)
        8: 0,
        9: 15000,   # 15000
        10: 15000,
        11: 1000,
        12: 1000,
        13: 14000,   # 15000 - 1000
        14: 66000,
        15: 48350,
        16: 48350,
        17: 48350,
        18: 65000,
        19: 80000,
        20: 66000,
        21: 66000,
        22: 0,
        23: 14000,
        24: 0,
        25: 14000,
        26: 533400,
        27: 80000,
        28: 66000,
        29: 14000,
        30: 14000,
        31: 2100,
        32: 14000,
        33: 0,
        34: 0,
        35: 1000,
        36: 81000,
        37: 80000,
        38: 1000,
        39: 0,
        40: 0,
        44: 9440,   # tax on 66000 (slot 66000-66050, midpoint 66025): 9439.50 -> 9440
        45: 11540,
        46: 12520,
        47: 11540,   # smaller of 45 and 46
    }, skipped=[41, 42, 43])

def test_i_1250_gain_bigger_than_line_9(tmp_path):
    # 1250 gain (5000) is larger than line 9 (2000), so line 12 is capped at line 9 and the rest is taxed as ordinary.
    result = run_worksheet(80000, 0, 3000, -1000, 5000)

    assert result == 12520
    saved = read_saved(tmp_path, "schedule_d_tax_worksheet")
    check_lines(saved, {
        1: 80000,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 2000,   # min(LT 3000, line 16 = 2000)
        8: 0,
        9: 2000,
        10: 2000,
        11: 5000,   # 1250 gain 5000
        12: 2000,   # smaller of line 9 (2000) and line 11 (5000)
        13: 0,   # line 10 2000 - line 12 2000 = 0
        14: 80000,
        15: 48350,
        16: 48350,
        17: 48350,
        18: 78000,
        19: 80000,
        20: 80000,
        21: 80000,
        22: 0,
        23: 0,   # nothing left for the 15% and 20% bands
        24: 0,
        25: 0,
        26: 533400,
        27: 80000,
        28: 80000,
        29: 0,
        30: 0,
        31: 0,
        32: 0,
        33: 0,
        34: 0,
        35: 2000,
        36: 82000,
        37: 80000,
        38: 2000,
        39: 0,
        40: 0,
        44: 12520,
        45: 12520,
        46: 12520,
        47: 12520,   # equals regular tax, since no gain is taxed at a lower rate
    }, skipped=[41, 42, 43])

def test_f_income_under_the_0_percent_limit_skips_to_line_44(tmp_path):
    # Line 1 (30000) equals line 16 (the smaller of line 1 and 48350), so lines 23-43 are skipped.
    # The gain is taxed at 0%: line 22 = 4000 of it, the other 26000 is taxed from the table.
    result = run_worksheet(30000, 0, 5000, 0, 1000)

    assert result == 2885
    saved = read_saved(tmp_path, "schedule_d_tax_worksheet")
    check_lines(saved, {
        1: 30000,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 5000,
        8: 0,
        9: 5000,
        10: 5000,
        11: 1000,
        12: 1000,
        13: 4000,
        14: 26000,
        15: 48350,
        16: 30000,
        17: 26000,
        18: 25000,
        19: 30000,
        20: 26000,
        21: 26000,
        22: 4000,   # taxed at 0%
        44: 2885,   # tax on 26000 (slot 26000-26050, midpoint 26025): 2884.50 -> 2885
        45: 2885,
        46: 3365,   # tax on 30000 (midpoint 30025): 3364.50 -> 3365
        47: 2885,   # smaller of 45 and 46
    }, skipped=[23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43])

def test_g_everything_in_the_0_and_15_percent_bands_skips_to_line_44(tmp_path):
    # Line 1 (60010) equals line 32 (line 24 + line 30 = 48350 + 11660), so lines 33-43 are skipped,
    # including the 25% calculation on the 1250 gain.
    result = run_worksheet(60010, 0, 70000, 0, 2000)

    assert result == 1749
    saved = read_saved(tmp_path, "schedule_d_tax_worksheet")
    check_lines(saved, {
        1: 60010,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 70000,
        8: 0,
        9: 70000,
        10: 70000,
        11: 2000,
        12: 2000,
        13: 68000,
        14: 0,
        15: 48350,
        16: 48350,
        17: 0,
        18: 0,
        19: 60010,
        20: 0,
        21: 0,
        22: 48350,   # taxed at 0%
        23: 60010,
        24: 48350,
        25: 11660,
        26: 533400,
        27: 60010,
        28: 48350,
        29: 11660,
        30: 11660,   # 15% band
        31: 1749,   # 15% of 11660
        32: 60010,   # equals line 1
        44: 0,   # nothing left to tax as ordinary income
        45: 1749,
        46: 8120,   # tax on 60010 (midpoint 60025): 8119.50 -> 8120
        47: 1749,   # smaller of 45 and 46
    }, skipped=[33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43])

def test_result_is_never_more_than_regular_tax(tmp_path):
    # Line 47 is the smaller of line 45 and line 46 (the tax with no special rates).
    run_worksheet(80000, 2000, 10000, 0, 1000)
    saved = read_saved(tmp_path, "schedule_d_tax_worksheet")
    assert saved["line_47"] == min(saved["line_45"], saved["line_46"])
    assert saved["line_47"] <= saved["line_46"]

def test_28_percent_gain_is_added_to_line_11(tmp_path):
    # Line 11 adds Schedule D lines 18 (28% gain) and 19 (1250 gain). The 28% worksheet is hardcoded
    # to 0 for you, so this only checks the line 11 arithmetic: 1000 + 500 = 1500.
    run_worksheet(80000, 0, 10000, 0, 1000, rate_gain_28=500)
    saved = read_saved(tmp_path, "schedule_d_tax_worksheet")
    assert saved["line_11"] == 1500
    assert saved["line_12"] == 1500