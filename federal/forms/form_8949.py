import library

class form_8949_context:
    def __init__(self):
        self.short_term_entries = {
            "A": [],
            "B": [],
            "C": [],
        }

        self.long_term_entries = {
            "D": [],
            "E": [],
            "F": [],
        }

#Short term stock sales from 1099-B forms
def collect_1099_b_short_term(context):
    short_term_codes = input("Enter the code(s) that are most applicable to you, based on your 1099-B(s), separated by spaces (Example: A B C)\n" \
    "(A) Short-term transactions reported on Form(s) 1099-B showing basis was reported to the IRS\n" \
    "(B) Short-term transactions reported on Form 1099-B without basis reported to the IRS\n" \
    "(C) Short-term transactions, other than digital asset transactions, not reported to you on Form 1099-B or Form 1099-DA\n" \
    "If you have no short-term transactions, enter X\n")
    #"(G) Short-term transactions reported on Form(s) 1099-DA showing basis was reported to the IRS " \
    #"(H) Short-term transactions reported on Form(s) 1099-DA showing basis was not reported to the IRS" \
    #"(I) Short-term digital asset transactions not reported to you on Form 1099-DA or Form 1099-B")
    
    codes = short_term_codes.split(' ')
    for code in codes:
        if code.strip().upper() == 'X':
            return  #No long-term transactions to enter
        
        print(f"Enter all sales associated with code {code} from you 1099-B(s): ")
        while True:
            try:
                payer = input("Enter the name of the Brokerage: ")
                description = input("Enter the description of the property (e.g., '100 shares of XYZ Corp'): ")
                date_acquired = input("Enter the date acquired (MM/DD/YYYY): ")
                date_sold = input("Enter the date sold (MM/DD/YYYY): ")
                proceeds = float(input("Enter the proceeds from the sale: "))
                cost_basis = float(input("Enter the cost basis of the property: "))
                accrued_market_discount = float(input("Enter any accrued market discount (enter 0 if none): "))
                wash_sale_loss = float(input("Enter any wash sale loss (enter 0 if none): "))
                federal_tax_withheld = float(input("Enter any federal tax withheld (enter 0 if none): "))
                state_tax_withheld = float(input("Enter any state tax withheld (enter 0 if none): "))
                adjustment_code = None #Really the only code we'll have is 'W' for wash sale

                if wash_sale_loss > 0:
                    adjustment_code = 'W'
                
                #Round to 2 decimal places to avoid floating point issues.
                gain = round(proceeds - cost_basis + wash_sale_loss, 2)

                context.form_8949.short_term_entries[code.strip().capitalize()].append({
                    "description": description,
                    "date_acquired": date_acquired,
                    "date_sold": date_sold,
                    "proceeds": proceeds,
                    "cost_basis": cost_basis,
                    "adjustments": wash_sale_loss,  #Can hardcode this for now since we're only handling wash sales. Change in future (if nec.).
                    "adjustment_code": adjustment_code,
                    "gain": gain,
                    "federal_tax_withheld": federal_tax_withheld,
                    "state_tax_withheld": state_tax_withheld
                })

                if accrued_market_discount > 0:
                    context.schedule_b.interest_entries.append({
                        "payer": payer,
                        "amount": accrued_market_discount,
                        "bond_interest": 0,
                        "early_withdrawal_penalty": 0,
                        "fed_tax_withheld": 0,
                        "tax_exempt_interest": 0
                    })

                while True:
                    more_entries = input(f"Do you have more short term entries for code {code} to add? (yes/no): ").strip().lower()
                    if more_entries == 'no' or more_entries == 'yes':
                        break
                    else:
                        print("Invalid input. Please enter 'yes' or 'no'.")
                
                if more_entries == 'no':
                    break
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

def collect_1099_b_long_term(context):
    long_term_codes = input("Enter the code(s) that are most applicable to you, based on your 1099-B(s), separated by spaces (Example: D E F)\n" \
    "(D) Long-term transactions reported on Form(s) 1099-B showing basis was reported to the IRS\n" \
    "(E) Long-term transactions reported on Form(s) 1099-B showing basis was not reported to the IRS\n" \
    "(F) Long-term transactions, other than digital asset transactions, not reported to you on Form 1099-B or Form 1099-DA\n" \
    "If you have no long-term transactions, enter X\n")
    #"(J) Long-term transactions reported on Form(s) 1099-DA showing basis was reported to the IRS " \
    #"(K) Long-term transactions reported on Form(s) 1099-DA showing basis was not reported to the IRS" \
    #"(L) Long-term digital asset transactions not reported to you on Form 1099-DA or Form 1099-B")
    
    codes = long_term_codes.split(' ')
    for code in codes:
        if code.strip().upper() == 'X':
            return  #No long-term transactions to enter
        
        print(f"Enter all sales associated with code {code} from you 1099-B(s): ")
        while True:
            try:
                payer = input("Enter the name of the Brokerage: ")
                description = input("Enter the description of the property (e.g., '100 shares of XYZ Corp'): ")
                date_acquired = input("Enter the date acquired (MM/DD/YYYY): ")
                date_sold = input("Enter the date sold (MM/DD/YYYY): ")
                proceeds = float(input("Enter the proceeds from the sale: "))
                cost_basis = float(input("Enter the cost basis of the property: "))
                accrued_market_discount = float(input("Enter any accrued market discount (enter 0 if none): "))
                wash_sale_loss = float(input("Enter any wash sale loss (enter 0 if none): "))
                federal_tax_withheld = float(input("Enter any federal tax withheld (enter 0 if none): "))
                state_tax_withheld = float(input("Enter any state tax withheld (enter 0 if none): "))
                adjustment_code = None #Really the only code we'll have is 'W' for wash sale

                if wash_sale_loss > 0:
                    adjustment_code = 'W'
                
                #Round to 2 decimal places to avoid floating point issues.
                gain = round(proceeds - cost_basis + wash_sale_loss, 2)

                context.form_8949.long_term_entries[code.strip().capitalize()].append({
                    "description": description,
                    "date_acquired": date_acquired,
                    "date_sold": date_sold,
                    "proceeds": proceeds,
                    "cost_basis": cost_basis,
                    "adjustments": wash_sale_loss,  #Can hardcode this for now since we're only handling wash sales. Change in future (if nec.).
                    "adjustment_code": adjustment_code,
                    "gain": gain,
                    "federal_tax_withheld": federal_tax_withheld,
                    "state_tax_withheld": state_tax_withheld
                })

                if accrued_market_discount > 0:
                    context.schedule_b.interest_entries.append({
                        "payer": payer,
                        "amount": accrued_market_discount,
                        "bond_interest": 0,
                        "early_withdrawal_penalty": 0,
                        "fed_tax_withheld": 0,
                        "tax_exempt_interest": 0
                    })

                while True:
                    more_entries = input(f"Do you have more long term entries for code {code} to add? (yes/no): ").strip().lower()
                    if more_entries == 'no' or more_entries == 'yes':
                        break
                    else:
                        print("Invalid input. Please enter 'yes' or 'no'.")
                
                if more_entries == 'no':
                    break
            except ValueError:
                print("Invalid input. Please enter a numeric value.")