from typing import Callable, List, Optional

import tootanky.stats_calculator as sc
from tootanky.damage import damage_physical_auto_attack
from tootanky.data_parser import ALL_CHAMPION_BASE_STATS
from tootanky.glossary import DEFAULT_STAT_LIST, EXTRA_STAT_LIST
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
        for stat_name in DEFAULT_STAT_LIST:
            setattr(self, "base_" + stat_name, 0)
            setattr(self, "bonus_" + stat_name, 0)

        for stat_name in EXTRA_STAT_LIST:
            setattr(self, stat_name, 0)

        for name, value in self.orig_base_stats._dict.items():
            setattr(self, "base_" + name, value)

        if spell_levels is None:
            spell_levels = [1, 1, 1, 1]
        self.init_spells(spell_levels)

        self.inventory = Inventory(inventory, champion=self)
        self.orig_bonus_stats = self.get_bonus_stats()
        self.add_bonus_stats_to_champion()

        for stat_name in DEFAULT_STAT_LIST:
            setattr(self, "_" + stat_name, getattr(self, "base_" + stat_name) + getattr(self, "bonus_" + stat_name))

    def init_spells(self, spell_levels):
        """Initialize spells for the champion"""
        pass

    def getter_wrapper(stat_name: str) -> Callable:
        """Wrapper to use a single getter for all total stat attributes"""

        def total_stat_getter(self):
            base_value = getattr(self, "base_" + stat_name)
            bonus_value = getattr(self, "bonus_" + stat_name)
            return base_value + bonus_value

        return total_stat_getter

    # TODO: define specific setters for stats that are handled differently
    #       for example: armor with flat and percent armor reduction
    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value

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
        return self.inventory.item_stats

    def apply_item_active(self, item_name, target):
        assert item_name in [
            item.item_name for item in self.inventory.items
        ], "The item {} is not in the champion's inventory.".format(item_name)
        selected_item = self.inventory.get_item(item_name)
        assert hasattr(selected_item, "apply_active"), "The item {} does not have an active.".format(item_name)
        return selected_item.apply_active(target)

    def add_bonus_stats_to_champion(self):
        for name, value in self.orig_bonus_stats._dict.items():
            if name in EXTRA_STAT_LIST:
                setattr(self, name, value)
            elif name in DEFAULT_STAT_LIST:
                setattr(self, "bonus_" + name, value)
            else:
                raise AttributeError(f"{name} stat name not recognized")

    def equip_item(self, item: BaseItem):
        item.champion = self
        self.inventory.add_item(item)
        self.orig_bonus_stats = self.get_bonus_stats()
        self.add_bonus_stats_to_champion()

    def unequip_item(self, item_name: str):
        # TODO: This has not been tested yet. Only inventory.remove_item has been tested
        self.inventory.remove_item(item_name)
        self.orig_bonus_stats = self.get_bonus_stats()
        self.add_bonus_stats_to_champion()

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

        self._health -= damage

    def do_auto_attack(self, target, is_crit: bool = False):
        """Deals damage to an enemy champion with an autoattack"""

        damage = self.auto_attack_damage(target, is_crit)
        target.take_damage(damage)


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
        self.bonus_armor = bonus_resistance
        self.bonus_magic_resist = bonus_resistance
        self.base_health = 1000
        self.bonus_health = health - 1000
        self._health = self.base_health + self.bonus_health
