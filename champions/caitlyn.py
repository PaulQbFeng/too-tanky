from champion import BaseChampion
from damage import damage_physical_auto_attack, pre_mitigation_spell_damage, damage_after_resistance
from spell import BaseSpell


class Caitlyn(BaseChampion):
    champion_name = "Caitlyn"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)
        self.auto_attack_count = 0

    def auto_attack_damage(self, enemy_champion, is_crit: bool = False):
        if self.auto_attack_count < 6:
            damage = damage_physical_auto_attack(
                base_attack_damage=self.orig_base_stats.attack_damage,
                base_armor=enemy_champion.orig_base_stats.armor,
                bonus_attack_damage=self.orig_bonus_stats.get("attack_damage", 0),
                bonus_armor=enemy_champion.orig_bonus_stats.get("armor", 0),
                attacker_level=self.level,
                lethality=self.orig_bonus_stats.get("lethality", 0),
                armor_pen=self.orig_bonus_stats.get("armor_pen_percent", 0),
                bonus_armor_pen=self.orig_bonus_stats.get("bonus_armor_pen_percent", 0),
                crit=is_crit,
                crit_damage=self.orig_bonus_stats.get("crit_damage", 0),
            )
            self.auto_attack_count += 1
        if self.auto_attack_count == 6:
            if 1 <= self.level <= 6:
                attack_damage = self.orig_base_stats.get('attack_damage', 0) + self.orig_bonus_stats.get('attack_damage', 0)
                crit_chance = self.orig_base_stats.get('crit_chance', 0) + self.orig_bonus_stats.get('crit_chance', 0)
                damage_modifier_flat = attack_damage * (0.6 + 1.3125 * crit_chance)
            damage = damage_physical_auto_attack(
                base_attack_damage=self.orig_base_stats.attack_damage,
                base_armor=enemy_champion.orig_base_stats.armor,
                bonus_attack_damage=self.orig_bonus_stats.get("attack_damage", 0),
                bonus_armor=enemy_champion.orig_bonus_stats.get("armor", 0),
                attacker_level=self.level,
                lethality=self.orig_bonus_stats.get("lethality", 0),
                armor_pen=self.orig_bonus_stats.get("armor_pen_percent", 0),
                bonus_armor_pen=self.orig_bonus_stats.get("bonus_armor_pen_percent", 0),
                damage_modifier_flat=damage_modifier_flat,
                crit=is_crit,
                crit_damage=self.orig_bonus_stats.get("crit_damage", 0),
            )
            self.auto_attack_count = 0
        return damage

    def spell_q(self, level, enemy_champion):
        self.q = QCaitlyn(level=level)

        pre_mtg_dmg = pre_mitigation_spell_damage(
            base_spell_damage=self.q.base_spell_damage,
            ratio=self.q.ratios[level-1],
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


class QCaitlyn(BaseSpell):
    champion_name = "Annie"
    spell_key = "q"

    def __init__(self, level):
        super().__init__(champion_name=__class__.champion_name, spell_key=__class__.spell_key, level=level)

        if self.spell_key in ["q", "w", "e"]:
            self.nature = "normal"
        else:
            self.nature = "ulti"

        self.damage_type = "physical"
        self.base_damage_per_level = [50, 90, 130, 170, 210]
        self.base_spell_damage = self.base_damage_per_level[level - 1]
        self.ratios = [1.25, 1.45, 1.65, 1.85, 2.05]
