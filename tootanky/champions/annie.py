from tootanky.champion import BaseChampion
from tootanky.spell import BaseSpell
from tootanky.spell_registry import SpellFactory


class Annie(BaseChampion):
    champion_name = "Annie"
    range_type = "Ranged"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)


@SpellFactory.register_spell
class QAnnie(BaseSpell):
    champion_name = "Annie"
    spell_key = "q"
    damage_type = "magical"

    def __init__(self, champion, level):
        super().__init__(champion, level)
        self.base_damage_per_level = [80, 115, 150, 185, 220]
        self.ratios = [("ability_power", 0.8)]


@SpellFactory.register_spell
class WAnnie(BaseSpell):
    champion_name = "Annie"
    spell_key = "w"


@SpellFactory.register_spell
class EAnnie(BaseSpell):
    champion_name = "Annie"
    spell_key = "e"


@SpellFactory.register_spell
class RAnnie(BaseSpell):
    champion_name = "Annie"
    spell_key = "r"
