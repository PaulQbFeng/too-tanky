from tootanky.dummy import Dummy
from tootanky.champions.orianna import Orianna
from tootanky.item_factory import BlastingWand


def test_orianna_r():
    orianna = Orianna(level=17, inventory=[BlastingWand()], spell_levels=(1, 1, 1, 3))
    dummy = Dummy(health=1000, bonus_resistance=30)
    dmg = orianna.spell_r.damage(dummy)

    assert round(dmg, 2) == 293.85
