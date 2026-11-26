#Tax year constants for 2026
#Filed in early 2027

tax_year = 2026

STANDARD_DEDUCTION = {
    'single': 16100,
    'married_filing_jointly': 32200,
}

TAX_BRACKETS = {
    'single': [
        (0, 12400, 0.10),
        (12400, 50400, 0.12),
        (50400, 105700, 0.22),
        (105700, 201775, 0.24),
        (201775, 256225, 0.32),
        (256225, 640600, 0.35),
        (640600, float('inf'), 0.37)
    ],
    'married_filing_jointly': [
        (0, 24800, 0.10),
        (24800, 100800, 0.12),
        (100800, 211400, 0.22),
        (211400, 403550, 0.24),
        (403550, 512450, 0.32),
        (512450, 768700, 0.35),
        (768700, float('inf'), 0.37)
    ],
}   

#Qualified Dividends and Capital Gain Tax Worksheet thresholds for 2026
QDCGT_ZERO_RATE_MAX = {
    'single': 49450,
    #'married_filing_separately': 49450,
    'married_filing_jointly': 98900,
    #'qualifying_surviving_spouse': 98900,
    #'head_of_household': 66200,
}

QDCGT_FIFTEEN_RATE_MAX = {
    'single': 545500,
    #'married_filing_separately': 306850,
    'married_filing_jointly': 613700,
    #'qualifying_surviving_spouse': 613700,
    #'head_of_household': 579600,
}

#Schedule D: Max capital losses deductible in a year against ordinary income
SCHEDULE_D_CAPITAL_LOSS_DEDUCTION_LIMIT = {
    'single': 3000, #Includes everything except married filing separately
    'married_filing_jointly': 3000,
    #'married_filing_separately': 1500,
}

SCHEDULE_B_THRESHOLD = 1500