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
    def __init__(self, champion_name, spell_key, level):
        self.champion_name = champion_name
        self.spell_key = spell_key
        self.spell_specs = ALL_CHAMPION_SPELLS[champion_name][spell_key].copy()
        for name, value in self.spell_specs.items():
            setattr(self, name, value)

        self.level = level
        self.range = self.range[level - 1]
        self.cost = self.cost[level - 1]
        self.cooldown = self.cooldown[level - 1]
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
