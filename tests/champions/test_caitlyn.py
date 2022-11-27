from damage import damage_physical_auto_attack
from champion import Dummy
from champions import Caitlyn
from item import DoranBlade, LongSword, CloakofAgility


def test_auto_attack_dummy_60():
    """
    Tests of caitlyn non-crit autoattacks without her passive (Headshot) at different levels and with
    different items against a dummy with 60 bonus armor and 60 bonus mr
    Caitlyn has one adaptive force rune which gives 5.4 attack damage
    """
    dummy_60 = Dummy(health=1000, bonus_resistance=60)
    # Caitlyn level 1 with a doran's blade
    caitlyn = Caitlyn(level=1)
    caitlyn.equip_item(DoranBlade())
    # No headshot no crit
    assert round(caitlyn.auto_attack_damage(dummy_60, False)) == 44
    caitlyn.auto_attack_count = 6
    assert round(caitlyn.auto_attack_damage(dummy_60, False)) == 70
    # Caitlyn level 11 with an infinity edge
    # No headshot no crit


def test_q_dummy_30():
    dummy_30 = Dummy(1000, 30)
    caitlyn = Caitlyn(level=1)
    caitlyn.equip_item(LongSword())
    assert round(caitlyn.spell_q(1, dummy_30)) == 108
    caitlyn = Caitlyn(level=3)
    caitlyn.equip_item(LongSword())
    assert round(caitlyn.spell_q(2, dummy_30)) == 156
    caitlyn = Caitlyn(level=6)
    caitlyn.equip_item(LongSword())
    assert round(caitlyn.spell_q(3, dummy_30)) == 210
    caitlyn = Caitlyn(level=7)
    caitlyn.equip_item(LongSword())
    assert round(caitlyn.spell_q(4, dummy_30)) == 259
    caitlyn = Caitlyn(level=9)
    caitlyn.equip_item(LongSword())
    assert round(caitlyn.spell_q(5, dummy_30)) == 315


def test_w_auto_attack_dummy_30():
    dummy_30 = Dummy(1000, 30)

    caitlyn = Caitlyn(level=1)
    caitlyn.equip_item(LongSword())
    caitlyn.spell_w(level=1)
    assert round(caitlyn.auto_attack_damage(dummy_30, False)) == 122
    caitlyn.equip_item(CloakofAgility())
    caitlyn.spell_w(level=1)
    assert round(caitlyn.auto_attack_damage(dummy_30, False)) == 133
    assert round(caitlyn.auto_attack_damage(dummy_30, False)) == 55
    caitlyn.spell_w(level=1)
    assert round(caitlyn.auto_attack_damage(dummy_30, True)) == 175

    caitlyn = Caitlyn(level=3)
