import math

from tootanky.champions import Ezreal
from tootanky.stats_calculator import round_norm
from tootanky.item_factory import BlastingWand


def test_stat_level_1():
    """
    Tests champion's main stats at level 1
    """
    champion = Ezreal(level=1)

    assert math.ceil(champion.health) == 600
    assert champion.mana == 375
    assert round_norm(champion.attack_damage) == 60
    assert champion.ability_power == 0
    assert round_norm(champion.armor) == 24
    assert round_norm(champion.magic_resist) == 30
    assert round_norm(champion.attack_speed, 2) == 0.63
    assert champion.ability_haste == 0
    assert champion.crit_chance == 0
    assert champion.move_speed == 325
    assert champion.attack_range == 550


def test_stat_level_18():
    """
    Tests champion's main stats at level 18
    """
    champion = Ezreal(level=18)

    assert math.ceil(champion.health) + 1 == 2335
    assert champion.mana == 1565
    assert round_norm(champion.attack_damage) == 103
    assert champion.ability_power == 0
    assert round_norm(champion.armor) == 104
    assert round_norm(champion.magic_resist) == 52
    assert round_norm(champion.attack_speed, 2) == 0.89
    assert champion.ability_haste == 0
    assert champion.crit_chance == 0
    assert champion.move_speed == 325
    assert champion.attack_range == 550


def test_auto_attack(dummy_110):
    """
    Expected auto attack damage at different champion level
    """
    auto_expected_damage = [29, 39, 49]
    for i, level in enumerate((1, 11, 18)):
        champion = Ezreal(level=level)
        assert round_norm(champion.auto_attack.damage(dummy_110)) == auto_expected_damage[i]


def test_q(dummy_110):
    """
    Tests Q damage at level 1-5 when champion is level 18 with items that boost
    all ratios of the spell.
    """
    champion = Ezreal(level=18)
    champion.bonus_attack_damage += 10
    champion.bonus_ability_power += 40
    q_expected_damage = [82, 94, 106, 118, 130]

    for i, level in enumerate(range(1, 6)):
        champion.spell_q.level = level
        assert round_norm(champion.spell_q.damage(dummy_110)) == q_expected_damage[i]


# def test_w(dummy_110):
#     """
#     Tests W damage at level 1-5 when champion is level 18 with items that boost
#     all ratios of the spell.
#     """
#     champion = Ezreal(level=18)
#     q_expected_damage = [54, 81, 108, 135, 162]

#     for i, level in enumerate(range(1, 6)):
#         champion.spell_q.level = level
#         assert round_norm(champion.spell_q.damage(dummy_110)) == q_expected_damage[i]


def test_e(dummy_110):
    """
    Tests E damage at level 1-5 when champion is level 18.
    """
    champion = Ezreal(level=18)
    champion.bonus_attack_damage += 10
    champion.bonus_ability_power += 40

    expected_damage = [55, 79, 102, 126, 150]

    for i, level in enumerate(range(1, 6)):
        champion.spell_e.level = level
        assert round_norm(champion.spell_e.damage(dummy_110)) == expected_damage[i]


# def test_r(dummy_110):
#     """
#     Tests W damage at level 1-5 when champion is level 18 with items that boost
#     all ratios of the spell.
#     """
#     champion = Ezreal(level=18)
#     q_expected_damage = [188, 260, 331]

#     for i, level in enumerate(range(1, 3)):
#         champion.spell_q.level = level
#         assert round_norm(champion.spell_q.damage(dummy_110)) == q_expected_damage[i]
