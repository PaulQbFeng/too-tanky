from tootanky.champion import BaseChampion
from tootanky.spell import BaseSpell
from tootanky.spell_registry import SpellFactory


class Ahri(BaseChampion):
    champion_name = "Ahri"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)


@SpellFactory.register_spell
class QAhri(BaseSpell):
    champion_name = "Ahri"
    spell_key = "q"


@SpellFactory.register_spell
class WAhri(BaseSpell):
    champion_name = "Ahri"
    spell_key = "w"


@SpellFactory.register_spell
class EAhri(BaseSpell):
    champion_name = "Ahri"
    spell_key = "e"


@SpellFactory.register_spell
class RAhri(BaseSpell):
    champion_name = "Ahri"
    spell_key = "r"
