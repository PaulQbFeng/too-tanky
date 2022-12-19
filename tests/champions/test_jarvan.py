from tootanky.champion import Dummy
from tootanky.champions import JarvanIV
from tootanky.item import LongSword


def test_q():
    champion_levels = [1, 4, 5, 7, 9]
    damage_values = [61, 85, 108, 132, 155]
    armor_values = [63, 60, 57, 55, 52]
    for spell_level in range(5):
        jarvan = JarvanIV(level=champion_levels[spell_level], inventory=[LongSword()])
        dummy = Dummy(bonus_resistance=70)
        assert round(jarvan.spell_q.hit_damage(dummy)) == damage_values[spell_level]
        assert round(dummy.armor) == armor_values[spell_level]
