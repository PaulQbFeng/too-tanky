from data_parser import ALL_ITEM_STATS
from damage import damage_after_positive_resistance
from champion import Dummy

class BaseItem:
    def __init__(self, item_name: str):
        self.stats = ALL_ITEM_STATS[item_name]


class DoranBlade(BaseItem):
    item_name = "Doran's Blade"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, **kwargs)

class Sheen(BaseItem):
    item_name = "Sheen"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, **kwargs)

    def spellblade(self, owner_champion, enemy_champion):
        """Calculates the bonus damage dealt with an autoattack : 100% of base AD """
        if isinstance(enemy_champion, Dummy):
            return damage_after_positive_resistance(owner_champion.attack_damage, enemy_champion.bonus_armor)
        return damage_after_positive_resistance(owner_champion.attack_damage, enemy_champion.armor)
