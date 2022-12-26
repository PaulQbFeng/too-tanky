from tootanky.champion import BaseChampion
from tootanky.spell import BaseSpell
from tootanky.spell_registry import SpellFactory


class Ezreal(BaseChampion):
    champion_name = "Ezreal"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@SpellFactory.register_spell
class QEzreal(BaseSpell):
    champion_name = "Ezreal"
    spell_key = "q"
    damage_type = "physical"
    apply_on_hit = True

    def __init__(self, champion, level):
        super().__init__(champion, level)
        self.base_damage_per_level = [20, 45, 70, 95, 120]
        self.ratios = [("attack_damage", 1.3), ("ability_power", 0.15)]


@SpellFactory.register_spell
class WEzreal(BaseSpell):
    champion_name = "Ezreal"
    spell_key = "w"


@SpellFactory.register_spell
class EEzreal(BaseSpell):
    champion_name = "Ezreal"
    spell_key = "e"


@SpellFactory.register_spell
class REzreal(BaseSpell):
    champion_name = "Ezreal"
    spell_key = "r"
