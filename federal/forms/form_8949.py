import library, tax_context

class form_8949_context:
    def __init__(self):
        self.short_term_entries = {
            "A": [],
            "B": [],
            "C": [],
        }

        self.long_term_entries = {

        }

#Short term stock sales from 1099-B forms
def collect_1099_b_short_term(context: tax_context.tax_context):
    while True:
        short_term_codes = input("Enter the code(s) that are most applicable to you, based on your 1099-B(s), separated by spaces (Example: A B C)" \
        "(A) Short-term transactions reported on Form(s) 1099-B showing basis was reported to the IRS" \
        "(B) Short-term transactions reported on Form 1099-B without basis reported to the IRS" \
        "(C) Short-term transactions, other than digital asset transactions, not reported to you on Form 1099-B or Form 1099-DA")
        #"(G) Short-term transactions reported on Form(s) 1099-DA showing basis was reported to the IRS " \
        #"(H) Short-term transactions reported on Form(s) 1099-DA showing basis was not reported to the IRS" \
        #"(I) Short-term digital asset transactions not reported to you on Form 1099-DA or Form 1099-B")
        
        codes = short_term_codes.split(' ')
        for code in codes:
            try:
                print(f"Enter all sales associated with code {code} from you 1099-B(s): ")
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
                
                gain = proceeds - cost_basis + wash_sale_loss

                context.form_8949.short_term_entries[code.strip().capitalize()].append({
                    "description": description,
                    "date_acquired": date_acquired,
                    "date_sold": date_sold,
                    "proceeds": proceeds,
                    "cost_basis": cost_basis,
                    "adjustments": wash_sale_loss,  #Can hardcode this for now since we're only handling wash sales. Change in future (if nec.).
                    "adjustment_code": adjustment_code,
                    "gain": gain,
                })

                while True:
                    more_1099_b = input("Do you have more 1099-B entries to add? (yes/no): ").strip().lower()
                    if more_1099_b == 'no' or more_1099_b == 'yes':
                        break
                    else:
                        print("Invalid input. Please enter 'yes' or 'no'.")
