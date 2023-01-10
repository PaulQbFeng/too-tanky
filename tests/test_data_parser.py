from tootanky.data_parser import ALL_CHAMPION_BASE_STATS, ALL_CHAMPION_SPELLS


def test_normalize_name_consistency():
    assert sorted(list(ALL_CHAMPION_BASE_STATS.keys()), key=str.casefold) == sorted(
        list(ALL_CHAMPION_SPELLS.keys()) + ["Dummy"], key=str.casefold
    )
