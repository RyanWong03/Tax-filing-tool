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

    wages = 0
    print("Please gather all of your W-2 forms from any jobs you have worked during the year.")
    while True:
        try:
            wages += library.irs_round(float(input("Enter the total wages from a W-2 form. You will see this on Line 1, "
            "labeled \"Wages, tips, and other compensation\": ")))
            
            more_w2 = None
            while True:
                more_w2 = input("Do you have another W-2 to enter? (yes/no): ").strip().lower()
                if more_w2 == 'no' or more_w2 == 'yes':
                    break
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")
            
            if more_w2 == 'no':
                break
        except ValueError:
            print("Invalid input. Please enter a numeric value for wages.")


    filing_data = {
        'year': year,
        'filing_status': filing_status,
        'wages': wages,
        'constants': tax_year
    }

    federal.forms.f1040.calculate(filing_data)


if __name__ == "__main__":
    main()