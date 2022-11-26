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
    xerath.equip_item(blastingwand)
    assert round(xerath.spell_q(1, dummy)) == 80
    xerath = Xerath(level=3)
    xerath.equip_item(blastingwand)
    assert round(xerath.spell_q(2, dummy)) == 111
    xerath = Xerath(level=5)
    xerath.equip_item(blastingwand)
    assert round(xerath.spell_q(3, dummy)) == 142
    xerath = Xerath(level=7)
    xerath.equip_item(blastingwand)
    assert round(xerath.spell_q(4, dummy)) == 172
    xerath = Xerath(level=9)
    xerath.equip_item(blastingwand)
    assert round(xerath.spell_q(5, dummy)) == 203

