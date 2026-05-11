import federal.forms.schedule_b

class tax_context():
    def __init__(self):
        self.schedule_b = federal.forms.schedule_b.schedule_b_context()

def irs_round(amount):
    if amount >= 0: return int(amount + 0.5)
    else: return -int(-amount + 0.5)