from champion import BaseChampion
from spell import BaseSpell
from damage import damage_after_resistance, pre_mitigation_spell_damage

class Malphite(BaseChampion):
    champion_name = "Malphite"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)

    def spell_q(self, level, enemy_champion):
        self.q = QMalphite(level=level)

        pre_mtg_dmg = pre_mitigation_spell_damage(
            base_spell_damage=self.q.base_spell_damage,
            ratio=self.q.ratio,
            base_offensive_stats=self.base_ability_power,
            bonus_offensive_stats=self.bonus_ability_power,
        )

        post_mtg_dmg = damage_after_resistance(
            pre_mitigation_damage=pre_mtg_dmg,
            base_resistance=enemy_champion.base_magic_resist,
            bonus_resistance=enemy_champion.bonus_magic_resist,
            flat_resistance_pen=self.magic_pen_flat,
            resistance_pen=self.magic_pen_percent,
        )
        return post_mtg_dmg

    def spell_e(self, level, enemy_champion):
        self.e = EMalphite(level=level)

        pre_mtg_dmg = pre_mitigation_spell_damage(
            base_spell_damage=self.e.base_spell_damage,
            ratio=self.e.ratio,
            base_offensive_stats=self.base_ability_power,
            bonus_offensive_stats=self.bonus_ability_power,
        )
        #add armor ratio
        pre_mtg_dmg = pre_mtg_dmg + pre_mitigation_spell_damage(
            base_spell_damage=0,
            ratio=0.3,
            base_offensive_stats=self.base_armor,
            bonus_offensive_stats=self.bonus_armor,
        )

        post_mtg_dmg = damage_after_resistance(
            pre_mitigation_damage=pre_mtg_dmg,
            base_resistance=enemy_champion.base_magic_resist,
            bonus_resistance=enemy_champion.bonus_magic_resist,
            flat_resistance_pen=self.magic_pen_flat,
            resistance_pen=self.magic_pen_percent,
        )
        return post_mtg_dmg
    
    def spell_r(self, level, enemy_champion):
        self.r = RMalphite(level=level)

        pre_mtg_dmg = pre_mitigation_spell_damage(
            base_spell_damage=self.r.base_spell_damage,
            ratio=self.r.ratio,
            base_offensive_stats=self.base_ability_power,
            bonus_offensive_stats=self.bonus_ability_power,
        )

        post_mtg_dmg = damage_after_resistance(
            pre_mitigation_damage=pre_mtg_dmg,
            base_resistance=enemy_champion.base_magic_resist,
            bonus_resistance=enemy_champion.bonus_magic_resist,
            flat_resistance_pen=self.magic_pen_flat,
            resistance_pen=self.magic_pen_percent,
        )
        return post_mtg_dmg
   
class QMalphite(BaseSpell):
    champion_name = "Malphite"
    spell_key = "q"

    def __init__(self, level):
        super().__init__(champion_name=__class__.champion_name, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)        
        self.damage_type = "magical"
        self.base_damage_per_level = [70, 120, 170, 220, 270]
        self.base_spell_damage = self.base_damage_per_level[level - 1]
        self.ratio = self.ratios[0] # ratios is a list of 2 values, maybe it's ratio for 2 different damage type 

class EMalphite(BaseSpell):
    champion_name = "Malphite"
    spell_key = "e"

    def __init__(self, level):
        super().__init__(champion_name=__class__.champion_name, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)        
        self.damage_type = "magical"
        self.base_damage_per_level = [60, 95, 130, 165, 200]
        self.base_spell_damage = self.base_damage_per_level[level - 1]
        self.ratio = 0.9 # ratio ap only, armor ratio is coded in Malphite
        
class RMalphite(BaseSpell):
    champion_name = "Malphite"
    spell_key = "r"

    def __init__(self, level):
        super().__init__(champion_name=__class__.champion_name, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)        
        self.damage_type = "magical"
        self.base_damage_per_level = [200, 300, 400]
        self.base_spell_damage = self.base_damage_per_level[level - 1]
        self.ratio = 0.9 # ratios is a list of 2 values, maybe it's ratio for 2 different damage type 
        