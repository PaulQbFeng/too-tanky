import json
import os

import numpy as np

from damage import damage_ad_armor

file = open("data/ddragon/champion.json", encoding="utf8")
dataset = json.load(file)

# define champion list
champion_list = list(dataset["data"].keys())

# build dictionnary {champion_name : {stats}}
ALL_CHAMPION_BASE_STAT = {}
for x in champion_list:
    ALL_CHAMPION_BASE_STAT[x] = dataset["data"][x]["stats"]

scaling_stat_names = [
    "hp",
    "mp",
    "armor",
    "spellblock",
    "hpregen",
    "mpregen",
    "crit",
    "attackdamage",
    "attackspeed",
]

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

    def __init__(self, champion_name: str, level: int):
        assert level in np.arange(1, 19), "Champion level should be in the [1,18] range"
        self.level = level
        self.base_stats = ALL_CHAMPION_BASE_STAT[champion_name]
        self.update_stat_from_level()

    def update_stat_from_level(self):
        """Takes all the base stats from the input dictionary and create the corresponding attributes in the instance"""

        def get_stat_from_level(base_stats: dict, stat_name: str):
            """Flat scaling for all stats except for attack speed"""
            stat = base_stats[stat_name]
            stat_perlevel = base_stats[stat_name + "perlevel"]
            if stat_name == "attackspeed":
                # attack speed scaling is in % instead of flat.
                return stat * (1 + stat_perlevel * (self.level - 1) / 100)
            return stat + stat_perlevel * (self.level - 1)

        for stat_name in scaling_stat_names:
            self.__dict__[stat_name] = get_stat_from_level(self.base_stats, stat_name)

    def auto_attack(self, enemy_champion):
        """Calculates the damage dealt to an enemy champion with an autoattack"""
        return damage_ad_armor(self.attackdamage, enemy_champion.armor)


# Each champion has its own class as their spells have different effects.
class Annie(BaseChampion):
    champion_name = "Annie"

    def __init__(self, level: int = 1):
        super().__init__(champion_name=__class__.champion_name, level=level)


class Ahri(BaseChampion):
    champion_name = "Ahri"

    def __init__(self, level: int = 1):
        super().__init__(champion_name=__class__.champion_name, level=level)


class Jax(BaseChampion):
    champion_name = "Jax"

    def __init__(self, level: int = 1):
        super().__init__(champion_name=__class__.champion_name, level=level)


class Irelia(BaseChampion):
    champion_name = "Irelia"

    def __init__(self, level: int = 1):
        super().__init__(champion_name=__class__.champion_name, level=level)
