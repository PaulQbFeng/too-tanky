import json
import os

from glossary import MAPPING_CHAMPION_STANDARD, MAPPING_ITEM_STANDARD

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
    out_stats = dict()
    for name, data in dataset["data"].items():
        standard_keys = [MAPPING_CHAMPION_STANDARD[orig_stat_name] for orig_stat_name in data["stats"].keys()]
        out_stats[name] = dict(zip(standard_keys, data["stats"].values()))
    return out_stats

def fill_item_stats(item_set: dict):
    """{item_name : {stat_name : stat_value}}"""
    out_stats = dict()
    for item in item_set["data"].values():
        item["stats"].update({"gold" : item["gold"]["total"]})
        standard_keys = [MAPPING_ITEM_STANDARD[orig_stat_name] for orig_stat_name in item["stats"].keys()]
        out_stats[item["name"]] = dict(zip(standard_keys, item["stats"].values()))
    return out_stats

def get_scaling_stat_names(mapping_champion_standard):
    """Get the stat names that scale with level"""
    scaling_stat_names = []
    for standard in mapping_champion_standard.values():
        if standard.endswith("_perlevel"):
            scaling_stat_names.append(standard.replace("_perlevel", ""))
    return scaling_stat_names


dataset = get_dataset_from_json("data/ddragon/champion.json")
ALL_CHAMPION_BASE_STATS = fill_champion_stats(dataset)

item_set = get_dataset_from_json("data/ddragon/item.json")
ALL_ITEM_STATS = fill_item_stats(item_set)

SCALING_STAT_NAMES = get_scaling_stat_names(MAPPING_CHAMPION_STANDARD)