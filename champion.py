from damage import damage_after_positive_resistance
from data_parser import ALL_CHAMPION_BASE_STATS, SCALING_STAT_NAMES


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
        self.update_stat_from_level(ALL_CHAMPION_BASE_STATS[champion_name])
        self.passive = Spell( "passive", type, level)
        self.q = Spell( "basic", "not leveled", 0)
        self.w = Spell( "basic", "not leveled", 0)
        self.e = Spell( "basic", "not leveled", 0)
        self.r = Spell( "ulti", "not leveled", 0)

    def update_stat_from_level(self, champion_stats):
        """Takes all the base stats from the input dictionary and create the corresponding attributes in the instance"""

        def calculate_flat_stat_from_level(base: float, mean_growth_perlevel: float, level: int):
            """As described in league wiki: https://leagueoflegends.fandom.com/wiki/Champion_statistic#Growth_statistic_calculations"""

            return base + mean_growth_perlevel * (level - 1) * (0.7025 + 0.0175 * (level - 1))

        def calculate_stat_from_level(base_stats: dict, stat_name: str, level: int):
            """Flat scaling for all stats except for attack speed"""
            stat = base_stats[stat_name]
            mean_growth_perlevel = base_stats[stat_name + "_perlevel"]
            if stat_name == "attack_speed":
                # attack speed scaling is in % instead of flat. Base increase level 1 is considered to be 0 %.
                percentage_increase = calculate_flat_stat_from_level(0, mean_growth_perlevel, level)
                return stat * (1 + percentage_increase / 100)
            return calculate_flat_stat_from_level(stat, mean_growth_perlevel, level)

        for stat_name in SCALING_STAT_NAMES:
            setattr(self, stat_name, calculate_stat_from_level(champion_stats, stat_name, self.level))

    def auto_attack(self, enemy_champion):
        """Calculates the damage dealt to an enemy champion with an autoattack"""
        return damage_after_positive_resistance(self.attack_damage, enemy_champion.armor)


# Dummy class for tests in practice tool.
class Dummy:
    def __init__(self, health: float, bonus_armor: float, bonus_magic_resist: float):
        assert bonus_armor == bonus_magic_resist
        assert bonus_armor % 10 == 0
        assert health % 100 == 0
        assert health <= 10000
        self.health = health
        self.armor = 0
        self.magic_resist = 0
        self.bonus_armor = bonus_armor
        self.bonus_magic_resist = bonus_magic_resist

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


class Jax(BaseChampion):
    champion_name = "Jax"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)


class Irelia(BaseChampion):
    champion_name = "Irelia"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)


