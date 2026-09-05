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
    assert context.schedule_d.line_22 is None

def test_aggregate_single_code_a_entry():
    context = tax_context.tax_context(2025)
    context.form_8949.short_term_entries["A"].append({
        "description": "5 shares of Apple",
        "date_acquired": "",
    })