import library

#Enums for determining which section of Schedule B to fill out
INTEREST = 0
DIVIDENDS = 1

#Interest from 1099-INT forms
#Only the fields from the form that are expected from me are implemented.
#Not implemented:
# - Box 5: Investment expenses
# - Box 6: Foreign tax paid
# - Box 7: Foreign country or U.S. possession
# - Box 9: Specified private activity bond interest
# - Box 10: Market discount
# - Box 11: Bond premium
# - Box 12: Bond premium on Treasury obligations
# - Box 13: Bond premium on tax-exempt bond obligations
# - Box 14: Tax-exempt bond CUSIP no.
#For boxes 15-17, it's unlikely these will be filled out. If they are, we can handle these manually.
def total_interest():
    taxable_interest = 0

    interest_forms = {
        "payers": [],
        #Each index is an array. First index stores the interest from anything except U.S. Savings Bonds.
        #second index stores the interest from U.S. Savings Bonds only. These are exempt from state tax
        "amounts": [] 
    }

    form_data = {
        "taxable_interest": 0,
        "early_withdrawal_penalty": 0,
        "interest_on_savings_bonds": 0,
        "federal_tax_withheld": 0,
        "tax_exempt_interest": 0
    }

    form_avail = input("Please gather all of your 1099-INT forms. If none, enter 'n', otherwise press Enter. ")

    if form_avail == "n": return form_data

    while True:
        try:
            payer = input("Enter the name of the payer from a 1099-INT form: ").strip()
            amount = float(input("Enter the total interest from the 1099-INT form (Box 1): "))
            early_withdrawal_penalty = library.irs_round(float(input("Enter the total early withdrawal penalty from the 1099-INT form (Box 2): ")))

            #Not taxable by state and local, but is taxable federally.
            bond_interest = float(input("Enter the total interest on U.S. Savings Bonds from the 1099-INT form (Box 3): "))

            fed_tax_withheld = library.irs_round(float(input("Enter the total federal income tax withheld from the 1099-INT form (Box 4): ")))

            #Exempt federally, taxed by state or local.
            tax_exempt_interest = library.irs_round(float(input("Enter the total tax-exempt interest from the 1099-INT form (Box 8): ")))

            taxable_interest += amount + bond_interest
            amounts_arr = [library.irs_round(amount), library.irs_round(bond_interest)]
            interest_forms["payers"].append(payer)
            interest_forms["amounts"].append(amounts_arr)

            #Populating return dict
            form_data["taxable_interest"] = library.irs_round(amount + bond_interest)
            form_data["early_withdrawal_penalty"] = early_withdrawal_penalty
            form_data["interest_on_savings_bonds"] = bond_interest
            form_data["federal_tax_withheld"] = fed_tax_withheld
            form_data["tax_exempt_interest"] = tax_exempt_interest

            more_1099_int = None
            while True:
                more_1099_int = input("Do you have another 1099-INT to enter? (yes/no): ").strip().lower()
                if more_1099_int == 'no' or more_1099_int == 'yes':
                    break
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")
            
            if more_1099_int == 'no':
                break
        except ValueError:
            print("Invalid input. Please enter a numeric value for interest.")
    
    print(f"Total taxable interest collected: ${form_data["taxable_interest"]:.2f}")

    if taxable_interest > 1500:
        res = schedule_b_fillout(interest_forms, INTEREST)
        print(res)
    return form_data

