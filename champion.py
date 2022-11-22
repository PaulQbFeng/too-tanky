from damage import damage_auto_attack
from data_parser import ALL_CHAMPION_BASE_STATS, SCALING_STAT_NAMES
from stats import Stats


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
        self.orig_base_stats = Stats()
        self.orig_bonus_stats = Stats()
        self.base_stats = Stats()
        self.bonus_stats = Stats()
        self.update_stat_from_level(ALL_CHAMPION_BASE_STATS[champion_name])
        self.items = []
        self.buff_list = []

    @property
    def orig_total_stats(self):
        stats = Stats()
        stats.add_stats(self.orig_base_stats)
        stats.add_stats(self.orig_bonus_stats)
        return stats

    @property
    def total_stats(self):
        stats = Stats()
        stats.add_stats(self.base_stats)
        stats.add_stats(self.bonus_stats)
        return stats

    def update_stat_from_level(self, champion_stats):
        """Takes all the base stats from the input dictionary and create the corresponding attributes in the instance"""

        def calculate_flat_stat_from_level(base: float, mean_growth_perlevel: float, level: int):
            """As described in league wiki: https://leagueoflegends.fandom.com/wiki/Champion_statistic#Growth_statistic_calculations"""

            return base + mean_growth_perlevel * (level - 1) * (0.7025 + 0.0175 * (level - 1))

        def calculate_stat_from_level(all_base_stats: dict, stat_name: str, level: int):
            """Flat scaling for all stats except for attack speed"""
            stat = all_base_stats[stat_name]
            mean_growth_perlevel = all_base_stats[stat_name + "_perlevel"]
            if stat_name == "attack_speed":
                # attack speed scaling is in % instead of flat. Base increase level 1 is considered to be 0 %.
                percentage_increase = calculate_flat_stat_from_level(0, mean_growth_perlevel, level)
                return stat * (1 + percentage_increase / 100)
            return calculate_flat_stat_from_level(stat, mean_growth_perlevel, level)

        for stat_name in SCALING_STAT_NAMES:
            setattr(self.orig_base_stats, stat_name, calculate_stat_from_level(champion_stats, stat_name, self.level))
            setattr(self.base_stats, stat_name, calculate_stat_from_level(champion_stats, stat_name, self.level))

    def auto_attack(self, enemy_champion):
        """Calculates the damage dealt to an enemy champion with an autoattack"""
        if len(self.buff_list) == 0:
            damage = damage_auto_attack(self.base_stats.attack_damage, self.bonus_stats.attack_damage,
                                        self.total_stats.lethality, self.level, self.total_stats.armor_pen_percent,
                                        self.total_stats.bonus_armor_pen_percent, enemy_champion.base_stats.armor,
                                        enemy_champion.bonus_stats.armor, 0, 1, False, 0)
        else:
            for buff in self.buff_list:
                if buff.transfer_type == 'to owner' or buff.transfer_type == 'to spell':
                    if buff.compatible_damage_type == 'physical' or buff.compatible_spell_type == 'on-hit':
                        # damage_auto_attack can take a buff argument and be adapted for it
                        damage = damage_auto_attack(self.base_stats.attack_damage, self.bonus_stats.attack_damage,
                                                    self.total_stats.lethality, self.level, self.total_stats.armor_pen_percent,
                                                    self.total_stats.bonus_armor_pen_percent, enemy_champion.base_stats.armor,
                                                    enemy_champion.bonus_stats.armor, 0, 1, False, 0)
                    else:
                        damage = damage_auto_attack(self.base_stats.attack_damage, self.bonus_stats.attack_damage,
                                                    self.total_stats.lethality, self.level, self.total_stats.armor_pen_percent,
                                                    self.total_stats.bonus_armor_pen_percent, enemy_champion.base_stats.armor,
                                                    enemy_champion.bonus_stats.armor, 0, 1, False, 0)
                elif buff.transfer_type == 'to enemy':
                    buff.add_buff_to(enemy_champion)
                else:
                    print("this transfer type does not exist")
        return damage

    def equip_item(self, item):
        self.items.append(item)
        item.item_holder = self
        self.orig_bonus_stats.add_stats(item.stats)
        self.bonus_stats.add_stats(item.stats)

    def apply_buffs(self):
        for buff in self.buff_list:
            if buff.transfer_type == 'to owner':
                buff.apply_buff_to(self)



# Dummy class for tests in practice tool.
class Dummy:
    def __init__(self, health: float, bonus_armor: float, bonus_magic_resist: float):
        assert bonus_armor == bonus_magic_resist
        assert bonus_armor % 10 == 0
        assert health % 100 == 0
        assert health <= 10000
        self.orig_base_stats = Stats()
        self.orig_bonus_stats = Stats()
        self.base_stats = Stats()
        self.bonus_stats = Stats()
        self.orig_base_stats.health = health
        self.orig_bonus_stats.armor = bonus_armor
        self.orig_bonus_stats.magic_resist = bonus_magic_resist
        self.base_stats.health = health
        self.bonus_stats.armor = bonus_armor
        self.bonus_stats.magic_resist = bonus_magic_resist


# Each champion has its own class as their spells have different effects.
class Annie(BaseChampion):
    champion_name = "Annie"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)


class Ahri(BaseChampion):
    champion_name = "Ahri"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)


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
