import federal.forms.schedule_b
import federal.forms.form_8949
import federal.forms.schedule_d

class tax_context():
    def __init__(self, tax_year):
        self.tax_year = tax_year
        self.filing_status = None
        self.constants = None
        self.form_1040 = federal.forms.f1040.form_1040_context()
        self.schedule_b = federal.forms.schedule_b.schedule_b_context()
        self.form_8949 = federal.forms.form_8949.form_8949_context()
        self.schedule_d = federal.forms.schedule_d.schedule_d_context()