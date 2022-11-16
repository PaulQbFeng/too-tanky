import json
import os

#gets a list of json files from a directory
def get_json_files(directory : str):
    list_of_json = []
    for file in os.listdir(directory):
        if file.endswith(".json"):
            list_of_json.append(file)
    return(list_of_json)

#get dataset from a .json file    
def get_dataset_from_json(filename : str):
    file = open(filename, encoding="utf8")
    dataset = json.load(file)
    return dataset

# build dictionnary {champion_name : {stats}}
def fill_champion_stats(dataset: dict):
    return { name: data["stats"] for name, data in dataset["data"].items() }

def fill_item_stats(item_set: dict):
    """{item_name : {stat_name : stat_value}}"""
    ALL_ITEM_STATS = dict()
    for item_id in item_set["data"]:
        item = item_set["data"][item_id]
        item["stats"].update({"gold" : item["gold"]["total"]})
        ALL_ITEM_STATS[item["name"]] = item["stats"]
    return ALL_ITEM_STATS


dataset = get_dataset_from_json("data/ddragon/champion.json")
ALL_CHAMPION_BASE_STATS = fill_champion_stats(dataset)

item_set = get_dataset_from_json("data/ddragon/item.json")
ALL_ITEM_STATS = fill_item_stats(item_set)


SCALING_STAT_NAMES = [
    "hp",
    "mp",
    "armor",
    "spellblock",
    "hpregen",
    "mpregen",
    "crit",
    "attackdamage",
    "attackspeed",
]

