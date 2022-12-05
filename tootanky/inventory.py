from typing import Optional, List
from tootanky.item import BaseItem
from tootanky.stats import Stats


class Inventory:

    def __init__(self, items: Optional[List[BaseItem]] = None):
        self.items = []
        self.unique_item_passives = []
        self.nb_legendary = 0
        self.nb_mythic = 0
        self.item_stats = Stats()
        if items is not None:
            assert len(items) <= 6, "Inventory can't contain more than 6 items."
            for item in items:
                self.add_item(item)

    def get_item(self, name):
        # TODO: what happens with this method when there are several copies of the same item in the inventory
        return next(item for item in self.items if item.name == name)

    def get_mythic_item(self):
        return next((item for item in self.items if item.type == "Mythic"), None)

    def is_unique_copy(self, name):
        nb_copy = 0
        for item in self.items:
            if item.name == name:
                nb_copy += 1
            if nb_copy > 2:
                return False
        return True

    def is_unique_limitation(self, limitations):
        nb_copy = 0
        for item in self.items:
            if item.limitation in limitations:
                nb_copy += 1
            if nb_copy > 2:
                return False
        return True

    def get_all_indexes(self, name):
        indexes = []
        for index, item in enumerate(self.items):
            if item.name == name:
                indexes.append(index)
        return indexes

    def check_item(self, item):
        if item.type == "Legendary":
            assert self.is_unique_copy(item.name), "A champion can't have more than one copy of {}".format(item.name)
        if item.type == "Mythic":
            assert self.nb_mythic <= 1, "A champion can't have more than one mythic item."
        if item.limitation in ["Immolate", "Lifeline", "Mana Charge", "Last Whisper", "Void Pen", "Sightstone",
                               "Ability Haste Capstone", "Quicksilver", "Hydra", "Glory", "Eternity",
                               "Mythic Component"]:
            assert self.is_unique_limitation([item.limitation])
        if item.limitation in ["Support", "Jungle"]:
            assert self.is_unique_limitation(["Support", "Jungle"])
        if item.limitation in ["Crit Modifier", "Marksman Capstone"]:
            assert self.is_unique_limitation(["Crit Modifier", "Marksman Capstone"])

    def apply_item_passive(self, item):
        # TODO: some items have unique passives AND passives that are not unique
        if item.passive.unique:
            if item.passive.name not in self.unique_item_passives:
                self.unique_item_passives.append(item.passive.name)
                item.apply_passive()
        else:
            item.apply_passive()

    def get_price(self):
        price = 0
        for item in self.items:
            price += item.gold
        return price

    def add_item(self, item):
        assert len(self.items) <= 5, "Inventory can't contain more than 6 items."
        if item.type == "Legendary":
            self.nb_legendary += 1
        if item.type == "Mythic":
            self.nb_mythic += 1
        self.check_item(item)
        self.apply_item_passive(item)
        self.item_stats = self.item_stats + item.stats
        self.items.append(item)

    def remove_item(self, name):
        indexes = self.get_all_indexes(name)
        assert len(indexes) != 0, "The item {} is not in the inventory.".format(name)
        # by default, we remove the last occurence to remove an item that did not apply its unique passive
        item = self.items[indexes[-1]]
        if item.type == "Legendary":
            self.nb_legendary -= 1
        if item.type == "Mythic":
            self.nb_mythic -= 1
        if item.passive.unique:
            if len(indexes) == 1:
                self.unique_item_passives.remove(item.passive.name)
        self.item_stats = self.item_stats - item.stats
        del self.items[indexes[-1]]

    def mythic_passive_stats(self):
        # TODO
        mythic_item = self.get_mythic_item()
        if mythic_item is None:
            return 0