#Dividends from 1099-DIV forms
#Only the fields from the form that are expected from me are implemented.
#Not implemented:
# - Box 2c: Section 1202 gain
# - Box 2d: Collectibles (28%) gain
# - Box 2e: Section 897 Ordinary Dividends
# - Box 2f: Section 897 Capital gain
# - Box 3: Nondividend distributions
# - Box 6: Investment expenses  
# - Box 7: Foreign tax paid
# - Box 8: Foreign country or U.S. possession
# - Box 9: Cash liquidation distributions
# - Box 10: Noncash liquidation distributions
# - Box 12: Exempt-interest dividends
# - Box 13: Specified private activity bond dividends
#For boxes 14-16, it's unlikely these will be filled out. If they are, we can handle these manually.
def total_dividends():
    total_ordinary_dividends = 0

    dividend_forms = {
        "payers": [],
        #Each index is an array. First index stores the ordinary dividends.
        #Second index stores the qualified dividends.
        "amounts": []
    }

    form_data = {
        "ordinary_dividends": 0,
        "qualified_dividends": 0,
        "cap_gain_distributions": 0,
        "unrecaptured_sec_1250_gain": 0,
        "federal_tax_withheld": 0,
        "section_199a_dividends": 0
    }

    form_avail = input("Please gather all of your 1099-DIV forms. If none, enter 'n', otherwise press Enter. ")

    if form_avail == "n": return form_data

    while True:
        try:
            payer = input("Enter the name of the payer from a 1099-DIV form: ").strip()

            ordinary_dividends = library.irs_round(float(input("Enter the total ordinary dividends from the 1099-DIV form (Box 1a): ")))
            qualified_dividends = library.irs_round(float(input("Enter the total qualified dividends from the 1099-DIV form (Box 1b): ")))
            cap_gain_distributions = library.irs_round(float(input("Enter the total capital gain distributions from the 1099-DIV form (Box 2a): ")))
            
            #line 2b, must complete Unrecaptured Section 1250 Gain Worksheet in schedule d instructions. line 2b goes onto line 11 of the worksheet.
            #for worksheet skip lines, 1-10, 12, 14.
            #here just return line 2b val basically, but later on in schedule D, we need to fill out the worksheet to fill in line 19 of schedule D.
            unrecaptured_sec_1250_gain = library.irs_round(float(input("Enter the total Unrecaptured Section 1250 gains from the 1099-DIV form (Box 2b): ")))

            fed_tax_withheld = library.irs_round(float(input("Enter the total federal income tax withheld from the 1099-DIV form (Box 4): ")))

            #box 5, section 199a dividends, need to fill out form 8995 with info. check taxable income though, if made enough later on, will need to fill 8995-A instead
            section_199a_dividends = library.irs_round(float(input("Enter the total Section 199A dividends from the 1099-DIV form (Box 5): ")))

            dividends_arr = [ordinary_dividends]
            dividend_forms["payers"].append(payer)
            dividend_forms["amounts"].append(dividends_arr)
            total_ordinary_dividends += ordinary_dividends

            #Populating return dict
            form_data["ordinary_dividends"] = ordinary_dividends
            form_data["qualified_dividends"] = qualified_dividends
            form_data["cap_gain_distributions"] = cap_gain_distributions
            form_data["unrecaptured_sec_1250_gain"] = unrecaptured_sec_1250_gain
            form_data["federal_tax_withheld"] = fed_tax_withheld
            form_data["section_199a_dividends"] = section_199a_dividends

            more_1099_div = None
            while True:
                more_1099_div = input("Do you have another 1099-DIV to enter? (yes/no): ").strip().lower()
                if more_1099_div == 'no' or more_1099_div == 'yes':
                    break
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")
            
            if more_1099_div == 'no':
                break
        except ValueError:
            print("Invalid input. Please enter a numeric value for dividends.")
    
    print(f"Total ordinary dividends collected: ${total_ordinary_dividends:.2f}")

    if total_ordinary_dividends > 1500:
        res = schedule_b_fillout(dividend_forms, DIVIDENDS)
        print(res)

    return form_data

def schedule_b_fillout(form_data, section):
    fields = []
    if section == INTEREST:
        fields.append("Part 1: Interest\n")
        for index, (payer, amount) in enumerate(zip(form_data["payers"], form_data["amounts"])):
            fields.append(f"Line {index + 1}: {payer} ... ${(amount[0] + amount[1]):.2f}\n")
    elif section == DIVIDENDS:
        fields.append("Part 2: Dividends\n")
        for index, (payer, amount) in enumerate(zip(form_data["payers"], form_data["amounts"])):
            fields.append(f"Line {index + 1}: {payer} ... ${amount[0]:.2f}\n")
    
    return fields