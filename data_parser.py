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

dataset = get_dataset_from_json("data/ddragon/champion.json")
ALL_CHAMPION_BASE_STATS = fill_champion_stats(dataset)

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

