import json

#open the json file
file = open("data/1.json", encoding="utf8")

#json to dict
Annie = json.load(file)

#list of skins
skin_list=[]
for i in range(len(Annie['skins'])-1):
    skin_list.append(Annie['skins'][i]['name'])

print(skin_list)
