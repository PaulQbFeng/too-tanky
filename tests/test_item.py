import math
import pytest

from tootanky.champion import Dummy
from tootanky.champions import Ahri, Annie, Caitlyn, Yasuo, Yone
from tootanky.damage import damage_after_positive_resistance
from tootanky.item_factory import (
    ALL_ITEMS,
    ALL_MYTHIC_ITEMS,
    DoransBlade,
    Sheen,
    InfinityEdge,
    CloakofAgility,
    RabadonsDeathcap,
    BlastingWand,
    BlackCleaver,
    RecurveBow,
    BFSword,
    Tiamat,
    Rageknife,
    SerratedDirk,
    LastWhisper
)


@pytest.fixture()
def infinity_edge():
    return InfinityEdge()


@pytest.fixture()
def agility_cloak():
    return CloakofAgility()


def test_doranblade():
    doranblade = DoransBlade()
    assert doranblade.stats._dict == {"attack_damage": 8, "health": 80}


def test_infinity_edge(infinity_edge, agility_cloak):
    assert infinity_edge.stats.attack_damage == 70
    assert infinity_edge.stats.crit_chance == 0.2

    ahri = Ahri(inventory=[infinity_edge] + 2 * [agility_cloak])
    assert ahri.crit_damage == 0
    ahri = Ahri(inventory=[infinity_edge] + 3 * [agility_cloak])
    assert ahri.crit_damage == 0.35


def test_infinity_edge_cait(infinity_edge, agility_cloak):
    dummy = Dummy(health=1000, bonus_resistance=100)
    caitlyn = Caitlyn(level=11, inventory=[infinity_edge] + 2 * [agility_cloak])
    assert round(caitlyn.auto_attack.damage(dummy, is_crit=False)) == 83
    assert round(caitlyn.auto_attack.damage(dummy, is_crit=True)) == 145
    caitlyn = Caitlyn(level=11, inventory=[infinity_edge] + 3 * [agility_cloak])
    assert caitlyn.crit_damage == 0.35
    assert round(caitlyn.auto_attack.damage(dummy, is_crit=False)) == 83
    assert round(caitlyn.auto_attack.damage(dummy, is_crit=True)) == 174


def test_sheen():
    annie = Annie(level=2, inventory=[Sheen()])
    dummy = Dummy(health=1000, bonus_resistance=100)
    assert len(annie.on_hits) == 1
    assert round(annie.auto_attack.damage(dummy)) == 26
    assert annie.spell_q.damage(dummy, spellblade=True) == 40
    assert round(annie.auto_attack.damage(dummy)) == 52
    assert round(annie.auto_attack.damage(dummy)) == 26


def test_serrated_unique_passive():
    item_names = ["Serrated Dirk", "Last Whisper"]
    inventory = [ALL_ITEMS[item_name]() for item_name in item_names]
    ahri = Ahri(level=7, inventory=inventory)

    assert ahri.orig_bonus_stats.attack_damage == 50
    assert ahri.orig_bonus_stats.lethality == 10
    assert ahri.orig_bonus_stats.armor_pen_percent == 0.18

    item_names = ["Serrated Dirk", "Last Whisper", "Serrated Dirk"]
    inventory = [ALL_ITEMS[item_name]() for item_name in item_names]
    ahri = Ahri(level=7, inventory=inventory)

    assert ahri.orig_bonus_stats.attack_damage == 80
    assert ahri.orig_bonus_stats.lethality == 10
    assert ahri.orig_bonus_stats.armor_pen_percent == 0.18


def galeforce_default_run(
    item_names, target, test_bonus_attack_damage: float, test_crit_chance: float, test_active: list
):
    inventory = [ALL_ITEMS[item_name]() for item_name in item_names]
    ahri = Ahri(level=1, inventory=inventory)
    assert ahri.bonus_attack_damage == test_bonus_attack_damage
    assert ahri.crit_chance == test_crit_chance
    # TODO: attack speed test is missing, we have to define how attack speed stacks before

    for champion_level in range(1, 19):
        ahri = Ahri(level=champion_level, inventory=inventory)
        assert round(ahri.apply_item_active(item_name="Galeforce", target=target)) == test_active[champion_level - 1]
        target.reset_health()

    ahri = Ahri(level=1, inventory=inventory)
    dummy = Dummy(2000, 60)
    test_active_2 = [134, 275, 422, 577, 739, 909, 1087, 1273, 1468, 1666]
    total_damage = 0
    for i in range(10):
        total_damage += ahri.apply_item_active(item_name="Galeforce", target=dummy)
        assert round(total_damage) == test_active_2[i]


def test_galeforce():
    item_names = ["Galeforce", "Long Sword", "Cloak of Agility"]
    galeforce_default_run(
        item_names=item_names,
        target=Dummy(1000, 60),
        test_bonus_attack_damage=70,
        test_crit_chance=0.35,
        test_active=[136, 136, 136, 136, 136, 136, 136, 136, 136, 146, 156, 167, 177, 187, 197, 207, 218, 228],
    )


def test_rabadon():
    ahri = Ahri(level=11, inventory=[RabadonsDeathcap()])
    assert ahri.ability_power == 162
    ahri = Ahri(level=11, inventory=[RabadonsDeathcap(), BlastingWand()])
    assert ahri.ability_power == 216


