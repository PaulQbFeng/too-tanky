from data_parser import ALL_CHAMPION_SPELLS

NORMAL_SPELL_KEY = ["q", "w", "e"]


class BaseSpell:
    def __init__(self, champion_name, spell_key):
        self.champion_name = champion_name
        self.spell_key = spell_key
        spell_specs = ALL_CHAMPION_SPELLS[champion_name][spell_key].copy()
        for name, value in spell_specs.items():
            setattr(self, name, value)

    def print_specs(self):
        """pretty print the stats"""
        return print("\n".join([f"{k}: {v}" for k, v in self.__dict__.items()]))


class QAnnie(BaseSpell):
    champion_name = "Annie"
    spell_key = "q"

    def __init__(self, level):
        super().__init__(champion_name=__class__.champion_name, spell_key=__class__.spell_key)

        if self.spell_key in NORMAL_SPELL_KEY:
            self.nature = "normal"
        else:
            self.nature = "ulti"

        self.base_damage_per_level = [80, 115, 150, 185, 220]
        self.damage_type = "magical"
        self.level = level
        self.range = self.range[level - 1]
        self.cost = self.cost[level - 1]
        self.cooldown = self.cooldown[level - 1]
        self.ratio = self.ratios[0]
        self.base_spell_damage = self.base_damage_per_level[level - 1]
