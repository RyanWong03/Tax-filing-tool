import tax_context
import federal.forms.schedule_d as schedule_d
import json
from conftest import YEAR, TAX_YEAR

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

    schedule_d.aggregate_schedule_d(context, make_prior_year(0, 0, 0, 0, 0))

    assert context.schedule_d.line_17 is True
    assert context.schedule_d.unrecaptured_section_1250_gain == 1000
    assert context.schedule_d.line_20 is False
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

    schedule_d.aggregate_schedule_d(context, make_prior_year(0, 0, 0, 0, 0))

    assert context.schedule_d.line_16 == 4700
    assert context.schedule_d.unrecaptured_section_1250_gain == 700   # 1000 - 300
    assert context.schedule_d.line_20 is False

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

    schedule_d.aggregate_schedule_d(context, make_prior_year(0, 0, 0, 0, 0))

    assert context.schedule_d.net_long_term_gain_loss == 4600
    assert context.schedule_d.unrecaptured_section_1250_gain == 600   # 1000 - 400
    assert context.schedule_d.line_20 is False

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

def read_saved(tmp_path, name):
    with open(tmp_path / f"{name}_{YEAR}.json") as f:
        return json.load(f)

# ---------- Capital Loss Carryover Worksheet, called directly ----------

def test_carryover_worksheet_short_and_long_term_losses(tmp_path):
    # Last year: taxable income 50000, ST loss 5000, LT loss 6000, total loss 11000, deducted 3000
    context = tax_context.tax_context(YEAR)
    schedule_d.compute_capital_loss_carryover_worksheet(context, make_prior_year(50000, -5000, -6000, -11000, -3000))

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
    schedule_d.compute_capital_loss_carryover_worksheet(context, make_prior_year(50000, 0, -8000, -8000, -3000))

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
    schedule_d.compute_capital_loss_carryover_worksheet(context, make_prior_year(50000, -8000, 0, -8000, -3000))

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

    schedule_d.compute_unrecaptured_section_1250_gain_worksheet(context)

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

    schedule_d.compute_unrecaptured_section_1250_gain_worksheet(context)

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

    schedule_d.compute_unrecaptured_section_1250_gain_worksheet(context)

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