from abc import ABC, abstractmethod
from dataclasses import dataclass

from damage import damage_after_positive_resistance
from data_parser import ALL_ITEM_STATS
from stats import Stats


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


class BaseItem:
    """
    Base class to represent an item. It is initialized with the base stats of the item.
    Additional effects passive/active are handled in the children Champion specific classes.
    """

    def __init__(self, item_name: str):
        self.stats = Stats(ALL_ITEM_STATS[item_name].copy())
        self.passive = ItemPassive()

    def apply_passive(self):
        pass


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
        self.passive = ItemPassive(name="Gouge", unique=True, stats=Stats({"lethality": 10}))

    def apply_passive(self):
        self.stats = self.stats + self.passive.stats


class LastWhisper(BaseItem):
    item_name = "Last Whisper"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, **kwargs)
        self.stats.add("armor_pen_percent", 18)


class Sheen(BaseItem):
    item_name = "Sheen"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, **kwargs)

    def spellblade(self, owner_champion, enemy_champion):
        """Calculates the bonus damage dealt with an autoattack : 100% of base AD"""
        return damage_after_positive_resistance(
            owner_champion.orig_base_stats.attack_damage, enemy_champion.orig_bonus_stats.armor
        )


class RubyCrystal(BaseItem):
    item_name = "Ruby Crystal"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, **kwargs)

        
class SeryldaGrudge(BaseItem): #missing passive, ability haste
    item_name = "Serylda's Grudge"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, **kwargs)
        self.stats.add("armor_pen_percent", 30)

        
class YoumuuGhostblade(BaseItem): #missing passive, active, ability haste
    item_name = "Youmuu's Ghostblade"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, **kwargs)
        self.stats.add("lethality", 18)

class AmplifyingTome(BaseItem):
    item_name = "Amplifying Tome"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, **kwargs)


class BlastingWand(BaseItem):
    item_name = "Blasting Wand"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, **kwargs)


ALL_ITEM_CLASSES = {cls.item_name: cls for cls in BaseItem.__subclasses__()}
