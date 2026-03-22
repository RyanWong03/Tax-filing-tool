import library

#Interest from 1099-INT forms
def taxable_interest():
    total_interest = 0

    print("Please gather all of your 1099-INT forms.")

    while True:
        try:
            total_interest += library.irs_round(float(input("Enter the total interest from a 1099-INT form (Box 1): ")))

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
    return total_interest