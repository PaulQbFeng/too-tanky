
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