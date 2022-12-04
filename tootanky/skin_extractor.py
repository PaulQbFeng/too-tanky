import json, os
import matplotlib.pyplot as plt
from tootanky.data_parser import get_json_files


#sort a list of dic of type {key: value}, by value from highest to lowest
def sort_list_of_dict_by_value_high_to_low(list_of_dic : list):
    list_of_dic = sorted(list_of_dic, key=lambda d : next(iter(d.values())), reverse=True)
    return list_of_dic

#takes a json file and returns a dictionnary {champion name : list_of_skins}
def skin_parser(file : str):
    champ = json.load(open(file, encoding="utf8"))
    #name, check if json file is valid
    if "name" in champ:
        name = champ['name']
    #list of skins
    skin_list=[]
    if "skins" in champ: #check if json file is valid
        for i in range(len(champ['skins'])):
            skin_list.append(champ['skins'][i]['name'])
    return {name : skin_list}

def sort_list_of_dict_by_key(list_of_dic : list):
    list_of_dic = sorted(list_of_dic, key = lambda d: next(iter(d)), reverse=True)
    return list_of_dic

#takes {champion : list_of_skins} and returns {champion : number_of_skins}
def get_number_of_skins(dic : dict):
    keys = list(dic.keys())
    name = keys[0]
    nb_skins = len(x[name])
    dictionnary = {name : nb_skins}
    return dictionnary

def plot_nb_skins(list_of_dic : list):
    names=[]
    values=[]
    for x in list_of_dic:
        keys=list(x.keys())
        names.append(keys[0])
        values.append(x[keys[0]])
    plt.bar(range(len(names)), values, tick_label=names)
    plt.show()


#init
all_skins = []

#get the list of all the json files
list_of_json = get_json_files("data/raw-community-dragon/champions")
os.chdir("data/raw-community-dragon/champions")

#parse the json file and build a list of all dictionnaries {champion : list_of skins}
for x in list_of_json:
        dictionnary = skin_parser(x)
        all_skins.append(dictionnary)

#sort the list of dict, by alphabetical order of champion name, dict is {champion name : list of skins}
all_skins=sort_list_of_dict_by_key(all_skins)
print(all_skins)

#list of dict {champion name : nb of skins (including base)}
list_dict_nb_skin=[]
for x in all_skins:
    list_dict_nb_skin.append(get_number_of_skins(x))

#sort dict_nb_skin by number of skins, highest to lowest
list_dict_nb_skin = sort_list_of_dict_by_value_high_to_low(list_dict_nb_skin)

#plot
plot_nb_skins(list_dict_nb_skin)

