from damage import damage_ad_armor


annie_stats = {
    "hp": 594,
    "hpperlevel": 102,
    "mp": 418,
    "mpperlevel": 25,
    "movespeed": 335,
    "armor": 19,
    "armorperlevel": 5.2,
    "spellblock": 30,
    "spellblockperlevel": 1.3,
    "attackrange": 625,
    "hpregen": 5.5,
    "hpregenperlevel": 0.55,
    "mpregen": 8,
    "mpregenperlevel": 0.8,
    "crit": 0,
    "critperlevel": 0,
    "attackdamage": 50,
    "attackdamageperlevel": 2.65,
    "attackspeedperlevel": 1.36,
    "attackspeed": 0.579
}

ahri_stats = {
    "hp": 570,
    "hpperlevel": 96,
    "mp": 418,
    "mpperlevel": 25,
    "movespeed": 330,
    "armor": 18,
    "armorperlevel": 4.7,
    "spellblock": 30,
    "spellblockperlevel": 1.3,
    "attackrange": 550,
    "hpregen": 2.5,
    "hpregenperlevel": 0.6,
    "mpregen": 8,
    "mpregenperlevel": 0.8,
    "crit": 0,
    "critperlevel": 0,
    "attackdamage": 53,
    "attackdamageperlevel": 3,
    "attackspeedperlevel": 2,
    "attackspeed": 0.668
}

ALL_CHAMPION_BASE_STAT = {
    "annie": annie_stats,
    "ahri": ahri_stats
}


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
    champion_name = "annie"
    def __init__(self):
        super().__init__(champion_name=__class__.champion_name)

class Ahri(BaseChampion):
    champion_name = "ahri"
    def __init__(self):
        super().__init__(champion_name=__class__.champion_name)