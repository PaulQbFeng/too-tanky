import math
from champion import Ahri, Annie, Caitlyn, Dummy
from item import BlackCleaver


def test_auto_attack_lvl1():
    annie = Annie()
    ahri = Ahri()
    assert round(annie.auto_attack(ahri), 2) == 42.37
    assert round(ahri.auto_attack(annie), 2) == 44.54


def test_ahri_stat_perlevel():
    """Stats per level are checked in game"""
    attack_speed = []
    health_point = []
    attack_damage = []
    for i in range(1, 19):
        ahri = Ahri(level=i)
        attack_damage.append(round(ahri.orig_base_stats.attack_damage))
        health_point.append(math.ceil(ahri.orig_base_stats.health))
        attack_speed.append(round(ahri.orig_base_stats.attack_speed, 3))

    assert attack_speed == [
        0.668,
        0.678,
        0.688,
        0.698,
        0.709,
        0.721,
        0.733,
        0.745,
        0.758,
        0.771,
        0.785,
        0.8,
        0.814,
        0.83,
        0.845,
        0.861,
        0.878,
        0.895,
    ]

    assert health_point == [
        570,
        640,
        712,
        788,
        867,
        950,
        1036,
        1125,
        1218,
        1314,
        1413,
        1516,
        1622,
        1731,
        1844,
        1960,
        2080,
        2202,
    ]

    assert attack_damage == [53, 55, 57, 60, 62, 65, 68, 70, 73, 76, 79, 83, 86, 89, 93, 96, 100, 104]


def test_get_stats():
    annie = Annie(level=18)
    assert round(annie.orig_base_stats.health, 2) == 2328.0
    assert round(annie.orig_base_stats.mana, 2) == 843.0
    assert round(annie.orig_base_stats.armor, 2) == 107.4
    assert round(annie.orig_base_stats.magic_resist, 2) == 52.1
    assert round(annie.orig_base_stats.health_regen, 2) == 14.85
    assert round(annie.orig_base_stats.mana_regen, 2) == 21.6
    assert round(annie.orig_base_stats.crit_chance, 2) == 0.0
    assert round(annie.orig_base_stats.attack_damage, 2) == 95.05
    assert round(annie.orig_base_stats.attack_speed, 2) == 0.71
    assert annie.level == 18


def test_equip_black_cleaver():
    caitlyn = Caitlyn(level=4)
    blackcleaver = BlackCleaver()
    assert blackcleaver.stats.health == 350
    caitlyn.equip_item(blackcleaver)
    assert round(caitlyn.total_stats.attack_damage) == 116
    assert round(caitlyn.orig_total_stats.attack_damage) == 116
    assert math.ceil(caitlyn.total_stats.health) == 1173
    assert math.ceil(caitlyn.orig_total_stats.health) == 1173


def test_auto_attack_black_cleaver():
    caitlyn = Caitlyn(level=11)
    dummy_60 = Dummy(1000, 60, 60)
    blackcleaver = BlackCleaver()
    caitlyn.equip_item(blackcleaver)
