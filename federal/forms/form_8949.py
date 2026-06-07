import library, tax_context

class form_8949_context:
    def __init__(self):
        self.entries = []

def collect_1099_b(context: tax_context.tax_context):
    while True:
        input("Which code(s) are most applicable to you?" \
        "(A) Short-term transactions reported on Form(s) 1099-B showing basis was reported to the IRS" \
        "(B) Short-term transactions reported on Form 1099-B without basis reported to the IRS" \
        "(C) Short-term transactions, other than digital asset transactions, not reported to you on Form 1099-B or Form 1099-DA" \
        "(G) Short-term transactions reported on Form(s) 1099-DA showing basis was reported to the IRS " \
        "(H) Short-term transactions reported on Form(s) 1099-DA showing basis was not reported to the IRS" \
        "(I) Short-term digital asset transactions not reported to you on Form 1099-DA or Form 1099-B")
        
        try:
            description = input("Enter the description of the property (e.g., '100 shares of XYZ Corp'): ")
            date_acquired = input("Enter the date acquired (MM/DD/YYYY): ")
            date_sold = input("Enter the date sold (MM/DD/YYYY): ")
            proceeds = float(input("Enter the proceeds from the sale: "))
            cost_basis = float(input("Enter the cost basis of the property: "))
            adjustments = float(input("Enter any adjustments (enter 0 if none): "))

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
