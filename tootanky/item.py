from abc import ABC, abstractmethod
from dataclasses import dataclass

from tootanky.data_parser import ALL_ITEM_STATS
from tootanky.stats import Stats
from tootanky.attack import BaseDamageMixin


class BaseItem:
    """
    Additional effects passive/active are handled in the children Item specific classes.
    """

    name = None

    def __init__(self):
        item_stats = ALL_ITEM_STATS[self.name].copy()
        self.gold = item_stats.pop("gold")
        self.stats = Stats(item_stats)
        self.limitations = None

    def apply_passive(self):
        pass


class ActiveItem(BaseDamageMixin, BaseItem):
    champion = None
    damage_type = None
    ratios = []


@dataclass
class ItemPassive:
    """Class to define item (or more?) passive"""

    name: str = ""
    unique: bool = False
    stats: Stats = None


class AbstractItem(ABC):
    """Abstract BaseItem class"""

    @abstractmethod
    def apply_passive(self):
        pass
