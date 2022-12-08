import pytest

from tootanky.champion import Dummy
from tootanky.champions import Ahri, Annie
from tootanky.damage import damage_after_positive_resistance
from tootanky.item import ALL_ITEM_CLASSES, DoranBlade, Sheen, InfinityEdge
from tootanky.inventory import Inventory


def test_doranblade():
    doranblade = DoranBlade()
    assert doranblade.stats._dict == {"attack_damage": 8, "health": 80}


def test_infinity_edge():
    ie = InfinityEdge()
    assert ie.stats.attack_damage == 70
    assert ie.stats.crit_chance == 0.2


def test_sheen():
    sheen = Sheen()
    annie = Annie()
    dummy = Dummy(health=1000, bonus_resistance=50)
    assert sheen.spellblade(annie, dummy) == damage_after_positive_resistance(
        annie.base_attack_damage, dummy.bonus_armor
    )


def test_serrated_unique_passive():
    item_names = ["Serrated Dirk", "Last Whisper"]
    inventory = [ALL_ITEM_CLASSES[item_name]() for item_name in item_names]
    ahri = Ahri(level=7, inventory=inventory)

    assert ahri.orig_bonus_stats.attack_damage == 50
    assert ahri.orig_bonus_stats.lethality == 10
    assert ahri.orig_bonus_stats.armor_pen_percent == 0.18

    item_names = ["Serrated Dirk", "Last Whisper", "Serrated Dirk"]
    inventory = [ALL_ITEM_CLASSES[item_name]() for item_name in item_names]
    ahri = Ahri(level=7, inventory=inventory)

    assert ahri.orig_bonus_stats.attack_damage == 80
    assert ahri.orig_bonus_stats.lethality == 10
    assert ahri.orig_bonus_stats.armor_pen_percent == 0.18


def galeforce_default_run(
    item_names, target, test_bonus_attack_damage: float, test_crit_chance: float, test_active: list
):
    inventory = [ALL_ITEM_CLASSES[item_name]() for item_name in item_names]
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
