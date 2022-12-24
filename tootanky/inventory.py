from typing import List, Optional

from tootanky.item import BaseItem, ActiveItem
from tootanky.item_factory import SPELL_BLADE_ITEMS
from tootanky.stats import Stats


class Inventory:
    def __init__(self, items: Optional[List[BaseItem]] = None, champion=None):
        self.items = []
        self.unique_item_passives = []
        self.item_type_count = {"Starter": 0, "Basic": 0, "Epic": 0, "Legendary": 0, "Mythic": 0}
        self.item_stats = Stats()

        if items is not None:
            assert len(items) <= 6, "Inventory can't contain more than 6 items."
            for item in items:
                item.champion = champion
                self.item_type_count[item.type] += 1
                self.check_item(item)
                self.items.append(item)
                self.apply_item_passive(item)
                self.item_stats += item.stats
                if isinstance(item, ActiveItem):
                    item.init_champion_type()

    def contains(self, name):
        """Check if an item is in the inventory or if atleast one item of a list of items is in the inventory"""
        if isinstance(name, list):
            return any(n in (item.name for item in self.items) for n in name)
        return name in (item.name for item in self.items)

    def get_item(self, name):
        # TODO: Handle case where there are item duplicates
        return next((item for item in self.items if item.name == name), None)

    def get_mythic_item(self):
        return next((item for item in self.items if item.type == "Mythic"), None)

    def is_unique_limitation(self, limitations):
        for item in self.items:
            if item.limitations is None:
                continue
            if set(item.limitations) & set(limitations):
                return False
        return True

    def get_all_indexes(self, name):
        indexes = []
        for index, item in enumerate(self.items):
            if item.name == name:
                indexes.append(index)
        return indexes

    def check_item(self, item):
        # TODO: test, navori quickblades with spear of shojin (must download new patch) should raise AssertionError
        if item.type == "Legendary":
            assert not self.contains(
                item.name
            ), "A champion can't have more than one copy of {}. (Legendart Item)".format(item.name)
        if item.type == "Mythic":
            assert self.item_type_count["Mythic"] <= 1, "A champion can't have more than one mythic item."
        if item.limitations is None:
            return None
        for limitation in item.limitations:
            if limitation in [
                "Immolate",
                "Lifeline",
                "Mana Charge",
                "Last Whisper",
                "Void Pen",
                "Sightstone",
                "Ability Haste Capstone",
                "Quicksilver",
                "Hydra",
                "Glory",
                "Eternity",
                "Mythic Component",
            ]:
                assert self.is_unique_limitation([limitation]), "A champion can have only one {} item".format(
                    limitation
                )
            if limitation in ["Support", "Jungle"]:
                assert self.is_unique_limitation(
                    ["Support", "Jungle"]
                ), "A champion can have only one Support/Jungle item"
            if limitation in ["Crit Modifier", "Marksman Capstone"]:
                assert self.is_unique_limitation(
                    ["Crit Modifier", "Marksman Capstone"]
                ), "A champion can have only one Crit Modifier/Marksman Capstone item"

    def apply_item_passive(self, item):
        # TODO: some items have unique passives AND passives that are not unique
        if hasattr(item, "passive"):
            if item.passive.unique:
                if item.passive.name not in self.unique_item_passives:
                    self.unique_item_passives.append(item.passive.name)
                    item.apply_passive()
            else:
                item.apply_passive()

    def get_mythic_passive_stats(self):
        if self.item_type_count["Mythic"] == 1:
            nb_legendary = self.item_type_count["Legendary"]
            if nb_legendary > 0:
                mythic_item = self.get_mythic_item()
                for i in range(len(mythic_item.mythic_passive_stats)):
                    mythic_item.mythic_passive_stats[i][1] *= nb_legendary
                return mythic_item.mythic_passive_stats
        return None

    def get_price(self):
        price = 0
        for item in self.items:
            price += item.gold
        return price

    def mythic_passive_stats(self):
        # TODO
        mythic_item = self.get_mythic_item()
        if mythic_item is None:
            return 0

    def get_spellblade_item(self):
        for name in SPELL_BLADE_ITEMS:
            item = self.get_item(name)
            if item:
                return item
        return None
