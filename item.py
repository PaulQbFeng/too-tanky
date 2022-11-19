from data_parser import ALL_ITEM_STATS


class BaseItem:
    """
    Base class to represent an item. It is initialized with the base stats of the item.
    Additional effects passive/active are handled in the children Champion specific classes.
    """
    def __init__(self, item_name: str):
        self.update_stat(item_name)

    def update_stat(self, item_name):
        for stat_name, stat_value in ALL_ITEM_STATS[item_name].items():
            setattr(self, stat_name, stat_value)


class DoranBlade(BaseItem):
    item_name = "Doran's Blade"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, **kwargs)

