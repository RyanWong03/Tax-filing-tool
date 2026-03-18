import library

def calculate(filing_data):
    constants = filing_data['constants']
    filing_status = filing_data['filing_status']
    wages = filing_data['wages']
    standard_deduction = constants.STANDARD_DEDUCTION[filing_status]

    line_1a = wages
    line_1z = line_1a #Total wages
    
    line_9 = line_1z #Total income

    line_11 = line_9 #AGI

    line_12 = standard_deduction

    line_14 = line_12 #AGI - standard deduction

    line_15 = max(0, line_11 - line_14) #Taxable income

    line_16 = calculate_income_tax(line_15, constants.TAX_BRACKETS[filing_status]) #Tax owed


def calculate_income_tax(taxable_income, tax_brackets):
    tax = 0

    for lower, upper, rate in tax_brackets:
        if taxable_income <= lower:
            break
        taxable_at_rate = min(taxable_income, upper) - lower
        tax += taxable_at_rate * rate
    
    return library.irs_round(tax)