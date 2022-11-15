from data_parser import get_dataset_from_json

item_set = get_dataset_from_json("data/ddragon/item.json")


item_list=[]
item_stat=[]
for item_id in item_set["data"]:
    item_list.append(item_set["data"][item_id]["name"])
    item_stat.append(item_set["data"][item_id]["stats"])


"""{item_name : {stat : value}}"""
ALL_ITEM_STATS=dict(zip(item_list, item_stat)) 

