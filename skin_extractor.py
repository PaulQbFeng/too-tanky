import json
import os

import matplotlib.pyplot as plt

# lists of all json files
list_of_json = []
for file in os.listdir("data/raw-community-dragon/champions"):
    if file.endswith(".json"):
        list_of_json.append(file)

os.chdir("data/raw-community-dragon/champions")

# init
all_skins = []
name_list = []

for x in list_of_json:
    # open the json file
    file = open(x, encoding="utf8")

    # json to dict
    champ = json.load(file)

    # name
    if "name" in champ:
        name = champ["name"]

    # list of skins
    skin_list = []
    if "skins" in champ:
        for i in range(len(champ["skins"])):
            skin_list.append(champ["skins"][i]["name"])

    if (name != "None") and ("name" in champ):
        dictionnary = {name: skin_list}
        all_skins.append(dictionnary)
        name_list.append(name)

# sort the list of dict, dict is {champion name : list of skins}
name_list.sort()
all_skins = sorted(all_skins, key=lambda d: [k in d for k in name_list], reverse=True)
print(all_skins)

# nombre de skin par champion trié par ordre croissant : dict is {champion name : nb of skins (including base)}
dict_nb_skin = []
for x in all_skins:
    keys = list(x.keys())
    name = keys[0]
    nb_skins = len(x[name])
    dictionnary = {name: nb_skins}
    dict_nb_skin.append(dictionnary)
# print(dict_nb_skin)

# sort dict_nb_skin by value
def first_value(d):
    return next(iter(d.values()))


dict_nb_skin = sorted(dict_nb_skin, key=first_value, reverse=True)

# print(dict_nb_skin)

# plot
names = []
values = []
for x in dict_nb_skin:
    keys = list(x.keys())
    names.append(keys[0])
    values.append(x[keys[0]])

plt.bar(range(len(names)), values, tick_label=names)
plt.show()
