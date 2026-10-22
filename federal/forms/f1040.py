import library
import federal.forms.schedule_b
import federal.forms.schedule_d
import os
import json

class form_1040_context:
    def __init__(self):
        self.line_1a = 0
        self.line_1b = 0
        self.line_1c = 0
        self.line_1d = 0
        self.line_1e = 0
        self.line_1f = 0
        self.line_1g = 0
        self.line_1h = 0
        self.line_1i = 0
        self.line_1z = 0
        self.line_2a = 0
        self.line_2b = 0
        self.line_3a = 0
        self.line_3b = 0
        self.line_3c_childs_dividends_included_in_line_3a = False
        self.line_3c_childs_dividends_included_in_line_3b = False
        self.line_4a = 0
        self.line_4b = 0
        self.line_4c_rollover = False
        self.line_4c_qcd = False
        self.line_4c_misc = False
        self.line_4c_misc_value = ""
        self.line_5a = 0
        self.line_5b = 0
        self.line_5c_rollover = False
        self.line_5c_pso = False
        self.line_5c_misc = False
        self.line_5c_misc_value = ""
        self.line_6a = 0
        self.line_6b = 0
        self.line_6c = False
        self.line_6d = False
        self.line_7a = 0
        self.line_7b_schedule_d_not_required = False
        self.line_7b_includes_childs_capital_gain_loss = False
        self.line_7b_includes_childs_capital_gain_loss_amt = 0
        self.line_8 = 0
        self.line_9 = 0
        self.line_10 = 0
        self.line_11a = 0
        self.line_11b = 0
        self.line_12a_you_are_claimed_as_dependent = False
        self.line_12a_spouse_is_claimed_as_dependent = False
        self.line_12b = False
        self.line_12c = False
        self.line_12d_you_are_age_65_plus = False
        self.line_12d_you_are_blind = False
        self.line_12d_spouse_is_age_65_plus = False
        self.line_12d_spouse_is_blind = False
        self.line_12e = 0
        self.line_13a = 0
        self.line_13b = 0
        self.line_14 = 0
        self.line_15 = 0
        self.line_16_amt = 0
        self.line_16_form_8814 = False
        self.line_16_form_4972 = False
        self.line_16_form_misc = False
        self.line_16_form_misc_value = ""
        self.line_17 = 0
        self.line_18 = 0
        self.line_19 = 0
        self.line_20 = 0
        self.line_21 = 0
        self.line_22 = 0
        self.line_23 = 0
        self.line_24 = 0
        self.line_25a = 0
        self.line_25b = 0
        self.line_25c = 0
        self.line_25d = 0
        self.line_26 = 0
        self.line_27a = 0
        self.line_27b = False
        self.line_27c = False
        self.line_28_reject_actc_claim = False
        self.line_28_actc_amt = 0
        self.line_29 = 0
        self.line_30 = 0
        self.line_31 = 0
        self.line_32 = 0
        self.line_33 = 0
        self.line_34 = 0
        self.line_36 = 0
        self.line_37 = 0
        self.line_38 = 0

def collect_w2():
    print("Please gather all of your W-2 forms from any jobs you have worked during the year.")

    total_wages = 0
    total_w2_fed_tax_withheld = 0

    form_data = {
        "wages": 0,
        "w2_federal_tax_withheld": 0,
    }

    while True:
        try:
            wages = float(input("Enter the total wages from a W-2 form (Box 1): "))
            
            w2_fed_tax_withheld = float(input("Enter the total federal income tax withheld from the W-2 form (Box 2): "))

            total_wages += wages
            total_w2_fed_tax_withheld += w2_fed_tax_withheld

            more_w2 = None
            while True:
                more_w2 = input("Do you have another W-2 to enter? (yes/no): ").strip().lower()
                if more_w2 == 'no' or more_w2 == 'yes':
                    break
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")
            
            if more_w2 == 'no':
                break
        except ValueError:
            print("Invalid input. Please enter a numeric value for wages.")
    
    #Populating return dict
    form_data["wages"] = library.irs_round(total_wages)
    form_data["w2_federal_tax_withheld"] = library.irs_round(total_w2_fed_tax_withheld)

    return form_data

