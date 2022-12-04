from tootanky.champion import BaseChampion
from tootanky.damage import damage_after_resistance, pre_mitigation_spell_damage
from tootanky.spell import BaseSpell


class Orianna(BaseChampion):
    champion_name = "Orianna"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)

    def init_spells(self, spell_levels):
        level_q, level_w, level_e, level_r = spell_levels
        self.spell_r = ROrianna(self, level_r)


class ROrianna(BaseSpell):
    champion_name = "Orianna"
    spell_key = "r"

    def __init__(self, champion, level):
        super().__init__(champion, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)
        self.damage_type = "magical"
        self.target_res_type = self.get_resistance_type()
        self.base_damage_per_level = [200, 275, 350]
        self.ratios = [("ability_power", 0.8)]
