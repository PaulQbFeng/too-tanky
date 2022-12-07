from tootanky.damage import damage_after_resistance, pre_mitigation_spell_damage
from tootanky.data_parser import ALL_CHAMPION_SPELLS


class BaseSpell:
    """
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

    def __init__(self, champion, level=1):
        self.champion = champion
        self.spell_specs = ALL_CHAMPION_SPELLS[champion.champion_name][self.spell_key].copy()
        for name, value in self.spell_specs.items():
            setattr(self, name, value)
        self.ratios = []

        self.set_level(level)
        self.damage_type = None

    @staticmethod
    def get_spell_nature(spell_key: str) -> str:
        if spell_key in ["q", "w", "e"]:
            return "basic"
        return "ulti"

    def get_resistance_type(self) -> str:
        """Get resistance type based on spell damage type"""
        # TODO: Might be changed into a dict

        if self.damage_type == "magical":
            res_type = "magic_resist"
        elif self.damage_type == "physical":
            res_type = "armor"
        else:
            raise AttributeError(f"spell_damage type {self.damage_type} not taken into account")

        return res_type

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

    def ratio_damage(self, target) -> float:
        """Get the damage dealt by the ratio part of a spell, taking into account multiple ratios"""
        damage = 0
        for stat_name, ratio in self.ratios:
            if "target_" in stat_name:
                stat_value = getattr(target, stat_name.replace("target_", ""))
            else:
                stat_value = getattr(self.champion, stat_name)
            if isinstance(ratio, list):
                ratio = ratio[self.level - 1]
            damage += stat_value * ratio
        return damage

    def damage(self, target, damage_modifier_flat=0, damage_modifier_ratio=1) -> float:
        """Calculates the damage dealt to a champion with a spell"""

        ratio_damage = self.ratio_damage(target)

        pre_mtg_dmg = pre_mitigation_spell_damage(
            self.get_base_damage(),
            ratio_damage,
            damage_modifier_flat=damage_modifier_flat,
            damage_modifier_ratio=damage_modifier_ratio,
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

    def get_damage_modifier_ratio(self, **kwargs):
        return 1

    def on_hit_effect(self, target, **kwargs):
        """Effect on hit"""
        pass

    def hit_damage(self, target, **kwargs):
        damage_modifier_flat = self.get_damage_modifier_flat(**kwargs)
        damage_modifier_ratio = self.get_damage_modifier_ratio(**kwargs)
        damage = self.damage(target, damage_modifier_flat, damage_modifier_ratio)
        self.on_hit_effect(target, **kwargs)  # Be sure to compute the damage before the effect
        return damage
