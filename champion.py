from typing import List, Optional

import stats_calculator as sc
from damage import damage_physical_auto_attack
from data_parser import ALL_CHAMPION_BASE_STATS
from glossary import DEFAULT_STAT_LIST, EXTRA_STAT_LIST
from item import BaseItem
from stats import Stats


# TODO: Might be a good opportunity to use abstract class for base champion
class BaseChampion:
    """
    Base class to represent a champion. It is initialized with the stats of a champion at a given level.
    Some mechanisms are shared accross all champions:
        - equip_item
        - auto attack
    """

    def __init__(self, champion_name: str, inventory: Optional[List[BaseItem]] = None, level: int = 1):
        assert isinstance(level, int) and 1 <= level <= 18, "Champion level should be in the [1,18] range"
        self.level = level
        self.orig_base_stats = sc.get_champion_base_stats(ALL_CHAMPION_BASE_STATS[champion_name].copy(), level=level)
        for stat_name in DEFAULT_STAT_LIST:
            setattr(self, "base_" + stat_name, 0)
            setattr(self, "bonus_" + stat_name, 0)
        
        for stat_name in EXTRA_STAT_LIST:
            setattr(self, stat_name, 0)

        for name, value in self.orig_base_stats._dict.items():
            setattr(self, "base_" + name, value)

        if inventory is None:
            self.inventory = []
        else:
            self.inventory = inventory
        self.unique_item_passives = set()
        for item in self.inventory:
            self.apply_unique_item_passive(item)

        self.item_stats = sc.get_items_total_stats(self.inventory)
        self.orig_bonus_stats = self.get_bonus_stats()
        self.add_bonus_stats_to_champion()
    
    def getter_wrapper(stat_name):
        """Wrapper to use a single getter for all total stat attributes"""
        def total_stat_getter(self):
            base_value = getattr(self, "base_" + stat_name)
            bonus_value = getattr(self, "bonus_" + stat_name)
            return base_value + bonus_value
        return total_stat_getter
    
    # TODO: currently the setter is not supporter 
    health = property(fget=getter_wrapper("health"))
    mana = property(fget=getter_wrapper("mana"))
    movespeed = property(fget=getter_wrapper("movespeed"))
    armor = property(fget=getter_wrapper("armor"))
    magic_resist = property(fget=getter_wrapper("magic_resist"))
    attack_range = property(fget=getter_wrapper("attack_range"))
    health_regen = property(fget=getter_wrapper("health_regen"))
    mana_regen = property(fget=getter_wrapper("mana_regen"))
    attack_damage = property(fget=getter_wrapper("attack_damage"))
    ability_power = property(fget=getter_wrapper("ability_power"))
    attack_speed = property(fget=getter_wrapper("attack_speed"))
    crit_chance = property(fget=getter_wrapper("crit_chance"))

    def get_bonus_stats(self):  # TODO: add runes
        """Get bonus stats from all sources of bonus stats (items, runes)"""
        if len(self.inventory) == 0:
            return Stats()
        return self.item_stats

    def apply_unique_item_passive(self, item):
        if item.passive.name not in self.unique_item_passives:
            item.apply_passive()
            if item.passive.unique is True:
                self.unique_item_passives |= {item.passive.name}

    def add_bonus_stats_to_champion(self):
        for name, value in self.orig_bonus_stats._dict.items():
            if name in EXTRA_STAT_LIST:
                setattr(self, name, value)
            elif name in DEFAULT_STAT_LIST:
                setattr(self, "bonus_" + name, value)
            else:
                raise AttributeError(f"{name} stat name not recognized")


    def equip_item(self, item: BaseItem):
        assert len(self.inventory) <= 5, "inventory can't contain more than 6 items"
        self.apply_unique_item_passive(item)
        self.inventory.append(item)
        self.item_stats = sc.get_items_total_stats(self.inventory)
        self.orig_bonus_stats = self.get_bonus_stats()
        self.add_bonus_stats_to_champion()

    def auto_attack_damage(self, enemy_champion, is_crit: bool = False):
        """Calculates the damage dealt to an enemy champion with an autoattack"""

        damage = damage_physical_auto_attack(
            base_attack_damage=self.base_attack_damage,
            base_armor=enemy_champion.base_armor,
            bonus_attack_damage=self.bonus_attack_damage,
            bonus_armor=enemy_champion.bonus_armor,
            attacker_level=self.level,
            lethality=self.lethality,
            armor_pen=self.armor_pen_percent,
            bonus_armor_pen=self.bonus_armor_pen_percent,
            crit=is_crit,
            crit_damage=self.crit_damage,
        )
        return damage

    def take_damage(self, damage):
        """Takes damage from an enemy champion"""

        self.health -= damage

    def do_auto_attack(self, enemy_champion, is_crit: bool = False):
        """Deals damage to an enemy champion with an autoattack"""

        damage = self.auto_attack_damage(enemy_champion, is_crit)
        enemy_champion.take_damage(damage)


# Dummy class for tests in practice tool.
class Dummy:
    def __init__(self, health: float, bonus_resistance: int):
        """Dummy champion have the same armor and mr"""
        assert bonus_resistance % 10 == 0
        assert health % 100 == 0
        assert health <= 10000
        
        self.base_armor = 0
        self.base_magic_resist = 0 
        self.bonus_armor = bonus_resistance
        self.bonus_magic_resist = bonus_resistance
        self.health = health

    def take_damage(self, damage):
        """Takes damage from an enemy champion"""

        self.health -= damage
