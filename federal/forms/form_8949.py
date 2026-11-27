import math
import library
import form_fillout
from itertools import zip_longest
import os

ENTRIES_PER_FORM = 11

# Field numbers on f8949.pdf for each part of the form
SHORT_TERM_PART = {"checkboxes": {"A": 3, "B": 4, "C": 5}, "first_row": 9, "totals": 97}
LONG_TERM_PART = {"checkboxes": {"D": 104, "E": 105, "F": 106}, "first_row": 110, "totals": 198}

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
                proceeds = library.irs_round(float(input("Enter the proceeds from the sale: ")))
                cost_basis = library.irs_round(float(input("Enter the cost basis of the property: ")))
                accrued_market_discount = float(input("Enter any accrued market discount (enter 0 if none): "))
                wash_sale_loss = library.irs_round(float(input("Enter any wash sale loss (enter 0 if none): ")))
                federal_tax_withheld = library.irs_round(float(input("Enter any federal tax withheld (enter 0 if none): ")))
                state_tax_withheld = library.irs_round(float(input("Enter any state tax withheld (enter 0 if none): ")))
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
                    "federal_tax_withheld": federal_tax_withheld,
                    "state_tax_withheld": state_tax_withheld
                })

                if accrued_market_discount > 0:
                    context.schedule_b.interest_entries.append({
                        "payer": payer,
                        "amount": accrued_market_discount,
                        "bond_interest": 0,
                        "early_withdrawal_penalty": 0,
                        "federal_tax_withheld": 0,
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

#Long term stock sales from 1099-B forms
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
                proceeds = library.irs_round(float(input("Enter the proceeds from the sale: ")))
                cost_basis = library.irs_round(float(input("Enter the cost basis of the property: ")))
                accrued_market_discount = float(input("Enter any accrued market discount (enter 0 if none): "))
                wash_sale_loss = library.irs_round(float(input("Enter any wash sale loss (enter 0 if none): ")))
                federal_tax_withheld = library.irs_round(float(input("Enter any federal tax withheld (enter 0 if none): ")))
                state_tax_withheld = library.irs_round(float(input("Enter any state tax withheld (enter 0 if none): ")))
                adjustment_code = None #Really the only code we'll have is 'W' for wash sale

                if wash_sale_loss > 0:
                    adjustment_code = 'W'
                
                gain = proceeds - cost_basis + wash_sale_loss

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
                        "federal_tax_withheld": 0,
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

def page_path(context, i, x):
    return f"{library.get_data_dir()}/{context.tax_year}/federal/form_8949_{i}_{x}.pdf"

def fill_part(context, entries, code, x, part, i):
    """Fills one page (up to 11 rows) of Part I or Part II. Short-term and long-term
    for the same i/x share one physical sheet, so reuse the page if it already exists."""
    path = page_path(context, i, x)
    source = path if os.path.exists(path) else f"{library.FED_FORM_DIR}f8949.pdf"
    form = form_fillout.Form(source)

    form.put(part["checkboxes"][code], True)

    proceeds_sum = 0
    cost_basis_sum = 0
    adjustments_sum = 0
    gain_sum = 0

    field = part["first_row"]
    start = x * ENTRIES_PER_FORM
    end = min(len(entries), start + ENTRIES_PER_FORM)
    for entry in entries[start:end]:
        form.put(field, entry["description"])
        form.put(field + 1, entry["date_acquired"])
        form.put(field + 2, entry["date_sold"])
        form.put(field + 3, entry["proceeds"])
        form.put(field + 4, entry["cost_basis"])
        if entry["adjustments"] != 0:
            form.put(field + 5, entry["adjustment_code"])
            form.put(field + 6, entry["adjustments"])
        form.put(field + 7, library.pdf_amount(entry["gain"]))

        proceeds_sum += entry["proceeds"]
        cost_basis_sum += entry["cost_basis"]
        adjustments_sum += entry["adjustments"]
        gain_sum += entry["gain"]
        field += 8

    totals = part["totals"]
    form.put(totals, proceeds_sum)
    form.put(totals + 1, cost_basis_sum)
    if adjustments_sum != 0:
        form.put(totals + 3, adjustments_sum)   # field totals+2 is skipped (code column)
    form.put(totals + 4, gain_sum)

    form.save(path)

def form_8949_fillout(context):
    short = context.form_8949.short_term_entries
    long = context.form_8949.long_term_entries

    present_short = [k for k, v in short.items() if v]
    present_long = [k for k, v in long.items() if v]

    # i = which code pair (A with D, B with E, ...). x = which continuation page for that code.
    for i, (short_code, long_code) in enumerate(zip_longest(present_short, present_long)):
        if short_code is not None:
            for x in range(math.ceil(len(short[short_code]) / ENTRIES_PER_FORM)):
                fill_part(context, short[short_code], short_code, x, SHORT_TERM_PART, i)

        if long_code is not None:
            for x in range(math.ceil(len(long[long_code]) / ENTRIES_PER_FORM)):
                fill_part(context, long[long_code], long_code, x, LONG_TERM_PART, i)