import library, json, os, federal.forms.f1040

class schedule_d_context:
    def __init__(self):
        #Short term
        self.code_a_proceeds_total = 0
        self.code_a_cost_basis_total = 0
        self.code_a_adjustments_total = 0
        self.code_a_gain_loss_total = 0

        self.code_b_proceeds_total = 0
        self.code_b_cost_basis_total = 0
        self.code_b_adjustments_total = 0
        self.code_b_gain_loss_total = 0

        self.code_c_proceeds_total = 0
        self.code_c_cost_basis_total = 0
        self.code_c_adjustments_total = 0
        self.code_c_gain_loss_total = 0

        self.short_term_capital_loss_carryover = 0
        self.net_short_term_gain_loss = 0

        #Long term
        self.code_d_proceeds_total = 0
        self.code_d_cost_basis_total = 0
        self.code_d_adjustments_total = 0
        self.code_d_gain_loss_total = 0

        self.code_e_proceeds_total = 0
        self.code_e_cost_basis_total = 0
        self.code_e_adjustments_total = 0
        self.code_e_gain_loss_total = 0

        self.code_f_proceeds_total = 0
        self.code_f_cost_basis_total = 0
        self.code_f_adjustments_total = 0
        self.code_f_gain_loss_total = 0

        self.long_term_capital_loss_carryover = 0
        self.net_long_term_gain_loss = 0

        #Part 3
        self.unrecaptured_section_1250_gain = 0


def aggregate_schedule_d(context, prior_year_return):
    #TODO Make sure all check boxes are accounted for in this form and if any other forms have make sure to fix those.
    #can just put true/false as yes/no
    #TODO Did you dispose of any investment(s) in a qualified opportunity fund during the tax year? checkbox
    #Short term
    context.schedule_d.code_a_proceeds_total = library.irs_round(sum(entry["proceeds"] for entry in context.form_8949.short_term_entries["A"]))
    context.schedule_d.code_b_proceeds_total = library.irs_round(sum(entry["proceeds"] for entry in context.form_8949.short_term_entries["B"]))
    context.schedule_d.code_c_proceeds_total = library.irs_round(sum(entry["proceeds"] for entry in context.form_8949.short_term_entries["C"]))

    context.schedule_d.code_a_cost_basis_total = library.irs_round(sum(entry["cost_basis"] for entry in context.form_8949.short_term_entries["A"]))
    context.schedule_d.code_b_cost_basis_total = library.irs_round(sum(entry["cost_basis"] for entry in context.form_8949.short_term_entries["B"]))
    context.schedule_d.code_c_cost_basis_total = library.irs_round(sum(entry["cost_basis"] for entry in context.form_8949.short_term_entries["C"]))

    context.schedule_d.code_a_adjustments_total = library.irs_round(sum(entry["adjustments"] for entry in context.form_8949.short_term_entries["A"]))
    context.schedule_d.code_b_adjustments_total = library.irs_round(sum(entry["adjustments"] for entry in context.form_8949.short_term_entries["B"]))
    context.schedule_d.code_c_adjustments_total = library.irs_round(sum(entry["adjustments"] for entry in context.form_8949.short_term_entries["C"]))

    context.schedule_d.code_a_gain_loss_total = library.irs_round(sum(entry["gain"] for entry in context.form_8949.short_term_entries["A"]))
    context.schedule_d.code_b_gain_loss_total = library.irs_round(sum(entry["gain"] for entry in context.form_8949.short_term_entries["B"]))
    context.schedule_d.code_c_gain_loss_total = library.irs_round(sum(entry["gain"] for entry in context.form_8949.short_term_entries["C"]))

    #Lines 4 and 5 omitted; irrelevant to us.

    #Check if we need to fill out capital loss carryover worksheet. Line 6
    if prior_year_return["schedule_d_line_21"] < 0 \
    and (prior_year_return["schedule_d_line_21"] < prior_year_return["schedule_d_line_16"] \
        or prior_year_return["form_1040_line_15"] < 0):
        compute_capital_loss_carryover_worksheet(context, prior_year_return)

    #Line 7
    context.schedule_d.net_short_term_gain_loss = library.irs_round(context.schedule_d.code_a_gain_loss_total +
                                                                    context.schedule_d.code_b_gain_loss_total +
                                                                    context.schedule_d.code_c_gain_loss_total +
                                                                    context.schedule_d.short_term_capital_loss_carryover)

    #Long term
    context.schedule_d.code_d_proceeds_total = library.irs_round(sum(entry["proceeds"] for entry in context.form_8949.long_term_entries["D"]))
    context.schedule_d.code_e_proceeds_total = library.irs_round(sum(entry["proceeds"] for entry in context.form_8949.long_term_entries["E"]))
    context.schedule_d.code_f_proceeds_total = library.irs_round(sum(entry["proceeds"] for entry in context.form_8949.long_term_entries["F"]))

    context.schedule_d.code_d_cost_basis_total = library.irs_round(sum(entry["cost_basis"] for entry in context.form_8949.long_term_entries["D"]))
    context.schedule_d.code_e_cost_basis_total = library.irs_round(sum(entry["cost_basis"] for entry in context.form_8949.long_term_entries["E"]))
    context.schedule_d.code_f_cost_basis_total = library.irs_round(sum(entry["cost_basis"] for entry in context.form_8949.long_term_entries["F"]))

    context.schedule_d.code_d_adjustments_total = library.irs_round(sum(entry["adjustments"] for entry in context.form_8949.long_term_entries["D"]))
    context.schedule_d.code_e_adjustments_total = library.irs_round(sum(entry["adjustments"] for entry in context.form_8949.long_term_entries["E"]))
    context.schedule_d.code_f_adjustments_total = library.irs_round(sum(entry["adjustments"] for entry in context.form_8949.long_term_entries["F"]))

    context.schedule_d.code_d_gain_loss_total = library.irs_round(sum(entry["gain"] for entry in context.form_8949.long_term_entries["D"]))
    context.schedule_d.code_e_gain_loss_total = library.irs_round(sum(entry["gain"] for entry in context.form_8949.long_term_entries["E"]))
    context.schedule_d.code_f_gain_loss_total = library.irs_round(sum(entry["gain"] for entry in context.form_8949.long_term_entries["F"]))

    #Lines 11 and 12 omitted; irrelevant to us.

    #Line 13
    context.schedule_d.capital_gain_distributions = library.irs_round(sum(entry["cap_gain_distributions"] for entry in context.schedule_b.dividend_entries))

    #Line 14 is already computed in line 6 above.

    #Line 15
    context.schedule_d.net_long_term_gain_loss = library.irs_round(context.schedule_d.code_d_gain_loss_total +
                                                                   context.schedule_d.code_e_gain_loss_total +
                                                                   context.schedule_d.code_f_gain_loss_total +
                                                                   context.schedule_d.capital_gain_distributions +
                                                                   context.schedule_d.long_term_capital_loss_carryover)

    #Part 3

    line_16 = context.schedule_d.net_short_term_gain_loss + context.schedule_d.net_long_term_gain_loss

    if line_16 > 0:
        context.form_1040.line_7a = line_16
        #Line 17
        if context.schedule_d.net_long_term_gain_loss > 0 and line_16 > 0:
            #Line 18 omitted; irrelevant to us. #TODO 28% rate gain worksheet
            line_18 = 0 #Hardcoded for line 20

            if context.schedule_b.unrecaptured_sec_1250_gain > 0: #Only relevant case for us.
                #Line 19
                compute_unrecaptured_section_1250_gain_worksheet(context)

            #Line 20, #TODO handle form 4952
            if line_18 == 0 and context.schedule_d.unrecaptured_section_1250_gain == 0:
                #For now we are hardcoding that we are not filing form 4952.
                federal.forms.f1040.compute_qualified_dividends_and_capital_gain_tax_worksheet(context)

            
    if line_16 < 0 or line_16 > 0:
        #line 21

    if line_16 == 0:
        context.form_1040.line_7a = 0

    #line 22

