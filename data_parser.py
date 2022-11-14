import json


file = open("data/ddragon/champion.json", encoding="utf8")
dataset = json.load(file)

# build dictionnary {champion_name : {stats}}
def fill_champion_stats(dataset: dict):
    # define champion list
    champion_list = list(dataset["data"].keys())
    ALL_CHAMPION_BASE_STAT = {}
    for x in champion_list:
        ALL_CHAMPION_BASE_STAT[x] = dataset["data"][x]["stats"]
    return ALL_CHAMPION_BASE_STAT

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

