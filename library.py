import os

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