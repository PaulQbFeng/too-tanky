from tootanky.champion import BaseChampion
from tootanky.spell import BaseSpell
from tootanky.spell_factory import SpellFactory


class MissFortune(BaseChampion):
    champion_name = "Miss Fortune"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)


@SpellFactory.register_spell
class QMissFortune(BaseSpell):
    champion_name = "Miss Fortune"
    spell_key = "q"


@SpellFactory.register_spell
class WMissFortune(BaseSpell):
    champion_name = "Miss Fortune"
    spell_key = "w"


@SpellFactory.register_spell
class EMissFortune(BaseSpell):
    champion_name = "Miss Fortune"
    spell_key = "e"


@SpellFactory.register_spell
class RMissFortune(BaseSpell):
    champion_name = "Miss Fortune"
    spell_key = "r"
