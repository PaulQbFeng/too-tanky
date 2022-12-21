from typing import Callable, List, Optional

import tootanky.stats_calculator as sc

from tootanky.damage import damage_physical_auto_attack
from tootanky.data_parser import ALL_CHAMPION_BASE_STATS
from tootanky.glossary import (
    STAT_SUM_BASE_BONUS,
    STAT_STANDALONE,
    STAT_TOTAL_PROPERTY,
    STAT_UNDERLYING_PROPERTY,
    STAT_TEMPORARY_BUFF,
    normalize_champion_name,
)
from tootanky.inventory import Inventory
from tootanky.item import BaseItem, SPELL_BLADE_ITEMS, ON_HIT_ITEMS
from tootanky.spell_factory import SpellFactory
from tootanky.stats import Stats


class BaseChampion:
    """
    Base class to represent a champion. It is initialized with the stats of a champion at a given level.
    Some mechanisms are shared accross all champions:
        - auto attack
    """

    def __init__(
            self,
            champion_name: str,
            level: int = 1,
            inventory: Optional[List[BaseItem]] = None,
            spell_levels: Optional[List[int]] = None,
            spell_max_order: Optional[List[str]] = None,
    ):
        assert isinstance(level, int) and 1 <= level <= 18, "Champion level should be in the [1,18] range"
        self.level = level
        champion_name = normalize_champion_name(champion_name)
        self.orig_base_stats = sc.get_champion_base_stats(ALL_CHAMPION_BASE_STATS[champion_name].copy(), level=level)
        self.orig_bonus_stats = sc.get_champion_bonus_stats(ALL_CHAMPION_BASE_STATS[champion_name].copy(), level=level)
        self.initialize_champion_stats_by_default()

        if spell_levels is None:
            if spell_max_order is None:
                spell_levels = [1, 1, 1, 1]
            else:
                self.spell_max_order = spell_max_order
                spell_levels = self.get_default_spell_levels()

        self.init_spells(spell_levels)

        self.inventory = Inventory(inventory, champion=self)
        self.orig_bonus_stats += self.get_bonus_stats()
        self.orig_bonus_stats += self.get_mythic_passive_stats()
        self.apply_stat_modifiers()
        self.apply_caps()  # TODO: test if caps have to be applied before or after modifiers (cannot be tested for
        # ability haste because the cap is unattainable
        self.__update_champion_stats()

        self.on_hits = []
        self.spellblade_item = None

        for name in SPELL_BLADE_ITEMS:
            if self.inventory.contains(name):
                self.spellblade_item = self.inventory.get_item(name)
                self.on_hits.append(self.spellblade_item)
                break
        for name in ON_HIT_ITEMS:
            if self.inventory.contains(name):
                self.on_hits.append(self.inventory.get_item(name))

    def initialize_champion_stats_by_default(self):
        """Set all stats to 0"""
        for stat_name in STAT_SUM_BASE_BONUS:
            setattr(self, stat_name, 0)

        for stat_name in STAT_STANDALONE + STAT_TEMPORARY_BUFF:
            setattr(self, stat_name, 0)

        for stat_name in STAT_TOTAL_PROPERTY:
            setattr(self, "base_" + stat_name, 0)
            setattr(self, "bonus_" + stat_name, 0)

    def get_mythic_passive_stats(self):
        if self.inventory.item_type_count["Mythic"] == 1:
            mythic_item = self.inventory.get_mythic_item()
            mythic_passive_stats = dict()
            for mythic_passive_stat in mythic_item.mythic_passive_stats:
                stat_name, value, value_type = mythic_passive_stat
                value *= self.inventory.item_type_count["Legendary"]
                assert value_type in ["flat", "percent"], "mythic_passive_stats[2] must be flat or percent."
                if any(s in stat_name for s in STAT_SUM_BASE_BONUS):
                    assert not stat_name.startswith("base_"), "Base {} isn't affected by mythic passives.".format(
                        stat_name.replace("base_", "")
                    )
                    stat = stat_name.replace("bonus_", "")
                    if value_type == "percent":
                        value = value * (getattr(self.orig_base_stats, stat) + getattr(self.orig_bonus_stats, stat))
                if any(s in stat_name for s in STAT_STANDALONE + STAT_TOTAL_PROPERTY):
                    assert not stat_name.startswith("base_"), "Base {} isn't affected by mythic passives.".format(
                        stat_name.replace("base_", "")
                    )
                    stat = stat_name.replace("bonus_", "")
                    if stat == "move_speed":
                        stat = stat + "_" + value_type
                    else:
                        assert value_type == "flat", "Only flat bonuses for {} in mythic passives.".format(stat)
                mythic_passive_stats[stat] = value

            return Stats(mythic_passive_stats)
        else:
            return Stats()

    def get_default_spell_levels(self):
        # This method will be overriden for champions like jayce, udyr, etc.
        spell_1, spell_2, spell_3 = self.spell_max_order
        default_order = [
            spell_1, spell_2, spell_3, spell_1, spell_1, "r",
            spell_1, spell_2, spell_1, spell_2, "r",
            spell_2, spell_2, spell_3, spell_3, "r",
            spell_3, spell_3
        ]
        default_order_per_level = default_order[0:self.level]
        return [
            default_order_per_level.count("q"),
            default_order_per_level.count("w"),
            default_order_per_level.count("e"),
            default_order_per_level.count("r")
        ]

    def apply_stat_modifiers(self):
        """
        Stat modifier from some items that are applied at the end of the inventory initialisation. (E.g rabadon, infinity_edge)
        Stat modifiers can affect both base and bonus stats (e.g rabadon)
        """
        self.apply_crit_damage_modifier()
        self.apply_item_multipliers()

    def apply_caps(self):
        """
        Some stats are capped at a certain amount (attack_speed, ability_haste, ...)
        """
        self.orig_bonus_stats.ability_haste = min(self.orig_bonus_stats.ability_haste, 500)

    def apply_crit_damage_modifier(self):
        bonus_crit_damage = 0
        if self.inventory.contains("Infinity Edge") and self.orig_bonus_stats.crit_chance >= 0.6:
            bonus_crit_damage += 0.35
        self.orig_bonus_stats.crit_damage += bonus_crit_damage

    def apply_item_multipliers(self):
        ap_multiplier = 1
        if self.inventory.contains("Vigilant Wardstone"):  # missing ability haste
            ap_multiplier += 0.12
            self.orig_bonus_stats.attack_damage *= 1.12
            self.orig_bonus_stats.health *= 1.12
            self.orig_bonus_stats.ability_haste *= 1.12
        if self.inventory.contains("Rabadon's Deathcap"):
            ap_multiplier += 0.35
        self.orig_base_stats.ability_power *= ap_multiplier
        self.orig_bonus_stats.ability_power *= ap_multiplier

    def apply_black_cleaver(self, target):
        if self.inventory.contains("Black Cleaver"):
            carve_stack_value = self.inventory.get_item("Black Cleaver").get_carve_stack_stats(target)
            target.update_armor_stats(percent_debuff=carve_stack_value)
        pass

    def __update_champion_stats(self):
        """
        Updates/restores the stat depending on the stat type.
            - STAT_SUM_BASE_BONUS: set the stat as the sum of orig_base and orig_bonus stat.
            - STAT_STANDALONE: set the stat as orig_bonus stat.
            - STAT_TOTAL_PROPERTY: set base_stat, bonus_stat. the attribute stat is a property.
            - STAT_UNDERLYING_PROPERTY: set the _stat. the attribute stat is a property with conditions (like
            crit_damage)
            - STAT_TEMPORARY_BUFF: set the stat back to 0.
        """
        for name in STAT_SUM_BASE_BONUS:
            setattr(self, name, self.orig_base_stats.__getattr__(name) + self.orig_bonus_stats.__getattr__(name))

        for name in STAT_STANDALONE:
            setattr(self, name, self.orig_bonus_stats.__getattr__(name))

        for name in STAT_TOTAL_PROPERTY:
            setattr(self, "base_" + name, self.orig_base_stats.__getattr__(name))
            if name == "move_speed":
                self.move_speed_flat = self.orig_bonus_stats.move_speed_flat
                self.move_speed_percent = self.orig_bonus_stats.move_speed_percent
            else:
                setattr(self, "bonus_" + name, self.orig_bonus_stats.__getattr__(name))

        for name in STAT_UNDERLYING_PROPERTY:
            setattr(self, "_" + name, self.orig_bonus_stats.__getattr__(name))

        for name in STAT_TEMPORARY_BUFF:
            setattr(self, name, 0)

    def restore_champion_stats(self):
        self.__update_champion_stats()

    def update_armor_stats(self, flat_debuff: float = 0, percent_debuff: float = 0):
        """
        Updates armor with additional armor reduction debuffs. (no debuffs by default)
        """
        self.armor_reduction_flat += flat_debuff
        self.armor_reduction_percent = 1 - (1 - self.armor_reduction_percent) * (1 - percent_debuff)
        orig_base_armor = self.orig_base_stats.armor
        orig_bonus_armor = self.orig_bonus_stats.armor
        orig_total_armor = orig_base_armor + orig_bonus_armor
        if orig_total_armor == 0:
            self.bonus_armor = orig_bonus_armor - self.armor_reduction_flat
        else:
            self.base_armor = orig_base_armor - self.armor_reduction_flat * orig_base_armor / orig_total_armor
            self.bonus_armor = orig_bonus_armor - self.armor_reduction_flat * orig_bonus_armor / orig_total_armor
        if self.base_armor + self.bonus_armor > 0:
            self.base_armor *= (1 - self.armor_reduction_percent)
            self.bonus_armor *= (1 - self.armor_reduction_percent)

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
            if stat_name == "attack_speed":
                # missing attack speed cap, any bonus AS above the cap still affects scalings
                # missing attack speed decrease (stacks multiplicatively and take percentages off the final attack speed
                # value after all bonus attack speed has been factored in)
                bonus_value = getattr(self, "bonus_" + stat_name)
                return base_value * (1 + bonus_value)
            elif stat_name == "move_speed":  # missing slow ratio and multiplicative movespeed bonus
                bonus_flat = self.move_speed_flat
                bonus_percent = self.move_speed_percent
                return (base_value + bonus_flat) * (1 + bonus_percent)
            else:
                bonus_value = getattr(self, "bonus_" + stat_name)
                return base_value + bonus_value

        return total_stat_getter

    armor = property(fget=getter_wrapper("armor"))
    magic_resist = property(fget=getter_wrapper("magic_resist"))
    attack_damage = property(fget=getter_wrapper("attack_damage"))
    ability_power = property(fget=getter_wrapper("ability_power"))
    attack_speed = property(fget=getter_wrapper("attack_speed"))
    move_speed = property(fget=getter_wrapper("move_speed"))

    def get_bonus_stats(self):  # TODO: add runes
        """
        Get bonus stats from all sources of bonus stats (items, runes).
        This does not include mythic passives.
        """
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
        on_hit_damage = 0
        for on_hit_source in self.on_hits:
            on_hit_damage = on_hit_source.on_hit_effect(target)
        return damage + on_hit_damage

    def take_damage(self, damage):
        """Takes damage from an enemy champion"""

        self.health -= damage

    def do_auto_attack(self, target, is_crit: bool = False):
        """Deals damage to an enemy champion with an autoattack"""

        damage = self.auto_attack_damage(target, is_crit)
        target.take_damage(damage)
        self.apply_black_cleaver(target)

    def reset_health(self):
        self.health = self.orig_base_stats.health + self.orig_bonus_stats.health


# Dummy class for tests in practice tool.
class Dummy(BaseChampion):
    champion_name = "Dummy"

    def __init__(self, health: float = 1000, bonus_resistance: int = 0):
        super().__init__(champion_name=__class__.champion_name, inventory=None, level=1)
        """Dummy champion have the same armor and mr"""
        assert bonus_resistance % 10 == 0
        assert health % 100 == 0
        assert health <= 10000
        self.orig_bonus_stats.armor = bonus_resistance
        self.orig_bonus_stats.magic_resist = bonus_resistance
        self.orig_bonus_stats.health = health - 1000
        self.restore_champion_stats()
