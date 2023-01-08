import pytest

from tootanky.item_factory import DoransBlade


@pytest.fixture
def doransblade():
    return DoransBlade()


def test_item_properties(doransblade):
    """
    Tests raw stats and limitations. (Test values need to be retrieved in game)
    """
    assert doransblade.price == 450

    assert set(doransblade.stats.get_stat_names()) == {"attack_damage", "health"}

    assert doransblade.stats.attack_damage == 8
    assert doransblade.stats.health == 80
