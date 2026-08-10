import library, json

class schedule_d_context:
    def __init__(self):
        #Short term
        self.code_a_proceeds_total = 0
        self.code_b_proceeds_total = 0
        self.code_c_proceeds_total = 0
        self.short_term_capital_loss_carryover = 0

        #Long term
        self.code_d_proceeds_total = 0
        self.code_e_proceeds_total = 0
        self.code_f_proceeds_total = 0
        self.long_term_capital_loss_carryover = 0

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
    worksheet_file = f"{local_app_data_dir} + /capital_loss_carryover_worksheet_{context.tax_year}.json"

    with open(worksheet_file, "w") as wf:
        wf.write("{\n")
        wf.write(f'    "Tax Year: {context.tax_year},\n')
        wf.write(f'    "Line 1: {(line_1 := prior_year_return["form_1040_line_15"])},\n')
        wf.write(f'    "Line 2: {(line_2 := abs(prior_year_return["schedule_d_line_21"]))},\n')
        wf.write(f'    "Line 3: {(line_3 := max(line_1 + line_2, 0))},\n')
        wf.write(f'    "Line 4: {(line_4 := min(line_2, line_3))},\n')

        if prior_year_return["schedule_d_line_7"] < 0:
            wf.write(f'    "Line 5: {(line_5 := abs(prior_year_return["schedule_d_line_7"]))},\n')
            wf.write(f'    "Line 6: {(line_6 := max(prior_year_return["schedule_d_line_15"], 0))},\n')
            wf.write(f'    "Line 7: {(line_7 := line_4 + line_6)},\n')
            wf.write(f'    "Line 8: {(line_8 := max(line_5 - line_7, 0))},\n')

            if line_8 > 0:
                context.schedule_d.short_term_capital_loss_carryover = line_8
        else:
            wf.write(f'    "Line 5: 0,\n')

        if prior_year_return["schedule_d_line_15"] >= 0:
            wf.write("}\n")
            return

        #line 9 starts here
        wf.write(f'    "Line 9: {(line_9 := abs(prior_year_return["schedule_d_line_15"]))},\n')
        wf.write(f'    "Line 10: {(line_10 := max(prior_year_return["schedule_d_line_7"], 0))},\n')
        wf.write(f'    "Line 11: {(line_11 := line_4 - line_5)},\n')
        wf.write(f'    "Line 12: {(line_12 := line_10 + line_11)},\n')
        wf.write(f'    "Line 13: {(line_13 := max(line_9 - line_12, 0))},\n')

        if line_13 > 0:
            context.schedule_d.long_term_capital_loss_carryover = line_13
            
        wf.write("}\n")