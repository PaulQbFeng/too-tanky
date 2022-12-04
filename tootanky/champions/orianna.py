from tootanky.champion import BaseChampion
from tootanky.damage import damage_after_resistance, pre_mitigation_spell_damage
from tootanky.spell import BaseSpell


class Orianna(BaseChampion):
    champion_name = "Orianna"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)

    def spell_r(self, level, enemy_champion):
        self.r = ROrianna(level=level)

        return self.spell_damage(spell=self.r, enemy_champion=enemy_champion)


class ROrianna(BaseSpell):
    champion_name = "Orianna"
    spell_key = "r"

    def __init__(self, level):
        super().__init__(champion_name=__class__.champion_name, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)
        self.damage_type = "magical"
        self.target_res_type = self.get_resistance_type()
        self.base_damage_per_level = [200, 275, 350]
        self.base_spell_damage = self.base_damage_per_level[level - 1]
        self.ratios = [0.8]
        self.ratio_stats = ["ability_power"]
