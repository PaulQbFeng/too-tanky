from typing import List

import stats
from damage import damage_after_positive_resistance, damage_auto_attack
from data_parser import ALL_CHAMPION_BASE_STATS, SCALING_STAT_NAMES, ALL_ITEM_STATS


# TODO: Might be a good opportunity to use abstract class for base champion
class BaseChampion:
    """
    Base class to represent a champion. It is initialized with the stats of a champion at a given level.
    Some mechanisms are shared accross all champions:
        - equip_item
        - auto attack
    """

    def __init__(self, champion_name: str, level: int = 1, items: List[str] = None):
        assert isinstance(level, int) and 1 <= level <= 18, "Champion level should be in the [1,18] range"
        self.level = level
        self.items = items
        self.orig_base_stats = self.get_champion_base_stats(ALL_CHAMPION_BASE_STATS[champion_name])
        self.item_stats = self.get_items_total_stats(items)
        self.bonus_stats = self.get_bonus_stats()

    def get_champion_base_stats(self, champion_stats):
        """Takes all the base stats from the input dictionary and create the corresponding attributes in the instance"""
        
        return {stat_name: stats.calculate_stat_from_level(champion_stats, stat_name, self.level) for stat_name in SCALING_STAT_NAMES}

    def get_items_total_stats(self, items):
        """Sum the base stats of each item"""
        if items is None:
            return dict()

        total_item_stats = dict()
        for item_name in items:
            item_stats =  ALL_ITEM_STATS[item_name]
            self.update_bonus_stat_with_item(total_item_stats, item_stats)

        return total_item_stats

    def update_bonus_stat_with_item(self, total_item_stats, item_stats):
        """Update the base stats in the item stats dict with a new item."""
        for stat_name, stat_value in item_stats.items():
            if stat_name not in total_item_stats:
                total_item_stats[stat_name] = stat_value
            else:
                total_item_stats[stat_name] += stat_value

    def get_bonus_stats(self): # TODO: add runes
        """Get bonus stats from all sources of bonus stats (items, runes)"""
        if self.items is None:
            return dict()
        return self.item_stats.copy()

    def equip_item(self, item_name):
        self.items.append(item_name)
        self.update_bonus_stat_with_item(self.item_stats, ALL_ITEM_STATS[item_name])
        self.bonus_stats = self.get_bonus_stats()

    def auto_attack(self, enemy_champion):
        """Calculates the damage dealt to an enemy champion with an autoattack"""
        bonus_attack_damage = self.bonus_stats["attack_damage"] if "attack_damage" in self.bonus_stats else 0
        bonus_armor = enemy_champion.bonus_stats["armor"] if "armor" in enemy_champion.bonus_stats else 0

        damage = damage_auto_attack(
            base_attack_damage=self.orig_base_stats["attack_damage"], 
            bonus_attack_damage=bonus_attack_damage,
            base_armor=enemy_champion.orig_base_stats["armor"],
            bonus_armor=bonus_armor
            )
        return damage

# Dummy class for tests in practice tool.
class Dummy:
    def __init__(self, health: float, bonus_armor: float, bonus_magic_resist: float):
        assert bonus_armor == bonus_magic_resist
        assert bonus_armor % 10 == 0
        assert health % 100 == 0
        assert health <= 10000

        self.orig_base_stats = {"armor": 0, "magic_resist": 0}
        self.bonus_stats = {"health":health, "armor": bonus_armor, "magic_resist": bonus_magic_resist}


# Each champion has its own class as their spells have different effects.
class Annie(BaseChampion):
    champion_name = "Annie"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)


class Ahri(BaseChampion):
    champion_name = "Ahri"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)


class Caitlyn(BaseChampion):
    champion_name = "Caitlyn"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)


class Jax(BaseChampion):
    champion_name = "Jax"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)


class Irelia(BaseChampion):
    champion_name = "Irelia"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)
