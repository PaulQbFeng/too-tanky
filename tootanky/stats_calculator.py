import math

from tootanky.data_parser import SCALING_STAT_NAMES, NON_SCALING_STAT_NAMES, ALL_CHAMPION_BASE_STATS
from tootanky.item_factory import BaseItem
from tootanky.stats import Stats


# champions
def calculate_flat_stat_from_level(base: float, mean_growth_perlevel: float, level: int) -> float:
    """As described in league wiki: https://leagueoflegends.fandom.com/wiki/Champion_statistic#Growth_statistic_calculations"""

    return base + mean_growth_perlevel * (level - 1) * (0.7025 + 0.0175 * (level - 1))


def calculate_base_stat_from_level(base_stats: dict, stat_name: str, level: int) -> float:
    """Flat scaling for all stats except for attack speed"""
    stat = base_stats[stat_name]
    if stat_name == "attack_speed":
        # attack speed per level is considered as bonus attack speed
        return stat

    mean_growth_perlevel = base_stats[stat_name + "_perlevel"]
    return calculate_flat_stat_from_level(stat, mean_growth_perlevel, level)


def calculate_bonus_stat_from_level(base_stats: dict, stat_name: str, level: int) -> float:
    """Bonus scaling for attack speed"""
    if stat_name == "attack_speed":
        # bonus attack speed is in % instead of flat. Bonus attack speed level 1 is considered to be 0 %.
        mean_growth_perlevel = base_stats[stat_name + "_perlevel"]
        percentage_increase = calculate_flat_stat_from_level(0, mean_growth_perlevel, level)
        return percentage_increase / 100
    return 0


def get_champion_base_stats(champion_name: str, level: int) -> Stats:
    """Takes all the base stats from the input dictionary and create the corresponding attributes in the instance"""
    champion_stats = ALL_CHAMPION_BASE_STATS[champion_name].copy()

    stats_dict = dict()
    for stat_name in SCALING_STAT_NAMES:
        stats_dict[stat_name] = calculate_base_stat_from_level(champion_stats, stat_name, level)

    for stat_name in NON_SCALING_STAT_NAMES:
        stats_dict[stat_name] = champion_stats[stat_name]

    if champion_name in ALL_CHAMPION_OUTLIERS_ATTACK_SPEED_RATIO:
        stats_dict["attack_speed_ratio"] = ALL_CHAMPION_OUTLIERS_ATTACK_SPEED_RATIO[champion_name]
    else:
        stats_dict["attack_speed_ratio"] = stats_dict["attack_speed"]
    return Stats(stats_dict)


def get_champion_bonus_stats(champion_name: str, level: int) -> Stats:
    champion_stats = ALL_CHAMPION_BASE_STATS[champion_name].copy()
    return Stats(
        {
            stat_name: calculate_bonus_stat_from_level(champion_stats, stat_name, level)
            for stat_name in SCALING_STAT_NAMES
        }
    )


def get_items_total_stats(items: BaseItem):
    """Return the sum of the base stats + potential passives of each item"""

    total_item_stats = Stats()
    for item in items:
        total_item_stats = total_item_stats + item.stats  # TODO: implem __iadd__
    return total_item_stats


ALL_CHAMPION_OUTLIERS_ATTACK_SPEED_RATIO = {
    "Akshan": 0.4,
    "Amumu": 0.638,
    "Blitzcrank": 0.7,
    "Caitlyn": 0.568,
    "DrMundo": 0.625,
    "Ekko": 0.625,
    "Gangplank": 0.69,
    "Gragas": 0.625,
    "Graves": 0.49,
    "Kayle": 0.667,
    "Kennen": 0.69,
    "Lissandra": 0.625,
    "Lux": 0.625,
    "Malphite": 0.638,
    "Maokai": 0.695,
    "Nautilus": 0.612,
    "Neeko": 0.67,
    "Nilah": 0.67,
    "Qiyana": 0.625,
    "Rammus": 0.625,
    "Sejuani": 0.625,
    "Senna": 0.3,
    "Seraphine": 0.625,
    "Shen": 0.651,
    "Tristana": 0.679,
    "Trundle": 0.67,
    "Udyr": 0.65,
    "Vex": 0.625,
    "Volibear": 0.7,
    "Wukong": 0.658,
    "Yasuo": 0.67,
    "Zac": 0.638,
    "Zeri": 0.625,
}


def round_norm(number: float, decimals=0) -> int:
    """
    In Python, the built-in round function rounds to the nearest even number (bankers rounding).
    e.g round(2.5) == 2 but round(3.5) == 4
    Call this function to ensure it's always rounding up.
    Adapted from https://stackoverflow.com/a/52617883
    """
    expoN = number * 10**decimals
    if abs(expoN) - abs(math.floor(expoN)) < 0.5:
        res = math.floor(expoN)
        if decimals > 0:
            res /= 10**decimals
        return res

    res = math.ceil(expoN)
    if decimals > 0:
        res /= 10**decimals
    return res
