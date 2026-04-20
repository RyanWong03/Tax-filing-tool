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

    form_avail = input("Please gather all of your 1099-INT forms. If none, enter 'n', otherwise press Enter. ")

    if form_avail == "n": return [0,0]

    interest_forms = {
        "payers": [],
        #Each index is an array. First index stores the interest from anything except U.S. Savings Bonds.
        #second index stores the interest from U.S. Savings Bonds only. These are exempt from state tax
        "amounts": [] 
    }

    while True:
        try:
            payer = input("Enter the name of the payer from a 1099-INT form: ").strip()
            amount = library.irs_round(float(input("Enter the total interest from the 1099-INT form (Box 1): ")))
            early_withdrawal_penalty = library.irs_round(float(input("Enter the total early withdrawal penalty from the 1099-INT form (Box 2): ")))

            #Not taxable by state and local, but is taxable federally.
            bond_interest = library.irs_round(float(input("Enter the total interest on U.S. Savings Bonds from the 1099-INT form (Box 3): ")))

            fed_tax_withheld = library.irs_round(float(input("Enter the total federal income tax withheld from the 1099-INT form (Box 4): ")))

            #Exempt federally, taxed by state or local.
            tax_exempt_interest = library.irs_round(float(input("Enter the total tax-exempt interest from the 1099-INT form (Box 8): ")))

            amounts_arr = [amount, bond_interest]
            interest_forms["payers"].append(payer)
            interest_forms["amounts"].append(amounts_arr)
            taxable_interest += (amount + bond_interest)

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
    
    print(f"Total taxable interest collected: ${taxable_interest:.2f}")

    if taxable_interest > 1500:
        res = schedule_b_fillout(interest_forms, INTEREST)
        print(res)
    return [taxable_interest, fed_tax_withheld]

def total_dividends():
    total_ordinary_dividends = 0
    total_qualified_dividends = 0

    print("Please gather all of your 1099-DIV forms.")

    dividend_forms = {
        "payers": [],
        #Each index is an array. First index stores the ordinary dividends.
        #Second index stores the qualified dividends.
        "amounts": []
    }

    while True:
        try:
            payer = input("Enter the name of the payer from a 1099-DIV form: ").strip()
            dividend_forms["payers"].append(payer)

            ordinary_dividends = library.irs_round(float(input("Enter the total ordinary dividends from the 1099-DIV form (Box 1a): ")))
            qualified_dividends = library.irs_round(float(input("Enter the total qualified dividends from the 1099-DIV form (Box 1b): ")))
            dividends_arr = [ordinary_dividends, qualified_dividends]
            dividend_forms["amounts"].append(dividends_arr)
            total_ordinary_dividends += ordinary_dividends
            total_qualified_dividends += qualified_dividends

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
    return [total_ordinary_dividends, total_qualified_dividends]

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