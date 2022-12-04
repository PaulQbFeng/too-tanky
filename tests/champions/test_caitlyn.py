from tootanky.champion import Dummy
from tootanky.champions import Caitlyn
from tootanky.item import LongSword, CloakofAgility


def auto_attack_default_run(inventory, enemy_champion, test_values):
    for i in range(1, 4):
        caitlyn = Caitlyn(level=6*(i-1)+1, inventory=inventory)  # for levels 1, 7, 13
        assert round(caitlyn.auto_attack_damage(enemy_champion, False)) == test_values[2*i-2]  # No headshot no crit
        caitlyn.auto_attack_count = 6
        assert round(caitlyn.auto_attack_damage(enemy_champion, False)) == test_values[2*i-1]  # Headshot and no crit


def test_auto_attack():
    """
    Tests of caitlyn non-crit autoattacks without her passive (Headshot) at different levels and with
    different items against a dummy with 60 bonus armor and 60 bonus mr
    Caitlyn has one adaptive force rune which gives 5.4 attack damage
    """
    # Test of attack_count
    caitlyn = Caitlyn()
    dummy = Dummy(1000, 0)
    caitlyn.auto_attack_damage(dummy, False)
    caitlyn.auto_attack_damage(dummy, False)
    caitlyn.auto_attack_damage(dummy, False)
    caitlyn.auto_attack_damage(dummy, False)
    caitlyn.auto_attack_damage(dummy, False)
    caitlyn.auto_attack_damage(dummy, False)
    assert caitlyn.auto_attack_count == 6
    # Test of auto attack damage (with consideration of headshot and crit)
    auto_attack_default_run([LongSword()], Dummy(1000, 60), [45, 72, 57, 107, 71, 156])


def q_default_run(inventory, enemy_champion, test_values):
    for spell_level in range(1, 6):
        caitlyn = Caitlyn(level=2*spell_level-1, inventory=inventory)  # for levels 1, 3, 5, 7, 9
        assert round(caitlyn.spell_q(spell_level, enemy_champion)) == test_values[spell_level-1]


def test_q():
    q_default_run([LongSword()], Dummy(1000, 30), [108, 156, 206, 259, 315])


def w_default_run(inventory, enemy_champion, test_values):
    for spell_level in range(1, 5):
        caitlyn = Caitlyn(level=2*spell_level-1, inventory=inventory)  # for levels 1, 3, 5, 7
        caitlyn.spell_w(level=spell_level)
        assert round(caitlyn.auto_attack_damage(enemy_champion, False)) == test_values[2*spell_level-2]
        caitlyn.spell_w(level=spell_level)
        assert round(caitlyn.auto_attack_damage(enemy_champion, True)) == test_values[2*spell_level-1]
    # last test with lvl 13 for robustness with headshot dmg lvl scaling
    caitlyn = Caitlyn(level=13, inventory=inventory)
    caitlyn.spell_w(level=5)
    assert round(caitlyn.auto_attack_damage(enemy_champion, False)) == test_values[8]
    caitlyn.spell_w(level=5)
    assert round(caitlyn.auto_attack_damage(enemy_champion, True)) == test_values[9]


def test_w():
    w_default_run([LongSword(), CloakofAgility()], Dummy(1000, 30), [133, 175, 176, 221, 220, 269, 286, 338, 385, 450])


def e_default_run(inventory, enemy_champion, test_values_e, test_values_empowered_auto_attack):
    for spell_level in range(1, 6):
        caitlyn = Caitlyn(level=2*spell_level-1, inventory=inventory)  # for levels 1, 3, 5, 7, 9
        assert round(caitlyn.spell_e(level=spell_level, enemy_champion=enemy_champion)) == test_values_e[spell_level-1]
        assert round(caitlyn.auto_attack_damage(enemy_champion, False)) == test_values_empowered_auto_attack[2*spell_level-2]
        caitlyn.spell_e(level=spell_level, enemy_champion=enemy_champion)
        assert round(caitlyn.auto_attack_damage(enemy_champion, True)) == test_values_empowered_auto_attack[2*spell_level-1]


def test_e():
    e_default_run([LongSword(), CloakofAgility()], Dummy(1000, 30), [62, 100, 138, 177, 215], [100, 141, 107, 152, 116, 164, 146, 198, 157, 214])


def r_default_run(inventory, enemy_champion, test_values):
    for spell_level in range(1, 4):
        caitlyn = Caitlyn(level=spell_level*5+1, inventory=inventory)  # for levels 6, 11, 16
        assert round(caitlyn.spell_r(level=spell_level, enemy_champion=enemy_champion)) == test_values[spell_level-1]


def test_r():
    r_default_run([LongSword()], Dummy(1000, 30), [246, 419, 592])
    r_default_run([LongSword(), CloakofAgility()], Dummy(1000, 30), [255, 435, 615])
    r_default_run([LongSword(), CloakofAgility(), CloakofAgility()], Dummy(1000, 30), [265, 451, 637])
    r_default_run([LongSword(), CloakofAgility(), CloakofAgility(), CloakofAgility()], Dummy(1000, 30), [274, 466, 659])
    r_default_run([LongSword(), CloakofAgility(), CloakofAgility(), CloakofAgility(), CloakofAgility()], Dummy(1000, 30), [283, 482, 681])
    r_default_run([LongSword(), CloakofAgility(), CloakofAgility(), CloakofAgility(), CloakofAgility(), CloakofAgility()], Dummy(1000, 30), [292, 498, 703])


def test_passive_w_e_interaction():
    dummy = Dummy(1000, 40)
    caitlyn = Caitlyn(level=2, inventory=[LongSword()])
    # Caitlyn has Headshot ready
    caitlyn.auto_attack_count = 6
    # W and E should empower the next autoattack without consuming stacks
    # If cait uses W and E (regardless of the order), the first autoattack will always apply the W additional damage
    caitlyn.spell_w(level=1)
    caitlyn.spell_e(level=1, enemy_champion=dummy)
    assert round(caitlyn.auto_attack_damage(dummy, False)) == 117
    assert caitlyn.auto_attack_count == 6
    assert round(caitlyn.auto_attack_damage(dummy, False)) == 85
    assert caitlyn.auto_attack_count == 6
    assert round(caitlyn.auto_attack_damage(dummy, False)) == 85
    assert caitlyn.auto_attack_count == 0
    caitlyn.auto_attack_count = 6
    caitlyn.spell_e(level=1, enemy_champion=dummy)
    caitlyn.spell_w(level=1)
    assert round(caitlyn.auto_attack_damage(dummy, False)) == 117
    assert caitlyn.auto_attack_count == 6
    assert round(caitlyn.auto_attack_damage(dummy, False)) == 85
    assert caitlyn.auto_attack_count == 6
    assert round(caitlyn.auto_attack_damage(dummy, False)) == 85
    assert caitlyn.auto_attack_count == 0
