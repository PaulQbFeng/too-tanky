from tootanky.champion import BaseChampion
from tootanky.spell import BaseSpell
from tootanky.spell_registry import SpellFactory


class Orianna(BaseChampion):
    champion_name = "Orianna"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)


@SpellFactory.register_spell
class QOrianna(BaseSpell):
    champion_name = "Orianna"
    spell_key = "q"


@SpellFactory.register_spell
class WOrianna(BaseSpell):
    champion_name = "Orianna"
    spell_key = "w"


@SpellFactory.register_spell
class EOrianna(BaseSpell):
    champion_name = "Orianna"
    spell_key = "e"


@SpellFactory.register_spell
class ROrianna(BaseSpell):
    champion_name = "Orianna"
    spell_key = "r"
    damage_type = "magical"

    def __init__(self, champion, level):
        super().__init__(champion, level)
        self.base_damage_per_level = [200, 275, 350]
        self.ratios = [("ability_power", 0.8)]
