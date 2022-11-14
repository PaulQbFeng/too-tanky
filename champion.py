import json

import numpy as np

from damage import damage_ad_armor
from data_parser import SCALING_STAT_NAMES, ALL_CHAMPION_BASE_STATS


# TODO: Might be a good opportunity to use abstract class for base champion
class BaseChampion:
    """
    Base class to represent a champion. It is initialized with level 1 stats and have traits shared
    accross all champions:
        - Base State
        - Level up mechanism
        - Equip item
        - auto attack
        ...
    """

    def __init__(self, champion_name: str, level: int = 1):
        assert isinstance(level, int) and 1 <= level <= 18, "Champion level should be in the [1,18] range"
        self.level = level
        self.base_stats = ALL_CHAMPION_BASE_STATS[champion_name]
        self.update_stat_from_level()
        
    def update_stat_from_level(self):
        """Takes all the base stats from the input dictionary and create the corresponding attributes in the instance"""

        def calculate_flat_stat_from_level(base: float, mean_growth_perlevel: float, level: int):
            """As described in league wiki: https://leagueoflegends.fandom.com/wiki/Champion_statistic#Growth_statistic_calculations"""
            
            return base + mean_growth_perlevel * (level - 1) * (0.7025 + 0.0175 * (level - 1))

        def calculate_stat_from_level(base_stats: dict, stat_name: str, level: int):
            """Flat scaling for all stats except for attack speed"""
            stat = base_stats[stat_name]
            mean_growth_perlevel = base_stats[stat_name + "perlevel"]
            if stat_name == "attackspeed":
                # attack speed scaling is in % instead of flat. Base increase level 1 is considered to be 0 %.
                percentage_increase = calculate_flat_stat_from_level(0, mean_growth_perlevel, level)
                return stat * (1 + percentage_increase / 100)
            return calculate_flat_stat_from_level(stat, mean_growth_perlevel, level)

        for stat_name in SCALING_STAT_NAMES:
            self.__dict__[stat_name] = calculate_stat_from_level(self.base_stats, stat_name, self.level)

    def auto_attack(self, enemy_champion):
        """Calculates the damage dealt to an enemy champion with an autoattack"""
        return damage_ad_armor(self.attackdamage, enemy_champion.armor)

    def get_stats(self):
        """Get the dictionnary of stats"""
        stats={}
        for stat_name in SCALING_STAT_NAMES:
            stats[stat_name] = (self.__dict__[stat_name])
        return stats

# Each champion has its own class as their spells have different effects.
class Annie(BaseChampion):
    champion_name = "Annie"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)


class Ahri(BaseChampion):
    champion_name = "Ahri"

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
