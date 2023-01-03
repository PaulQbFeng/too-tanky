import math

from tootanky.champions import Annie
from tootanky.item_factory import BlastingWand


def test_stat_level_1():
    """
    Tests champion's main stats at level 1
    """
    annie = Annie(level=1)

    assert math.ceil(annie.health) == 594
    assert annie.mana == 418
    assert round(annie.attack_damage) == 50
    assert annie.ability_power == 0
    assert round(annie.armor) == 19
    assert round(annie.magic_resist) == 30
    assert round(annie.attack_speed, 2) == 0.58
    assert annie.ability_haste == 0
    assert annie.crit_chance == 0
    assert annie.move_speed == 335
    assert annie.attack_range == 625


def test_stat_level_18():
    """
    Tests champion's main stats at level 18
    """
    annie = Annie(level=18)

    assert math.ceil(annie.health) == 2329 - 1  # TODO: check why ingame health is 2329
    assert annie.mana == 843
    assert round(annie.attack_damage) == 95
    assert annie.ability_power == 0
    assert round(annie.armor) == 107
    assert round(annie.magic_resist) == 52
    assert round(annie.attack_speed, 2) == 0.71
    assert annie.ability_haste == 0
    assert annie.crit_chance == 0
    assert annie.move_speed == 335
    assert annie.attack_range == 625


def test_auto_attack(dummy_110):
    """
    Expected auto attack damage at different champion level
    """
    auto_expected_damage = [24, 35, 45]
    for i, level in enumerate((1, 11, 18)):
        annie = Annie(level=level)
        assert round(annie.auto_attack.damage(dummy_110)) == auto_expected_damage[i]


def test_q(dummy_110):
    """
    Tests Q damage at level 1-5 when champion is level 18 with items that boost
    all ratios of the spell.
    """
    annie = Annie(level=18, inventory=[BlastingWand()])
    q_expected_damage = [53, 70, 87, 103, 120]

    for i, level in enumerate(range(1, 6)):
        annie.spell_q.level = level
        assert round(annie.spell_q.damage(dummy_110)) == q_expected_damage[i]


def test_w(dummy_110):
    """
    Tests W damage at level 1-5 when champion is level 18 with items that boost
    all ratios of the spell.
    """
    annie = Annie(level=18, inventory=[BlastingWand()])
    w_expected_damage = [50, 71, 92, 114, 135]

    for i, level in enumerate(range(1, 6)):
        annie.spell_w.level = level
        assert round(annie.spell_w.damage(dummy_110)) == w_expected_damage[i]
