from tootanky.champion import Dummy
from tootanky.champions import Caitlyn
from tootanky.item_factory import CloakofAgility, LongSword


def auto_attack_default_run(inventory, target, test_values):
    for i in range(1, 4):
        caitlyn = Caitlyn(level=6 * (i - 1) + 1, inventory=inventory)  # for levels 1, 7, 13
        assert round(caitlyn.auto_attack_damage(target, False)) == test_values[2 * i - 2]  # No headshot no crit
        caitlyn.auto_attack_count = 6
        assert round(caitlyn.auto_attack_damage(target, False)) == test_values[2 * i - 1]  # Headshot and no crit


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


def q_default_run(inventory, target, test_values):
    for spell_level in range(1, 6):
        caitlyn = Caitlyn(
            level=2 * spell_level - 1, inventory=inventory, spell_levels=[spell_level, 1, 1, 1]
        )  # for levels 1, 3, 5, 7, 9
        assert round(caitlyn.spell_q.damage(target)) == test_values[spell_level - 1]


def test_q():
    q_default_run([LongSword()], Dummy(1000, 30), [108, 156, 206, 259, 315])


def test_w_level_1():
    # W has no damage, but we call damage to trigger passive headshot effect
    dummy = Dummy(1000, 30)
    caitlyn = Caitlyn(level=1)
    assert round(caitlyn.auto_attack_damage(dummy, False)) == 48
    caitlyn.spell_w.damage(dummy)
    assert round(caitlyn.auto_attack_damage(dummy, False)) == 107


def w_default_run(inventory, target, test_values):
    for spell_level in range(1, 5):
        caitlyn = Caitlyn(
            level=2 * spell_level - 1, spell_levels=[1, spell_level, 1, 1], inventory=inventory
        )  # for levels 1, 3, 5, 7, 9
        caitlyn.spell_w.damage(target)
        assert round(caitlyn.auto_attack_damage(target, False)) == test_values[2 * spell_level - 2]
        caitlyn.spell_w.damage(target)
        assert round(caitlyn.auto_attack_damage(target, True)) == test_values[2 * spell_level - 1]
    # last test with lvl 13 for robustness with headshot dmg lvl scaling
    caitlyn = Caitlyn(level=13, spell_levels=[1, 5, 1, 1], inventory=inventory)
    caitlyn.spell_w.damage(target)
    assert round(caitlyn.auto_attack_damage(target, False)) == test_values[8]
    caitlyn.spell_w.damage(target)
    assert round(caitlyn.auto_attack_damage(target, True)) == test_values[9]


def test_w():
    w_default_run([LongSword(), CloakofAgility()], Dummy(1000, 30), [133, 175, 176, 221, 220, 269, 286, 338, 385, 450])


def e_default_run(inventory, target, test_values_e, test_values_empowered_auto_attack):
    for spell_level in range(1, 6):
        caitlyn = Caitlyn(
            level=2 * spell_level - 1, inventory=inventory, spell_levels=[1, 1, spell_level, 1]
        )  # for levels 1, 3, 5, 7, 9
        assert round(caitlyn.spell_e.damage(target)) == test_values_e[spell_level - 1]
        assert (
            round(caitlyn.auto_attack_damage(target, False)) == test_values_empowered_auto_attack[2 * spell_level - 2]
        )
        caitlyn.spell_e.damage(target)
        assert round(caitlyn.auto_attack_damage(target, True)) == test_values_empowered_auto_attack[2 * spell_level - 1]


def test_e():
    e_default_run(
        [LongSword(), CloakofAgility()],
        Dummy(1000, 30),
        [62, 100, 138, 177, 215],
        [100, 141, 107, 152, 116, 164, 146, 198, 157, 214],
    )


def r_default_run(inventory, target, test_values):
    for spell_level in range(1, 4):
        caitlyn = Caitlyn(
            level=spell_level * 5 + 1, spell_levels=[1, 1, 1, spell_level], inventory=inventory
        )  # for levels 6, 11, 16
        assert round(caitlyn.spell_r.damage(target)) == test_values[spell_level - 1]


def test_r():
    r_default_run([LongSword()], Dummy(1000, 30), [246, 419, 592])
    r_default_run([LongSword(), CloakofAgility()], Dummy(1000, 30), [255, 435, 615])
    r_default_run([LongSword(), CloakofAgility(), CloakofAgility()], Dummy(1000, 30), [265, 451, 637])
    r_default_run([LongSword(), CloakofAgility(), CloakofAgility(), CloakofAgility()], Dummy(1000, 30), [274, 466, 659])
    r_default_run(
        [LongSword(), CloakofAgility(), CloakofAgility(), CloakofAgility(), CloakofAgility()],
        Dummy(1000, 30),
        [283, 482, 681],
    )
    r_default_run(
        [LongSword(), CloakofAgility(), CloakofAgility(), CloakofAgility(), CloakofAgility(), CloakofAgility()],
        Dummy(1000, 30),
        [292, 498, 703],
    )


def test_passive_w_e_interaction():
    dummy = Dummy(1000, 40)
    caitlyn = Caitlyn(level=2, inventory=[LongSword()])
    # Caitlyn has Headshot ready
    caitlyn.auto_attack_count = 6
    # W and E should empower the next autoattack without consuming stacks
    # If cait uses W and E (regardless of the order), the first autoattack will always apply the W additional damage
    caitlyn.spell_w.damage(dummy)
    caitlyn.spell_e.damage(dummy)
    assert round(caitlyn.auto_attack_damage(dummy, False)) == 117
    assert caitlyn.auto_attack_count == 6
    assert round(caitlyn.auto_attack_damage(dummy, False)) == 85
    assert caitlyn.auto_attack_count == 6
    assert round(caitlyn.auto_attack_damage(dummy, False)) == 85
    assert caitlyn.auto_attack_count == 0
    caitlyn.auto_attack_count = 6
    caitlyn.spell_e.damage(dummy)
    caitlyn.spell_w.damage(dummy)
    assert round(caitlyn.auto_attack_damage(dummy, False)) == 117
    assert caitlyn.auto_attack_count == 6
    assert round(caitlyn.auto_attack_damage(dummy, False)) == 85
    assert caitlyn.auto_attack_count == 6
    assert round(caitlyn.auto_attack_damage(dummy, False)) == 85
    assert caitlyn.auto_attack_count == 0
