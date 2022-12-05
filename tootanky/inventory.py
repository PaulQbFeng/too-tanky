from typing import List, Optional

from tootanky.item import BaseItem
from tootanky.stats import Stats


class Inventory:
    def __init__(self, items: Optional[List[BaseItem]] = None, champion=None):
        if items is None:
            self.items = []
        else:
            self.items = items
        assert len(self.items) <= 6, "Inventory can't contain more than 6 items."
        self.item_type_count = {"Starter": 0, "Basic": 0, "Epic": 0, "Legendary": 0, "Mythic": 0}
        for item in self.items:
            item.champion = champion
            assert self.item_type_count["Mythic"] <= 1, "A champion can't have more than one mythic item."
            self.item_type_count[item.type] += 1

        self.unique_item_passives = []
        self.item_stats = self.get_stats()

    def get_item(self, item_name):
        # TODO: what happens when there are several copies of the same item in the inventory
        return next(item for item in self.items if item.item_name == item_name)

    def get_mythic_item(self):
        return next((item for item in self.items if item.type == "Mythic"), None)

    def get_all_indexes(self, item_name):
        indexes = []
        for index, item in enumerate(self.items):
            if item.item_name == item_name:
                indexes.append(index)
        return indexes

    def get_stats(self):
        """Get total stats from all items (including passives that give stats)"""
        if len(self.items) == 0:
            return Stats()
        total_item_stats = Stats()
        for item in self.items:
            # TODO: some items have unique passives AND passives that are not unique
            if item.passive.unique:
                if item.passive.name not in self.unique_item_passives:
                    self.unique_item_passives.append(item.passive.name)
                    item.apply_passive()
            else:
                item.apply_passive()
            total_item_stats = total_item_stats + item.stats
        return total_item_stats

    def get_price(self):
        price = 0
        for item in self.items:
            price += item.gold
        return price

    def add_item(self, item):
        assert len(self.items) <= 5, "Inventory can't contain more than 6 items."
        assert self.item_type_count["Mythic"] <= 1, "A champion can't have more than one mythic item."
        self.items.append(item)
        self.item_type_count[item.type] += 1
        if item.passive.unique:
            if item.passive.name not in self.unique_item_passives:
                self.unique_item_passives.append(item.passive.name)
                item.apply_passive()
        self.item_stats = self.item_stats + item.stats

    def remove_item(self, item_name):
        indexes = self.get_all_indexes(item_name)
        assert len(indexes) != 0, "The item {} is not in the inventory.".format(item_name)
        # by default, we remove the last occurence to remove an item that did not apply its unique passive
        item = self.items.pop(indexes[-1])
        self.item_type_count[item.type] -= 1
        if item.passive.unique:
            if len(indexes) == 1:
                self.unique_item_passives.remove(item.passive.name)
        self.item_stats = self.item_stats - item.stats

    def mythic_passive_stats(self):
        # TODO
        mythic_item = self.get_mythic_item()
        if mythic_item is None:
            return 0
