from tootanky.champion import Dummy
from tootanky.champions.orianna import Orianna
from tootanky.item import BlastingWand


def test_orianna_r():
    orianna = Orianna(level=17, spell_levels=[1, 1, 1, 3])
    dummy = Dummy(health=1000, bonus_resistance=30)
    orianna.equip_item(item=BlastingWand())
    dmg = orianna.spell_r.hit_damage(dummy)

    assert round(dmg, 2) == 293.85
