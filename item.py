from data_parser import ALL_ITEM_STATS
from champion import Stats
from buff import ArmorReduction, StackableArmorReduction


print(ALL_ITEM_STATS["Black Cleaver"])


class BaseItem:
    def __init__(self, item_name: str):
        self.stats = Stats()
        self.gold = ALL_ITEM_STATS[item_name]['gold']
        self.item_holder = None
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
        # percent armor penetration stacks are calculated so that they stack multiplicatively and correspond to 5%
        # percent armor reduction stacked additively
        self.flat_reduction_stacks = [0, 0, 0, 0, 0, 0]
        self.percent_armor_reduction_stacks = [0.05, 0.05/0.95, 0.05/0.9, 0.05/0.85, 0.05/0.8, 0.05/0.75]

    def apply_effect(self):
        buff = StackableArmorReduction(name='Carve', flat_reduction=self.flat_reduction_stacks,
                                       percent_reduction=self.percent_armor_reduction_stacks,
                                       duration_type='indefinite', stack_number=6, compatible_damage_type='physical',
                                       compatible_spell_type='all')
        buff.add_buff_to(self.item_holder)
