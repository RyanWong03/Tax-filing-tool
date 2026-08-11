import library, json, os

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
    worksheet = {"tax_year": context.tax_year}

    line_1 = prior_year_return["form_1040_line_15"]
    line_2 = abs(prior_year_return["schedule_d_line_21"])
    line_3 = max(line_1 + line_2, 0)
    line_4 = min(line_2, line_3)

    worksheet["line_1"] = line_1
    worksheet["line_2"] = line_2
    worksheet["line_3"] = line_3
    worksheet["line_4"] = line_4

    if prior_year_return["schedule_d_line_7"] < 0:
        line_5 = abs(prior_year_return["schedule_d_line_7"])
        line_6 = max(prior_year_return["schedule_d_line_15"], 0)
        line_7 = line_4 + line_6
        line_8 = max(line_5 - line_7, 0)

        worksheet["line_5"] = line_5
        worksheet["line_6"] = line_6
        worksheet["line_7"] = line_7
        worksheet["line_8"] = line_8

        if line_8 > 0:
            context.schedule_d.short_term_capital_loss_carryover = line_8
    else:
        line_5 = 0
        worksheet["line_5"] = line_5

    if prior_year_return["schedule_d_line_15"] >= 0:
        save_capital_loss_carryover_worksheet(context, worksheet)
        return

    line_9 = abs(prior_year_return["schedule_d_line_15"])
    line_10 = max(prior_year_return["schedule_d_line_7"], 0)
    line_11 = max(line_4 - line_5, 0)
    line_12 = line_10 + line_11
    line_13 = max(line_9 - line_12, 0)

    worksheet["line_9"] = line_9
    worksheet["line_10"] = line_10
    worksheet["line_11"] = line_11
    worksheet["line_12"] = line_12
    worksheet["line_13"] = line_13

    if line_13 > 0:
        context.schedule_d.long_term_capital_loss_carryover = line_13

    save_capital_loss_carryover_worksheet(context, worksheet)

def save_capital_loss_carryover_worksheet(context, worksheet):
    local_app_data_dir = library.get_data_dir()
    worksheet_file = os.path.join(local_app_data_dir, f"capital_loss_carryover_worksheet_{context.tax_year}.json")

    with open(worksheet_file, "w") as f:
        json.dump(worksheet, f, indent=4)