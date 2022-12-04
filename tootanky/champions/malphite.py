from tootanky.champion import BaseChampion
from tootanky.spell import BaseSpell

class Malphite(BaseChampion):
    champion_name = "Malphite"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)

    def init_spells(self, spell_levels):
        level_q, level_w, level_e, level_r = spell_levels
        self.spell_q = QMalphite(self, level_q)
        self.spell_e = EMalphite(self, level_e)
        self.spell_r = RMalphite(self, level_r)

class QMalphite(BaseSpell):
    champion_name = "Malphite"
    spell_key = "q"

    def __init__(self, champion, level):
        super().__init__(champion, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)        
        self.damage_type = "magical"
        self.target_res_type = self.get_resistance_type()
        self.base_damage_per_level = [70, 120, 170, 220, 270]
        self.ratios = [("ability_power", 0.6)]

class EMalphite(BaseSpell):
    champion_name = "Malphite"
    spell_key = "e"

    def __init__(self, champion, level):
        super().__init__(champion, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)        
        self.damage_type = "magical"
        self.target_res_type = self.get_resistance_type()
        self.base_damage_per_level = [60, 95, 130, 165, 200]
        self.ratios = [("ability_power", 0.9), ("armor", 0.3)]

class RMalphite(BaseSpell):
    champion_name = "Malphite"
    spell_key = "r"

    def __init__(self, champion, level):
        super().__init__(champion, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)        
        self.damage_type = "magical"
        self.target_res_type = self.get_resistance_type()
        self.base_damage_per_level = [200, 300, 400]
        self.ratios = [("ability_power", 0.9)]
