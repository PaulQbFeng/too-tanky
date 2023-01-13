from tootanky.champions import Annie


def test_ignite_level_1(dummy_110):

    dmg_champion_level_1 = [14 * tick for tick in range(1, 6)]

    annie = Annie(level=1, summoner_spells=["Ignite"])

    for i, tick in enumerate(range(1, 6)):
        assert annie.ignite.damage(dummy_110, number_of_ticks=tick) == dmg_champion_level_1[i]


def test_ignite_level_18(dummy_110):

    dmg_champion_level_18 = [82 * tick for tick in range(1, 6)]

    annie = Annie(level=18, summoner_spells=["Ignite"])

    for i, tick in enumerate(range(1, 6)):
        assert annie.ignite.damage(dummy_110, number_of_ticks=tick) == dmg_champion_level_18[i]
