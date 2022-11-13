from champion import Annie, Ahri

def test_auto_attack_lvl1():
    annie = Annie()
    ahri = Ahri()
    assert round(annie.auto_attack(ahri), 2) == 42.37
    assert round(ahri.auto_attack(annie), 2) == 44.54
