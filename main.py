import importlib, library, federal.forms.f1040

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

    w2_data = federal.forms.f1040.collect_w2()

    wages = w2_data["wages"]
    w2_federal_tax_withheld = w2_data["federal_tax_withheld"]

    filing_data = {
        'year': year,
        'filing_status': filing_status,
        'wages': wages,
        'w2_federal_tax_withheld': w2_federal_tax_withheld,
        'constants': tax_year
    }

    federal.forms.f1040.calculate(filing_data)


if __name__ == "__main__":
    main()