from champion import BaseChampion
from damage import pre_mitigation_spell_damage, damage_after_resistance
from spell import BaseSpell


class Xerath(BaseChampion):
    champion_name = "Xerath"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)

    def spell_q(self, level, enemy_champion):
        self.q = QXerath(level=level)

        pre_mtg_dmg = pre_mitigation_spell_damage(
            base_spell_damage=self.q.base_spell_damage,
            ratio=self.q.ratio,
            base_offensive_stats=self.orig_base_stats.get("ability_power", 0),
            bonus_offensive_stats=self.orig_bonus_stats.get("ability_power", 0),
        )

        post_mtg_dmg = damage_after_resistance(
            pre_mitigation_damage=pre_mtg_dmg,
            base_resistance=enemy_champion.orig_base_stats.magic_resist,
            bonus_resistance=enemy_champion.orig_bonus_stats.magic_resist,
            flat_resistance_pen=self.orig_bonus_stats.get("flat_magic_resist_pen", 0),
            resistance_pen=self.orig_bonus_stats.get("percent_magic_resist_pen", 0),
        )
        return post_mtg_dmg

    def spell_w(self, level: int, enemy_champion: BaseChampion, is_empowered: bool):
        self.w = WXerath(level=level)

        pre_mtg_dmg = pre_mitigation_spell_damage(
            base_spell_damage=self.w.base_spell_damage,
            ratio=self.w.ratio,
            base_offensive_stats=self.orig_base_stats.get("ability_power", 0),
            bonus_offensive_stats=self.orig_bonus_stats.get("ability_power", 0),
        )

        post_mtg_dmg = damage_after_resistance(
            pre_mitigation_damage=pre_mtg_dmg,
            base_resistance=enemy_champion.orig_base_stats.magic_resist,
            bonus_resistance=enemy_champion.orig_bonus_stats.magic_resist,
            flat_resistance_pen=self.orig_bonus_stats.get("flat_magic_resist_pen", 0),
            resistance_pen=self.orig_bonus_stats.get("percent_magic_resist_pen", 0),
        )
        if not is_empowered:
            return post_mtg_dmg
        else:
            return post_mtg_dmg * 1.667

    def spell_e(self, level, enemy_champion):
        self.e = EXerath(level=level)

        pre_mtg_dmg = pre_mitigation_spell_damage(
            base_spell_damage=self.e.base_spell_damage,
            ratio=self.e.ratio,
            base_offensive_stats=self.orig_base_stats.get("ability_power", 0),
            bonus_offensive_stats=self.orig_bonus_stats.get("ability_power", 0),
        )

        post_mtg_dmg = damage_after_resistance(
            pre_mitigation_damage=pre_mtg_dmg,
            base_resistance=enemy_champion.orig_base_stats.magic_resist,
            bonus_resistance=enemy_champion.orig_bonus_stats.magic_resist,
            flat_resistance_pen=self.orig_bonus_stats.get("flat_magic_resist_pen", 0),
            resistance_pen=self.orig_bonus_stats.get("percent_magic_resist_pen", 0),
        )
        return post_mtg_dmg

    def spell_r(self, level: int, enemy_champion: BaseChampion, nb_hit):
        self.r = RXerath(level=level)
        assert 0 <= nb_hit <= self.r.recast_per_level[level-1]

        pre_mtg_dmg = pre_mitigation_spell_damage(
            base_spell_damage=self.r.base_spell_damage,
            ratio=self.r.ratio,
            base_offensive_stats=self.orig_base_stats.get("ability_power", 0),
            bonus_offensive_stats=self.orig_bonus_stats.get("ability_power", 0),
        )

        post_mtg_dmg = damage_after_resistance(
            pre_mitigation_damage=pre_mtg_dmg,
            base_resistance=enemy_champion.orig_base_stats.magic_resist,
            bonus_resistance=enemy_champion.orig_bonus_stats.magic_resist,
            flat_resistance_pen=self.orig_bonus_stats.get("flat_magic_resist_pen", 0),
            resistance_pen=self.orig_bonus_stats.get("percent_magic_resist_pen", 0),
        )
        return post_mtg_dmg * nb_hit


class QXerath(BaseSpell):
    champion_name = "Xerath"
    spell_key = "q"

    def __init__(self, level):
        super().__init__(champion_name=__class__.champion_name, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)
        self.damage_type = "magical"
        self.base_damage_per_level = [70, 110, 150, 190, 230]
        self.base_spell_damage = self.base_damage_per_level[level - 1]
        self.ratio = self.ratios[0]  # ratios is a list of 2 values, maybe it's ratio for 2 different damage type


class WXerath(BaseSpell):
    champion_name = "Xerath"
    spell_key = "w"

    def __init__(self, level):
        super().__init__(champion_name=__class__.champion_name, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)
        self.damage_type = "magical"
        self.base_damage_per_level = [60, 95, 130, 165, 200]
        self.base_spell_damage = self.base_damage_per_level[level - 1]
        self.ratio = 0.6


class EXerath(BaseSpell):
    champion_name = "Xerath"
    spell_key = "e"

    def __init__(self, level):
        super().__init__(champion_name=__class__.champion_name, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)
        self.damage_type = "magical"
        self.base_damage_per_level = [80, 110, 140, 170, 200]
        self.base_spell_damage = self.base_damage_per_level[level - 1]
        self.ratio = 0.45


class RXerath(BaseSpell):
    champion_name = "Xerath"
    spell_key = "r"

    def __init__(self, level):
        super().__init__(champion_name=__class__.champion_name, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)
        self.damage_type = "magical"
        self.base_damage_per_level = [200, 250, 300]
        self.recast_per_level = [3, 4, 5]
        self.base_spell_damage = self.base_damage_per_level[level - 1]
        self.ratio = 0.45