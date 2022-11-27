from champion import Dummy
from champions import Caitlyn
from item import LongSword, CloakofAgility


def auto_attack_default_run(inventory, enemy_champion, test_values):
    for level in [1]:  # should include levels 7 and 13 because headshot damage scales with level
        caitlyn = Caitlyn(level=level, inventory=inventory)
        assert round(caitlyn.auto_attack_damage(enemy_champion, False)) == test_values[0]  # No headshot no crit
        caitlyn.auto_attack_count = 6
        assert round(caitlyn.auto_attack_damage(enemy_champion, False)) == test_values[1]  # Headshot and no crit


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
    auto_attack_default_run([LongSword()], Dummy(1000, 60), [45, 72])


def q_default_run(inventory, enemy_champion, test_values):
    for i in range(1, 6):
        caitlyn = Caitlyn(level=2*i-1, inventory=inventory)
        assert round(caitlyn.spell_q(i, enemy_champion)) == test_values[i-1]


def test_q():
    q_default_run([LongSword()], Dummy(1000, 30), [108, 156, 206, 259, 315])


def w_default_run(inventory, enemy_champion, test_values):
    for i in range(1, 5):
        caitlyn = Caitlyn(level=2*i-1, inventory=inventory)
        caitlyn.spell_w(level=i)
        assert round(caitlyn.auto_attack_damage(enemy_champion, False)) == test_values[2*i-2]
        caitlyn.spell_w(level=i)
        assert round(caitlyn.auto_attack_damage(enemy_champion, True)) == test_values[2*i-1]
    # last test with lvl 13 for robustness with headshot dmg lvl scaling
    caitlyn = Caitlyn(level=13, inventory=inventory)
    caitlyn.spell_w(level=5)
    assert round(caitlyn.auto_attack_damage(enemy_champion, False)) == test_values[8]
    caitlyn.spell_w(level=5)
    assert round(caitlyn.auto_attack_damage(enemy_champion, True)) == test_values[9]


def test_w():
    w_default_run([LongSword(), CloakofAgility()], Dummy(1000, 30), [133, 175, 176, 221, 220, 269, 286, 338, 385, 450])
