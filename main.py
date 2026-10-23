import importlib
import federal.forms.f1040
import federal.forms.form_8949
import federal.forms.schedule_b
import tax_context

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
        'context': context
    }

    federal.forms.schedule_b.collect_1099_int(context)
    federal.forms.schedule_b.collect_1099_div(context)
    federal.forms.form_8949.collect_1099_b_short_term(context)
    federal.forms.form_8949.collect_1099_b_long_term(context)
    federal.forms.f1040.calculate(filing_data)


if __name__ == "__main__":
    main()