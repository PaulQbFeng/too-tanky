import pytest

from tootanky.item_factory import RabadonsDeathcap, BlastingWand
from tootanky.champions import Ahri


@pytest.fixture
def rabadon():
    return RabadonsDeathcap()


def test_item_properties(rabadon):
    """
    Tests raw stats and limitations. (Test values need to be retrieved in game)
    """
    assert rabadon.price == 3600

    assert set(rabadon.stats.get_stat_names()) == {"ability_power"}

    assert rabadon.stats.ability_power == 120


def test_ap_multiplier(rabadon):
    ahri = Ahri(level=11, inventory=[rabadon])
    assert ahri.ability_power == 162
    ahri = Ahri(level=11, inventory=[rabadon, BlastingWand()])
    assert ahri.ability_power == 216
