from tootanky.champion import BaseChampion
from tootanky.spell import BaseSpell


class Annie(BaseChampion):
    champion_name = "Annie"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)

    def init_spells(self, spell_levels):
        level_q, level_w, level_e, level_r = spell_levels
        self.spell_q = QAnnie(self, level_q)

   
class QAnnie(BaseSpell):
    champion_name = "Annie"
    spell_key = "q"

    def __init__(self, champion, level):
        super().__init__(champion, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)        
        self.damage_type = "magical"
        self.target_res_type = self.get_resistance_type()
        self.base_damage_per_level = [80, 115, 150, 185, 220]
        # ["target_ability_power", "base_armor", "target_bonus_health"] add prefix target ?
        self.ratios = [("ability_power", 0.8)]
    