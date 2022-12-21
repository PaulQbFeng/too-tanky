import pytest
from tootanky.inventory import Inventory
from tootanky.item import (
    CloakofAgility,
    Galeforce,
    LongSword,
    SerratedDirk,
    SeryldasGrudge,
    InfinityEdge,
    NavoriQuickblades,
)


def test_inventory():
    inventory = Inventory([LongSword(), Galeforce(), LongSword(), CloakofAgility()])
    assert inventory.item_type_count["Legendary"] == 0
    assert inventory.item_type_count["Mythic"] == 1
    assert inventory.item_stats.attack_damage == 80
    assert inventory.item_stats.crit_chance == 0.35
    assert inventory.item_stats.attack_speed == 0.2
    assert inventory.item_stats.armor_pen_percent == 0
    inventory = Inventory([LongSword(), Galeforce(), LongSword(), CloakofAgility(), SeryldasGrudge()])
    assert inventory.item_type_count["Legendary"] == 1
    assert inventory.item_type_count["Mythic"] == 1
    assert inventory.item_stats.attack_damage == 125
    assert inventory.item_stats.crit_chance == 0.35
    assert inventory.item_stats.attack_speed == 0.2
    assert inventory.item_stats.armor_pen_percent == 0.3
    # Test of unique passive feature
    inventory = Inventory(
        [LongSword(), Galeforce(), SerratedDirk(), CloakofAgility(), SeryldasGrudge(), SerratedDirk()]
    )
    assert inventory.item_stats.attack_damage == 175
    assert inventory.item_stats.lethality == 10


def test_legendary_unicity():
    ie = InfinityEdge()
    assert ie.stats.attack_damage == 70
    assert ie.stats.crit_chance == 0.2
    with pytest.raises(AssertionError):
        inv = Inventory([ie, ie])


def test_crit_modifier_unicity():
    ie = InfinityEdge()
    navory = NavoriQuickblades()
    with pytest.raises(AssertionError):
        inv = Inventory([ie, navory])
