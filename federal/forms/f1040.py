import math
import library
import federal.forms.schedule_b
import federal,forms.schedule_d
import os
import json

class form_1040_context:
    def __init__(self):
        self.line_1a = 0
        self.line_1z = 0
        self.line_2a = 0
        self.line_2b = 0
        self.line_3a = 0
        self.line_3b = 0
        self.line_7a = 0
        self.line_9 = 0
        self.line_11 = 0
        self.line_12 = 0
        self.line_14 = 0
        self.line_15 = 0
        self.line_16 = 0
        self.line_17 = 0
        self.line_18 = 0
        self.line_21 = 0
        self.line_22 = 0
        self.line_23 = 0
        self.line_24 = 0
        self.line_25a = 0
        self.line_25b = 0
        self.line_25d = 0
        self.line_26 = 0
        self.line_27a = 0
        self.line_28 = 0
        self.line_29 = 0
        self.line_30 = 0
        self.line_31 = 0
        self.line_32 = 0
        self.line_33 = 0
        self.line_34 = 0
        self.line_36 = 0
        self.line_37 = 0

def collect_w2():
    print("Please gather all of your W-2 forms from any jobs you have worked during the year.")

    total_wages = 0
    total_fed_tax_withheld = 0

    form_data = {
        "wages": 0,
        "federal_tax_withheld": 0,
    }

    while True:
        try:
            wages = float(input("Enter the total wages from a W-2 form (Box 1): "))
            
            fed_tax_withheld = float(input("Enter the total federal income tax withheld from the W-2 form (Box 2): "))

            total_wages += wages
            total_fed_tax_withheld += fed_tax_withheld

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
    form_data["federal_tax_withheld"] = library.irs_round(total_fed_tax_withheld)

    return form_data

def calculate(filing_data):
    context = filing_data['context']
    constants = filing_data['constants']
    filing_status = context.filing_status
    tax_year = context.tax_year
    wages = filing_data['wages']
    standard_deduction = constants.STANDARD_DEDUCTION[filing_status]

    prior_year_return = library.load_prior_year_return(tax_year)
    # #testing
    # federal.forms.schedule_b.collect_1099_int(context)
    # federal.forms.schedule_b.collect_1099_div(context)
    #federal.forms.form_8949.collect_1099_b_short_term(context)
    #print(context.form_8949.short_term_entries)
    #federal.forms.form_8949.collect_1099_b_long_term(context)
    #print(context.form_8949.long_term_entries)

    # federal.forms.schedule_b.aggregate_schedule_b(context)

    # print(f"interest entries: {context.schedule_b.interest_entries}")
    # print(f"dividend entries: {context.schedule_b.dividend_entries}")
    # print(f"taxable interest: {context.schedule_b.taxable_interest}")
    # print(f"ordinary dividends: {context.schedule_b.ordinary_dividends}")

    # federal.forms.schedule_b.schedule_b_fillout(context)
    # ####### testing end #######
    # line_1a = wages
    # line_1z = line_1a #Total wages

    # total_interest_data = federal.forms.schedule_b.total_interest() #From 1099-INT forms
    # line_2a = total_interest_data["tax_exempt_interest"]
    # line_2b = total_interest_data["taxable_interest"]

    # total_dividends_data = federal.forms.schedule_b.total_dividends() #From 1099-DIV forms
    # line_3a = total_dividends_data["qualified_dividends"]
    # line_3b = total_dividends_data["ordinary_dividends"]
    
    # line_9 = line_1z + line_2b + line_3b #Total income

    # line_11 = line_9 #AGI

    # line_12 = standard_deduction

    # line_14 = line_12 #AGI - standard deduction

    # line_15 = max(0, line_11 - line_14) #Taxable income

    # print(f"Taxable income: ${line_15:.2f}")

    # line_16 = calculate_income_tax(line_15, constants.TAX_BRACKETS[filing_status]) #Tax owed

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

def calculate_income_tax(taxable_income, tax_brackets):
    tax = 0

    #Protect against $0 or lower case
    if taxable_income <= 0:
        return 0
    
    #If taxable income is under $100,000, calculate tax using IRS tax table via 1040 instructions.
    if taxable_income < 100000:
        #The way the IRS calculates the tax owed on income under $100k, is by figuring out which $50 slot you are in,
        #getting the midpoint of that slot then applying the tax brackets to that income.
        #If you make under $3k, the slot goes from $50 to $25.
        #Example income = $15019:
        #You'd fall between the slot of $15000 and $15050, so the midpoint would be $15025.
        #Then you'd apply the tax brackets to $15025 to get your tax owed.
        #Example income = $1000:
        #You'd fall between the slot of $1000 and $1025, so the midpoint would be $1012.5.

        if taxable_income < 3000:
            income_slot = math.floor(taxable_income / 25) * 25
            income_midpoint = income_slot + 12.5
            taxable_income = income_midpoint
        else:
            income_slot = math.floor(taxable_income / 50) * 50
            income_midpoint = income_slot + 25
            taxable_income = income_midpoint

    #If taxable income is >= $100k, the tax calculation is much more straightforward.
    #There is no table, just basic percentage the IRS has given us.
    #They do differ based on filing status.
        
    for lower, upper, rate in tax_brackets:
        if taxable_income <= lower:
            break
        taxable_at_rate = min(taxable_income, upper) - lower
        tax += taxable_at_rate * rate

    return library.irs_round(tax)

