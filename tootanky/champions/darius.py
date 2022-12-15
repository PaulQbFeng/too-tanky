from tootanky.champion import BaseChampion
from tootanky.spell import BaseSpell
from tootanky.spell_factory import SpellFactory

class Darius(BaseChampion):
    champion_name = "Darius"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)


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
