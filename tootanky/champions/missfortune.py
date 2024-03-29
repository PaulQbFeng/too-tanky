from tootanky.champion import BaseChampion
from tootanky.spell import BaseSpell
from tootanky.spell_registry import SpellFactory


class MissFortune(BaseChampion):
    name = "MissFortune"
    range_type = "Ranged"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


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
