import pytest
from tootanky.champions import Annie
from tootanky.item_factory import (
    CloakofAgility,
    Galeforce,
    LongSword,
    SerratedDirk,
    SeryldasGrudge,
    InfinityEdge,
    NavoriQuickblades,
    Everfrost,
)


def test_inventory_mythic():
    annie = Annie(inventory=[LongSword(), Galeforce(), LongSword(), CloakofAgility()])
    assert annie.item_type_count["Legendary"] == 0
    assert annie.item_type_count["Mythic"] == 1
    assert annie.item_stats.attack_damage == 80
    assert annie.item_stats.crit_chance == 0.35
    assert annie.item_stats.attack_speed == 0.2
    assert annie.item_stats.armor_pen_percent == 0


def test_inventory_legendary():
    annie = Annie(inventory=[LongSword(), Galeforce(), LongSword(), CloakofAgility(), SeryldasGrudge()])
    assert annie.item_type_count["Legendary"] == 1
    assert annie.item_type_count["Mythic"] == 1
    assert annie.item_stats.attack_damage == 125
    assert annie.item_stats.crit_chance == 0.35
    assert annie.item_stats.attack_speed == 0.2
    assert annie.item_stats.armor_pen_percent == 0.3


def test_inventory_unique_passive():
    annie = Annie(
        inventory=[LongSword(), Galeforce(), SerratedDirk(), CloakofAgility(), SeryldasGrudge(), SerratedDirk()]
    )
    assert annie.item_stats.attack_damage == 175
    assert annie.item_stats.lethality == 10


def test_legendary_unicity():
    ie = InfinityEdge()
    with pytest.raises(AssertionError):
        annie = Annie(inventory=[ie, ie])


def test_mythic_unicity():
    everfrost = Everfrost()
    galeforce = Galeforce()
    with pytest.raises(AssertionError):
        annie = Annie(inventory=[everfrost, galeforce])


def test_crit_modifier_unicity():
    ie = InfinityEdge()
    navory = NavoriQuickblades()
    with pytest.raises(AssertionError):
        annie = Annie(inventory=[ie, navory])
