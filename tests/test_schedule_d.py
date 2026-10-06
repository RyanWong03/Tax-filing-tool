import tax_context
import federal.forms.schedule_d as schedule_d
import federal.tax_years.y_2025 as y_2025

def test_aggregate_zero_entries():
    context = tax_context.tax_context(2025)
    prior_year_return = {
        "form_1040_line_15": 0,
        "schedule_d_line_7": 0,
        "schedule_d_line_15": 0,
        "schedule_d_line_16": 0,
        "schedule_d_line_21": 0
    }

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
    context = tax_context.tax_context(2025)
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

    prior_year_return = {
        "form_1040_line_15": 0,
        "schedule_d_line_7": 0,
        "schedule_d_line_15": 0,
        "schedule_d_line_16": 0,
        "schedule_d_line_21": 0
    }

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.code_a_proceeds_total == 3000
    assert context.schedule_d.code_a_cost_basis_total == 2000
    assert context.schedule_d.code_a_adjustments_total == 0
    assert context.schedule_d.code_a_gain_loss_total == 1000

def test_aggregate_multiple_code_a_entries():
    context = tax_context.tax_context(2025)
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

    prior_year_return = {
        "form_1040_line_15": 0,
        "schedule_d_line_7": 0,
        "schedule_d_line_15": 0,
        "schedule_d_line_16": 0,
        "schedule_d_line_21": 0
    }

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.code_a_proceeds_total == 31382
    assert context.schedule_d.code_a_cost_basis_total == 24452
    assert context.schedule_d.code_a_adjustments_total == 0
    assert context.schedule_d.code_a_gain_loss_total == 6930

def test_aggregate_single_code_b_entry():
    context = tax_context.tax_context(2025)
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

    prior_year_return = {
        "form_1040_line_15": 0,
        "schedule_d_line_7": 0,
        "schedule_d_line_15": 0,
        "schedule_d_line_16": 0,
        "schedule_d_line_21": 0
    }

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.code_b_proceeds_total == 3000
    assert context.schedule_d.code_b_cost_basis_total == 2000
    assert context.schedule_d.code_b_adjustments_total == 0
    assert context.schedule_d.code_b_gain_loss_total == 1000

def test_aggregate_multiple_code_b_entries():
    context = tax_context.tax_context(2025)
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

    prior_year_return = {
        "form_1040_line_15": 0,
        "schedule_d_line_7": 0,
        "schedule_d_line_15": 0,
        "schedule_d_line_16": 0,
        "schedule_d_line_21": 0
    }

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.code_b_proceeds_total == 31382
    assert context.schedule_d.code_b_cost_basis_total == 24452
    assert context.schedule_d.code_b_adjustments_total == 0
    assert context.schedule_d.code_b_gain_loss_total == 6930

def test_aggregate_single_code_c_entry():
    context = tax_context.tax_context(2025)
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

    prior_year_return = {
        "form_1040_line_15": 0,
        "schedule_d_line_7": 0,
        "schedule_d_line_15": 0,
        "schedule_d_line_16": 0,
        "schedule_d_line_21": 0
    }

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.code_c_proceeds_total == 3000
    assert context.schedule_d.code_c_cost_basis_total == 2000
    assert context.schedule_d.code_c_adjustments_total == 0
    assert context.schedule_d.code_c_gain_loss_total == 1000

def test_aggregate_multiple_code_c_entries():
    context = tax_context.tax_context(2025)
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

    prior_year_return = {
        "form_1040_line_15": 0,
        "schedule_d_line_7": 0,
        "schedule_d_line_15": 0,
        "schedule_d_line_16": 0,
        "schedule_d_line_21": 0
    }

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.code_c_proceeds_total == 31382
    assert context.schedule_d.code_c_cost_basis_total == 24452
    assert context.schedule_d.code_c_adjustments_total == 0
    assert context.schedule_d.code_c_gain_loss_total == 6930

def test_aggregate_single_code_d_entry():
    context = tax_context.tax_context(2025)
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

    prior_year_return = {
        "form_1040_line_15": 0,
        "schedule_d_line_7": 0,
        "schedule_d_line_15": 0,
        "schedule_d_line_16": 0,
        "schedule_d_line_21": 0
    }

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.code_d_proceeds_total == 5050
    assert context.schedule_d.code_d_cost_basis_total == 2033
    assert context.schedule_d.code_d_adjustments_total == 0
    assert context.schedule_d.code_d_gain_loss_total == 3017

