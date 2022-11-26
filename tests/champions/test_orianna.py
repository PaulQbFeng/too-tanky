from champion import Dummy
from champions.orianna import Orianna
from item import BlastingWand


def test_orianna_r():
    orianna = Orianna(level=17)
    dummy = Dummy(health=1000, bonus_resistance=30)
    orianna.equip_item(item=BlastingWand())
    dmg = orianna.spell_r(level=3, enemy_champion=dummy)

    assert round(dmg, 2) == 293.85
