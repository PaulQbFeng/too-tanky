import math

import pytest

from tootanky.champions import Annie


@pytest.fixture
def annie(level):
    return Annie(level=level)


@pytest.mark.parametrize("level", [1])
def test_stat_level_1(annie):
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


@pytest.mark.parametrize("level", [18])
def test_stat_level_18(annie):
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


@pytest.mark.parametrize("level", [18])
def test_q(annie, dummy_110):
    q_expected_damage = [38, 55, 71, 88, 105]
    for i, level in enumerate(range(1, 6)):
        annie.spell_q.level = level
        assert round(annie.spell_q.damage(dummy_110)) == q_expected_damage[i]


@pytest.mark.parametrize("level", [18])
def test_w(annie, dummy_110):
    w_expected_damage = [33, 55, 76, 98, 119]
    for i, level in enumerate(range(1, 6)):
        annie.spell_w.level = level
        assert round(annie.spell_w.damage(dummy_110)) == w_expected_damage[i]
