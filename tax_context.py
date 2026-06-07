import federal.forms.schedule_b

class tax_context():
    def __init__(self):
        self.schedule_b = federal.forms.schedule_b.schedule_b_context()
        self.form_8949 = federal.forms.form_8949.form_8949_context()