#Builds the json dump of the capital loss carryover worksheet and saves it to the user's local app data directory.
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

def compute_unrecaptured_section_1250_gain_worksheet(context):
    worksheet = {"tax_year": context.tax_year}

    #Lines 1-9 omitted; irrelevant to us.

    line_10 = 0 #Hardcode to 0; irrevelant to us
    line_11 = context.schedule_b.unrecaptured_sec_1250_gain #Schedule K-1, Form 2439, Form 1099-R are irrelevant to us.
    line_12 = 0 #Hardcode to 0; irrevelant to us
    line_13 = line_10 + line_11 + line_12
    line_14 = 0 #Hardcode to 0; irrevelant to us
    line_15 = min(context.schedule_d.net_short_term_gain_loss, 0)
    line_16 = context.schedule_d.long_term_capital_loss_carryover #Schedule K-1 irrelevant to us.
    line_17 = abs(min(line_14 + line_15 + line_16, 0))
    line_18 = max(line_13 - line_17, 0)

    worksheet["line_10"] = line_10
    worksheet["line_11"] = line_11
    worksheet["line_12"] = line_12
    worksheet["line_13"] = line_13
    worksheet["line_14"] = line_14
    worksheet["line_15"] = line_15
    worksheet["line_16"] = line_16
    worksheet["line_17"] = line_17
    worksheet["line_18"] = line_18

    if line_18 > 0:
        context.schedule_d.unrecaptured_section_1250_gain = line_18

    save_unrecaptured_section_1250_gain_worksheet(context, worksheet)

def save_unrecaptured_section_1250_gain_worksheet(context, worksheet):
    local_app_data_dir = library.get_data_dir()
    worksheet_file = os.path.join(local_app_data_dir, f"unrecaptured_section_1250_gain_worksheet_{context.tax_year}.json")

    with open(worksheet_file, "w") as f:
        json.dump(worksheet, f, indent=4)

def is_filing_schedule_d(context):
    has_short_term_sales = any(context.form_8949.short_term_entries[code] for code in context.form_8949.short_term_entries)
    has_long_term_sales = any(context.form_8949.long_term_entries[code] for code in context.form_8949.long_term_entries)
    has_cap_gain_distributions = context.schedule_d.cap_gain_distributions != 0
    has_capital_loss_carryover = context.schedule_d.short_term_capital_loss_carryover != 0 or context.schedule_d.long_term_capital_loss_carryover != 0

    return has_short_term_sales or has_long_term_sales or has_cap_gain_distributions or has_capital_loss_carryover