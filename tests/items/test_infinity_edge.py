import pytest

from tootanky.item_factory import InfinityEdge, CloakofAgility
from tootanky.champions import Caitlyn


@pytest.fixture
def infinity_edge():
    return InfinityEdge()


@pytest.fixture
def agility_cloak():
    return CloakofAgility()


def test_item_properties(infinity_edge):
    """
    Tests raw stats and limitations. (Test values need to be retrieved in game)
    """
    assert infinity_edge.price == 3400

    assert set(infinity_edge.stats.get_stat_names()) == {"attack_damage", "crit_chance"}

    assert infinity_edge.stats.attack_damage == 70
    assert infinity_edge.stats.crit_chance == 0.2


def test_infinity_edge_cait(infinity_edge, agility_cloak, dummy_100):
    """
    Tests bonue crit damage
    """
    caitlyn = Caitlyn(level=11, inventory=[infinity_edge] + 2 * [agility_cloak])
    assert caitlyn.crit_damage == 0
    assert round(caitlyn.auto_attack.damage(dummy_100, is_crit=False)) == 83
    assert round(caitlyn.auto_attack.damage(dummy_100, is_crit=True)) == 145

    caitlyn = Caitlyn(level=11, inventory=[infinity_edge] + 3 * [agility_cloak])
    assert caitlyn.crit_damage == 0.35
    assert round(caitlyn.auto_attack.damage(dummy_100, is_crit=False)) == 83
    assert round(caitlyn.auto_attack.damage(dummy_100, is_crit=True)) == 174
