from tootanky.champion import BaseChampion
from tootanky.spell import BaseSpell
from tootanky.spell_factory import SpellFactory


class Annie(BaseChampion):
    champion_name = "Annie"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)


@SpellFactory.register_spell
class QAnnie(BaseSpell):
    champion_name = "Annie"
    spell_key = "q"

    def __init__(self, champion, level):
        super().__init__(champion, level=level)

        self.nature = self.get_spell_nature(self.spell_key)
        self.damage_type = "magical"
        self.target_res_type = self.get_resistance_type()
        self.base_damage_per_level = [80, 115, 150, 185, 220]
        # ["target_ability_power", "base_armor", "target_bonus_health"] add prefix target ?
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
