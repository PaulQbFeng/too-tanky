import math

from item import DoranBlade
from item import Sheen
from champion import Ahri, Annie
from champion import Dummy
from damage import damage_after_positive_resistance


def test_DoranBlade():
    doranblade = DoranBlade()
    assert doranblade.stats == {'attack_damage': 8, 'health': 80, "gold": 450}

def test_Sheen():
    sheen = Sheen()
    annie = Annie()
    dummy=Dummy(1000,50,50)
    assert sheen.spellblade(annie, dummy) ==  damage_after_positive_resistance(annie.attack_damage, dummy.bonus_armor)
