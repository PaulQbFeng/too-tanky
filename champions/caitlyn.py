from champion import BaseChampion
from damage import damage_physical_auto_attack, pre_mitigation_spell_damage, damage_after_resistance
from spell import BaseSpell


class Caitlyn(BaseChampion):
    champion_name = "Caitlyn"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)
        self.auto_attack_count = 0
        self.w_hit = False
        self.e_hit = False
        if 1 <= self.level <= 6:
            self.passive_multiplier = 0.6
        if 7 <= self.level <= 12:
            self.passive_multiplier = 0.9
        if 13 <= self.level <= 18:
            self.passive_multiplier = 1.2

    def auto_attack_damage(self, enemy_champion, is_crit: bool = False):
        base_attack_damage = self.orig_base_stats.attack_damage
        bonus_attack_damage = self.orig_bonus_stats.get('attack_damage', 0)
        attack_damage = base_attack_damage + bonus_attack_damage
        crit_chance = self.orig_bonus_stats.get("crit_chance", 0)
        crit_damage = self.orig_bonus_stats.get("crit_damage", 0)
        base_armor = enemy_champion.orig_base_stats.armor
        bonus_armor = enemy_champion.orig_bonus_stats.armor
        lethality = self.orig_bonus_stats.get("lethality", 0)
        armor_pen = self.orig_bonus_stats.get("armor_pen_percent", 0)
        bonus_armor_pen = self.orig_bonus_stats.get("bonus_armor_pen_percent", 0)
        damage_modifier_flat = 0
        std_headshot_dmg = attack_damage * (self.passive_multiplier + 1.3125 * crit_chance)

        if self.w_hit:
            damage_modifier_flat = (
                std_headshot_dmg + self.w.base_spell_damage + 
                self.w.bonus_attack_damage_ratio * bonus_attack_damage
            )
            self.w_hit = False
        else:
            if self.e_hit:
                damage_modifier_flat = std_headshot_dmg
                self.e_hit = False
            else:
                if self.auto_attack_count < 6:
                    self.auto_attack_count += 1
                elif self.auto_attack_count == 6:
                    damage_modifier_flat = std_headshot_dmg
                    self.auto_attack_count = 0

        damage = damage_physical_auto_attack(
            base_attack_damage=base_attack_damage,
            base_armor=base_armor,
            bonus_attack_damage=bonus_attack_damage,
            bonus_armor=bonus_armor,
            attacker_level=self.level,
            lethality=lethality,
            armor_pen=armor_pen,
            bonus_armor_pen=bonus_armor_pen,
            damage_modifier_flat=damage_modifier_flat,
            crit=is_crit,
            crit_damage=crit_damage,
        )
        return damage

    def spell_q(self, level, enemy_champion):
        self.q = QCaitlyn(level=level)

        pre_mtg_dmg = pre_mitigation_spell_damage(
            base_spell_damage=self.q.base_spell_damage,
            ratio=self.q.ratio,
            base_offensive_stats=self.orig_base_stats.get("attack_damage", 0),
            bonus_offensive_stats=self.orig_bonus_stats.get("attack_damage", 0),
        )

        post_mtg_dmg = damage_after_resistance(
            pre_mitigation_damage=pre_mtg_dmg,
            base_resistance=enemy_champion.orig_base_stats.armor,
            bonus_resistance=enemy_champion.orig_bonus_stats.armor,
            flat_resistance_pen=self.orig_bonus_stats.get('flat_armor_pen', 0),
            resistance_pen=self.orig_bonus_stats.get('percent_armor_pen', 0),
            bonus_resistance_pen=self.orig_bonus_stats.get('percent_bonus_armor_pen', 0)
        )
        return post_mtg_dmg

    def spell_w(self, level):
        self.w = WCaitlyn(level=level)
        self.w_hit = True

    def spell_e(self, level, enemy_champion):
        self.e = ECaitlyn(level=level)
        self.e_hit = True

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

    def spell_r(self, level, enemy_champion):
        self.r = RCaitlyn(level=level)

        damage_modifier_flat = self.r.bonus_attack_damage_ratio * self.orig_bonus_stats.get("attack_damage", 0)
        crit_chance = self.orig_bonus_stats.get("crit_chance", 0)

        pre_mtg_dmg = pre_mitigation_spell_damage(
            base_spell_damage=self.r.base_spell_damage,
            ratio=0,
            base_offensive_stats=self.orig_base_stats.get("attack_damage", 0),
            bonus_offensive_stats=self.orig_bonus_stats.get("attack_damage", 0),
            damage_modifier_flat=damage_modifier_flat,
        )

        post_mtg_dmg = damage_after_resistance(
            pre_mitigation_damage=pre_mtg_dmg,
            base_resistance=enemy_champion.orig_base_stats.armor,
            bonus_resistance=enemy_champion.orig_bonus_stats.armor,
            flat_resistance_pen=self.orig_bonus_stats.get('flat_armor_pen', 0),
            resistance_pen=self.orig_bonus_stats.get('percent_armor_pen', 0),
            bonus_resistance_pen=self.orig_bonus_stats.get('percent_bonus_armor_pen', 0)
        )
        return post_mtg_dmg * (1 + crit_chance*0.25)


class QCaitlyn(BaseSpell):
    champion_name = "Caitlyn"
    spell_key = "q"

    def __init__(self, level):
        super().__init__(champion_name=__class__.champion_name, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)
        self.damage_type = "physical"
        self.base_damage_per_level = [50, 90, 130, 170, 210]
        self.base_spell_damage = self.base_damage_per_level[level - 1]
        self.ratios = [1.25, 1.45, 1.65, 1.85, 2.05]
        self.ratio = self.ratios[level-1]


class WCaitlyn(BaseSpell):
    champion_name = "Caitlyn"
    spell_key = "w"

    def __init__(self, level):
        super().__init__(champion_name=__class__.champion_name, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)
        self.damage_type = "physical"
        self.base_damage_per_level = [40, 85, 130, 175, 220]
        self.base_spell_damage = self.base_damage_per_level[level - 1]
        self.ratios = [0.4, 0.5, 0.6, 0.7, 0.8]
        self.bonus_attack_damage_ratio = self.ratios[level-1]


class ECaitlyn(BaseSpell):
    champion_name = "Caitlyn"
    spell_key = "e"

    def __init__(self, level):
        super().__init__(champion_name=__class__.champion_name, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)
        self.damage_type = "magical"
        self.base_damage_per_level = [80, 130, 180, 230, 280]
        self.base_spell_damage = self.base_damage_per_level[level - 1]
        self.ratio = 0.8


class RCaitlyn(BaseSpell):
    champion_name = "Caitlyn"
    spell_key = "r"

    def __init__(self, level):
        super().__init__(champion_name=__class__.champion_name, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)        
        self.damage_type = "physical"
        self.base_damage_per_level = [300, 525, 750]
        self.base_spell_damage = self.base_damage_per_level[level - 1]
        self.bonus_attack_damage_ratio = 2