def calculate(filing_data):
    context = filing_data['context']
    constants = filing_data['context'].constants
    filing_status = context.filing_status
    tax_year = context.tax_year
    wages = filing_data['wages']
    w2_federal_tax_withheld = filing_data['w2_federal_tax_withheld']
    standard_deduction = constants.STANDARD_DEDUCTION[filing_status]

    prior_year_return = library.load_prior_year_return(tax_year)

    context.form_1040.line_1a = wages
    #TODO: Check if any of line_1b-i need to be implemented
    context.form_1040.line_1z = context.form_1040.line_1a

    federal.forms.schedule_b.aggregate_schedule_b(context)
    context.form_1040.line_2a = context.schedule_b.tax_exempt_interest
    context.form_1040.line_2b = context.schedule_b.taxable_interest
    context.form_1040.line_3a = context.schedule_b.qualified_dividends
    context.form_1040.line_3b = context.schedule_b.ordinary_dividends
    #Note: line 3c can be left blank since the applicant has no children.

    #TODO: Implement lines 4a-c

    #TODO: Implement lines 5a-c

    #TODO: Implement lines 6a-c

    #Line 7a is set inside aggregate_schedule_d
    federal.forms.schedule_d.aggregate_schedule_d(context, prior_year_return)

    #Note: 7b "Schedule D not required": always unchecked. We file Schedule D whenever there are sales,
    # capital gain distributions, or a loss carryover, even when Exception 1 would let us skip it.
    # "Includes child's capital gain or (loss)": always unchecked (no Form 8814) since the applicant has no children. 

    #TODO: Implement line 8

    #Total income
    #TODO: Append lines 4b, 5b, 6b, 8 once implemented
    context.form_1040.line_9 = sum(x or 0 for x in (
        context.form_1040.line_1z, context.form_1040.line_2b, context.form_1040.line_3b, context.form_1040.line_7a,
    ))

    #TODO: Implement line 10

    #AGI
    context.form_1040.line_11a = context.form_1040.line_9 - context.form_1040.line_10
    context.form_1040.line_11b = context.form_1040.line_11a

    #Note: Line 12a-12d checkboxes: all unchecked. We assume: not claimable as a dependent, not MFS, not
    # dual-status, under 65, not blind. Revisit if any of these change (they change the standard deduction).

    #TODO: Implement Schedule A. Then, change line 12e so it picks between standard/itemized deduction depending on the
    #greater value.
    context.form_1040.line_12e = standard_deduction

    #TODO: Look into the necessity of implementing lines 13a-b

    #TODO: If lines 13a-b get implemented, append those to the sum of line 14
    context.form_1040.line_14 = context.form_1040.line_12e

    context.form_1040.line_15 = max(context.form_1040.line_11b - context.form_1040.line_14, 0)

    if context.schedule_d.line_20 is False:
        context.form_1040.line_16_amt = federal.forms.schedule_d.compute_schedule_d_tax_worksheet(context)
    elif context.schedule_d.line_20 is True or context.schedule_d.line_22 is True:
        context.form_1040.line_16_amt = compute_qualified_dividends_and_capital_gain_tax_worksheet(context)
    else:
        context.form_1040.line_16_amt = library.calculate_income_tax(context.form_1040.line_15, constants.TAX_BRACKETS[filing_status])

    # line_17 = 0 #Placeholder 

    # line_18 = line_16 + line_17 

    # line_21 = 0 #Placeholder

    # line_22 = 0 if line_18 - line_21 < 0 else line_18 - line_21

    # line_23 = 0 #Placeholder

    # line_24 = line_22 + line_23 #Total tax owed

    # print(f"Total tax owed: ${line_24:.2f}")

    # line_25a = filing_data['w2_federal_tax_withheld'] #Federal income tax withheld from W-2s
    # line_25b = 0 #Federal income tax withheld from 1099s

    # print(f"Total federal income tax withheld from W-2s: ${line_25a:.2f}")

    # line_25d = line_25a + line_25b

    # line_26 = 0 #Placeholder

    # line_27a = 0 #Placeholder
    # line_28 = 0 #Placeholder
    # line_29 = 0 #Placeholder
    # line_30 = 0 #Placeholder
    # line_31 = 0 #Placeholder
    # line_32 = line_27a + line_28 + line_29 + line_30 + line_31 #Total other payments and refundable credits

    # line_33 = line_25d + line_26 + line_32 #Total payments

    # line_34 = (line_33 - line_24) if (line_33 > line_24) else 0 #Overpaid amount in taxes

    # print(f"Refund amount: ${line_34:.2f}")

    # line_36 = 0 #Default amount
    # while True:
    #     line_36 = float(input(f"Enter the amount from line 34 you want to apply to your {constants.tax_year+1} estimated tax (if any): "))
    #     if(line_36 > line_34):
    #         print("You cannot apply more than your total refund to estimated taxes. Please try again.")
    #     else:
    #         break

    # line_37 = line_24 - line_33 if (line_24 - line_33 > 0) else 0 #Amount of taxed owed

    # print(f"Amount of tax owed: ${line_37:.2f}")
    # line_38 = 0 #For the sake of this, ignore penalties...

