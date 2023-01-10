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


# build dictionnary
def get_champion_stats(json_file: str) -> dict:
    """
    From ddragon champion.json file
    Name standardisation is applied.
    Dummy stats added to dict.

    Output format:
        {
            champion_name : {
                stat_name_1: stat_value_1,
                stat_name_2: stat_value_2,
            }
        }

    """
    dataset = get_dataset_from_json(json_file)

    champion_stats = dict()
    for name, data in dataset["data"].items():
        std_stat_name = [MAPPING_CHAMPION_STANDARD[orig_stat_name] for orig_stat_name in data["stats"].keys()]
        std_champion_name = normalize_champion_name(name)
        champion_stats[std_champion_name] = dict(zip(std_stat_name, data["stats"].values()))

    champion_stats.update(
        {
            "Dummy": {
                "health": 1000,
                "health_perlevel": 0,
                "mana": 0,
                "mana_perlevel": 0,
                "move_speed": 0,
                "armor": 0,
                "armor_perlevel": 0,
                "magic_resist": 0,
                "magic_resist_perlevel": 0,
                "attack_range": 0,
                "health_regen": 0,
                "health_regen_perlevel": 0,
                "mana_regen": 0,
                "mana_regen_perlevel": 0,
                "crit_chance": 0,
                "crit_chance_perlevel": 0,
                "attack_damage": 0,
                "attack_damage_perlevel": 0,
                "attack_speed_perlevel": 0,
                "attack_speed": 0,
            }
        }
    )
    return champion_stats


def get_item_stats(json_file: str) -> dict:
    """
    From ddragon item.json file.
    output format
        {
            item_name : {stat_name : stat_value}
        }
    """
    dataset = get_dataset_from_json(json_file)

    out_stats = dict()
    for item in dataset["data"].values():
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
        std_champion_name = normalize_champion_name(data["name"])
        out_dict[std_champion_name] = dict()
        for spell in data["spells"]:
            spell_key = spell["spellKey"]
            out_dict[std_champion_name][spell_key] = {
                "name": spell["name"],
                "range": spell["range"],
                "cost": spell["costCoefficients"],
                "base_cooldown_per_level": spell["cooldownCoefficients"],
                "max_level": spell["maxLevel"],
            }

    return out_dict


ALL_CHAMPION_BASE_STATS = get_champion_stats("data/ddragon/champion.json")
ALL_CHAMPION_SPELLS = get_champion_spell_stats("data/raw-community-dragon/champions")
ALL_ITEM_STATS = get_item_stats("data/ddragon/item.json")

SCALING_STAT_NAMES = get_scaling_stat_names(MAPPING_CHAMPION_STANDARD)
NON_SCALING_STAT_NAMES = ["move_speed", "attack_range"]
