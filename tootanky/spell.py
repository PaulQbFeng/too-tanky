from tootanky.damage import damage_after_resistance, pre_mitigation_spell_damage, ratio_stat, get_resistance_type
from tootanky.data_parser import ALL_CHAMPION_SPELLS
from tootanky.stats import Stats


class BaseSpell:
    """
    Some class variables that can be overwritten in the subclasses:
        - spell_key: q, w, e, r (default=None)
        - damage_type: physical, magical (default=None)
        - apply_on_hit: If the spell can apply on_hit (default=False)
        - can_trigger_spellblade: If the spell can activate spellblade effect (default=True)

    ALL_CHAMPION_SPELLS["Kog\'Maw"]["e"] contains:
        {
            'name': 'Void Ooze',
            'range': [1200.0, 1200.0, 1200.0, 1200.0, 1200.0],
            'cost': [60.0, 70.0, 80.0, 90.0, 100.0],
            'cooldown': [12.0, 12.0, 12.0, 12.0, 12.0],
            'ratios': [0.7, 0.0],
            'max_level': 0
        }
    Not all spell specifications are included in the data file which means there is a need to double check
    the current specs + add the missing ones inside the subclass of BaseSpell.
    """

    spell_key = None
    damage_type = None
    apply_on_hit = False
    can_trigger_spellblade = True

    def __init__(self, champion, level=1):
        self.champion = champion
        self.set_level(level)
        self.spell_specs = ALL_CHAMPION_SPELLS[champion.champion_name][self.spell_key].copy()
        self.nature = self.get_spell_nature(self.spell_key)
        for name, value in self.spell_specs.items():
            setattr(self, name, value)
        self.ratios = []
        self.buffs = []
        if self.damage_type is not None:
            self.target_res_type = get_resistance_type(self.damage_type)

    @staticmethod
    def get_spell_nature(spell_key: str) -> str:
        if spell_key in ["q", "w", "e"]:
            return "basic"
        return "ulti"

    def print_specs(self):
        """pretty print the stats"""
        return print("\n".join([f"{k}: {v}" for k, v in self.__dict__.items() if k != "spell_specs"]))

    def print_orig_specs(self):
        """pretty print the stats"""
        return print("\n".join([f"{k}: {v}" for k, v in self.spell_specs.items()]))

    def set_level(self, level):
        """Set spell level"""
        self.level = level

    def get_base_damage(self):
        """Get the base damage of a spell"""
        return self.base_damage_per_level[self.level - 1]

    def damage(self, target, damage_modifier_flat=0, damage_modifier_coeff=1) -> float:
        """Calculates the damage dealt to a champion with a spell"""

        ratio_dmg = ratio_stat(champion=self.champion, target=target, ratios=self.ratios, spell_level=self.level)

        pre_mtg_dmg = pre_mitigation_spell_damage(
            self.get_base_damage(),
            ratio_dmg,
            damage_modifier_flat=damage_modifier_flat,
            damage_modifier_coeff=damage_modifier_coeff,
        )

        res_type = self.target_res_type
        if res_type == "armor":
            bonus_resistance_pen = self.champion.bonus_armor_pen_percent
        else:
            bonus_resistance_pen = 0
        # TODO: Can be refactored once we know more about bonus res pen
        post_mtg_dmg = damage_after_resistance(
            pre_mitigation_damage=pre_mtg_dmg,
            base_resistance=getattr(target, f"base_{res_type}"),
            bonus_resistance=getattr(target, f"bonus_{res_type}"),
            flat_resistance_pen=getattr(self.champion, f"{res_type}_pen_flat"),
            resistance_pen=getattr(self.champion, f"{res_type}_pen_percent"),
            bonus_resistance_pen=bonus_resistance_pen,
        )

        return post_mtg_dmg

    def get_damage_modifier_flat(self, **kwargs):
        return 0

    def get_damage_modifier_coeff(self, **kwargs):
        return 1

    def on_attack_state_change(self):
        """Change internal attribute e.g cait w and e"""
        pass

    def apply_buffs(self, target, **kwargs):
        """Debuff, maybe buff later if it can handle buffs also"""
        stats_dict = dict()
        target_stats_dict = dict()
        for stat, value_per_level in self.buffs:
            value = value_per_level[self.level - 1]
            if stat.startswith("target_"):
                stat = stat.replace("target_", "")
                target_stats_dict[stat] = value
            else:
                stats_dict[stat] = value
        self.champion.orig_bonus_stats += Stats(stats_dict)
        self.champion.update_champion_stats()
        target.orig_bonus_stats += Stats(target_stats_dict)
        target.update_champion_stats()

    def deapply_buffs(self, target, **kwargs):
        stats_dict = dict()
        target_stats_dict = dict()
        for stat, value_per_level in self.buffs:
            value = value_per_level[self.level]
            if stat.startswith("target_"):
                stat = stat.replace("target_", "")
                target_stats_dict[stat] = value
            else:
                stats_dict[stat] = value
        self.champion.orig_bonus_stats -= Stats(stats_dict)
        self.champion.update_champion_stats()
        target.orig_bonus_stats -= Stats(target_stats_dict)
        target.update_champion_stats()

    def hit_damage(self, target, spellblade=False, **kwargs):
        on_hit_damage = 0
        self.on_attack_state_change()
        if spellblade and self.can_trigger_spellblade:
            if self.champion.spellblade_item is not None:
                self.champion.spellblade_item.activate = True

        damage_modifier_flat = self.get_damage_modifier_flat(**kwargs)
        damage_modifier_coeff = self.get_damage_modifier_coeff(**kwargs)
        damage = self.damage(target, damage_modifier_flat, damage_modifier_coeff)

        if self.apply_on_hit:
            for on_hit_source in self.champion.on_hits:
                on_hit_damage = on_hit_source.on_hit_effect(target)

        self.apply_buffs(target, **kwargs)  # Applied after the on-hits based on test with sheen + blackcleaver

        return damage + on_hit_damage

