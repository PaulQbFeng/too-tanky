from tootanky.inventory import Inventory
from tootanky.item import CloakofAgility, Galeforce, LongSword, SerratedDirk, SeryldaGrudge


def test_inventory():
    inventory = Inventory([LongSword(), Galeforce(), LongSword(), CloakofAgility()])
    assert inventory.item_type_count["Legendary"] == 0
    assert inventory.item_type_count["Mythic"] == 1
    assert inventory.item_stats.attack_damage == 80
    assert inventory.item_stats.crit_chance == 0.35
    assert inventory.item_stats.attack_speed == 0.2
    assert inventory.item_stats.armor_pen_percent == 0
    inventory.add_item(SeryldaGrudge())
    assert inventory.item_type_count["Legendary"] == 1
    assert inventory.item_type_count["Mythic"] == 1
    assert inventory.item_stats.attack_damage == 125
    assert inventory.item_stats.crit_chance == 0.35
    assert inventory.item_stats.attack_speed == 0.2
    assert inventory.item_stats.armor_pen_percent == 0.3
    inventory.remove_item("Serylda's Grudge")
    assert inventory.item_type_count["Legendary"] == 0
    assert inventory.item_type_count["Mythic"] == 1
    assert inventory.item_stats.attack_damage == 80
    assert inventory.item_stats.crit_chance == 0.35
    assert inventory.item_stats.attack_speed == 0.2
    assert round(inventory.item_stats.armor_pen_percent) == 0
    # Test of unique passive feature
    inventory.remove_item("Long Sword")
    inventory.add_item(SerratedDirk())
    assert inventory.item_type_count["Legendary"] == 0
    assert inventory.item_type_count["Mythic"] == 1
    assert inventory.item_stats.attack_damage == 100
    assert inventory.item_stats.lethality == 10
    inventory.add_item(SerratedDirk())
    assert inventory.item_stats.attack_damage == 130
    assert inventory.item_stats.lethality == 10
    inventory.remove_item("Serrated Dirk")
    assert inventory.item_stats.attack_damage == 100
    assert inventory.item_stats.lethality == 10
    inventory.remove_item("Serrated Dirk")
    assert inventory.item_stats.attack_damage == 70
    assert inventory.item_stats.lethality == 0
