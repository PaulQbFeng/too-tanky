from tootanky.champion import BaseChampion
from tootanky.attack import AutoAttack
from tootanky.spell import BaseSpell
from tootanky.spell_registry import SpellFactory


class Caitlyn(BaseChampion):
    name = "Caitlyn"
    range_type = "Ranged"

    def __init__(self, **kwargs):
        super().__init__(spell_max_order=["q", "w", "e"], **kwargs)
        self.auto_attack_count = 0
        self.w_hit = False
        self.e_hit = False
        if 1 <= self.level <= 6:
            self.passive_multiplier = 0.6
        if 7 <= self.level <= 12:
            self.passive_multiplier = 0.9
        if 13 <= self.level <= 18:
            self.passive_multiplier = 1.2

    def initialize_auto_attack(self):
        self.auto_attack = AutoAttackCaitlyn(champion=self)


class AutoAttackCaitlyn(AutoAttack):
    def get_damage_modifier_flat(self):
        champion = self.champion
        base_attack_damage = champion.base_attack_damage
        bonus_attack_damage = champion.bonus_attack_damage
        crit_chance = champion.crit_chance
        damage_modifier_flat = 0
        std_headshot_dmg = (base_attack_damage + bonus_attack_damage) * (champion.passive_multiplier + 1.3125 * crit_chance)

        if champion.w_hit:
            bonus_flat, bonus_ratio = champion.spell_w.get_headshot_bonus_damage()
            damage_modifier_flat = std_headshot_dmg + bonus_flat + bonus_ratio * bonus_attack_damage
        else:
            if champion.e_hit:
                damage_modifier_flat = std_headshot_dmg
            else:
                if champion.auto_attack_count == 6:
                    damage_modifier_flat = std_headshot_dmg

        return damage_modifier_flat

    def apply_auto_attack_count(self):
        champion = self.champion
        if champion.w_hit:
            champion.w_hit = False
        else:
            if champion.e_hit:
                champion.e_hit = False
            else:
                if champion.auto_attack_count < 6:
                    champion.auto_attack_count += 1
                elif champion.auto_attack_count == 6:
                    champion.auto_attack_count = 0

    def damage(self, target, is_crit: bool = False):
        damage = self._compute_damage(
            target=target,
            damage_modifier_flat=self.get_damage_modifier_flat(),
            damage_modifier_coeff=self.get_damage_modifier_coeff(),
            is_crit=is_crit
        )
        self.apply_auto_attack_count()
        return damage


@SpellFactory.register_spell
class QCaitlyn(BaseSpell):
    champion_name = "Caitlyn"
    spell_key = "q"
    damage_type = "physical"

    def __init__(self, champion, level):
        super().__init__(champion, level)
        self.base_damage_per_level = [50, 90, 130, 170, 210]
        self.base_spell_damage = self.base_damage_per_level[level - 1]
        self.ratios = [("attack_damage", [1.25, 1.45, 1.65, 1.85, 2.05])]

    def get_ratio_per_level(self):
        return self.ratio_per_level[self.level - 1]


@SpellFactory.register_spell
class WCaitlyn(BaseSpell):
    champion_name = "Caitlyn"
    spell_key = "w"
    damage_type = "physical"

    def __init__(self, champion, level):
        super().__init__(champion, level)
        self.base_damage_per_level = [0, 0, 0, 0, 0]
        self.headshot_bonus_damage_flat = [40, 85, 130, 175, 220]
        self.headshot_bonus_damage_ratio = [0.4, 0.5, 0.6, 0.7, 0.8]

    def get_headshot_bonus_damage(self):
        flat = self.headshot_bonus_damage_flat[self.level - 1]
        ratio = self.headshot_bonus_damage_ratio[self.level - 1]
        return flat, ratio

    def on_attack_state_change(self):
        self.champion.w_hit = True


@SpellFactory.register_spell
class ECaitlyn(BaseSpell):
    champion_name = "Caitlyn"
    spell_key = "e"
    damage_type = "magical"

    def __init__(self, champion, level):
        super().__init__(champion, level)
        self.base_damage_per_level = [80, 130, 180, 230, 280]
        self.ratios = [("ability_power", 0.8)]

    def on_attack_state_change(self):
        self.champion.e_hit = True


@SpellFactory.register_spell
class RCaitlyn(BaseSpell):
    champion_name = "Caitlyn"
    spell_key = "r"
    damage_type = "physical"

    def __init__(self, champion, level):
        super().__init__(champion, level)
        self.base_damage_per_level = [300, 525, 750]
        self.ratios = [("bonus_attack_damage", 2)]

    def get_damage_modifier_coeff(self):
        return 1 + self.champion.crit_chance / 4
