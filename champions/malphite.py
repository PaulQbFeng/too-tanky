from champion import BaseChampion
from spell import BaseSpell

class Malphite(BaseChampion):
    champion_name = "Malphite"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)

    def spell_q(self, level, enemy_champion):
        self.q = QMalphite(level=level)

        return self.spell_damage(spell=self.q, enemy_champion=enemy_champion)

    def spell_e(self, level, enemy_champion):
        self.e = EMalphite(level=level)

        return self.spell_damage(spell=self.e, enemy_champion=enemy_champion)

    
    def spell_r(self, level, enemy_champion):
        self.r = RMalphite(level=level)

        return self.spell_damage(spell=self.r, enemy_champion=enemy_champion)

   
class QMalphite(BaseSpell):
    champion_name = "Malphite"
    spell_key = "q"

    def __init__(self, level):
        super().__init__(champion_name=__class__.champion_name, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)        
        self.damage_type = "magical"
        self.target_res_type = self.get_resistance_type()
        self.base_damage_per_level = [70, 120, 170, 220, 270]
        self.base_spell_damage = self.base_damage_per_level[level - 1]
        self.ratios = [0.6]
        self.ratio_stats = ["ability_power"]

class EMalphite(BaseSpell):
    champion_name = "Malphite"
    spell_key = "e"

    def __init__(self, level):
        super().__init__(champion_name=__class__.champion_name, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)        
        self.damage_type = "magical"
        self.target_res_type = self.get_resistance_type()
        self.base_damage_per_level = [60, 95, 130, 165, 200]
        self.base_spell_damage = self.base_damage_per_level[level - 1]
        self.ratios = [0.9, 0.3]
        self.ratio_stats = ["ability_power", "armor"]

class RMalphite(BaseSpell):
    champion_name = "Malphite"
    spell_key = "r"

    def __init__(self, level):
        super().__init__(champion_name=__class__.champion_name, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)        
        self.damage_type = "magical"
        self.target_res_type = self.get_resistance_type()
        self.base_damage_per_level = [200, 300, 400]
        self.base_spell_damage = self.base_damage_per_level[level - 1]
        self.ratios = [0.9]
        self.ratio_stats = ["ability_power"]
        