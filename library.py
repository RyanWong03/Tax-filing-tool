import os, json

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
            prior_return["short_term_carryover_to_next_year"] = float(input("Enter short-term carryover shown on worksheet (0 if none): "))
            prior_return["long_term_carryover_to_next_year"] = float(input("Enter long-term carryover shown on worksheet (0 if none): "))

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
        "short_term_carryover_to_next_year": 0,
        "long_term_carryover_to_next_year": 0
    }

def save_tax_return(tax_year, tax_return):
    path = os.path.join(get_data_dir(), f"tax_return_{tax_year}.json")
    with open(path, "w") as f:
        json.dump(tax_return, f, indent=4)
