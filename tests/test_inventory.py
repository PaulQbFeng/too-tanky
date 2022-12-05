from tootanky.inventory import Inventory
from tootanky.item import CloakofAgility, Galeforce, LongSword, SerratedDirk, SeryldaGrudge


def test_inventory():
    inventory = Inventory([LongSword(), Galeforce(), SeryldaGrudge(), LongSword(), CloakofAgility()])
    assert inventory.item_type_count["Legendary"] == 1
    assert inventory.item_type_count["Mythic"] == 1
    assert inventory.item_stats.attack_damage == 125
    assert inventory.item_stats.crit_chance == 0.35
    assert inventory.item_stats.attack_speed == 0.2
    assert inventory.item_stats.armor_pen_percent == 0.3
    inventory.add_item(SeryldaGrudge())
    assert inventory.item_type_count["Legendary"] == 2
    assert inventory.item_type_count["Mythic"] == 1
    assert inventory.item_stats.attack_damage == 170
    assert inventory.item_stats.crit_chance == 0.35
    assert inventory.item_stats.attack_speed == 0.2
    assert inventory.item_stats.armor_pen_percent == 0.51
    inventory.remove_item("Serylda's Grudge")
    assert inventory.item_type_count["Legendary"] == 1
    assert inventory.item_type_count["Mythic"] == 1
    assert inventory.item_stats.attack_damage == 125
    assert inventory.item_stats.crit_chance == 0.35
    assert inventory.item_stats.attack_speed == 0.2
    assert round(inventory.item_stats.armor_pen_percent, 2) == 0.3
    # Test of unique passive feature
    inventory.remove_item("Long Sword")
    inventory.add_item(SerratedDirk())
    assert inventory.item_type_count["Legendary"] == 1
    assert inventory.item_type_count["Mythic"] == 1
    assert inventory.item_stats.attack_damage == 145
    assert inventory.item_stats.lethality == 10
    inventory.add_item(SerratedDirk())
    assert inventory.item_stats.attack_damage == 175
    assert inventory.item_stats.lethality == 10
    inventory.remove_item("Serrated Dirk")
    assert inventory.item_stats.attack_damage == 145
    assert inventory.item_stats.lethality == 10
    inventory.remove_item("Serrated Dirk")
    assert inventory.item_stats.attack_damage == 115
    assert inventory.item_stats.lethality == 0
