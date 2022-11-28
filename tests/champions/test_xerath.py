from champion import Dummy
from champions.xerath import Xerath
from item import BlastingWand


def test_dummy_0_res():
    dummy = Dummy(1000, 0)
    xerath = Xerath(level=18)
    assert round(xerath.spell_q(1, dummy)) == 70

    xerath.equip_item(BlastingWand())
    damage_per_level = [104, 144, 184, 224, 264]
    for spell_level in range(1, 6):
        assert round(xerath.spell_q(spell_level, dummy)) == damage_per_level[spell_level - 1]


def test_dummy_30_res():
    dummy = Dummy(1000, 30)
    q_test_values = [80, 111, 142, 172, 203]
    w_test_values = [65, 108, 92, 153, 118, 197, 145, 242, 172, 287]
    e_test_values = [75, 98, 122, 145, 168]
    r_test_values = [168, 206, 245]
    xerath = Xerath(level=16, inventory=[BlastingWand()])  # since xerath damage doesn't scale with his level we can fix his level
    for spell_level in range(1, 6):
        assert round(xerath.spell_q(spell_level, dummy)) == q_test_values[spell_level-1]
        assert round(xerath.spell_w(spell_level, dummy, False)) == w_test_values[2*spell_level-2]
        assert round(xerath.spell_w(spell_level, dummy, True)) == w_test_values[2*spell_level-1]
        assert round(xerath.spell_e(spell_level, dummy)) == e_test_values[spell_level - 1]
    r_exact_values = []
    for spell_level in range(1, 4):
        r_exact_value = xerath.spell_r(spell_level, dummy, 1)
        assert round(r_exact_value) == r_test_values[spell_level-1]
        r_exact_values.append(r_exact_value)
    for spell_level in range(1, 4):
        for i in range(0, spell_level + 3):
            assert round(xerath.spell_r(spell_level, dummy, i)) == round(i * r_exact_values[spell_level-1])
