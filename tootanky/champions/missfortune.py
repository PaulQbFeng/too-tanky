from tootanky.champion import BaseChampion
from tootanky.spell import BaseSpell
from tootanky.spell_registry import SpellFactory


class MissFortune(BaseChampion):
    champion_name = "MissFortune"
    champion_type = "Ranged"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)


@SpellFactory.register_spell
class QMissFortune(BaseSpell):
    champion_name = "MissFortune"
    spell_key = "q"


@SpellFactory.register_spell
class WMissFortune(BaseSpell):
    champion_name = "MissFortune"
    spell_key = "w"


@SpellFactory.register_spell
class EMissFortune(BaseSpell):
    champion_name = "MissFortune"
    spell_key = "e"


@SpellFactory.register_spell
class RMissFortune(BaseSpell):
    champion_name = "MissFortune"
    spell_key = "r"
