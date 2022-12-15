import math

from tootanky.champion import Dummy
from tootanky.champions import Ahri, Annie, Darius, Caitlyn
from tootanky.item import ALL_ITEM_CLASSES, BlastingWand, RubyCrystal, BlackCleaver


def test_auto_attack_lvl1():
    annie = Annie()
    ahri = Ahri()
    assert round(annie.auto_attack_damage(ahri), 2) == 42.37
    assert round(ahri.auto_attack_damage(annie), 2) == 44.54


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
    assert round(annie.health, 2) == 2328.0
    assert round(annie.mana, 2) == 843.0
    assert round(annie.armor, 2) == 107.4
    assert round(annie.magic_resist, 2) == 52.1
    assert round(annie.health_regen, 2) == 14.85
    assert round(annie.mana_regen, 2) == 21.6
    assert round(annie.crit_chance, 2) == 0.0
    assert round(annie.attack_damage, 2) == 95.05
    assert round(annie.attack_speed, 2) == 0.71
    assert annie.level == 18


def test_annie_q():
    annie = Annie(level=17, inventory=[BlastingWand()], spell_levels=[5, 5, 5, 5])
    dummy = Dummy(health=1000, bonus_resistance=30)
    dmg = annie.spell_q.hit_damage(dummy)

    assert round(dmg, 2) == 193.85


def test_auto_attack_with_item_component():
    item_names = ["Cloth Armor", "Long Sword", "Pickaxe", "B. F. Sword"]
    inventory = [ALL_ITEM_CLASSES[item_name]() for item_name in item_names]
    ahri = Ahri(level=4, inventory=inventory)
    dummy = Dummy(health=1000, bonus_resistance=100)

    assert ahri.orig_bonus_stats.armor == 15
    assert ahri.orig_bonus_stats.attack_damage == 75
    assert round(ahri.auto_attack_damage(dummy)) == 67


def test_auto_attack_with_item_component_2():
    """Test auto attack damage with letha, armor pen percent, crit"""
    item_names = ["Serrated Dirk", "Last Whisper", "Serrated Dirk"]
    inventory = [ALL_ITEM_CLASSES[item_name]() for item_name in item_names]
    ahri = Ahri(level=7, inventory=inventory)
    dummy = Dummy(health=1000, bonus_resistance=60)

    assert ahri.bonus_attack_damage == 80
    assert ahri.lethality == 10
    assert ahri.armor_pen_percent == 0.18

    assert round(ahri.auto_attack_damage(dummy)) == 104
    assert round(ahri.auto_attack_damage(dummy, is_crit=True)) == 182


def test_darius_auto_attack():
    darius = Darius(level=18)
    assert round(darius.health) == 2590

    dummy = Dummy(health=1000, bonus_resistance=100)
    darius.do_auto_attack(dummy)
    assert round(dummy.health) == 926


def test_equip_item_health():
    ahri = Ahri(level=17, spell_levels=[5, 5, 5, 5])
    assert math.ceil(ahri.health) == 2080
    ahri = Ahri(level=17, inventory=[RubyCrystal()], spell_levels=[5, 5, 5, 5])
    assert math.ceil(ahri.health) == 2230


def test_auto_attack_black_cleaver():
    caitlyn = Caitlyn(level=11, inventory=BlackCleaver())
    ahri = Ahri(level=11)
    orig_armor = ahri.orig_base_stats.armor + ahri.orig_bonus_stats.armor
    caitlyn.do_auto_attack(ahri)
    assert round(ahri.armor, 3) == round(orig_armor * 0.95, 3)
    caitlyn.do_auto_attack(ahri)
    assert round(ahri.armor, 3) == round(orig_armor * 0.9, 3)
    caitlyn.do_auto_attack(ahri)
    assert round(ahri.armor, 3) == round(orig_armor * 0.85, 3)
    caitlyn.do_auto_attack(ahri)
    assert round(ahri.armor, 3) == round(orig_armor * 0.8, 3)
    caitlyn.do_auto_attack(ahri)
    assert round(ahri.armor, 3) == round(orig_armor * 0.75, 3)
    caitlyn.do_auto_attack(ahri)
    assert round(ahri.armor, 3) == round(orig_armor * 0.7, 3)
    caitlyn.do_auto_attack(ahri)
    assert round(ahri.armor, 3) == round(orig_armor * 0.7, 3)
    caitlyn.do_auto_attack(ahri)
    assert round(ahri.armor, 3) == round(orig_armor * 0.7, 3)
