from tootanky.champion import BaseChampion
from tootanky.damage import damage_physical_auto_attack
from tootanky.spell import BaseSpell


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

    def init_spells(self, spell_levels):
        [level_q, level_w, level_e, level_r] = spell_levels
        self.spell_q = QCaitlyn(self, level_q)
        self.spell_w = WCaitlyn(self, level_w)
        self.spell_e = ECaitlyn(self, level_e)
        self.spell_r = RCaitlyn(self, level_r)

    def auto_attack_damage(self, target, is_crit: bool = False):
        base_attack_damage = self.base_attack_damage
        bonus_attack_damage = self.bonus_attack_damage
        attack_damage = base_attack_damage + bonus_attack_damage
        crit_chance = self.crit_chance
        crit_damage = self.crit_damage
        base_armor = target.base_armor
        bonus_armor = target.bonus_armor
        lethality = self.lethality
        armor_pen = self.armor_pen_percent
        bonus_armor_pen = self.bonus_armor_pen_percent
        damage_modifier_flat = 0
        std_headshot_dmg = attack_damage * (self.passive_multiplier + 1.3125 * crit_chance)

        if self.w_hit:
            bonus_flat, bonus_ratio = self.spell_w.get_headshot_bonus_damage()
            damage_modifier_flat = std_headshot_dmg + bonus_flat + bonus_ratio * bonus_attack_damage
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


class QCaitlyn(BaseSpell):
    champion_name = "Caitlyn"
    spell_key = "q"

    def __init__(self, champion, level):
        super().__init__(champion, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)
        self.damage_type = "physical"
        self.target_res_type = self.get_resistance_type()
        self.base_damage_per_level = [50, 90, 130, 170, 210]
        self.base_spell_damage = self.base_damage_per_level[level - 1]
        self.ratios = [("attack_damage", [1.25, 1.45, 1.65, 1.85, 2.05])]

    def get_ratio_per_level(self):
        return self.ratio_per_level[self.level - 1]


class WCaitlyn(BaseSpell):
    champion_name = "Caitlyn"
    spell_key = "w"

    def __init__(self, champion, level):
        super().__init__(champion, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)
        self.damage_type = "physical"
        self.target_res_type = self.get_resistance_type()
        self.base_damage_per_level = [0, 0, 0, 0, 0]
        self.headshot_bonus_damage_flat = [40, 85, 130, 175, 220]
        self.headshot_bonus_damage_ratio = [0.4, 0.5, 0.6, 0.7, 0.8]

    def get_headshot_bonus_damage(self):
        flat = self.headshot_bonus_damage_flat[self.level - 1]
        ratio = self.headshot_bonus_damage_ratio[self.level - 1]
        return flat, ratio

    def on_hit_effect(self, target):
        self.champion.w_hit = True


class ECaitlyn(BaseSpell):
    champion_name = "Caitlyn"
    spell_key = "e"

    def __init__(self, champion, level):
        super().__init__(champion, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)
        self.damage_type = "magical"
        self.target_res_type = self.get_resistance_type()
        self.base_damage_per_level = [80, 130, 180, 230, 280]
        self.ratios = [("ability_power", 0.8)]

    def on_hit_effect(self, target):
        self.champion.e_hit = True


class RCaitlyn(BaseSpell):
    champion_name = "Caitlyn"
    spell_key = "r"

    def __init__(self, champion, level):
        super().__init__(champion, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)
        self.damage_type = "physical"
        self.target_res_type = self.get_resistance_type()
        self.base_damage_per_level = [300, 525, 750]
        self.ratios = [("bonus_attack_damage", 2)]

    def get_damage_modifier_coeff(self):
        return 1 + self.champion.crit_chance / 4
