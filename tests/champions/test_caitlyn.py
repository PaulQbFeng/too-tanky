from damage import damage_physical_auto_attack
from champion import Dummy
from champions import Caitlyn
from item import DoranBlade


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

