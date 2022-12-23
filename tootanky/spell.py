from tootanky.damage import damage_after_resistance, pre_mitigation_damage, ratio_damage, get_resistance_type
from tootanky.data_parser import ALL_CHAMPION_SPELLS
from tootanky.attack import BaseDamageMixin


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
        self.spell_specs = ALL_CHAMPION_SPELLS[champion.champion_name][self.spell_key].copy()

        self.nature = self.get_spell_nature(self.spell_key)
        for name, value in self.spell_specs.items():
            setattr(self, name, value)

        self.ratios = []
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

    # TODO: write on spell effect

    def damage(self, target, spellblade=False, **kwargs):
        on_damage = 0
        self.on_attack_state_change()
        if spellblade and self.can_trigger_spellblade:
            if self.champion.spellblade_item is not None:
                self.champion.spellblade_item.activate = True

        damage_modifier_flat = self.get_damage_modifier_flat(**kwargs)
        damage_modifier_coeff = self.get_damage_modifier_coeff(**kwargs)
        damage = self._compute_damage(target, damage_modifier_flat, damage_modifier_coeff)

        if self.apply_on_hit:
            for on_hit_source in self.champion.on_hits:
                on_damage = on_hit_source.on_hit_effect(target)

        return damage + on_damage
