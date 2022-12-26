from tootanky.champion import BaseChampion
from tootanky.spell import BaseSpell
from tootanky.spell_registry import SpellFactory
from tootanky.damage import get_resistance_type


class JarvanIV(BaseChampion):
    champion_name = "JarvanIV"

    def __init__(self, **kwargs):
        super().__init__(spell_max_order=["q", "e", "w"], **kwargs)


@SpellFactory.register_spell
class QJarvanIV(BaseSpell):
    champion_name = "JarvanIV"
    spell_key = "q"

    def __init__(self, champion, level):
        super().__init__(champion, level=level)

        self.nature = self.get_spell_nature(self.spell_key)
        self.damage_type = "physical"
        self.target_res_type = get_resistance_type(self.damage_type)
        self.base_damage_per_level = [90, 130, 170, 210, 250]
        self.ratios = [("bonus_attack_damage", 1.4)]
        self.buffs.append(("target_armor_reduction_percent", [0.1, 0.14, 0.18, 0.22, 0.26]))

        self.buff_duration = "3s"  # to have easy access to this information while coding


@SpellFactory.register_spell
class WJarvanIV(BaseSpell):
    champion_name = "JarvanIV"
    spell_key = "w"

    def __init__(self, champion, level):
        super().__init__(champion, level=level)

        self.nature = self.get_spell_nature(self.spell_key)
        self.base_spell_damage = 0
        self.shield_per_level = [60, 80, 100, 120, 140]


@SpellFactory.register_spell
class EJarvanIV(BaseSpell):
    champion_name = "JarvanIV"
    spell_key = "e"

    def __init__(self, champion, level):
        super().__init__(champion, level=level)

        self.nature = self.get_spell_nature(self.spell_key)


@SpellFactory.register_spell
class RJarvanIV(BaseSpell):
    champion_name = "JarvanIV"
    spell_key = "e"

    def __init__(self, champion, level):
        super().__init__(champion, level=level)

        self.nature = self.get_spell_nature(self.spell_key)