def test_aggregate_multiple_code_d_entries():
    context = tax_context.tax_context(2025)
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

    prior_year_return = {
        "form_1040_line_15": 0,
        "schedule_d_line_7": 0,
        "schedule_d_line_15": 0,
        "schedule_d_line_16": 0,
        "schedule_d_line_21": 0
    }

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.code_d_proceeds_total == 85382
    assert context.schedule_d.code_d_cost_basis_total == 60452
    assert context.schedule_d.code_d_adjustments_total == 0
    assert context.schedule_d.code_d_gain_loss_total == 24930

def test_aggregate_single_code_e_entry():
    context = tax_context.tax_context(2025)
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

    prior_year_return = {
        "form_1040_line_15": 0,
        "schedule_d_line_7": 0,
        "schedule_d_line_15": 0,
        "schedule_d_line_16": 0,
        "schedule_d_line_21": 0
    }

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.code_e_proceeds_total == 5050
    assert context.schedule_d.code_e_cost_basis_total == 2033
    assert context.schedule_d.code_e_adjustments_total == 0
    assert context.schedule_d.code_e_gain_loss_total == 3017

def test_aggregate_multiple_code_e_entries():
    context = tax_context.tax_context(2025)
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

    prior_year_return = {
        "form_1040_line_15": 0,
        "schedule_d_line_7": 0,
        "schedule_d_line_15": 0,
        "schedule_d_line_16": 0,
        "schedule_d_line_21": 0
    }

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.code_e_proceeds_total == 85382
    assert context.schedule_d.code_e_cost_basis_total == 60452
    assert context.schedule_d.code_e_adjustments_total == 0
    assert context.schedule_d.code_e_gain_loss_total == 24930

def test_aggregate_single_code_f_entry():
    context = tax_context.tax_context(2025)
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

    prior_year_return = {
        "form_1040_line_15": 0,
        "schedule_d_line_7": 0,
        "schedule_d_line_15": 0,
        "schedule_d_line_16": 0,
        "schedule_d_line_21": 0
    }

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.code_f_proceeds_total == 5050
    assert context.schedule_d.code_f_cost_basis_total == 2033
    assert context.schedule_d.code_f_adjustments_total == 0
    assert context.schedule_d.code_f_gain_loss_total == 3017

def test_aggregate_multiple_code_f_entries():
    context = tax_context.tax_context(2025)
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

    prior_year_return = {
        "form_1040_line_15": 0,
        "schedule_d_line_7": 0,
        "schedule_d_line_15": 0,
        "schedule_d_line_16": 0,
        "schedule_d_line_21": 0
    }

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.code_f_proceeds_total == 85382
    assert context.schedule_d.code_f_cost_basis_total == 60452
    assert context.schedule_d.code_f_adjustments_total == 0
    assert context.schedule_d.code_f_gain_loss_total == 24930

def test_net_short_term_gain_loss_without_loss_carryover():
    context = tax_context.tax_context(2025)
    context.constants = y_2025
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

    prior_year_return = {
        "form_1040_line_15": 0,
        "schedule_d_line_7": 0,
        "schedule_d_line_15": 0,
        "schedule_d_line_16": 0,
        "schedule_d_line_21": 0
    }

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.net_short_term_gain_loss == -609

def test_net_short_term_gain_loss_with_loss_carryover():
    context = tax_context.tax_context(2025)
    context.constants = y_2025
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

    prior_year_return = {
        "form_1040_line_15": 0,
        "schedule_d_line_7": 0,
        "schedule_d_line_15": 0,
        "schedule_d_line_16": 0,
        "schedule_d_line_21": 0
    }

    context.schedule_d.short_term_capital_loss_carryover = 5000

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.net_short_term_gain_loss == -6000

def test_net_long_term_gain_loss_without_loss_carryover():
    context = tax_context.tax_context(2025)
    context.constants = y_2025
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

    prior_year_return = {
        "form_1040_line_15": 0,
        "schedule_d_line_7": 0,
        "schedule_d_line_15": 0,
        "schedule_d_line_16": 0,
        "schedule_d_line_21": 0
    }

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.net_long_term_gain_loss == -609

def test_net_long_term_gain_loss_with_loss_carryover():
    context = tax_context.tax_context(2025)
    context.constants = y_2025
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

    prior_year_return = {
        "form_1040_line_15": 0,
        "schedule_d_line_7": 0,
        "schedule_d_line_15": 0,
        "schedule_d_line_16": 0,
        "schedule_d_line_21": 0
    }

    context.schedule_d.long_term_capital_loss_carryover = 5000

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.net_long_term_gain_loss == -6000

