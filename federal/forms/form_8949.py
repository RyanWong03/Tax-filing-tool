import library, tax_context

class form_8949_context:
    def __init__(self):
        self.entries = []

#Short term stock sales from 1099-B forms
#Only the fields from the form that are expected from me are implemented.
#Not implemented:
# - Box 
def collect_1099_b_short_term(context: tax_context.tax_context):
    while True:
        input("Enter the code(s) that are most applicable to you, separated by spaces (Example: A B C)" \
        "(A) Short-term transactions reported on Form(s) 1099-B showing basis was reported to the IRS" \
        "(B) Short-term transactions reported on Form 1099-B without basis reported to the IRS" \
        "(C) Short-term transactions, other than digital asset transactions, not reported to you on Form 1099-B or Form 1099-DA" \
        "(G) Short-term transactions reported on Form(s) 1099-DA showing basis was reported to the IRS " \
        "(H) Short-term transactions reported on Form(s) 1099-DA showing basis was not reported to the IRS" \
        "(I) Short-term digital asset transactions not reported to you on Form 1099-DA or Form 1099-B")
        
        print("For each sell in your 1099-B, please provide the following information:")
        try:
            description = input("Enter the description of the property (e.g., '100 shares of XYZ Corp'): ")
            date_acquired = input("Enter the date acquired (MM/DD/YYYY): ")
            date_sold = input("Enter the date sold (MM/DD/YYYY): ")
            proceeds = float(input("Enter the proceeds from the sale: "))
            cost_basis = float(input("Enter the cost basis of the property: "))

            adjustments = {}
            adjustment_amount = float(input("Enter any adjustments (enter 0 if none): ")) 
            adjustments['adjustment_amount'] = adjustment_amount

            adjustment_code = None

            if adjustment_amount > 0:
                adjustment_code = input("Enter the code provided in box 1f")

            adjustments['adjustment_code'] = adjustment_code

            context.form_8949.entries.append({
                "description": description,
                "date_acquired": date_acquired,
                "date_sold": date_sold,
                "proceeds": proceeds,
                "cost_basis": cost_basis,
                "adjustments": adjustments
            })

            while True:
                more_1099_b = input("Do you have more 1099-B entries to add? (yes/no): ").strip().lower()
                if more_1099_b == 'no' or more_1099_b == 'yes':
                    break
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")
