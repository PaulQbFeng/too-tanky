from typing import List

from data_parser import ALL_ITEM_STATS
from damage import damage_after_positive_resistance


class Passive:
    """Class to define item (or more?) passive"""
    def __init__(self, name: str, stats: dict, unique: bool = False):
        self.name = name
        self.unique = unique
        self.stats = stats

class BaseItem:
    """
    Base class to represent an item. It is initialized with the base stats of the item.
    Additional effects passive/active are handled in the children Champion specific classes.
    """
    def __init__(self, item_name: str):
        self.stats = ALL_ITEM_STATS[item_name].copy()

class DoranBlade(BaseItem):
    item_name = "Doran's Blade"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, **kwargs)

class ClothArmor(BaseItem):
    item_name = "Cloth Armor"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, **kwargs)

class LongSword(BaseItem):
    item_name = "Long Sword"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, **kwargs)

class BFSword(BaseItem):
    item_name = "B. F. Sword"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, **kwargs)

class PickAxe(BaseItem):
    item_name = "Pickaxe"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, **kwargs)

class SerratedDirk(BaseItem):
    item_name = "Serrated Dirk"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, **kwargs)
        self.passive = Passive(name="Gouge", unique=True, stats={"lethality": 10})

    def apply_passive(self):
        for stat_name, stat_value in self.passive.stats.items():
            if stat_name not in self.stats:
                self.stats[stat_name] = stat_value
            else:
                self.stats[stat_name] += stat_value

class LastWhisper(BaseItem):
    item_name = "Last Whisper"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, **kwargs)
        self.stats["armor_pen_percent"] = 18 

class Sheen(BaseItem):
    item_name = "Sheen"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, **kwargs)

    def spellblade(self, owner_champion, enemy_champion):
        """Calculates the bonus damage dealt with an autoattack : 100% of base AD """
        return damage_after_positive_resistance(owner_champion.orig_base_stats["attack_damage"], enemy_champion.orig_bonus_stats["armor"])

ALL_ITEM_CLASSES = {cls.item_name: cls for cls in BaseItem.__subclasses__()}

class Inventory:
    """Inventory class that stores the 6 items"""
    def __init__(self, item_names: List[str] = None):
        self.item_names = item_names
        self.items = self.initialize_items()
        self.unique_passives = []
        self.initialize_item_passives()
    
    def initialize_items(self):
        if self.item_names is None:
            return []
        return [ALL_ITEM_CLASSES[item_name]() for item_name in self.item_names]

    def initialize_item_passives(self):
        for item in self.items:
            if hasattr(item, "passive"):
                if item.passive.name not in self.unique_passives:
                    item.apply_passive()
                    if item.passive.unique is True:
                        self.unique_passives.append(item.passive.name)

    @staticmethod
    def update_bonus_stat_with_item(total_item_stats, item_stats):
        """Update the base stats in the item stats dict with a new item."""
        for stat_name, stat_value in item_stats.items():
            if stat_name not in total_item_stats:
                total_item_stats[stat_name] = stat_value
            else:
                total_item_stats[stat_name] += stat_value

    def get_items_total_stats(self, items):
        """Sum the base stats of each item"""
        if len(items) == 0:
            return dict()

        total_item_stats = dict()
        for item in items:
            self.update_bonus_stat_with_item(total_item_stats, item.stats)

        return total_item_stats
