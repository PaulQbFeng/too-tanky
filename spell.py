from data_parser import ALL_CHAMPION_SPELLS


class BaseSpell:
    def __init__(self, champion_name, spell_key, level):
        self.champion_name = champion_name
        self.spell_key = spell_key
        spell_specs = ALL_CHAMPION_SPELLS[champion_name][spell_key].copy()
        for name, value in spell_specs.items():
            setattr(self, name, value)

        self.level = level
        self.range = self.range[level - 1]
        self.cost = self.cost[level - 1]
        self.cooldown = self.cooldown[level - 1]

    def print_specs(self):
        """pretty print the stats"""
        return print("\n".join([f"{k}: {v}" for k, v in self.__dict__.items()]))


class QAnnie(BaseSpell):
    champion_name = "Annie"
    spell_key = "q"

    def __init__(self, level):
        super().__init__(champion_name=__class__.champion_name, spell_key=__class__.spell_key, level=level)

        if self.spell_key in ["q", "w", "e"]:
            self.nature = "normal"
        else:
            self.nature = "ulti"
        
        self.damage_type = "magical"
        self.base_damage_per_level = [80, 115, 150, 185, 220]
        self.base_spell_damage = self.base_damage_per_level[level - 1]
        self.ratio = self.ratios[0] # ratios is a list of 2 values, maybe it's ratio for 2 different damage type idk 
