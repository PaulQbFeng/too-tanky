from tootanky.champion import Dummy
from tootanky.champions import Malphite
from tootanky.item import AmplifyingTome, BlastingWand, NeedlesslyLargeRod


def test_malphite_q():
    malph = Malphite(level=13, spell_levels=[5, 1, 1, 1])
    dummy = Dummy(health=1000, bonus_resistance=30)
    malph.equip_item(item=BlastingWand())
    malph.equip_item(item=AmplifyingTome())
    dmg = malph.spell_q.hit_damage(dummy)

    assert round(dmg, 2) == 235.38


def test_malphite_r():
    malph = Malphite(level=11, spell_levels=[1, 1, 1, 2])
    dummy = Dummy(health=1000, bonus_resistance=30)
    malph.equip_item(item=NeedlesslyLargeRod())
    dmg = malph.spell_r.hit_damage(dummy)
    malph.spell_r.print_specs()

    assert round(dmg, 2) == 272.31


def test_malphite_e():
    malph = Malphite(level=9, spell_levels=[1, 1, 5, 1])
    dummy = Dummy(health=1000, bonus_resistance=30)
    # malph.equip_item(item=NeedlesslyLargeRod())
    dmg = malph.spell_e.hit_damage(dummy)

    assert round(dmg, 2) == 170.08
