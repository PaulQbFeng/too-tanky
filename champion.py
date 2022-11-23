from typing import List, Optional

import stats_calculator as sc
from damage import damage_auto_attack
from data_parser import ALL_CHAMPION_BASE_STATS
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
        if inventory is None:
            self.inventory = []
        else:
            self.inventory = inventory
        self.unique_item_passives = set()
        for item in self.inventory:
            self.apply_unique_item_passive(item)

        self.item_stats = sc.get_items_total_stats(self.inventory)              
        self.orig_bonus_stats = self.get_bonus_stats()
        self.current_health = self.orig_base_stats.health
        
        self.passive = Spell( "passive", type, level)
        self.q = Spell( "basic", "not leveled", 0)
        self.w = Spell( "basic", "not leveled", 0)
        self.e = Spell( "basic", "not leveled", 0)
        self.r = Spell( "ulti", "not leveled", 0)

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

    def equip_item(self, item: BaseItem):
        assert len(self.inventory) <= 5, "inventory can't contain more than 6 items"
        self.apply_unique_item_passive(item)
        self.inventory.append(item)
        self.item_stats = sc.get_items_total_stats(self.inventory)
        self.orig_bonus_stats = self.get_bonus_stats()

    def auto_attack_damage(self, enemy_champion, is_crit: bool = False):
        """Calculates the damage dealt to an enemy champion with an autoattack"""

        damage = damage_auto_attack(
            base_attack_damage=self.orig_base_stats.attack_damage,
            base_armor=enemy_champion.orig_base_stats.armor,
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

    def take_damage(self, damage):
        """Takes damage from an enemy champion"""

        self.current_health -= damage

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

        self.orig_base_stats = Stats({"armor": 0, "magic_resist": 0})
        self.orig_bonus_stats = Stats({
            "health": health,
            "armor": bonus_resistance,
            "magic_resist": bonus_resistance,
        })
        self.current_health = health

    def take_damage(self, damage):
        """Takes damage from an enemy champion"""

        self.current_health -= damage

class Spell:
    def __init__(self, nature: str = "not leveled", spell_type : str = "not leveled", level : int = 0):
        self.nature = nature
        self.spell_type = spell_type
        self.level = level

# Each champion has its own class as their spells have different effects.
class Annie(BaseChampion):
    champion_name = "Annie"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)

    class Q(Spell):
        damage = 0
        ap_ratio = 0.8
        def __init__(self, level: int = 0, **kwargs):
            super().__init__("magic_damage", level)
            self.update_spell_from_level(level)

        def update_spell_from_level(self, level : int):
            damage_list = [80,115,150,185,220]
            self.damage=damage_list[level -1]
        
        def pre_mitig_damage(self): #pre-mitigation damage , need to add ap ratio
            return self.damage # + ap_ratio * 


class Ahri(BaseChampion):
    champion_name = "Ahri"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)

    def Q(Spell):
        damage = 0
        def __init__(self, level: int = 0, **kwargs):
            super().__init__("magic_damage", level)
            self.update_spell_from_level(level)

        def update_spell_from_level(self, level : int):
            if level == 1:
                self.damage = 2*40
            if level == 2:
                self.damage = 2*65
            if level == 3:
                self.damage = 2*90
            if level == 4:
                self.damage = 2*115
            if level == 5:
                self.damage = 2*140
        
        def pre_mitig_damage(self): #pre-mitigation damage
            return self.damage


class Caitlyn(BaseChampion):
    champion_name = "Caitlyn"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)


class Darius(BaseChampion):
    champion_name = "Darius"

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


class Zed(BaseChampion):
    champion_name = "Zed"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)
