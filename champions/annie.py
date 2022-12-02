from champion import BaseChampion
from spell import BaseSpell

class Annie(BaseChampion):
    champion_name = "Annie"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)

    def spell_q(self, level, enemy_champion):
        self.q = QAnnie(level=level)
        return self.spell_damage(spell=self.q, enemy_champion=enemy_champion)
   
class QAnnie(BaseSpell):
    champion_name = "Annie"
    spell_key = "q"

    def __init__(self, level):
        super().__init__(champion_name=__class__.champion_name, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)        
        self.damage_type = "magical"
        self.target_res_type = self.get_resistance_type()
        self.base_damage_per_level = [80, 115, 150, 185, 220]
        self.base_spell_damage = self.base_damage_per_level[level - 1]
        self.ratios = [0.8] 
        # ["target_ability_power", "base_armor", "target_bonus_health"] add prefix target ?
        self.ratio_stats = ["ability_power"] 
    