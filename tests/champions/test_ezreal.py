from tootanky.champion import Dummy
from tootanky.champions import Ezreal
from tootanky.item_factory import BlastingWand, Sheen, BFSword


dummy = Dummy(health=1000, bonus_resistance=100)


def test_ezreal_q(dummy_100):
    """with and without spellblade"""
    inv = [BlastingWand(), BFSword(), Sheen()]
    expected_q_dmgs = [92, 105, 117, 130, 142]
    expected_q_sb_dmgs = [133, 146, 158, 171, 183]
    for spell_level in range(1, 6):
        ezreal = Ezreal(level=11, inventory=inv, spell_levels=(spell_level, 1, 1, 1))
        dmg = ezreal.spell_q.damage(dummy_100)
        assert round(dmg) == expected_q_dmgs[spell_level - 1]
        dmg = ezreal.spell_q.damage(dummy_100, spellblade=True)
        assert round(dmg) == expected_q_sb_dmgs[spell_level - 1]
