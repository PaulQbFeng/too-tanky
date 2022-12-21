import json
import os

from tootanky.glossary import MAPPING_CHAMPION_STANDARD, MAPPING_ITEM_STANDARD, normalize_champion_name


# gets a list of json files from a directory
def get_json_files(directory: str):
    list_of_json = []
    for file in os.listdir(directory):
        if file.endswith(".json"):
            list_of_json.append(file)
    return list_of_json


# get dataset from a .json file
def get_dataset_from_json(filename: str):
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
        item["stats"].update({"gold": item["gold"]["total"]})
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


def get_champion_spell_stats(folder: str):
    """
    From raw community dragon individual champions (data/raw-community-dragon/champions.{number}.json)
        - Extract Champion spells
        - Store all spells in a dict with format
            out_dict = {
                "Annie": {
                    "q": {
                        "name",
                        "range
                        etc..
                    }
                    ...

                    "r" :
                    {},
                "Ahri": {
                    etc..
                }
                }
            }
    """
    json_paths = get_json_files(folder)
    json_paths.remove("-1.json")
    out_dict = dict()
    for json_file in json_paths:
        data = get_dataset_from_json(folder + "/" + json_file)
        out_dict[data["name"]] = dict()
        for spell in data["spells"]:
            spell_key = spell["spellKey"]
            out_dict[data["name"]][spell_key] = {
                "name": spell["name"],
                "range": spell["range"],
                "cost": spell["costCoefficients"],
                "cooldown": spell["cooldownCoefficients"],
                "ratios": [spell["coefficients"]["coefficient1"], spell["coefficients"]["coefficient2"]],
                "max_level": spell["maxLevel"],
            }

    return out_dict


ALL_CHAMPION_BASE_STATS_ORIGINAL = fill_champion_stats(get_dataset_from_json("data/ddragon/champion.json"))
ALL_CHAMPION_SPELLS_ORIGINAL = get_champion_spell_stats("data/raw-community-dragon/champions")

ALL_CHAMPION_BASE_STATS = dict()
ALL_CHAMPION_SPELLS = dict()

for i in range(len(ALL_CHAMPION_BASE_STATS_ORIGINAL.keys())):
    key = list(ALL_CHAMPION_BASE_STATS_ORIGINAL.keys())[i]
    new_key = normalize_champion_name(key)
    ALL_CHAMPION_BASE_STATS[new_key] = ALL_CHAMPION_BASE_STATS_ORIGINAL[key]

for i in range(len(ALL_CHAMPION_SPELLS_ORIGINAL.keys())):
    key = list(ALL_CHAMPION_SPELLS_ORIGINAL.keys())[i]
    new_key = normalize_champion_name(key)
    ALL_CHAMPION_SPELLS[new_key] = ALL_CHAMPION_SPELLS_ORIGINAL[key]

assert sorted(list(ALL_CHAMPION_BASE_STATS.keys()), key=str.casefold) == sorted(ALL_CHAMPION_SPELLS.keys(), key=str.casefold)

ALL_CHAMPION_BASE_STATS.update({'Dummy': {'health': 1000, 'health_perlevel': 0, 'mana': 0, 'mana_perlevel': 0,
                                          'move_speed': 0, 'armor': 0, 'armor_perlevel': 0, 'magic_resist': 0,
                                          'magic_resist_perlevel': 0, 'attack_range': 0, 'health_regen': 0,
                                          'health_regen_perlevel': 0, 'mana_regen': 0, 'mana_regen_perlevel': 0,
                                          'crit_chance': 0, 'crit_chance_perlevel': 0, 'attack_damage': 0,
                                          'attack_damage_perlevel': 0, 'attack_speed_perlevel': 0, 'attack_speed': 0}})

item_set = get_dataset_from_json("data/ddragon/item.json")
ALL_ITEM_STATS = fill_item_stats(item_set)

SCALING_STAT_NAMES = get_scaling_stat_names(MAPPING_CHAMPION_STANDARD)
