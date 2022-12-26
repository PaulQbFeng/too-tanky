from tootanky.spell_registry import SpellFactory
from tootanky.champion import BaseChampion
from tootanky.item_factory import WRATH_ITEMS


class Yasuo(BaseChampion):
    champion_name = "Yasuo"
    champion_type = "Melee"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, spell_max_order=["q", "e", "w"], **kwargs)
        if not self.inventory.contains(WRATH_ITEMS):
            self.orig_bonus_stats.crit_chance *= 2.5
            if self.orig_bonus_stats.crit_chance >= 1:
                self.orig_bonus_stats.attack_damage += 0.4 * (self.orig_bonus_stats.crit_chance - 1) * 100
                self.bonus_attack_damage = self.orig_bonus_stats.attack_damage
                self.orig_bonus_stats.crit_chance = 1
            self.crit_chance = self.orig_bonus_stats.crit_chance
            self.apply_crit_damage_modifier()
        self.orig_bonus_stats.crit_damage = (1.75 + self.orig_bonus_stats.crit_damage) * 0.9 - 1.75
        self.crit_damage = self.orig_bonus_stats.crit_damage
