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

    def auto_attack_damage(self, enemy_champion, is_crit: bool = False):
        base_attack_damage = self.base_attack_damage
        bonus_attack_damage = self.bonus_attack_damage
        attack_damage = base_attack_damage + bonus_attack_damage
        crit_chance = self.bonus_crit_chance
        crit_damage = self.crit_damage
        base_armor = enemy_champion.base_armor
        bonus_armor = enemy_champion.bonus_armor
        lethality = self.lethality
        armor_pen = self.armor_pen_percent
        bonus_armor_pen = self.bonus_armor_pen_percent
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

        return self.spell_damage(spell=self.q, enemy_champion=enemy_champion)


    def spell_w(self, level):
        self.w = WCaitlyn(level=level)
        self.w_hit = True

    def spell_e(self, level, enemy_champion):
        self.e = ECaitlyn(level=level)
        self.e_hit = True

        return self.spell_damage(spell=self.e, enemy_champion=enemy_champion)


    def spell_r(self, level, enemy_champion):
        self.r = RCaitlyn(level=level)

        damage_modifier_flat = self.r.bonus_attack_damage_ratio * self.bonus_attack_damage

        post_mtg_dmg = self.spell_damage(
            spell=self.r, 
            enemy_champion=enemy_champion, 
            damage_modifier_flat=damage_modifier_flat
        )

        return post_mtg_dmg * (1 + self.bonus_crit_chance * 0.25)


class QCaitlyn(BaseSpell):
    champion_name = "Caitlyn"
    spell_key = "q"

    def __init__(self, level):
        super().__init__(champion_name=__class__.champion_name, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)
        self.damage_type = "physical"
        self.target_res_type = self.get_resistance_type()
        self.base_damage_per_level = [50, 90, 130, 170, 210]
        self.base_spell_damage = self.base_damage_per_level[level - 1]
        self.ratio_per_level = [1.25, 1.45, 1.65, 1.85, 2.05]
        self.ratios = [self.ratio_per_level[level - 1]]
        self.ratio_stats = ["attack_damage"]


class WCaitlyn(BaseSpell):
    champion_name = "Caitlyn"
    spell_key = "w"

    def __init__(self, level):
        super().__init__(champion_name=__class__.champion_name, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)
        self.damage_type = "physical"
        self.target_res_type = self.get_resistance_type()
        self.base_damage_per_level = [40, 85, 130, 175, 220]
        self.base_spell_damage = self.base_damage_per_level[level - 1]
        self.ratio_per_level = [0.4, 0.5, 0.6, 0.7, 0.8]
        self.bonus_attack_damage_ratio = self.ratio_per_level[level-1]


class ECaitlyn(BaseSpell):
    champion_name = "Caitlyn"
    spell_key = "e"

    def __init__(self, level):
        super().__init__(champion_name=__class__.champion_name, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)
        self.damage_type = "magical"
        self.target_res_type = self.get_resistance_type()
        self.base_damage_per_level = [80, 130, 180, 230, 280]
        self.base_spell_damage = self.base_damage_per_level[level - 1]
        self.ratios = [0.8]
        self.ratio_stats = ["ability_power"]


class RCaitlyn(BaseSpell):
    champion_name = "Caitlyn"
    spell_key = "r"

    def __init__(self, level):
        super().__init__(champion_name=__class__.champion_name, spell_key=__class__.spell_key, level=level)

        self.nature = self.get_spell_nature(self.spell_key)        
        self.damage_type = "physical"
        self.target_res_type = self.get_resistance_type()
        self.base_damage_per_level = [300, 525, 750]
        self.base_spell_damage = self.base_damage_per_level[level - 1]
        self.bonus_attack_damage_ratio = 2
        self.ratios = []
        self.ratio_stats = []
