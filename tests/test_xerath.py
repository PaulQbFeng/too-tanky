from champions.xerath import Xerath, QXerath
from champion import Dummy
from item import BlastingWand


def test_dummy_0_res():
    dummy = Dummy(1000, 0)
    xerath = Xerath(level=1)
    blastingwand = BlastingWand()
    assert round(xerath.spell_q(1, dummy)) == 70
    xerath.equip_item(blastingwand)
    assert round(xerath.spell_q(1, dummy)) == 104
    xerath = Xerath(level=3)
    xerath.equip_item(blastingwand)
    assert round(xerath.spell_q(2, dummy)) == 144
    xerath = Xerath(level=5)
    xerath.equip_item(blastingwand)
    assert round(xerath.spell_q(3, dummy)) == 184
    xerath = Xerath(level=7)
    xerath.equip_item(blastingwand)
    assert round(xerath.spell_q(4, dummy)) == 224
    xerath = Xerath(level=9)
    xerath.equip_item(blastingwand)
    assert round(xerath.spell_q(5, dummy)) == 264

def test_dummy_30_res():
    dummy = Dummy(1000, 30)
    xerath = Xerath(level=1)
    blastingwand = BlastingWand()
    assert round(xerath.spell_q(1, dummy)) == 54
    assert round(xerath.spell_w(1, dummy, False)) == 46
    assert round(xerath.spell_w(1, dummy, True)) == 77
    xerath.equip_item(blastingwand)
    assert round(xerath.spell_q(1, dummy)) == 80
    assert round(xerath.spell_w(1, dummy, False)) == 65
    assert round(xerath.spell_w(1, dummy, True)) == 108
    xerath = Xerath(level=3)
    xerath.equip_item(blastingwand)
    assert round(xerath.spell_q(2, dummy)) == 111
    assert round(xerath.spell_w(2, dummy, False)) == 92
    assert round(xerath.spell_w(2, dummy, True)) == 153
    xerath = Xerath(level=5)
    xerath.equip_item(blastingwand)
    assert round(xerath.spell_q(3, dummy)) == 142
    assert round(xerath.spell_w(3, dummy, False)) == 118
    assert round(xerath.spell_w(3, dummy, True)) == 197
    xerath = Xerath(level=7)
    xerath.equip_item(blastingwand)
    assert round(xerath.spell_q(4, dummy)) == 172
    assert round(xerath.spell_w(4, dummy, False)) == 145
    assert round(xerath.spell_w(4, dummy, True)) == 242
    xerath = Xerath(level=9)
    xerath.equip_item(blastingwand)
    assert round(xerath.spell_q(5, dummy)) == 203
    assert round(xerath.spell_w(5, dummy, False)) == 172
    assert round(xerath.spell_w(5, dummy, True)) == 287

