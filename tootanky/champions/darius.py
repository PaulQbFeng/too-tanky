from tootanky.champion import BaseChampion
from tootanky.spell import BaseSpell
from tootanky.spell_registry import SpellFactory


class Darius(BaseChampion):
    name = "Darius"
    range_type = "Melee"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@SpellFactory.register_spell
class QDarius(BaseSpell):
    champion_name = "Darius"
    spell_key = "q"


@SpellFactory.register_spell
class WDarius(BaseSpell):
    champion_name = "Darius"
    spell_key = "w"


@SpellFactory.register_spell
class EDarius(BaseSpell):
    champion_name = "Darius"
    spell_key = "e"


@SpellFactory.register_spell
class RDarius(BaseSpell):
    champion_name = "Darius"
    spell_key = "r"
