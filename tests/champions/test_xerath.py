from tootanky.champion import Dummy
from tootanky.champions.xerath import Xerath
from tootanky.item import BlastingWand


def test_dummy_0_res():
    dummy = Dummy(1000, 0)
    xerath = Xerath(level=18, spell_levels=[1,1,1,1])
    assert round(xerath.spell_q.hit_damage(dummy)) == 70

    xerath = Xerath(level=18, inventory=[BlastingWand()], spell_levels=[1, 1, 1, 1])
    damage_per_level = [104, 144, 184, 224, 264]
    for spell_level in range(1, 6):
        xerath.spell_q.set_level(spell_level)
        assert round(xerath.spell_q.hit_damage(dummy)) == damage_per_level[spell_level - 1]

dummy = Dummy(1000, 30)
xerath = Xerath(level=16, inventory=[BlastingWand()])  # since xerath damage doesn't scale with his level we can fix his level

def make_test_spell(spell, values, **kwargs):
    for spell_level in range(1,len(values)+1):
        spell.set_level(spell_level)
        assert round(spell.hit_damage(dummy, **kwargs)) == values[spell_level-1]

def test_xerath_q():
    make_test_spell(xerath.spell_q, [80, 111, 142, 172, 203])

def test_xerath_w():
    make_test_spell(xerath.spell_w, [65, 92, 118, 145, 172], is_empowered=False)
    make_test_spell(xerath.spell_w, [108, 153, 197, 242, 287], is_empowered=True)

def test_xerath_e():
    make_test_spell(xerath.spell_e, [75, 98, 122, 145, 168])

def test_xerath_r():
    make_test_spell(xerath.spell_r, [168, 206, 245])
