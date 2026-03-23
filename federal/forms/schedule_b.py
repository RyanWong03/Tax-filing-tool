import library

#Enums for determining which section of Schedule B to fill out
INTEREST = 0
DIVIDENDS = 1

#Interest from 1099-INT forms
def taxable_interest():
    total_interest = 0

    print("Please gather all of your 1099-INT forms.")

    interest_forms = {
        "payers": [],
        "amounts": []
    }

    while True:
        try:
            payer = input("Enter the name of the payer from a 1099-INT form: ").strip()
            interest_forms["payers"].append(payer)

            amount = library.irs_round(float(input("Enter the total interest from the 1099-INT form (Box 1): ")))
            interest_forms["amounts"].append(amount)
            total_interest += amount

            more_1099_int = None
            while True:
                more_1099_int = input("Do you have another 1099-INT to enter? (yes/no): ").strip().lower()
                if more_1099_int == 'no' or more_1099_int == 'yes':
                    break
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")
            
            if more_1099_int == 'no':
                break
        except ValueError:
            print("Invalid input. Please enter a numeric value for interest.")
    
    print(f"Total interest collected: ${total_interest:.2f}")
    #print(interest_forms)

    if total_interest > 1500:
        res = schedule_b_fillout(interest_forms, INTEREST)
        print(res)
    return total_interest

def schedule_b_fillout(form_data, section):
    fields = []
    if section == INTEREST:
        fields.append("Part 1: Interest\n")
        for index, (payer, amount) in enumerate(zip(form_data["payers"], form_data["amounts"])):
            print(type(payer))
            print(type(amount))
            print(amount)
            fields.append(f"Line {index + 1}: {payer} ... ${amount:.2f}\n")
    
    return fields