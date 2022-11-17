import math

from item import DoranBlade

def test_DoranBlade():
    doranblade = DoranBlade()
    assert doranblade.stats == {'attack_damage': 8, 'health': 80, "gold": 450}


