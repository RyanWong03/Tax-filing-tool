import importlib
import federal.forms.f1040
import federal.forms.form_8949
import federal.forms.schedule_b
import tax_context
import library

def load_year(year):
    try:
        module = importlib.import_module(f'federal.tax_years.y_{year}')
        return module
    except ImportError:
        raise ValueError(f"Tax year {year} is not supported.")

def main():
    print("=== TAX ASSISTANT ===")

    while True:
        try:
            year = int(input("Enter the tax year you are filing for (e.g., 2026): "))
            tax_year = load_year(year)
            break
        except ValueError:
            print("Invalid tax year. Please try again.")


    while True:
        filing_status = input("Enter your filing status (single/married_filing_jointly): ").strip().lower()
        if filing_status not in tax_year.STANDARD_DEDUCTION:
            print("Invalid filing status. Please try again.")
        else:
            break

    context = tax_context.tax_context(year)
    context.filing_status = filing_status
    context.constants = tax_year
    w2_data = federal.forms.f1040.collect_w2()

    wages = w2_data["wages"]
    w2_federal_tax_withheld = w2_data["w2_federal_tax_withheld"]

    filing_data = {
        'year': year,
        'wages': wages,
        'w2_federal_tax_withheld': w2_federal_tax_withheld,
        'context': context,
        'amount_refunded_to_taxpayer': 0,
        'apply_estimated_tax_next_year': 0,
    }

    federal.forms.schedule_b.collect_1099_int(context)
    federal.forms.schedule_b.collect_1099_div(context)
    federal.forms.form_8949.collect_1099_b_short_term(context)
    federal.forms.form_8949.collect_1099_b_long_term(context)
    federal.forms.f1040.calculate(filing_data)

    refund = context.form_1040.line_34
    if refund > 0:
        while True:
            filing_data["amount_refunded_to_taxpayer"] = library.irs_round(float(input(
                "Enter the amount based on line 34 that you want refunded to you. "
                "Note: the amount you put will be rounded to the nearest whole number. "
            )))
            #TODO: Implement routing/account number and type of bank account.
            filing_data["apply_estimated_tax_next_year"] = library.irs_round(float(input(
                f"Enter the amount based on line 34 that you want applied to your {year + 1} estimated tax."
                "Note: the amount you put will be rounded to the nearest whole number."
            )))

            if filing_data["amount_refunded_to_taxpayer"] >= 0 and \
            filing_data["apply_estimated_tax_next_year"] >= 0 and \
            filing_data["amount_refunded_to_taxpayer"] + filing_data["apply_estimated_tax_next_year"] == refund:
                break

            #If we reached here, the taxpayer's math is incorrect and needs to be redone.
            print(f"The two amounts must add up to ${refund}. Please try again.")

        #Calling calculate a second time just for refund and estimated tax.
        #Not sure if best way but for now, will suffice.
        federal.forms.f1040.calculate(filing_data)

    federal.forms.f1040.save_current_year_return(context)
    federal.forms.f1040.print_summary(context)
    federal.forms.schedule_b.schedule_b_fillout(context)


if __name__ == "__main__":
    main()