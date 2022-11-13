import json
import os

from damage import damage_ad_armor

file = open("data/ddragon/champion.json", encoding="utf8")
dataset = json.load(file)

# define champion list
champion_list = list(dataset["data"].keys())

# build dictionnary {champion_name : {stats}}
ALL_CHAMPION_BASE_STAT = {}
for x in champion_list:
    ALL_CHAMPION_BASE_STAT[x] = dataset["data"][x]["stats"]


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

    def __init__(self, champion_name: str):
        self.initialize_base_stat(champion_name)

    def initialize_base_stat(self, champion_name):
        """Takes all the base stats from the input dictionary and create the corresponding attributes in the instance"""
        self.__dict__.update(ALL_CHAMPION_BASE_STAT[champion_name])

    def auto_attack(self, enemy_champion):
        """Calculates the damage dealt to an enemy champion with an autoattack"""
        return damage_ad_armor(self.attackdamage, enemy_champion.armor)


# Each champion has its own class as their spells have different effects.
class Annie(BaseChampion):
    champion_name = "Annie"

    def __init__(self):
        super().__init__(champion_name=__class__.champion_name)


class Ahri(BaseChampion):
    champion_name = "Ahri"

    def __init__(self):
        super().__init__(champion_name=__class__.champion_name)


class Jax(BaseChampion):
    champion_name = "Jax"

    def __init__(self):
        super().__init__(champion_name=__class__.champion_name)


class Irelia(BaseChampion):
    champion_name = "Irelia"

    def __init__(self):
        super().__init__(champion_name=__class__.champion_name)
