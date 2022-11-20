from typing import List, Optional

from item import ALL_ITEM_CLASSES


class Passive:
    """Class to define item (or more?) passive"""

    def __init__(self, name: str, stats: dict, unique: bool = False):
        self.name = name
        self.unique = unique
        self.stats = stats


class Inventory:
    """Inventory class that stores the 6 items"""

    def __init__(self, item_names: Optional[List[str]]):
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