def test_mythic_passives():
    # tests on ahri level 9 + 16 MR in runes
    item_names = ["Cosmic Drive", "Nashor's Tooth", "Serylda's Grudge", "Guardian Angel", "Edge of Night"]
    test_dict = {
        "Everfrost": {
            "health": 1993,
            "attack_damage": 213,
            "ability_power": 285,
            "armor": 90,
            "magic_resist": 55 - 16,
            "attack_speed": 1.092,
            "move_speed": 346,
            "lethality": 10,
            "armor_pen_percent": 0.3,
        },
        "Galeforce": {
            "health": 1743,
            "attack_damage": 273,
            "ability_power": 165,
            "armor": 90,
            "magic_resist": 55 - 16,
            "attack_speed": 1.226,
            "move_speed": 380 - 1,  # exceptional case where ahri base_move_speed = 330 multiplied by 1.15 gives 379.5
            # Our program rounds it to 379 and in game the movespeed is rounded to 380 instead
            "lethality": 10,
            "armor_pen_percent": 0.3,
            "crit_chance": 0.2,
        },
    }
    for mythic_item_name, mythic_item in ALL_MYTHIC_ITEMS.items():
        item_names.append(mythic_item_name)
        ahri = Ahri(level=9, inventory=[ALL_ITEMS[item_name]() for item_name in item_names])
        for stat, value in test_dict[mythic_item_name].items():
            if stat == "health":
                assert math.ceil(getattr(ahri, stat)) == value
            elif stat in ["armor_pen_percent", "crit_chance"]:
                assert getattr(ahri, stat) == value
            elif stat == "attack_speed":
                assert round(getattr(ahri, stat), 3) == value
            else:
                assert round(getattr(ahri, stat)) == value
        item_names.remove(mythic_item_name)


def test_black_cleaver():
    ahri = Ahri(level=7, inventory=[BlackCleaver()])
    dummy = Dummy(bonus_resistance=100)
    damage_values = [56, 58, 59, 61, 63, 64, 66, 66]
    armor_values = [95, 90, 85, 80, 75, 70, 70, 70]
    for i in range(8):
        assert round(ahri.auto_attack.damage(dummy)) == damage_values[i]
        ahri.do_auto_attack(dummy)
        assert round(dummy.armor) == armor_values[i]
    ahri.inventory.get_item("Black Cleaver").deapply_buffs(dummy)
    assert round(dummy.armor) == 100
    assert ahri.inventory.get_item("Black Cleaver").carve_stack_count == 0


def test_recurve_bow():
    caitlyn = Caitlyn(level=3, inventory=[RecurveBow()])
    assert round(caitlyn.bonus_attack_speed, 3) == 0.309
    assert round(caitlyn.attack_speed, 3) == 0.857
    dummy = Dummy(bonus_resistance=80)
    assert round(caitlyn.auto_attack.damage(dummy)) == 46
    caitlyn.w_hit = True
    assert round(caitlyn.auto_attack.damage(dummy)) == 91


def test_tiamat():
    # TODO: tests with on hit and multiple targets
    caitlyn = Caitlyn(level=3, inventory=[BFSword(), Tiamat()])
    dummy = Dummy(bonus_resistance=80)
    assert round(caitlyn.auto_attack.damage(dummy)) == 74


def test_rageknife():
    # TODO: test with crit modifiers: https://github.com/PaulQbFeng/too-tanky/issues/69
    # crit_chance/crit_chance_converted test
    default_inventory = [Rageknife(), SerratedDirk(), LastWhisper(), CloakofAgility(), CloakofAgility()]
    crit_values = [(0.3, 0, 0.3), (0.3, 0, 0.3)]
    for i, champion in enumerate([Caitlyn(inventory=default_inventory), Yasuo(inventory=default_inventory)]):
        assert champion.orig_bonus_stats.crit_chance == crit_values[i][0]
        assert champion.crit_chance == crit_values[i][1]
        assert champion._crit_chance == crit_values[i][2]

    dummy = Dummy(bonus_resistance=50)
    caitlyn = Caitlyn(level=7, inventory=[Rageknife()])
    assert round(caitlyn.auto_attack.damage(dummy)) == 54
    caitlyn.w_hit = True
    assert round(caitlyn.auto_attack.damage(dummy)) == 129
    caitlyn = Caitlyn(level=7, inventory=default_inventory)
    assert round(caitlyn.auto_attack.damage(dummy)) == 137
    caitlyn.w_hit = True
    assert round(caitlyn.auto_attack.damage(dummy)) == 270

    yasuo = Yasuo(level=3, inventory=[Rageknife()])
    assert round(yasuo.auto_attack.damage(dummy)) == 43
    yasuo = Yasuo(level=3, inventory=default_inventory)
    assert round(yasuo.auto_attack.damage(dummy)) == 124

    yone = Yone(level=3, inventory=[Rageknife()])
    assert round(yone.auto_attack.damage(dummy)) == 42
    yone = Yone(level=3, inventory=default_inventory)
    assert round(yone.attack_damage) == 113
    assert round(yone.auto_attack.damage(dummy)) == 119
