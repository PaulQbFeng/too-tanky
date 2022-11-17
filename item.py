from data_parser import ALL_ITEM_STATS


class BaseItem:
    def __init__(self, item_name: str):
        self.stats = ALL_ITEM_STATS[item_name]


class DoranBlade(BaseItem):
    item_name = "Doran's Blade"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, **kwargs)