def compute_qualified_dividends_and_capital_gain_tax_worksheet(context):
    worksheet = {"tax_year": context.tax_year}

    #Any lines mentioning Form 2555 are irrelevant to us.
    
    line_1 = context.form_1040.line_15
    line_2 = context.form_1040.line_3a

    if federal.forms.schedule_d.is_filing_schedule_d(context):
        line_3 = min(context.schedule_d.net_long_term_gain_loss, context.schedule_d.line_16)
        if context.schedule_d.net_long_term_gain_loss <= 0 or context.schedule_d.line_16 <= 0:
            line_3 = 0
    else:
        line_3 = context.form_1040.line_7a

    line_4 = line_2 + line_3
    line_5 = max(line_1 - line_4, 0)

    if context.filing_status == "single" or context.filing_status == "married_filing_separately":
        line_6 = 48350
    elif context.filing_status == "married_filing_jointly" or context.filing_status == "qualifying_surviving_spouse":
        line_6 = 96700
    elif context.filing_status == "head_of_household":
        line_6 = 64750
    else:
        line_6 = 48350 #Fallback just in case, but this should never happen.

    line_7 = min(line_1, line_6)
    line_8 = min(line_5, line_7)
    line_9 = line_7 - line_8 #This is taxed at 0%
    line_10 = min(line_1, line_4)
    line_11 = line_9
    line_12 = line_10 - line_11

    if context.filing_status == "single":
        line_13 = 533400
    elif context.filing_status == "married_filing_separately":
        line_13 = 300000
    elif context.filing_status == "married_filing_jointly" or context.filing_status == "qualifying_surviving_spouse":
        line_13 = 600050
    elif context.filing_status == "head_of_household":
        line_13 = 566700
    else:
        line_13 = 533400 #Fallback just in case, but this should never happen

    line_14 = min(line_1, line_13)
    line_15 = line_5 + line_9
    line_16 = max(line_14 - line_15, 0)
    line_17 = min(line_12, line_16)
    line_18 = line_17 * 0.15
    line_19 = line_9 + line_17
    line_20 = line_10 - line_19
    line_21 = line_20 * 0.2
    line_22 = calculate_income_tax(line_5, context.constants.TAX_BRACKETS[context.filing_status])
    line_23 = line_18 + line_21 + line_22
    line_24 = calculate_income_tax(line_1, context.constants.TAX_BRACKETS[context.filing_status])
    line_25 = min(line_23, line_24)
    context.form_1040.line_16 = line_25

    worksheet["line_1"] = line_1
    worksheet["line_2"] = line_2
    worksheet["line_3"] = line_3
    worksheet["line_4"] = line_4
    worksheet["line_5"] = line_5
    worksheet["line_6"] = line_6
    worksheet["line_7"] = line_7
    worksheet["line_8"] = line_8
    worksheet["line_9"] = line_9
    worksheet["line_10"] = line_10
    worksheet["line_11"] = line_11
    worksheet["line_12"] = line_12
    worksheet["line_13"] = line_13
    worksheet["line_14"] = line_14
    worksheet["line_15"] = line_15
    worksheet["line_16"] = line_16
    worksheet["line_17"] = line_17
    worksheet["line_18"] = line_18
    worksheet["line_19"] = line_19
    worksheet["line_20"] = line_20
    worksheet["line_21"] = line_21
    worksheet["line_22"] = line_22
    worksheet["line_23"] = line_23
    worksheet["line_24"] = line_24
    worksheet["line_25"] = line_25

    save_qualified_dividends_and_capital_gain_tax_worksheet(context, worksheet)

def save_qualified_dividends_and_capital_gain_tax_worksheet(context, worksheet):
    local_app_data_dir = library.get_data_dir()
    worksheet_file = os.path.join(local_app_data_dir, f"qualified_dividends_and_capital_gain_tax_worksheet_{context.tax_year}.json")
    
    with open(worksheet_file, "w") as f:
        json.dump(worksheet, f, indent=4)