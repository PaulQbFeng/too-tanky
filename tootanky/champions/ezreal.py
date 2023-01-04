from tootanky.champion import BaseChampion
from tootanky.spell import BaseSpell
from tootanky.spell_registry import SpellFactory


class Ezreal(BaseChampion):
    name = "Ezreal"
    range_type = "Ranged"

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
    damage_type = "magical"

    def __init__(self, champion, level):
        super().__init__(champion, level)
        self.base_damage_per_level = [80, 130, 180, 230, 280]
        self.ratios = [("bonus_attack_damage", 0.5), ("ability_power", 0.75)]


@SpellFactory.register_spell
class REzreal(BaseSpell):
    champion_name = "Ezreal"
    spell_key = "r"
