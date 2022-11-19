from data_parser import ALL_ITEM_STATS
from damage import damage_after_positive_resistance
from champion import Dummy

class BaseItem:
    """
    Base class to represent an item. It is initialized with the base stats of the item.
    Additional effects passive/active are handled in the children Champion specific classes.
    """
    def __init__(self, item_name: str):
        self.update_stat(item_name)

    def update_stat(self, item_name):
        for stat_name, stat_value in ALL_ITEM_STATS[item_name].items():
            setattr(self, stat_name, stat_value)


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
            return damage_after_positive_resistance(owner_champion.orig_base_stats["attack_damage"], enemy_champion.orig_bonus_stats["armor"])
        return damage_after_positive_resistance(owner_champion.orig_base_stats["attack_damage"], enemy_champion.orig_bonus_stats["armor"])