def test_net_long_term_gain_loss_includes_capital_gain_distributions():
    context = tax_context.tax_context(2025)
    context.constants = y_2025
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

    prior_year_return = {
        "form_1040_line_15": 0,
        "schedule_d_line_7": 0,
        "schedule_d_line_15": 0,
        "schedule_d_line_16": 0,
        "schedule_d_line_21": 0
    }

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.capital_gain_distributions == 500
    assert context.schedule_d.net_long_term_gain_loss == 1500  # 1000 gain + 500 cap gain distributions

def test_aggregate_adjustments_all_codes():
    context = tax_context.tax_context(2025)
    context.constants = y_2025          # needed because the net total is a loss,
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
    context = tax_context.tax_context(2025)
    context.constants = y_2025
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

    prior_year_return = {
        "form_1040_line_15": 0,
        "schedule_d_line_7": 0,
        "schedule_d_line_15": 0,
        "schedule_d_line_16": 0,
        "schedule_d_line_21": 0
    }

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.line_16 == -10000  # the real, uncapped loss
    assert context.schedule_d.line_21 == -3000   # capped at the $3,000 limit
    assert context.form_1040.line_7a == -3000    # what actually flows to the 1040

def test_net_loss_under_limit_is_not_capped():
    context = tax_context.tax_context(2025)
    context.constants = y_2025
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

    prior_year_return = {
        "form_1040_line_15": 0,
        "schedule_d_line_7": 0,
        "schedule_d_line_15": 0,
        "schedule_d_line_16": 0,
        "schedule_d_line_21": 0
    }

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.line_16 == -1500
    assert context.schedule_d.line_21 == -1500   # under the limit, so unchanged
    assert context.form_1040.line_7a == -1500

def test_net_gain_with_long_term_gain_takes_line_17_yes_path():
    context = tax_context.tax_context(2025)
    context.constants = y_2025
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

    prior_year_return = {
        "form_1040_line_15": 0,
        "schedule_d_line_7": 0,
        "schedule_d_line_15": 0,
        "schedule_d_line_16": 0,
        "schedule_d_line_21": 0
    }

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
    context = tax_context.tax_context(2025)
    context.constants = y_2025
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

    prior_year_return = {
        "form_1040_line_15": 0,
        "schedule_d_line_7": 0,
        "schedule_d_line_15": 0,
        "schedule_d_line_16": 0,
        "schedule_d_line_21": 0
    }

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
    context = tax_context.tax_context(2025)
    context.constants = y_2025
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

    prior_year_return = {
        "form_1040_line_15": 0,
        "schedule_d_line_7": 0,
        "schedule_d_line_15": 0,
        "schedule_d_line_16": 0,
        "schedule_d_line_21": 0
    }

    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert context.schedule_d.line_17 is False
    assert context.schedule_d.line_22 is True

def test_filing_schedule_d_required_for_short_term_sale():
    context = tax_context.tax_context(2025)
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
    context = tax_context.tax_context(2025)
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
    context = tax_context.tax_context(2025)
    context.schedule_b.dividend_entries.append({
        "payer": "Fidelity",
        "ordinary_dividends": 0,
        "qualified_dividends": 0,
        "cap_gain_distributions": 500,
        "unrecaptured_sec_1250_gain": 0,
        "fed_tax_withheld": 0,
        "section_199a_dividends": 0
    })

    prior_year_return = {
        "form_1040_line_15": 0,
        "schedule_d_line_7": 0,
        "schedule_d_line_15": 0,
        "schedule_d_line_16": 0,
        "schedule_d_line_21": 0
    }

    # capital_gain_distributions is only populated by aggregation
    schedule_d.aggregate_schedule_d(context, prior_year_return)

    assert schedule_d.is_filing_schedule_d(context) == True

def test_filing_schedule_d_required_for_short_term_carryover_only():
    context = tax_context.tax_context(2025)
    context.schedule_d.short_term_capital_loss_carryover = 2000

    assert schedule_d.is_filing_schedule_d(context) == True

def test_filing_schedule_d_required_for_long_term_carryover_only():
    context = tax_context.tax_context(2025)
    context.schedule_d.long_term_capital_loss_carryover = 2000

    assert schedule_d.is_filing_schedule_d(context) == True

def test_filing_schedule_d_not_required_with_no_activity():
    context = tax_context.tax_context(2025)

    assert schedule_d.is_filing_schedule_d(context) == False