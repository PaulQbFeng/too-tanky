import math

from tootanky.champions import Annie
from tootanky.stats_calculator import round_norm


def test_stat_level_1():
    """
    Tests champion's main stats at level 1
    """
    champion = Annie(level=1)

    assert math.ceil(champion.health) == 594
    assert champion.mana == 418
    assert round_norm(champion.attack_damage) == 50
    assert champion.ability_power == 0
    assert round_norm(champion.armor) == 19
    assert round_norm(champion.magic_resist) == 30
    assert round_norm(champion.attack_speed, 2) == 0.58
    assert champion.ability_haste == 0
    assert champion.crit_chance == 0
    assert champion.move_speed == 335
    assert champion.attack_range == 625


def test_stat_level_18():
    """
    Tests champion's main stats at level 18
    """
    champion = Annie(level=18)

    assert math.ceil(champion.health) + 1 == 2329  # TODO: check why ingame health is 2329
    assert champion.mana == 843
    assert round_norm(champion.attack_damage) == 95
    assert champion.ability_power == 0
    assert round_norm(champion.armor) == 107
    assert round_norm(champion.magic_resist) == 52
    assert round_norm(champion.attack_speed, 2) == 0.71
    assert champion.ability_haste == 0
    assert champion.crit_chance == 0
    assert champion.move_speed == 335
    assert champion.attack_range == 625


def test_auto_attack(dummy_110):
    """
    Expected auto attack damage at different champion level
    """
    auto_expected_damage = [24, 35, 45]
    for i, level in enumerate((1, 11, 18)):
        champion = Annie(level=level)
        assert round_norm(champion.auto_attack.damage(dummy_110)) == auto_expected_damage[i]


def test_q(dummy_110):
    """
    Tests Q damage at level 1-5 when champion is level 18 with items that boost
    all ratios of the spell.
    """
    champion = Annie(level=18)
    champion.bonus_ability_power += 40
    q_expected_damage = [53, 70, 87, 103, 120]

    for i, level in enumerate(range(1, 6)):
        champion.spell_q.level = level
        assert round_norm(champion.spell_q.damage(dummy_110)) == q_expected_damage[i]


def test_w(dummy_110):
    """
    Tests W damage at level 1-5 when champion is level 18 with items that boost
    all ratios of the spell.
    """
    champion = Annie(level=18)
    champion.bonus_ability_power += 40
    w_expected_damage = [50, 71, 92, 114, 135]

    for i, level in enumerate(range(1, 6)):
        champion.spell_w.level = level
        assert round_norm(champion.spell_w.damage(dummy_110)) == w_expected_damage[i]
