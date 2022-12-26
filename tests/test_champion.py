import math

from tootanky.champion import Dummy
from tootanky.champions import Ahri, Annie, Darius, Xerath
from tootanky.item_factory import ALL_ITEMS, BlastingWand, RubyCrystal


def test_auto_attack_lvl1():
    annie = Annie()
    ahri = Ahri()
    assert round(annie.auto_attack_damage(ahri), 2) == 42.37
    assert round(ahri.auto_attack_damage(annie), 2) == 44.54


def test_ahri_stat_perlevel():
    """Stats per level are checked in game"""
    base_attack_speed = []
    bonus_attack_speed = []
    attack_speed = []
    base_health = []
    bonus_health = []
    health = []
    base_attack_damage = []
    bonus_attack_damage = []
    attack_damage = []
    base_move_speed = []
    bonus_move_speed = []
    move_speed = []
    for i in range(1, 19):
        ahri = Ahri(level=i)
        base_attack_speed.append(round(ahri.orig_base_stats.attack_speed, 3))
        bonus_attack_speed.append(round(ahri.orig_bonus_stats.attack_speed, 4))
        attack_speed.append(round(ahri.attack_speed, 3))
        base_health.append(math.ceil(ahri.orig_base_stats.health))
        bonus_health.append(round(ahri.orig_bonus_stats.health))
        health.append(math.ceil(ahri.health))
        base_attack_damage.append(round(ahri.orig_base_stats.attack_damage))
        bonus_attack_damage.append(round(ahri.orig_bonus_stats.attack_damage))
        attack_damage.append(round(ahri.attack_damage))
        base_move_speed.append(round(ahri.orig_base_stats.move_speed))
        bonus_move_speed.append(round(ahri.orig_bonus_stats.move_speed))
        move_speed.append(round(ahri.move_speed))

    assert base_attack_speed == [0.668] * 18

    assert bonus_attack_speed == [
        0.0,
        0.0144,
        0.0295,
        0.0453,
        0.0618,
        0.079,
        0.0969,
        0.1155,
        0.1348,
        0.1548,
        0.1755,
        0.1969,
        0.219,
        0.2418,
        0.2653,
        0.2895,
        0.3144,
        0.34,
    ]

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

    assert base_health == health

    assert bonus_health == [0] * 18

    assert health == [
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

    assert base_attack_damage == attack_damage

    assert bonus_attack_damage == [0] * 18

    assert attack_damage == [53, 55, 57, 60, 62, 65, 68, 70, 73, 76, 79, 83, 86, 89, 93, 96, 100, 104]

    assert base_move_speed == [330] * 18

    assert bonus_move_speed == [0] * 18

    assert move_speed == [330] * 18


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
    dmg = annie.spell_q.damage(dummy)

    assert round(dmg, 2) == 193.85


def test_auto_attack_with_item_component():
    item_names = ["Cloth Armor", "Long Sword", "Pickaxe", "B. F. Sword"]
    inventory = [ALL_ITEMS[item_name]() for item_name in item_names]
    ahri = Ahri(level=4, inventory=inventory)
    dummy = Dummy(health=1000, bonus_resistance=100)

    assert ahri.orig_bonus_stats.armor == 15
    assert ahri.orig_bonus_stats.attack_damage == 75
    assert round(ahri.auto_attack_damage(dummy)) == 67


def test_auto_attack_with_item_component_2():
    """Test auto attack damage with letha, armor pen percent, crit"""
    item_names = ["Serrated Dirk", "Last Whisper", "Serrated Dirk"]
    inventory = [ALL_ITEMS[item_name]() for item_name in item_names]
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


def test_default_init_spells_xerath():
    test_values = [
        [1, 0, 0, 0],
        [1, 1, 0, 0],
        [1, 1, 1, 0],
        [2, 1, 1, 0],
        [3, 1, 1, 0],
        [3, 1, 1, 1],
        [4, 1, 1, 1],
        [4, 2, 1, 1],
        [5, 2, 1, 1],
        [5, 3, 1, 1],
        [5, 3, 1, 2],
        [5, 4, 1, 2],
        [5, 5, 1, 2],
        [5, 5, 2, 2],
        [5, 5, 3, 2],
        [5, 5, 3, 3],
        [5, 5, 4, 3],
        [5, 5, 5, 3],
    ]
    for i in range(18):
        xerath = Xerath(level=i + 1)
        assert [xerath.spell_q.level, xerath.spell_w.level, xerath.spell_e.level, xerath.spell_r.level] == test_values[
            i
        ]
