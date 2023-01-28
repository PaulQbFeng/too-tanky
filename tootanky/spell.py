from tootanky.data_parser import ALL_CHAMPION_SPELLS
from tootanky.attack import BaseDamageMixin
from tootanky.stats import add_stat, sub_stat


class BaseSpell(BaseDamageMixin):
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
            'max_level': 0
        }
    Not all spell specifications are included in the data file which means there is a need to double check
    the current specs + add the missing ones inside the subclass of BaseSpell.
    """

    damage_type = None
    spell_key = None
    apply_on_hit = False
    can_trigger_spellblade = True

    def __init__(self, champion, level=1):
        self.set_level(level)
        self.champion = champion
        self.spell_specs = ALL_CHAMPION_SPELLS[champion.name][self.spell_key].copy()

        self.nature = self.get_spell_nature(self.spell_key)
        for name, value in self.spell_specs.items():
            setattr(self, name, value)

        self.ratios = []
        self.buffs = []

    @staticmethod
    def get_spell_nature(spell_key: str) -> str:
        if spell_key in ["q", "w", "e"]:
            return "basic"
        return "ulti"

    @property
    def cooldown(self):
        base_cooldown = ALL_CHAMPION_SPELLS[self.champion.name][self.spell_key]["base_cooldown_per_level"][
            self.level - 1
        ]
        return base_cooldown * 100 / (100 + self.champion.ability_haste)

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

    def get_damage_modifier_flat(self, **kwargs):
        return 0

    def get_damage_modifier_coeff(self, **kwargs):
        return 1

    def on_attack_state_change(self):
        """Change internal attribute e.g cait w and e"""
        pass

    def apply_buffs(self, target, **kwargs):
        """
        Can handle debuff/buff.
        Tested for armor reduction debuff (Jarvan/Black Cleaver PR - 20/12/2022)"""
        for stat, value_per_level in self.buffs:
            value = value_per_level[self.level - 1]
            if "armor_reduction" in stat:
                assert stat.startswith("target_"), "Armor reduction is always applied to the target in league."
                if stat.endswith("_flat"):
                    target.update_armor_stats(flat_debuff=value)
                elif stat.endswith("_percent"):
                    target.update_armor_stats(percent_debuff=value)
                else:
                    raise NameError("{} should end with _flat or _percent".format(stat))
            else:
                if stat.startswith("target_"):
                    stat = stat.replace("target_", "")
                    setattr(target, stat, add_stat(stat, getattr(target, stat), value))
                else:
                    setattr(self.champion, stat, add_stat(stat, getattr(self.champion, stat), value))
        if self.damage_type == "physical":
            self.champion.apply_black_cleaver(target)

    def remove_buffs(self, target, **kwargs):
        for stat, value_per_level in self.buffs:
            value = value_per_level[self.level - 1]
            if "armor_reduction" in stat:
                assert stat.startswith("target_"), "Armor reduction is always applied to the target in league."
                if stat.endswith("_flat"):
                    target.update_armor_stats(flat_debuff=-value)
                elif stat.endswith("_percent"):
                    target.update_armor_stats(
                        percent_debuff=1
                        - (1 - target.armor_reduction_percent + value) / (1 - target.armor_reduction_percent)
                    )
                else:
                    raise NameError("{} should end with _flat or _percent".format(stat))
            else:
                if stat.startswith("target_"):
                    stat = stat.replace("target_", "")
                    setattr(target, stat, sub_stat(stat, getattr(target, stat), value))
                else:
                    setattr(self.champion, stat, sub_stat(stat, getattr(self.champion, stat), value))

    def damage(self, target, spellblade=False, **kwargs):
        on_hit_damage = 0
        self.on_attack_state_change()
        if spellblade and self.can_trigger_spellblade:
            if self.champion.spellblade_item is not None:
                self.champion.spellblade_item.activate = True

        damage_modifier_flat = self.get_damage_modifier_flat(**kwargs)
        damage_modifier_coeff = self.get_damage_modifier_coeff(**kwargs)
        damage = self._compute_damage(target, damage_modifier_flat, damage_modifier_coeff)

        if self.apply_on_hit:
            for on_hit_source in self.champion.on_hits:
                on_hit_damage = on_hit_source.on_hit_effect(target)

        self.apply_buffs(target, **kwargs)  # Applied after the on-hits based on test with sheen + blackcleaver

        return damage + on_hit_damage


def get_spell_levels_from_max_order(spell_max_order, champion_level):
    # This method will be overriden for champions like jayce, udyr, etc.
    spell_1, spell_2, spell_3 = spell_max_order
    default_order = [
        spell_1,
        spell_2,
        spell_3,
        spell_1,
        spell_1,
        "r",
        spell_1,
        spell_2,
        spell_1,
        spell_2,
        "r",
        spell_2,
        spell_2,
        spell_3,
        spell_3,
        "r",
        spell_3,
        spell_3,
    ]
    default_order_per_level = default_order[0:champion_level]
    return (
        default_order_per_level.count("q"),
        default_order_per_level.count("w"),
        default_order_per_level.count("e"),
        default_order_per_level.count("r"),
    )


def get_spell_levels(spell_levels, spell_max_order, champion_level):
    if spell_levels is None:
        if spell_max_order is None:
            spell_levels = (1, 1, 1, 1)
        else:
            spell_levels = get_spell_levels_from_max_order(spell_max_order, champion_level)
    return spell_levels
