import math

from tootanky.champions import Malphite
from tootanky.champion import Dummy
from tootanky.item import ALL_ITEM_CLASSES, BlastingWand, AmplifyingTome, NeedlesslyLargeRod
from tootanky.stats import Stats

def test_malphite_q():
    malph = Malphite(level=13)
    dummy = Dummy(health=1000, bonus_resistance=30)
    malph.equip_item(item=BlastingWand())
    malph.equip_item(item=AmplifyingTome())
    dmg = malph.spell_q(level=5, enemy_champion=dummy)

    assert round(dmg, 2) == 235.38

def test_malphite_r():
    malph = Malphite(level=11)
    dummy = Dummy(health=1000, bonus_resistance=30)
    malph.equip_item(item=NeedlesslyLargeRod())
    dmg = malph.spell_r(level=2, enemy_champion=dummy)
    malph.r.print_specs()

    assert round(dmg, 2) == 272.31

def test_malphite_e():
    malph = Malphite(level=9)
    dummy = Dummy(health=1000, bonus_resistance=30)
    #malph.equip_item(item=NeedlesslyLargeRod())
    dmg = malph.spell_e(level=5, enemy_champion=dummy)

    assert round(dmg, 2) == 170.08
