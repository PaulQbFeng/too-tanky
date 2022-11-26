import math

from champions import Malphite
from champion import Dummy
from item import ALL_ITEM_CLASSES, BlastingWand, AmplifyingTome
from stats import Stats

def test_malphite_q():
    malph = Malphite(level=13)
    dummy = Dummy(health=1000, bonus_resistance=30)
    malph.equip_item(item=BlastingWand())
    malph.equip_item(item=AmplifyingTome())
    dmg = malph.spell_q(level=5, enemy_champion=dummy)

    assert round(dmg, 2) == 235.38