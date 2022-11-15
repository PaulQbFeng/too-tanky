from data_parser import get_dataset_from_json

item_set = get_dataset_from_json("data/ddragon/item.json")

item_list=[]
item_stat=[]
item_gold=[]
for item_id in item_set["data"]:
    item_list.append(item_set["data"][item_id]["name"])
    item_stat.append(item_set["data"][item_id]["stats"])
    item_gold.append(item_set["data"][item_id]["gold"]["total"])

 


"""{item_name : {stat : value}}"""
ALL_ITEM_STATS=dict(zip(item_list, item_stat)) 

"""{item_name : total gold}"""
ALL_ITEM_GOLD=dict(zip(item_list, item_gold)) 


class BaseItem:
    def __init__(self, item_name: str):
        self.stats = ALL_ITEM_STATS[item_name]
        self.gold = ALL_ITEM_GOLD[item_name]


class DoranBlade(BaseItem):
    item_name = "Doran's Blade"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, **kwargs)
