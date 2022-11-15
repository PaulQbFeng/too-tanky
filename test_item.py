import math

from item import DoranBlade

def test_DoranBlade():
    doranblade = DoranBlade()
    assert doranblade.stats == {'FlatPhysicalDamageMod': 8, 'FlatHPPoolMod': 80}
    assert doranblade.gold == 450


