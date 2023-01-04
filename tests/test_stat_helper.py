from tootanky.stats_calculator import round_norm


def test_round_norm():
    assert round_norm(0.5) == 1
    assert isinstance(round_norm(0.5), int)
    assert round_norm(1.5) == 2
    assert round_norm(0.125, 2) == 0.13
    assert round_norm(23.55, 1) == 23.6
