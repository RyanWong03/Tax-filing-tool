import library

class schedule_b_context:
    def __init__(self):
        #These two will be list of dicts. Each dict will have the keys "payer" and "amounts".
        self.interest_entries = []
        self.dividend_entries = []

        #Interest (mainly from 1099-INT forms, but not limited to 1099-INT forms)
        self.taxable_interest = 0
        self.early_withdrawal_penalty = 0
        self.interest_on_savings_bonds = 0
        self.federal_tax_withheld_interest = 0
        self.tax_exempt_interest = 0

        #Dividends (mainly from 1099-DIV forms, but not limited to 1099-DIV forms)
        self.ordinary_dividends = 0
        self.qualified_dividends = 0
        self.cap_gain_distributions = 0
        self.unrecaptured_sec_1250_gain = 0
        self.federal_tax_withheld_dividends = 0
        self.section_199a_dividends = 0


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
def collect_1099_int(context: library.tax_context):
    form_avail = input("Please gather all of your 1099-INT forms. If none, enter 'n', otherwise press Enter. ")

    if form_avail == "n": return

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

            context.schedule_b.interest_entries.append({
                "payer": payer,
                "amount": amount,
                "bond_interest": bond_interest,
                "early_withdrawal_penalty": early_withdrawal_penalty,
                "fed_tax_withheld": fed_tax_withheld,
                "tax_exempt_interest": tax_exempt_interest
            })

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
def collect_1099_div(context: library.tax_context):
    form_avail = input("Please gather all of your 1099-DIV forms. If none, enter 'n', otherwise press Enter. ")

    if form_avail == "n": return

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

            context.schedule_b.dividend_entries.append({
                "payer": payer,
                "ordinary_dividends": ordinary_dividends,
                "qualified_dividends": qualified_dividends,
                "cap_gain_distributions": cap_gain_distributions,
                "unrecaptured_sec_1250_gain": unrecaptured_sec_1250_gain,
                "fed_tax_withheld": fed_tax_withheld,
                "section_199a_dividends": section_199a_dividends
            })

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
    
def schedule_b_fillout(context: library.tax_context):
    if context.schedule_b.taxable_interest > 1500:
        print("Part 1: Interest\n")
        for index, entry in enumerate(context.schedule_b.interest_entries):
            print(f"Line {index + 1}: {entry['payer']} ... ${(entry['amount'] + entry['bond_interest']):.2f}\n")

    if context.schedule_b.ordinary_dividends > 1500:
        print("Part 2: Dividends\n")
        for index, entry in enumerate(context.schedule_b.dividend_entries):
            print(f"Line {index + 1}: {entry['payer']} ... ${entry['ordinary_dividends']:.2f}\n")