#Computes the Qualified Dividends and Capital Gain Tax Worksheet and saves it to the user's local app data directory.
#Arguments:
#   context: The tax context object containing the current tax year and other relevant information.
#Return values:
#   line_25: The computed tax amount from the Qualified Dividends and Capital Gain Tax Worksheet.
def compute_qualified_dividends_and_capital_gain_tax_worksheet(context):
    worksheet = {"tax_year": context.tax_year}

    #Any lines mentioning Form 2555 are irrelevant to us.
    
    worksheet["line_1"] = context.form_1040.line_15
    worksheet["line_2"] = context.form_1040.line_3a

    if federal.forms.schedule_d.is_filing_schedule_d(context):
        worksheet["line_3"] = [True, min(context.schedule_d.net_long_term_gain_loss, context.schedule_d.line_16)]
        if context.schedule_d.net_long_term_gain_loss <= 0 or context.schedule_d.line_16 <= 0:
            worksheet["line_3"] = [True, 0]
    else:
        worksheet["line_3"] = [False, context.form_1040.line_7a]

    worksheet["line_4"] = worksheet["line_2"] + worksheet["line_3"][1]
    worksheet["line_5"] = max(worksheet["line_1"] - worksheet["line_4"], 0)

    worksheet["line_6"] = context.constants.QDCGT_ZERO_RATE_MAX[context.filing_status]

    worksheet["line_7"] = min(worksheet["line_1"], worksheet["line_6"])
    worksheet["line_8"] = min(worksheet["line_5"], worksheet["line_7"])
    worksheet["line_9"] = worksheet["line_7"] - worksheet["line_8"]  # This is taxed at 0%
    worksheet["line_10"] = min(worksheet["line_1"], worksheet["line_4"])
    worksheet["line_11"] = worksheet["line_9"]
    worksheet["line_12"] = worksheet["line_10"] - worksheet["line_11"]

    worksheet["line_13"] = context.constants.QDCGT_FIFTEEN_RATE_MAX[context.filing_status]

    worksheet["line_14"] = min(worksheet["line_1"], worksheet["line_13"])
    worksheet["line_15"] = worksheet["line_5"] + worksheet["line_9"]
    worksheet["line_16"] = max(worksheet["line_14"] - worksheet["line_15"], 0)
    worksheet["line_17"] = min(worksheet["line_12"], worksheet["line_16"])
    worksheet["line_18"] = library.irs_round(worksheet["line_17"] * 0.15)
    worksheet["line_19"] = worksheet["line_9"] + worksheet["line_17"]
    worksheet["line_20"] = worksheet["line_10"] - worksheet["line_19"]
    worksheet["line_21"] = library.irs_round(worksheet["line_20"] * 0.2)
    worksheet["line_22"] = library.calculate_income_tax(worksheet["line_5"], context.constants.TAX_BRACKETS[context.filing_status])
    worksheet["line_23"] = worksheet["line_18"] + worksheet["line_21"] + worksheet["line_22"]
    worksheet["line_24"] = library.calculate_income_tax(worksheet["line_1"], context.constants.TAX_BRACKETS[context.filing_status])
    worksheet["line_25"] = library.irs_round(min(worksheet["line_23"], worksheet["line_24"]))

    save_qualified_dividends_and_capital_gain_tax_worksheet(context, worksheet)
    return worksheet["line_25"]

def save_qualified_dividends_and_capital_gain_tax_worksheet(context, worksheet):
    local_app_data_dir = library.get_data_dir()
    worksheet_file = os.path.join(local_app_data_dir, f"qualified_dividends_and_capital_gain_tax_worksheet_{context.tax_year}.json")
    
    with open(worksheet_file, "w") as f:
        json.dump(worksheet, f, indent=4)