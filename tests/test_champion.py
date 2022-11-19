import math

from champion import Ahri, Annie, Dummy


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
        attack_damage.append(round(ahri.orig_base_stats["attack_damage"]))
        health_point.append(math.ceil(ahri.orig_base_stats["health"]))
        attack_speed.append(round(ahri.orig_base_stats["attack_speed"], 3))

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
    stats_annie = annie.orig_base_stats
    stats_annie = {stat_name: round(stat, 2) for stat_name, stat in stats_annie.items()}

    assert stats_annie == {
        "health": 2328.0,
        "mana": 843.0,
        "armor": 107.4,
        "magic_resist": 52.1,
        "health_regen": 14.85,
        "mana_regen": 21.6,
        "crit_chance": 0.0,
        "attack_damage": 95.05,
        "attack_speed": 0.71,
    }

def test_auto_attack_with_item_component():
    items = ['Cloth Armor', 'Long Sword', 'Pickaxe', 'B. F. Sword'] 
    ahri = Ahri(level=4, items=items)
    dummy = Dummy(health=1000, bonus_armor=100, bonus_magic_resist=100)

    assert ahri.bonus_stats ==  {'armor': 15, 'gold': 2825, 'attack_damage': 75}
    assert round(ahri.auto_attack(dummy)) == 67
