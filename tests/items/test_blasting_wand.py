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
    assert blasting_wand.gold == 850
    assert blasting_wand.stats.ability_power == 40
    assert blasting_wand.limitations is None


def test_equipped(blasting_wand):
    """
    Tests damage output after equipping the item.
    """
    annie = Annie(level=17, inventory=[blasting_wand], spell_levels=(5, 5, 5, 5))
    dummy = Dummy(health=1000, bonus_resistance=30)
    dmg = annie.spell_q.damage(dummy)

    assert round(dmg, 2) == 193.85
