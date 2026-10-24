import os
import json
import math

FED_FORM_DIR = "federal/forms/raw_forms/"

#Rounds to the nearest whole dollar. Cents <= 0.49 get dropped, cents >= 0.50 get rounded up.
def irs_round(amount):
    if amount >= 0: return int(amount + 0.5)
    else: return -int(-amount + 0.5)

#Rounds to the nearest whole dollar
def irs_round_form_8949(amount):
    return round(amount % 1, 2)

#Returns user's local app data directory. This is where we store the user's data files.
def get_data_dir():
    if os.name == "nt": # Windows
        return os.path.join(os.environ["LOCALAPPDATA"], "Tax_filing_tool")
    else: # Mac/Linux
        return os.path.join(os.path.expanduser("~"), ".taxtool")

def load_prior_year_return(tax_year):
    path = os.path.join(get_data_dir(), f"tax_return_{tax_year - 1}.json")

    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return bootstrap_prior_year_return(tax_year)
    except json.JSONDecodeError:
        print(f"Warning: {tax_year - 1} tax return exists but is corrupted or invalid.")
        return bootstrap_prior_year_return(tax_year)

#Creates default prior year return. 
def bootstrap_prior_year_return(tax_year):
    print(f"No prior year tax return found for {tax_year - 1}.")
    print("This could be your first time running this tool, or the file may be missing/corrupted.")
    has_prior_return = input(f"Did you file a tax return for {tax_year - 1}? (yes/no): ").strip().lower()

    if has_prior_return.lower() == "no":
        prior_return = default_prior_year_return(tax_year)
    else:
        prior_return = default_prior_year_return(tax_year)
        prior_return["form_1040_line_15"] = float(input(f"Enter Form 1040 line 15 from your {tax_year - 1} return: "))
        has_schedule_d = input("Did you file a Schedule D that year? (yes/no): ").strip().lower()
        if has_schedule_d.lower() == "yes":
            prior_return["schedule_d_line_7"] = float(input(f"Enter Schedule D line 7 from your {tax_year - 1} return: "))
            prior_return["schedule_d_line_15"] = float(input(f"Enter Schedule D line 15 from your {tax_year - 1} return: "))
            prior_return["schedule_d_line_16"] = float(input(f"Enter Schedule D line 16 from your {tax_year - 1} return: "))
            prior_return["schedule_d_line_21"] = float(input(f"Enter Schedule D line 21 from your {tax_year - 1} return: "))

    save_tax_return(tax_year - 1, prior_return)
    return prior_return

def default_prior_year_return(tax_year):
    return {
        "tax_year": tax_year - 1,
        "form_1040_line_15": 0,
        "schedule_d_line_7": 0,
        "schedule_d_line_15": 0,
        "schedule_d_line_16": 0,
        "schedule_d_line_21": 0,
    }

def save_tax_return(tax_year, tax_return):
    os.makedirs(get_data_dir(), exist_ok=True) 
    path = os.path.join(get_data_dir(), f"tax_return_{tax_year}.json")
    with open(path, "w") as f:
        json.dump(tax_return, f, indent=4)

#Calculates income tax owed. If taxable income < $100k, uses tax table, otherwise uses tax computation table.
#Arguments:
#   taxable_income: The taxable income to calculate the tax on
#   tax_brackets: The tax brackets to calculate the tax owed from
#Return values:
#   tax: The tax owed (rounded)
def calculate_income_tax(taxable_income, tax_brackets):
    tax = 0

    #Protect against $0 or lower case
    if taxable_income <= 0:
        return 0
    
    #If taxable income is under $100,000, calculate tax using IRS tax table via 1040 instructions.
    if taxable_income < 100000:
        #The way the IRS calculates the tax owed on income under $100k, is by figuring out which $50 slot you are in,
        #getting the midpoint of that slot then applying the tax brackets to that income.
        #If you make under $3k, the slot goes from $50 to $25.
        #Example income = $15019:
        #You'd fall between the slot of $15000 and $15050, so the midpoint would be $15025.
        #Then you'd apply the tax brackets to $15025 to get your tax owed.
        #Example income = $1000:
        #You'd fall between the slot of $1000 and $1025, so the midpoint would be $1012.5.

        if taxable_income < 3000:
            income_slot = math.floor(taxable_income / 25) * 25
            income_midpoint = income_slot + 12.5
            taxable_income = income_midpoint
        else:
            income_slot = math.floor(taxable_income / 50) * 50
            income_midpoint = income_slot + 25
            taxable_income = income_midpoint

    #If taxable income is >= $100k, the tax calculation is much more straightforward.
    #There is no table, just basic percentage the IRS has given us.
    #They do differ based on filing status.
        
    for lower, upper, rate in tax_brackets:
        if taxable_income <= lower:
            break
        taxable_at_rate = min(taxable_income, upper) - lower
        tax += taxable_at_rate * rate

    return irs_round(tax)