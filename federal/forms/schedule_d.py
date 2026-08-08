import library, json

class schedule_d_context:
    def __init__(self):
        #Short term
        self.code_a_proceeds_total = 0
        self.code_b_proceeds_total = 0
        self.code_c_proceeds_total = 0

        #Long term
        self.code_d_proceeds_total = 0
        self.code_e_proceeds_total = 0
        self.code_f_proceeds_total = 0

def aggregate_schedule_d(context):
    #Short term
    context.schedule_d.code_a_proceeds_total = library.irs_round(sum(entry["proceeds"] for entry in context.form_8949.short_term_entries["A"]))
    context.schedule_d.code_b_proceeds_total = library.irs_round(sum(entry["proceeds"] for entry in context.form_8949.short_term_entries["B"]))
    context.schedule_d.code_c_proceeds_total = library.irs_round(sum(entry["proceeds"] for entry in context.form_8949.short_term_entries["C"]))

    #Long term
    context.schedule_d.code_d_proceeds_total = library.irs_round(sum(entry["proceeds"] for entry in context.form_8949.long_term_entries["D"]))
    context.schedule_d.code_e_proceeds_total = library.irs_round(sum(entry["proceeds"] for entry in context.form_8949.long_term_entries["E"]))
    context.schedule_d.code_f_proceeds_total = library.irs_round(sum(entry["proceeds"] for entry in context.form_8949.long_term_entries["F"]))

def compute_capital_loss_carryover_worksheet(context, prior_year_return):
    local_app_data_dir = library.get_data_dir()
    previous_tax_year = context.tax_year - 1
    user_prev_year_tax_return_file = f"{local_app_data_dir} + /tax_return_{previous_tax_year}.json"
    worksheet_file = f"{local_app_data_dir} + /capital_loss_carryover_worksheet_{context.tax_year}.json"

    with open(worksheet_file, "w") as wf:
        wf.write("{\n")
        wf.write(f'    "Tax Year: {context.tax_year},\n')
        wf.write(f'    "Line 1: {(line_1 := prior_year_return["form_1040_line_15"])},\n')
        wf.write(f'    "Line 2: {(line_2 := abs(prior_year_return["schedule_d_line_21"]))},\n')
        wf.write(f'    "Line 3: {(line_3 := max(line_1 + line_2, 0))},\n')
        wf.write(f'    "Line 4: {min(line_2, line_3)},\n')

        if prior_year_return["schedule_d_line_7"] < 0:
            wf.write(f'    "Line 5: {abs(prior_year_return["schedule_d_line_7"])},\n')
            wf.write(f'    "Line 6: {max(prior_year_return["schedule_d_line_15"], 0)},\n')
        wf.write("}\n")