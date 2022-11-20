import math

from item import DoranBlade


def test_DoranBlade():
    doranblade = DoranBlade()
    assert doranblade.stats.attack_damage == 8
    assert doranblade.stats.health == 80
    assert doranblade.gold == 450

