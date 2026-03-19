import math, library

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
    print(line_16)

    line_17 = 0 #Placeholder 

    line_18 = line_16 + line_17 

    line_21 = 0 #Placeholder

    line_22 = 0 if line_18 - line_21 < 0 else line_18 - line_21

    line_23 = 0 #Placeholder

    line_24 = line_22 + line_23 #Total tax owed
    print(f"Total tax owed: ${line_24:.2f}")

    line_25a = 0 #Federal income tax withheld from W-2s
    line_25b = 0 #Federal income tax withheld from 1099s

    while True:
        try:
            line_25a += library.irs_round(float(input("Enter the total federal income tax withheld from your W-2 forms (Box 2 on your W-2): ")))

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
            print("Invalid input. Please enter a numeric value for federal income tax withheld from W-2s.")

    while True:
        try:
            line_25b += library.irs_round(float(input("Enter the total federal income tax withheld from your 1099 forms (Box 4 on your 1099): ")))
            
            more_1099 = None
            while True:
                more_1099 = input("Do you have another 1099 to enter? (yes/no): ").strip().lower()
                if more_1099 == 'no' or more_1099 == 'yes':
                    break
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")
            
            if more_1099 == 'no':
                break
        except ValueError:
            print("Invalid input. Please enter a numeric value for federal income tax withheld from 1099s.")

    line_25d = line_25a + line_25b

    line_26 = 0 #Placeholder

    line_27a = 0 #Placeholder
    line_28 = 0 #Placeholder
    line_29 = 0 #Placeholder
    line_30 = 0 #Placeholder
    line_31 = 0 #Placeholder
    line_32 = line_27a + line_28 + line_29 + line_30 + line_31 #Total other payments and refundable credits

    line_33 = line_25d + line_26 + line_32 #Total payments

    line_34 = (line_33 - line_24) if (line_33 > line_24) else 0 #Overpaid amount in taxes

    print(f"Refund amount: ${line_34:.2f}")

def calculate_income_tax(taxable_income, tax_brackets):
    tax = 0

    #If taxable income is under $100,000, calculate tax using IRS tax table via 1040 instructions.
    if taxable_income < 100000:
        #The way the IRS calculates the tax owed on income under $100k, is by figuring out which $50 slot you are in,
        #getting the midpoint of that slot then applying the tax brackets to that income.
        #Example income = $15019:
        #You'd fall between the slot of $15000 and $15050, so the midpoint would be $15025.
        #Then you'd apply the tax brackets to $15025 to get your tax owed.

        income_slot = math.floor(taxable_income / 50) * 50
        income_midpoint = income_slot + 25
        taxable_income = income_midpoint
        
        for lower, upper, rate in tax_brackets:
            if taxable_income <= lower:
                break
            taxable_at_rate = min(taxable_income, upper) - lower
            tax += taxable_at_rate * rate
    
    return library.irs_round(tax)