import library

def test_irs_round_drops_cents_below_50():
    assert library.irs_round(100.49) == 100

def test_irs_round_rounds_up_at_exactly_50_cents():
    assert library.irs_round(100.5) == 101

def test_irs_round_rounds_up_above_50_cents():
    assert library.irs_round(100.51) == 101

def test_irs_round_whole_number_unchanged():
    assert library.irs_round(100.0) == 100

def test_irs_round_zero():
    assert library.irs_round(0) == 0

def test_irs_round_small_positive_amounts():
    assert library.irs_round(0.49) == 0
    assert library.irs_round(0.5) == 1

def test_irs_round_negative_drops_cents_below_50():
    assert library.irs_round(-100.49) == -100

def test_irs_round_negative_rounds_away_from_zero_at_50_cents():
    assert library.irs_round(-100.5) == -101

def test_irs_round_small_negative_rounds_to_zero():
    assert library.irs_round(-0.4) == 0