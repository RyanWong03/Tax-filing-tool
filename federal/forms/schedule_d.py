import library

class schedule_d_context:
    def __init__(self):
        #Short term
        self.code_a_proceeds_total = 0
        self.code_b_proceeds_total = 0
        self.code_c_proceeds_total = 0

        #Long term
        self.code_d_proceeds_total = 0
        self.code_e_proceeds_total = 0
        self.code_f_proceeds_total = 0

def aggregate_schedule_d(context):
    #Short term
    context.schedule_d.code_a_proceeds_total = library.irs_round(sum(entry["proceeds"] for entry in context.form_8949.short_term_entries["A"]))
    context.schedule_d.code_b_proceeds_total = library.irs_round(sum(entry["proceeds"] for entry in context.form_8949.short_term_entries["B"]))
    context.schedule_d.code_c_proceeds_total = library.irs_round(sum(entry["proceeds"] for entry in context.form_8949.short_term_entries["C"]))

    #Long term
    context.schedule_d.code_d_proceeds_total = library.irs_round(sum(entry["proceeds"] for entry in context.form_8949.long_term_entries["D"]))
    context.schedule_d.code_e_proceeds_total = library.irs_round(sum(entry["proceeds"] for entry in context.form_8949.long_term_entries["E"]))
    context.schedule_d.code_f_proceeds_total = library.irs_round(sum(entry["proceeds"] for entry in context.form_8949.long_term_entries["F"]))

def compute_capital_loss_carryover_worksheet():
    #TODO
    pass