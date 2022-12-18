from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from tootanky.damage import damage_after_resistance, ratio_damage, pre_mitigation_damage, get_resistance_type
from tootanky.data_parser import ALL_ITEM_STATS
from tootanky.stats import Stats


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
    Additional effects passive/active are handled in the children Item specific classes.
    """

    damage_type = None
    base_damage = 0

    def __init__(self):
        item_stats = ALL_ITEM_STATS[self.name].copy()
        self.gold = item_stats.pop("gold")
        self.stats = Stats(item_stats)
        self.limitations = None
        if self.damage_type is not None:
            self.target_res_type = get_resistance_type(self.damage_type)

    def apply_passive(self):
        pass

    def damage(self, target, damage_modifier_flat=0, damage_modifier_coeff=1) -> float:
        """Calculates the damage dealt to a champion with a spell"""

        ratio_dmg = ratio_damage(champion=self.champion, target=target, ratios=self.ratios)

        pre_mtg_dmg = pre_mitigation_damage(
            self.base_damage,
            ratio_dmg,
            damage_modifier_flat=damage_modifier_flat,
            damage_modifier_coeff=damage_modifier_coeff,
        )

        res_type = self.target_res_type
        if res_type == "armor":
            bonus_resistance_pen = self.champion.bonus_armor_pen_percent
        else:
            bonus_resistance_pen = 0
        # TODO: Can be refactored once we know more about bonus res pen
        post_mtg_dmg = damage_after_resistance(
            pre_mitigation_damage=pre_mtg_dmg,
            base_resistance=getattr(target, f"base_{res_type}"),
            bonus_resistance=getattr(target, f"bonus_{res_type}"),
            flat_resistance_pen=getattr(self.champion, f"{res_type}_pen_flat"),
            resistance_pen=getattr(self.champion, f"{res_type}_pen_percent"),
            bonus_resistance_pen=bonus_resistance_pen,
        )

        return post_mtg_dmg
