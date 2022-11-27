from champion import BaseChampion
from damage import damage_physical_auto_attack


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
