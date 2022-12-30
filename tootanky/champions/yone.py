from tootanky.spell_registry import SpellFactory
from tootanky.champion import BaseChampion


class Yone(BaseChampion):
    name = "Yone"
    range_type = "Melee"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.orig_bonus_stats.crit_chance >= 1:
            self.orig_bonus_stats.attack_damage += 0.4 * (self.orig_bonus_stats.crit_chance - 1) * 100
            self.bonus_attack_damage = self.orig_bonus_stats.attack_damage
            self.orig_bonus_stats.crit_chance = 1
            self.crit_chance = self.orig_bonus_stats.crit_chance

    def get_crit_chance_multiplier(self):
        return 2.5

    def get_crit_damage_multiplier(self):
        return 0.9
