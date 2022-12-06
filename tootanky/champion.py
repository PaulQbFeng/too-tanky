from typing import Callable, List, Optional

import tootanky.stats_calculator as sc
from tootanky.damage import damage_physical_auto_attack
from tootanky.data_parser import ALL_CHAMPION_BASE_STATS
from tootanky.glossary import STAT_BASE_BONUS_ONLY_INIT, STAT_BASE_BONUS_FOR_PROPERTY, STAT_STANDALONE_FROM_BONUS
from tootanky.inventory import Inventory
from tootanky.item import BaseItem


# TODO: Might be a good opportunity to use abstract class for base champion
class BaseChampion:
    """
    Base class to represent a champion. It is initialized with the stats of a champion at a given level.
    Some mechanisms are shared accross all champions:
        - equip_item
        - auto attack
    """

    def __init__(
        self,
        champion_name: str,
        inventory: Optional[List[BaseItem]] = None,
        level: int = 1,
        spell_levels: Optional[List[int]] = None,
    ):
        assert isinstance(level, int) and 1 <= level <= 18, "Champion level should be in the [1,18] range"
        self.level = level
        self.orig_base_stats = sc.get_champion_base_stats(ALL_CHAMPION_BASE_STATS[champion_name].copy(), level=level)
        self.initialize_champion_stats_by_default()

        if spell_levels is None:
            spell_levels = [1, 1, 1, 1]
        self.init_spells(spell_levels)

        self.inventory = Inventory(inventory, champion=self)
        self.orig_bonus_stats = self.get_bonus_stats()
        self.update_champion_stats()

    def initialize_champion_stats_by_default(self):
        """Set all stats to 0"""
        for stat_name in STAT_BASE_BONUS_FOR_PROPERTY:
            setattr(self, "base_" + stat_name, 0)
            setattr(self, "bonus_" + stat_name, 0)

        for stat_name in STAT_BASE_BONUS_ONLY_INIT + STAT_STANDALONE_FROM_BONUS:
            setattr(self, stat_name, 0)

    def update_champion_stats(self):
        """
        Updates the stat depending on the stat type.
            - STAT_BASE_BONUS_ONLY_INIT: set the stat as the sum of orig_base and orig_bonus stat.
            - STAT_BASE_BONUS_FOR_PROPERTY: set base_stat, bonus_stat. the attribute stat is a property.
            - STAT_STANDALONE_FROM_BONUS: set the stat taken from orig_bonus stat (without the bonus_prefix).
        """
        for name in STAT_BASE_BONUS_ONLY_INIT:
            setattr(self, name, self.orig_base_stats.__getattr__(name) + self.orig_bonus_stats.__getattr__(name))

        for name in STAT_BASE_BONUS_FOR_PROPERTY:
            setattr(self, "base_" + name, self.orig_base_stats.__getattr__(name))
            setattr(self, "bonus_" + name, self.orig_bonus_stats.__getattr__(name))

        for name in STAT_STANDALONE_FROM_BONUS:
            setattr(self, name, self.orig_bonus_stats.__getattr__(name))

    def init_spells(self, spell_levels):
        """Initialize spells for the champion"""
        pass

    def getter_wrapper(stat_name: str) -> Callable:
        """Wrapper to use a single getter for all total stat attributes"""

        def total_stat_getter(self):
            """
            The getter uses the the sum of base and bonus stat.
            Items and spells directly impact the base and bonus stat, hence no need for a setter.
            """
            base_value = getattr(self, "base_" + stat_name)
            bonus_value = getattr(self, "bonus_" + stat_name)
            return base_value + bonus_value

        return total_stat_getter

    armor = property(fget=getter_wrapper("armor"))
    magic_resist = property(fget=getter_wrapper("magic_resist"))
    attack_damage = property(fget=getter_wrapper("attack_damage"))

    def get_bonus_stats(self):  # TODO: add runes
        """Get bonus stats from all sources of bonus stats (items, runes)"""
        return self.inventory.item_stats

    def apply_item_active(self, item_name, target):
        assert item_name in [
            item.name for item in self.inventory.items
        ], "The item {} is not in the champion's inventory.".format(item_name)
        selected_item = self.inventory.get_item(item_name)
        assert hasattr(selected_item, "apply_active"), "The item {} does not have an active.".format(item_name)
        return selected_item.apply_active(target)

    def equip_item(self, item: BaseItem):
        item.champion = self
        self.inventory.add_item(item)
        self.orig_bonus_stats = self.get_bonus_stats()
        self.update_champion_stats()

    def unequip_item(self, item_name: str):
        # TODO: This has not been tested yet. Only inventory.remove_item has been tested
        self.inventory.remove_item(item_name)
        self.orig_bonus_stats = self.get_bonus_stats()
        self.update_champion_stats()

    def auto_attack_damage(self, target, is_crit: bool = False):
        """Calculates the damage dealt to an enemy champion with an autoattack"""
        damage = damage_physical_auto_attack(
            base_attack_damage=self.base_attack_damage,
            base_armor=target.base_armor,
            bonus_attack_damage=self.bonus_attack_damage,
            bonus_armor=target.bonus_armor,
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

    def do_auto_attack(self, target, is_crit: bool = False):
        """Deals damage to an enemy champion with an autoattack"""

        damage = self.auto_attack_damage(target, is_crit)
        target.take_damage(damage)

    def reset_health(self):
        self.health = self.orig_base_stats.health + self.orig_bonus_stats.health


# Dummy class for tests in practice tool.
class Dummy(BaseChampion):
    champion_name = "Dummy"

    def __init__(self, health: float, bonus_resistance: int):
        super().__init__(champion_name=__class__.champion_name, inventory=None, level=1)
        """Dummy champion have the same armor and mr"""
        assert bonus_resistance % 10 == 0
        assert health % 100 == 0
        assert health <= 10000
        self.orig_bonus_stats.armor = bonus_resistance
        self.orig_bonus_stats.magic_resist = bonus_resistance
        self.orig_bonus_stats.health = health - 1000

        self.update_champion_stats()
