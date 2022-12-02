from typing import Optional, List
from item import BaseItem
from stats import Stats


class Inventory:

    def __init__(self, items: Optional[List[BaseItem]] = None):
        if items is None:
            self.items = []
        else:
            self.items = items
        assert len(self.items) <= 6, "Inventory can't contain more than 6 items."
        self.nb_legendary = 0
        self.nb_mythic = 0
        for item in self.items:
            if item.type == "Legendary":
                self.nb_legendary += 1
            if item.type == "Mythic":
                self.nb_mythic += 1
        assert self.nb_mythic <= 1, "A champion can't have more than one mythic item."

    def get_item(self, item_name):
        return next(item for item in self.items if item.item_name == item_name)

    def get_stats(self):
        """Get total stats from all items (including passives that give stats)"""
        if len(self.items) == 0:
            return Stats()
        total_item_stats = Stats()
        for item in self.items:
            total_item_stats = total_item_stats + item.stats
        return total_item_stats

    def add_item(self, item):
        assert len(self.items) <= 5, "Inventory can't contain more than 6 items."
        if item.type == "Mythic":
            assert self.nb_mythic == 0, "A champion can't have more than one mythic item."
        self.items.append(item)

    def remove_item(self, item_name):
        item = next((item for item in self.items if item.item_name == item_name), None)
        assert item is not None, "The item {} is not in the inventory.".format(item_name)
        if item.type == "Legendary":
            self.nb_legendary -= 1
        if item.type == "Mythic":
            self.nb_mythic -= 1
        self.items.remove(item)
