from champion import BaseChampion
from damage import damage_after_resistance, pre_mitigation_spell_damage
from spell import BaseSpell


class Orianna(BaseChampion):
    champion_name = "Orianna"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)

    def spell_r(self, level, enemy_champion):
        self.r = ROrianna(level=level)

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


class ROrianna(BaseSpell):
    champion_name = "Orianna"
    spell_key = "r"

    def __init__(self, level):
        super().__init__(champion_name=__class__.champion_name, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)
        self.damage_type = "magical"
        self.base_damage_per_level = [200, 275, 350]
        self.base_spell_damage = self.base_damage_per_level[level - 1]
        self.ratio = 0.8
