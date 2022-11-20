from data_parser import ALL_ITEM_STATS
from champion import Stats
from buff import Buff


print(ALL_ITEM_STATS["Black Cleaver"])


class BaseItem:
    def __init__(self, item_name: str):
        self.stats = Stats()
        self.gold = ALL_ITEM_STATS[item_name]['gold']
        for stat_name in list(ALL_ITEM_STATS[item_name]):
            if stat_name != 'gold':
                setattr(self.stats, stat_name, ALL_ITEM_STATS[item_name][stat_name])


class DoranBlade(BaseItem):
    item_name = "Doran's Blade"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, **kwargs)


class BlackCleaver(BaseItem):
    item_name = "Black Cleaver"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, **kwargs)
        self.debuff = Buff()
        self.debuff_count = 0
        self.debuff.percent_armor_reduction = 0.05
        self.compatible_damage_type = 'physical'

    def apply_effect_to(self, champion):
        """
        There are atleast 2 different cases: the effect gives
        """
        if self.debuff_count < 6:
            champion.debuff_list.append(self.debuff)
            self.debuff_count += 1

