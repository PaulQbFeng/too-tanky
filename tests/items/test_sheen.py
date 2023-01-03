import pytest

from tootanky.item_factory import Sheen, BlastingWand, BFSword
from tootanky.champions import Annie, Ezreal


@pytest.fixture
def sheen():
    return Sheen()


def test_item_properties(sheen):
    """
    Tests raw stats and limitations. (Test values need to be retrieved in game)
    """
    assert sheen.price == 700

    assert len(sheen.stats.get_stat_names()) == 0


def test_sheen_std(sheen, dummy_100):
    """
    Basic behaviour of sheen.
    """
    annie = Annie(level=2, inventory=[sheen])
    assert len(annie.on_hits) == 1
    assert round(annie.auto_attack.damage(dummy_100)) == 26
    assert annie.spell_q.damage(dummy_100, spellblade=True) == 40
    assert round(annie.auto_attack.damage(dummy_100)) == 52
    assert round(annie.auto_attack.damage(dummy_100)) == 26


def test_ezreal_q_with_sheen(sheen, dummy_100):
    """
    Sheen proc on hit spell.
    """
    inv = [BlastingWand(), BFSword(), sheen]
    expected_q_dmgs = [92, 105, 117, 130, 142]
    expected_q_sb_dmgs = [133, 146, 158, 171, 183]
    for spell_level in range(1, 6):
        ezreal = Ezreal(level=11, inventory=inv, spell_levels=(spell_level, 1, 1, 1))
        dmg = ezreal.spell_q.damage(dummy_100)
        assert round(dmg) == expected_q_dmgs[spell_level - 1]
        dmg = ezreal.spell_q.damage(dummy_100, spellblade=True)
        assert round(dmg) == expected_q_sb_dmgs[spell_level - 1]
