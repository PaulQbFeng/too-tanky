from tootanky.champion import BaseChampion
from tootanky.spell import BaseSpell


class Xerath(BaseChampion):
    champion_name = "Xerath"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)

    def spell_q(self, level, enemy_champion):
        self.q = QXerath(level=level)

        return self.spell_damage(spell=self.q, enemy_champion=enemy_champion)

    def spell_w(self, level: int, enemy_champion: BaseChampion, is_empowered: bool):
        self.w = WXerath(level=level)

        post_mtg_dmg = self.spell_damage(spell=self.w, enemy_champion=enemy_champion)

        if not is_empowered:
            return post_mtg_dmg
        else:
            return post_mtg_dmg * 1.667

    def spell_e(self, level, enemy_champion):
        self.e = EXerath(level=level)

        return self.spell_damage(spell=self.e, enemy_champion=enemy_champion)


    def spell_r(self, level: int, enemy_champion: BaseChampion, nb_hit):
        self.r = RXerath(level=level)
        assert 0 <= nb_hit <= self.r.recast_per_level[level-1]

        post_mtg_dmg = self.spell_damage(spell=self.r, enemy_champion=enemy_champion)

        return post_mtg_dmg * nb_hit


class QXerath(BaseSpell):
    champion_name = "Xerath"
    spell_key = "q"

    def __init__(self, level):
        super().__init__(champion_name=__class__.champion_name, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)
        self.damage_type = "magical"
        self.target_res_type = self.get_resistance_type()
        self.base_damage_per_level = [70, 110, 150, 190, 230]
        self.base_spell_damage = self.base_damage_per_level[level - 1]
        self.ratios = [0.85]
        self.ratio_stats = ["ability_power"]


class WXerath(BaseSpell):
    champion_name = "Xerath"
    spell_key = "w"

    def __init__(self, level):
        super().__init__(champion_name=__class__.champion_name, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)
        self.damage_type = "magical"
        self.target_res_type = self.get_resistance_type()
        self.base_damage_per_level = [60, 95, 130, 165, 200]
        self.base_spell_damage = self.base_damage_per_level[level - 1]
        self.ratios = [0.6]
        self.ratio_stats = ["ability_power"]

class EXerath(BaseSpell):
    champion_name = "Xerath"
    spell_key = "e"

    def __init__(self, level):
        super().__init__(champion_name=__class__.champion_name, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)
        self.damage_type = "magical"
        self.target_res_type = self.get_resistance_type()
        self.base_damage_per_level = [80, 110, 140, 170, 200]
        self.base_spell_damage = self.base_damage_per_level[level - 1]
        self.ratios = [0.45]
        self.ratio_stats = ["ability_power"]

class RXerath(BaseSpell):
    champion_name = "Xerath"
    spell_key = "r"

    def __init__(self, level):
        super().__init__(champion_name=__class__.champion_name, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)
        self.damage_type = "magical"
        self.target_res_type = self.get_resistance_type()
        self.base_damage_per_level = [200, 250, 300]
        self.recast_per_level = [3, 4, 5]
        self.base_spell_damage = self.base_damage_per_level[level - 1]
        self.ratios = [0.45]
        self.ratio_stats = ["ability_power"]