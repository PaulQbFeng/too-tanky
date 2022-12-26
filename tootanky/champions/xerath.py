from tootanky.champion import BaseChampion
from tootanky.spell import BaseSpell
from tootanky.spell_registry import SpellFactory


class Xerath(BaseChampion):
    champion_name = "Xerath"

    def __init__(self, **kwargs):
        super().__init__(spell_max_order=["q", "w", "e"], **kwargs)


@SpellFactory.register_spell
class QXerath(BaseSpell):
    champion_name = "Xerath"
    spell_key = "q"
    damage_type = "magical"

    def __init__(self, champion, level):
        super().__init__(champion, level)
        self.base_damage_per_level = [70, 110, 150, 190, 230]
        self.ratios = [("ability_power", 0.85)]


@SpellFactory.register_spell
class WXerath(BaseSpell):
    champion_name = "Xerath"
    spell_key = "w"
    damage_type = "magical"

    def __init__(self, champion, level):
        super().__init__(champion, level)
        self.base_damage_per_level = [60, 95, 130, 165, 200]
        self.ratios = [("ability_power", 0.6)]

    def get_damage_modifier_coeff(self, is_empowered=True):
        return 1.667 if is_empowered else 1


@SpellFactory.register_spell
class EXerath(BaseSpell):
    champion_name = "Xerath"
    spell_key = "e"
    damage_type = "magical"

    def __init__(self, champion, level):
        super().__init__(champion, level)
        self.base_damage_per_level = [80, 110, 140, 170, 200]
        self.ratios = [("ability_power", 0.45)]


@SpellFactory.register_spell
class RXerath(BaseSpell):
    champion_name = "Xerath"
    spell_key = "r"
    damage_type = "magical"

    def __init__(self, champion, level):
        super().__init__(champion, level)
        self.base_damage_per_level = [200, 250, 300]
        self.recast_per_level = [3, 4, 5]
        self.ratios = [("ability_power", 0.45)]

    def get_damage_modifer_ratio(self, target: BaseChampion, nb_hit=None):
        if nb_hit is None:
            raise ValueError("nb_hit must be specified for Xerath R")
        assert 0 <= nb_hit <= self.r.recast_per_level[self.level - 1]
        return nb_hit
