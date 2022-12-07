from tootanky.champion import BaseChampion
from tootanky.spell import BaseSpell


class Xerath(BaseChampion):
    champion_name = "Xerath"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)

    def init_spells(self, spell_levels):
        level_q, level_w, level_e, level_r = spell_levels
        self.spell_q = QXerath(self, level_q)
        self.spell_w = WXerath(self, level_w)
        self.spell_e = EXerath(self, level_e)
        self.spell_r = RXerath(self, level_r)


class QXerath(BaseSpell):
    champion_name = "Xerath"
    spell_key = "q"

    def __init__(self, champion, level):
        super().__init__(champion, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)
        self.damage_type = "magical"
        self.target_res_type = self.get_resistance_type()
        self.base_damage_per_level = [70, 110, 150, 190, 230]
        self.ratios = [("ability_power", 0.85)]

    def init_per_level(self, level):
        self.base_spell_damage = self.base_damage_per_level[level - 1]

class WXerath(BaseSpell):
    champion_name = "Xerath"
    spell_key = "w"

    def __init__(self, champion, level):
        super().__init__(champion, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)
        self.damage_type = "magical"
        self.target_res_type = self.get_resistance_type()
        self.base_damage_per_level = [60, 95, 130, 165, 200]
        self.base_spell_damage = self.base_damage_per_level[level - 1]
        self.ratios = [("ability_power", 0.6)]

    def get_damage_modifier_coeff(self, is_empowered = True):
        return 1.667 if is_empowered else 1

class EXerath(BaseSpell):
    champion_name = "Xerath"
    spell_key = "e"

    def __init__(self, champion, level):
        super().__init__(champion, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)
        self.damage_type = "magical"
        self.target_res_type = self.get_resistance_type()
        self.base_damage_per_level = [80, 110, 140, 170, 200]
        self.base_spell_damage = self.base_damage_per_level[level - 1]
        self.ratios = [("ability_power", 0.45)]

class RXerath(BaseSpell):
    champion_name = "Xerath"
    spell_key = "r"

    def __init__(self, champion, level):
        super().__init__(champion, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)
        self.damage_type = "magical"
        self.target_res_type = self.get_resistance_type()
        self.base_damage_per_level = [200, 250, 300]
        self.recast_per_level = [3, 4, 5]
        self.base_spell_damage = self.base_damage_per_level[level - 1]
        self.ratios = [("ability_power", 0.45)]

    def get_damage_modifer_ratio(self, target: BaseChampion, nb_hit = None):
        if nb_hit is None:
            raise ValueError("nb_hit must be specified for Xerath R")
        assert 0 <= nb_hit <= self.r.recast_per_level[self.level-1]
        return nb_hit
