from champion import Ahri, Annie


def test_auto_attack_lvl1():
    annie = Annie()
    ahri = Ahri()
    assert round(annie.auto_attack(ahri), 2) == 42.37
    assert round(ahri.auto_attack(annie), 2) == 44.54


def test_ahri_stat_lvl18():
    ahri = Ahri(level=18)
    assert ahri.hp == 2202
    assert ahri.mp == 843
    assert ahri.attackdamage == 104
    assert round(ahri.attackspeed, 3) == 0.895
