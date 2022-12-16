from tootanky.champion import BaseChampion
from tootanky.spell import BaseSpell
from tootanky.spell_factory import SpellFactory


class Malphite(BaseChampion):
    champion_name = "Malphite"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)


@SpellFactory.register_spell
class QMalphite(BaseSpell):
    champion_name = "Malphite"
    spell_key = "q"
    damage_type = "magical"

    def __init__(self, champion, level):
        super().__init__(champion, level=level)

        self.nature = self.get_spell_nature(self.spell_key)
        self.base_damage_per_level = [70, 120, 170, 220, 270]
        self.ratios = [("ability_power", 0.6)]


@SpellFactory.register_spell
class WMalphite(BaseSpell):
    champion_name = "Malphite"
    spell_key = "w"


@SpellFactory.register_spell
class EMalphite(BaseSpell):
    champion_name = "Malphite"
    spell_key = "e"
    damage_type = "magical"

    def __init__(self, champion, level):
        super().__init__(champion, level=level)

        self.nature = self.get_spell_nature(self.spell_key)

        self.base_damage_per_level = [60, 95, 130, 165, 200]
        self.ratios = [("ability_power", 0.9), ("armor", 0.3)]


@SpellFactory.register_spell
class RMalphite(BaseSpell):
    champion_name = "Malphite"
    spell_key = "r"
    damage_type = "magical"

    def __init__(self, champion, level):
        super().__init__(champion, level=level)

        self.nature = self.get_spell_nature(self.spell_key)

        self.base_damage_per_level = [200, 300, 400]
        self.ratios = [("ability_power", 0.9)]
