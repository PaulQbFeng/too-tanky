from typing import List, Optional

import stats
from damage import damage_auto_attack
from data_parser import ALL_CHAMPION_BASE_STATS, SCALING_STAT_NAMES
from inventory import Inventory
from item import ALL_ITEM_CLASSES


# TODO: Might be a good opportunity to use abstract class for base champion
class BaseChampion:
    """
    Base class to represent a champion. It is initialized with the stats of a champion at a given level.
    Some mechanisms are shared accross all champions:
        - equip_item
        - auto attack
    """

    def __init__(self, champion_name: str, item_names: Optional[List[str]] = None, level: int = 1):
        assert isinstance(level, int) and 1 <= level <= 18, "Champion level should be in the [1,18] range"
        self.level = level
        self.inventory = Inventory(item_names=item_names)
        self.orig_base_stats = self.get_champion_base_stats(ALL_CHAMPION_BASE_STATS[champion_name])
        self.item_stats = self.inventory.get_items_total_stats(self.inventory.items)
        self.orig_bonus_stats = self.get_bonus_stats()

    def get_champion_base_stats(self, champion_stats):
        """Takes all the base stats from the input dictionary and create the corresponding attributes in the instance"""

        return {
            stat_name: stats.calculate_stat_from_level(champion_stats, stat_name, self.level)
            for stat_name in SCALING_STAT_NAMES
        }

    def get_bonus_stats(self):  # TODO: add runes
        """Get bonus stats from all sources of bonus stats (items, runes)"""
        if len(self.inventory.items) == 0:
            return dict()
        return self.item_stats

    def equip_item(self, item_name):
        self.inventory.items.append(ALL_ITEM_CLASSES[item_name]())
        self.inventory.initialize_item_passives()
        self.item_stats = self.inventory.get_items_total_stats(self.inventory.items)
        self.orig_bonus_stats = self.get_bonus_stats()

    def auto_attack(self, enemy_champion, is_crit: bool = False):
        """Calculates the damage dealt to an enemy champion with an autoattack"""

        damage = damage_auto_attack(
            base_attack_damage=self.orig_base_stats["attack_damage"],
            base_armor=enemy_champion.orig_base_stats["armor"],
            bonus_attack_damage=self.orig_bonus_stats.get("attack_damage", 0),
            bonus_armor=enemy_champion.orig_bonus_stats.get("armor", 0),
            attacker_level=self.level,
            lethality=self.orig_bonus_stats.get("lethality", 0),
            armor_pen_mult_factor=1 - self.orig_bonus_stats.get("armor_pen_percent", 0) / 100,
            bonus_armor_pen_mult_factor=1 - self.orig_bonus_stats.get("bonus_armor_pen_percent", 0) / 100,
            crit=is_crit,
            crit_damage=self.orig_bonus_stats.get("crit_damage", 0),
        )
        return damage


# Dummy class for tests in practice tool.
class Dummy:
    def __init__(self, health: float, bonus_resistance: int):
        """Dummy champion have the same armor and mr"""
        assert bonus_resistance % 10 == 0
        assert health % 100 == 0
        assert health <= 10000

        self.orig_base_stats = {"armor": 0, "magic_resist": 0}
        self.orig_bonus_stats = {"health": health, "armor": bonus_resistance, "magic_resist": bonus_resistance}


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
