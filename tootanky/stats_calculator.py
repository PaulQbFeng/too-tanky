from tootanky.data_parser import SCALING_STAT_NAMES
from tootanky.item import BaseItem
from tootanky.stats import Stats


# champions
def calculate_flat_stat_from_level(base: float, mean_growth_perlevel: float, level: int) -> float:
    """As described in league wiki: https://leagueoflegends.fandom.com/wiki/Champion_statistic#Growth_statistic_calculations"""

    return base + mean_growth_perlevel * (level - 1) * (0.7025 + 0.0175 * (level - 1))


def calculate_stat_from_level(base_stats: dict, stat_name: str, level: int) -> float:
    """Flat scaling for all stats except for attack speed"""
    stat = base_stats[stat_name]
    mean_growth_perlevel = base_stats[stat_name + "_perlevel"]
    if stat_name == "attack_speed":
        # attack speed scaling is in % instead of flat. Base increase level 1 is considered to be 0 %.
        percentage_increase = calculate_flat_stat_from_level(0, mean_growth_perlevel, level)
        return stat * (1 + percentage_increase / 100)
    return calculate_flat_stat_from_level(stat, mean_growth_perlevel, level)


def get_champion_base_stats(champion_stats, level):
    """Takes all the base stats from the input dictionary and create the corresponding attributes in the instance"""

    return Stats(
        {stat_name: calculate_stat_from_level(champion_stats, stat_name, level) for stat_name in SCALING_STAT_NAMES}
    )


def get_items_total_stats(items: BaseItem):
    """Return the sum of the base stats + potential passives of each item"""

    total_item_stats = Stats()
    for item in items:
        total_item_stats = total_item_stats + item.stats  # TODO: implem __iadd__
    return total_item_stats