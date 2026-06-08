#Rounds to the nearest whole dollar. Cents <= 0.49 get dropped, cents >= 0.50 get rounded up.
def irs_round(amount):
    if amount >= 0: return int(amount + 0.5)
    else: return -int(-amount + 0.5)

#Rounds to the nearest whole dollar
def irs_round_form_8949(amount):
    return round(amount % 1, 2)