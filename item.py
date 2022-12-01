from abc import ABC, abstractmethod
from dataclasses import dataclass

from damage import damage_after_resistance, damage_after_positive_resistance
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

    def __init__(self, item_name: str, item_type: str):
        item_stats = ALL_ITEM_STATS[item_name].copy()
        self.gold = item_stats.pop("gold")
        self.stats = Stats(item_stats)
        self.type = item_type
        self.passive = ItemPassive()
        self.holder = None

    def apply_passive(self):
        pass


class DoranBlade(BaseItem):
    item_name = "Doran's Blade"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, item_type="Starter", **kwargs)


class ClothArmor(BaseItem):
    item_name = "Cloth Armor"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, item_type="Basic", **kwargs)


class LongSword(BaseItem):
    item_name = "Long Sword"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, item_type="Basic", **kwargs)


class CloakofAgility(BaseItem):
    item_name = "Cloak of Agility"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, item_type="Basic", **kwargs)


class BFSword(BaseItem):
    item_name = "B. F. Sword"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, item_type="Basic", **kwargs)


class PickAxe(BaseItem):
    item_name = "Pickaxe"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, item_type="Basic", **kwargs)


class SerratedDirk(BaseItem):
    item_name = "Serrated Dirk"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, item_type="Epic", **kwargs)
        self.passive = ItemPassive(name="Gouge", unique=True, stats=Stats({"lethality": 10}))

    def apply_passive(self):
        self.stats = self.stats + self.passive.stats


class LastWhisper(BaseItem):
    item_name = "Last Whisper"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, item_type="Epic", **kwargs)
        self.stats.add("armor_pen_percent", 18)


class Sheen(BaseItem):
    item_name = "Sheen"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, item_type="Epic", **kwargs)

    def spellblade(self, owner_champion, enemy_champion):
        """Calculates the bonus damage dealt with an autoattack : 100% of base AD"""
        return damage_after_positive_resistance(
            owner_champion.base_attack_damage, enemy_champion.bonus_armor
        )


class RubyCrystal(BaseItem):
    item_name = "Ruby Crystal"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, item_type="Basic", **kwargs)

        
class SeryldaGrudge(BaseItem): #missing passive, ability haste
    item_name = "Serylda's Grudge"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, item_type="Legendary", **kwargs)
        self.stats.add("armor_pen_percent", 30)

        
class YoumuuGhostblade(BaseItem): #missing passive, active, ability haste
    item_name = "Youmuu's Ghostblade"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, item_type="Legendary", **kwargs)
        self.stats.add("lethality", 18)


class AmplifyingTome(BaseItem):
    item_name = "Amplifying Tome"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, item_type="Basic", **kwargs)


class BlastingWand(BaseItem):
    item_name = "Blasting Wand"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, item_type="Basic", **kwargs)


class NeedlesslyLargeRod(BaseItem):
    item_name = "Needlessly Large Rod"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, item_type="Basic", **kwargs)


class Galeforce(BaseItem):
    item_name = "Galeforce"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, item_type="Mythic", **kwargs)

    def apply_active(self, enemy_champion):
        if self.holder.level < 10:
            base_active_damage = 180
        elif self.holder.level >= 10:
            base_active_damage = 195 + (self.holder.level - 10) * 15
        percent_missing_health = 1 - enemy_champion.health/(enemy_champion.orig_base_stats.health + enemy_champion.orig_bonus_stats.health)
        if percent_missing_health <= 0.7:
            pre_mtg_dmg = base_active_damage + 0.45 * self.holder.bonus_attack_damage * (1 + percent_missing_health * 5 / 7)
        else:
            pre_mtg_dmg = base_active_damage + 0.45 * self.holder.bonus_attack_damage * 1.5
        return damage_after_resistance(
            pre_mitigation_damage=pre_mtg_dmg,
            base_resistance=enemy_champion.base_magic_resist,
            bonus_resistance=enemy_champion.bonus_magic_resist,
            flat_resistance_pen=self.holder.magic_pen_flat,
            resistance_pen=self.holder.magic_pen_percent,
            bonus_resistance_pen=0
        )


ALL_ITEM_CLASSES = {cls.item_name: cls for cls in BaseItem.__subclasses__()}
