import library
import json
import os

#TODO Change every form so it just uses worksheet["line_x"] instead of creating local variables for each line.

class schedule_d_context:
    def __init__(self):
        self.disposal_qof = None

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
        self.capital_gain_distributions = 0
        self.net_long_term_gain_loss = 0

        #Part 3
        self.line_16 = 0
        self.line_17 = None
        self.rate_gain_28 = 0
        self.unrecaptured_section_1250_gain = 0
        self.line_20 = None
        self.line_21 = 0
        self.line_22 = None

#Main schedule D function. Handles everything in Schedule D form.
def aggregate_schedule_d(context, prior_year_return):
    #TODO Make sure all check boxes are accounted for in this form and if any other forms have make sure to fix those.
    #can just put true/false as yes/no

    context.schedule_d.disposal_qof = False #Hardcode for now since irrevelant for us.
    
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

    #TODO #Lines 4 and 5 omitted; irrelevant to us.

    #Check if we need to fill out capital loss carryover worksheet. Line 6
    if prior_year_return["schedule_d_line_21"] < 0 \
    and (prior_year_return["schedule_d_line_21"] > prior_year_return["schedule_d_line_16"] \
        or prior_year_return["form_1040_line_15"] < 0):
        (context.schedule_d.short_term_capital_loss_carryover,
         context.schedule_d.long_term_capital_loss_carryover) \
        = compute_capital_loss_carryover_worksheet(context, prior_year_return)

    #Line 7
    context.schedule_d.net_short_term_gain_loss = library.irs_round(context.schedule_d.code_a_gain_loss_total +
                                                                    context.schedule_d.code_b_gain_loss_total +
                                                                    context.schedule_d.code_c_gain_loss_total -
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

    #TODO #Lines 11 and 12 omitted; irrelevant to us.

    #Line 13
    context.schedule_d.capital_gain_distributions = library.irs_round(sum(entry["cap_gain_distributions"] for entry in context.schedule_b.dividend_entries))

    #Line 14 is already computed in line 6 above.

    #Line 15
    context.schedule_d.net_long_term_gain_loss = library.irs_round(context.schedule_d.code_d_gain_loss_total +
                                                                   context.schedule_d.code_e_gain_loss_total +
                                                                   context.schedule_d.code_f_gain_loss_total +
                                                                   context.schedule_d.capital_gain_distributions -
                                                                   context.schedule_d.long_term_capital_loss_carryover)

    #Part 3

    context.schedule_d.line_16 = context.schedule_d.net_short_term_gain_loss + context.schedule_d.net_long_term_gain_loss

    if context.schedule_d.line_16 > 0:
        context.form_1040.line_7a = context.schedule_d.line_16
        #Line 17
        if context.schedule_d.net_long_term_gain_loss > 0 and context.schedule_d.line_16 > 0:
            context.schedule_d.line_17 = True
            #Line 18 omitted; irrelevant to us. #TODO 28% rate gain worksheet
            context.schedule_d.rate_gain_28 = 0 #Hardcoded for line 20

            if context.schedule_b.unrecaptured_sec_1250_gain > 0: #Only relevant case for us.
                #Line 19
                context.schedule_d.unrecaptured_section_1250_gain = compute_unrecaptured_section_1250_gain_worksheet(context)

            #Line 20, #TODO handle form 4952
            if context.schedule_d.rate_gain_28 == 0 and context.schedule_d.unrecaptured_section_1250_gain == 0:
                #For now we are hardcoding that we are not filing form 4952.
                #True means fill out Qualified Dividends and Capital Gain Tax Worksheet for Form 1040 - line 16
                context.schedule_d.line_20 = True
            else:
                #False means fill out Schedule D Tax Worksheet for Form 1040 - line 16
                context.schedule_d.line_20 = False

            return #Don't fill lines 21 and 22. We're done here
        else:
            context.schedule_d.line_17 = False
            context.schedule_d.line_22 = context.form_1040.line_3a > 0
            return

    if context.schedule_d.line_16 < 0:
        #line 21
        loss_limit = context.constants.SCHEDULE_D_CAPITAL_LOSS_DEDUCTION_LIMIT[context.filing_status]
        context.schedule_d.line_21 = -(min(abs(context.schedule_d.line_16), loss_limit))
        context.form_1040.line_7a = context.schedule_d.line_21

    if context.schedule_d.line_16 == 0:
        context.form_1040.line_7a = 0

    context.schedule_d.line_22 = context.form_1040.line_3a > 0

#Builds the json dump of the capital loss carryover worksheet and saves it to the user's local app data directory.
#Arguments:
#   context: The tax context object containing the current tax year and other relevant information.
#   prior_year_return: A dictionary containing the prior year's tax return data
#Return values:
#   short_term_capital_loss_carryover: The computed short-term capital loss carryover amount.
#   long_term_capital_loss_carryover: The computed long-term capital loss carryover
def compute_capital_loss_carryover_worksheet(context, prior_year_return):
    worksheet = {"tax_year": context.tax_year}
    short_term_capital_loss_carryover = 0
    long_term_capital_loss_carryover = 0

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
            short_term_capital_loss_carryover = line_8
    else:
        line_5 = 0
        worksheet["line_5"] = line_5

    if prior_year_return["schedule_d_line_15"] >= 0:
        save_capital_loss_carryover_worksheet(context, worksheet)
        return short_term_capital_loss_carryover, long_term_capital_loss_carryover

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
        long_term_capital_loss_carryover = line_13

    save_capital_loss_carryover_worksheet(context, worksheet)
    return short_term_capital_loss_carryover, long_term_capital_loss_carryover
    
def save_capital_loss_carryover_worksheet(context, worksheet):
    local_app_data_dir = library.get_data_dir()
    worksheet_file = os.path.join(local_app_data_dir, f"capital_loss_carryover_worksheet_{context.tax_year}.json")

    with open(worksheet_file, "w") as f:
        json.dump(worksheet, f, indent=4)

#Computes the unrecaptured section 1250 gain worksheet and saves it to the user's local app data directory.
#Arguments:
#   context: The tax context object containing the current tax year and other relevant information.
#Return values:
#   unrecaptured_section_1250_gain: The computed unrecaptured section 1250 gain amount.
def compute_unrecaptured_section_1250_gain_worksheet(context):
    worksheet = {"tax_year": context.tax_year}
    unrecaptured_section_1250_gain = 0

    #Lines 1-9 omitted; irrelevant to us.

    worksheet["line_10"] = 0 #Hardcode to 0; irrevelant to us
    worksheet["line_11"] = context.schedule_b.unrecaptured_sec_1250_gain #Schedule K-1, Form 2439, Form 1099-R are irrelevant to us.
    worksheet["line_12"] = 0 #Hardcode to 0; irrevelant to us
    worksheet["line_13"] = worksheet["line_10"] + worksheet["line_11"] + worksheet["line_12"]
    worksheet["line_14"] = 0 #Hardcode to 0; irrevelant to us
    worksheet["line_15"] = min(context.schedule_d.net_short_term_gain_loss, 0)
    worksheet["line_16"] = -context.schedule_d.long_term_capital_loss_carryover #Schedule K-1 irrelevant to us.
    worksheet["line_17"] = abs(min(worksheet["line_14"] + worksheet["line_15"] + worksheet["line_16"], 0))
    worksheet["line_18"] = max(worksheet["line_13"] - worksheet["line_17"], 0)

    if worksheet["line_18"] > 0:
        unrecaptured_section_1250_gain = worksheet["line_18"]

    save_unrecaptured_section_1250_gain_worksheet(context, worksheet)
    return unrecaptured_section_1250_gain

def save_unrecaptured_section_1250_gain_worksheet(context, worksheet):
    local_app_data_dir = library.get_data_dir()
    worksheet_file = os.path.join(local_app_data_dir, f"unrecaptured_section_1250_gain_worksheet_{context.tax_year}.json")

    with open(worksheet_file, "w") as f:
        json.dump(worksheet, f, indent=4)

#Computes the Schedule D Tax Worksheet and saves it to the user's local app data directory.
#Arguments:
#   context: The tax context object containing the current tax year and other relevant information.
#Return values:
#   total_tax: The total tax for form 1040 - line 16
def compute_schedule_d_tax_worksheet(context):
    worksheet = {"tax_year": context.tax_year}
    schedule_d_tax_worksheet_lines_1_22(context, worksheet)

    if worksheet["line_1"] != worksheet["line_16"]:
        schedule_d_tax_worksheet_lines_23_32(context, worksheet)

        if worksheet["line_1"] != worksheet["line_32"]:
            schedule_d_tax_worksheet_lines_33_34(worksheet)

            if context.schedule_d.unrecaptured_section_1250_gain != 0:
                schedule_d_tax_worksheet_lines_35_40(context, worksheet)

            if context.schedule_d.rate_gain_28 != 0:
                schedule_d_tax_worksheet_lines_41_43(worksheet)

    total_tax = schedule_d_tax_worksheet_lines_44_47(context, worksheet)
    save_schedule_d_tax_worksheet(context, worksheet)
    return total_tax

#Computes the Schedule D Tax Worksheet lines 1 through 22.
#Arguments:
#   context: The tax context object containing the current tax year and other relevant information.
#   worksheet: A dictionary to store the computed values for the Schedule D Tax Worksheet lines 1 through 22.
def schedule_d_tax_worksheet_lines_1_22(context, worksheet):
    #Ignore Form 2555 stuff
    worksheet["line_1"] = context.form_1040.line_15
    worksheet["line_2"] = context.form_1040.line_3a
    worksheet["line_3"] = 0 #TODO: Implement form 4952
    worksheet["line_4"] = 0 #TODO: Implement form 4952
    worksheet["line_5"] = max(worksheet["line_3"] - worksheet["line_4"], 0)
    worksheet["line_6"] = max(worksheet["line_2"] - worksheet["line_5"], 0)
    worksheet["line_7"] = min(context.schedule_d.net_long_term_gain_loss, context.schedule_d.line_16)

    worksheet["line_8"] = min(worksheet["line_3"], worksheet["line_4"])
    worksheet["line_9"] = max(worksheet["line_7"] - worksheet["line_8"], 0)
    worksheet["line_10"] = worksheet["line_6"] + worksheet["line_9"]
    worksheet["line_11"] = context.schedule_d.rate_gain_28 + context.schedule_d.unrecaptured_section_1250_gain
    worksheet["line_12"] = min(worksheet["line_9"], worksheet["line_11"])
    worksheet["line_13"] = worksheet["line_10"] - worksheet["line_12"]
    worksheet["line_14"] = max(worksheet["line_1"] - worksheet["line_13"], 0)
    worksheet["line_15"] = context.constants.QDCGT_ZERO_RATE_MAX[context.filing_status]
    worksheet["line_16"] = min(worksheet["line_1"], worksheet["line_15"])
    worksheet["line_17"] = min(worksheet["line_14"], worksheet["line_16"])
    worksheet["line_18"] = max(worksheet["line_1"] - worksheet["line_10"], 0)

    tax_rate_24_percent = context.constants.TAX_BRACKETS[context.filing_status][3] #24% tax rate
    if tax_rate_24_percent[2] != 0.24:
        raise ValueError(f"Tax rates have changed, expected 0.24 for 24% tax rate, got {tax_rate_24_percent[2]}")
    
    worksheet["line_19"] = min(worksheet["line_1"], tax_rate_24_percent[1]) #24% tax rate upper limit
    worksheet["line_20"] = min(worksheet["line_14"], worksheet["line_19"])
    worksheet["line_21"] = max(worksheet["line_18"], worksheet["line_20"])
    worksheet["line_22"] = worksheet["line_16"] - worksheet["line_17"] #This is taxed at 0% rate

#Computes the Schedule D Tax Worksheet lines 23 through 32.
#Arguments:
#   context: The tax context object containing the current tax year and other relevant information.
#   worksheet: A dictionary to store the computed values for the Schedule D Tax Worksheet lines 23 through 32.
def schedule_d_tax_worksheet_lines_23_32(context, worksheet):
    worksheet["line_23"] = min(worksheet["line_1"], worksheet["line_13"])
    worksheet["line_24"] = worksheet["line_22"]
    worksheet["line_25"] = max(worksheet["line_23"] - worksheet["line_24"], 0)
    worksheet["line_26"] = context.constants.QDCGT_FIFTEEN_RATE_MAX[context.filing_status]
    worksheet["line_27"] = min(worksheet["line_1"], worksheet["line_26"])
    worksheet["line_28"] = worksheet["line_21"] + worksheet["line_22"]
    worksheet["line_29"] = max(worksheet["line_27"] - worksheet["line_28"], 0)
    worksheet["line_30"] = min(worksheet["line_25"], worksheet["line_29"])
    worksheet["line_31"] = library.irs_round(worksheet["line_30"] * 0.15)
    worksheet["line_32"] = worksheet["line_24"] + worksheet["line_30"]

#Computes the Schedule D Tax Worksheet lines 33 through 34.
#Arguments:
#   worksheet: A dictionary to store the computed values for the Schedule D Tax Worksheet lines 33 through 34.
def schedule_d_tax_worksheet_lines_33_34(worksheet):
    worksheet["line_33"] = worksheet["line_23"] - worksheet["line_32"]
    worksheet["line_34"] = library.irs_round(worksheet["line_33"] * 0.20)

#Computes the Schedule D Tax Worksheet lines 35 through 40.
#Arguments:
#   context: The tax context object containing the current tax year and other relevant information.
#   worksheet: A dictionary to store the computed values for the Schedule D Tax Worksheet lines 35 through 40.
def schedule_d_tax_worksheet_lines_35_40(context, worksheet):
    worksheet["line_35"] = min(worksheet["line_9"], context.schedule_d.unrecaptured_section_1250_gain)
    worksheet["line_36"] = worksheet["line_10"] + worksheet["line_21"]
    worksheet["line_37"] = worksheet["line_1"]
    worksheet["line_38"] = max(worksheet["line_36"] - worksheet["line_37"], 0)
    worksheet["line_39"] = max(worksheet["line_35"] - worksheet["line_38"], 0)
    worksheet["line_40"] = library.irs_round(worksheet["line_39"] * 0.25)

#Computes the Schedule D Tax Worksheet lines 41 through 43.
#Arguments:
#   worksheet: A dictionary to store the computed values for the Schedule D Tax Worksheet lines 41 through 43.
def schedule_d_tax_worksheet_lines_41_43(worksheet):
    worksheet["line_41"] = sum(worksheet.get(f"line_{n}") or 0 for n in [21, 22, 30, 33, 39])
    worksheet["line_42"] = worksheet["line_1"] - worksheet["line_41"]
    worksheet["line_43"] = library.irs_round(worksheet["line_42"] * 0.28)

#Computes the Schedule D Tax Worksheet lines 44 through 47.
#Arguments:
#   context: The tax context object containing the current tax year and other relevant information.
#   worksheet: A dictionary to store the computed values for the Schedule D Tax Worksheet lines 44 through 47.
#Return values:
#   line_47: The tax on all taxable income to be included on Form 1040 - line 16.
def schedule_d_tax_worksheet_lines_44_47(context, worksheet):
    worksheet["line_44"] = library.calculate_income_tax(worksheet["line_21"], context.constants.TAX_BRACKETS[context.filing_status])
    worksheet["line_45"] = sum(worksheet.get(f"line_{n}") or 0 for n in [31, 34, 40, 43, 44])
    worksheet["line_46"] = library.calculate_income_tax(worksheet["line_1"], context.constants.TAX_BRACKETS[context.filing_status])

    #We can ignore Form 2555
    worksheet["line_47"] = min(worksheet["line_45"], worksheet["line_46"])
    return worksheet["line_47"]

def save_schedule_d_tax_worksheet(context, worksheet):
    path = os.path.join(library.get_data_dir(), f"schedule_d_tax_worksheet_{context.tax_year}.json")
    with open(path, "w") as f:
        json.dump(worksheet, f, indent=4)

def is_filing_schedule_d(context):
    has_short_term_sales = any(context.form_8949.short_term_entries[code] for code in context.form_8949.short_term_entries)
    has_long_term_sales = any(context.form_8949.long_term_entries[code] for code in context.form_8949.long_term_entries)
    has_cap_gain_distributions = context.schedule_d.capital_gain_distributions != 0
    has_capital_loss_carryover = context.schedule_d.short_term_capital_loss_carryover != 0 or context.schedule_d.long_term_capital_loss_carryover != 0

    return has_short_term_sales or has_long_term_sales or has_cap_gain_distributions or has_capital_loss_carryover

#TODO: Implement function that actually fill out the form(s). May not need to fill out the supplemental worksheets.