from typing import Callable, List, Optional

import tootanky.stats_calculator as sc

from tootanky.damage import damage_physical_auto_attack
from tootanky.data_parser import ALL_CHAMPION_BASE_STATS
from tootanky.glossary import (
    STAT_STANDALONE,
    STAT_TOTAL_PROPERTY,
    STAT_UNDERLYING_PROPERTY,
    normalize_champion_name,
)
from tootanky.inventory import Inventory
from tootanky.item import BaseItem
from tootanky.spell_factory import SpellFactory


class BaseChampion:
    """
    Base class to represent a champion. It is initialized with the stats of a champion at a given level.
    Some mechanisms are shared accross all champions:
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
        champion_name = normalize_champion_name(champion_name)
        self.orig_base_stats = sc.get_champion_base_stats(ALL_CHAMPION_BASE_STATS[champion_name].copy(), level=level)
        self.initialize_champion_stats_by_default()

        if spell_levels is None:
            spell_levels = [1, 1, 1, 1]

        self.init_spells(spell_levels)

        self.inventory = Inventory(inventory, champion=self)
        self.orig_bonus_stats = self.get_bonus_stats()
        self.apply_stat_modifiers()
        self.update_champion_stats()

    def initialize_champion_stats_by_default(self):
        """Set all stats to 0"""
        for stat_name in STAT_TOTAL_PROPERTY:
            setattr(self, "base_" + stat_name, 0)
            setattr(self, "bonus_" + stat_name, 0)

        for stat_name in STAT_STANDALONE:
            setattr(self, stat_name, 0)

    def apply_stat_modifiers(self):
        """
        Stat modifier from some items that are applied at the end of the inventory initialisation. (E.g rabadon, infinity_edge)
        Stat modifiers can affect both base and bonus stats (e.g rabadon)
        """
        self.apply_crit_damage_modifier()
        self.apply_ap_multipliers()

    def apply_crit_damage_modifier(self):
        bonus_crit_damage = 0
        if self.inventory.contains("Infinity Edge") and self.orig_bonus_stats.crit_chance >= 0.6:
            bonus_crit_damage += 0.35
        self.orig_bonus_stats.crit_damage += bonus_crit_damage

    def apply_ap_multipliers(self):
        ap_multiplier = 1
        if self.inventory.contains("Vigilant Wardstone"):  # missing ability haste
            ap_multiplier += 0.12
            self.orig_bonus_stats.attack_damage = self.orig_bonus_stats.attack_damage * 1.12
            self.orig_bonus_stats.health = self.orig_bonus_stats.health * 1.12
        if self.inventory.contains("Rabadon's Deathcap"):
            ap_multiplier += 0.35
        self.orig_base_stats.ability_power = self.orig_base_stats.ability_power * ap_multiplier
        self.orig_bonus_stats.ability_power = self.orig_bonus_stats.ability_power * ap_multiplier

    def update_champion_stats(self):
        """
        Updates the stat depending on the stat type.
            - STAT_STANDALONE: set the stat as the sum of orig_base and orig_bonus stat.
            - STAT_TOTAL_PROPERTY: set base_stat, bonus_stat. the attribute stat is a property.
            - STAT_UNDERLYING_PROPERTY: set the _stat. the attribute stat is a property with conditions (like crit_damage)
        """
        for name in STAT_STANDALONE:
            setattr(self, name, self.orig_base_stats.__getattr__(name) + self.orig_bonus_stats.__getattr__(name))

        for name in STAT_TOTAL_PROPERTY:
            setattr(self, "base_" + name, self.orig_base_stats.__getattr__(name))
            setattr(self, "bonus_" + name, self.orig_bonus_stats.__getattr__(name))

        for name in STAT_UNDERLYING_PROPERTY:
            setattr(self, "_" + name, self.orig_bonus_stats.__getattr__(name))

    def init_spells(self, spell_levels):
        """Initialize spells for the champion"""
        if self.champion_name not in SpellFactory()._SPELLS:
            return None

        spells = SpellFactory().get_spells_for_champion(self.champion_name)
        level_q, level_w, level_e, level_r = spell_levels
        self.spell_q = spells["q"](champion=self, level=level_q)
        self.spell_w = spells["w"](champion=self, level=level_w)
        self.spell_e = spells["e"](champion=self, level=level_e)
        self.spell_r = spells["r"](champion=self, level=level_r)

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
