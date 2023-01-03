import pytest

from tootanky.item_factory import BlastingWand
from tootanky.champions import Annie
from tootanky.champion import Dummy


@pytest.fixture
def blasting_wand():
    return BlastingWand()


def test_item_properties(blasting_wand):
    """
    Tests raw stats and limitations. (Test values need to be retrieved in game)
    """
    assert blasting_wand.price == 850

    assert set(blasting_wand.stats.get_stat_names()) == {"ability_power"}

    assert blasting_wand.stats.ability_power == 40
