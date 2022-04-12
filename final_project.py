

import requests, zipfile, os, pickle, json, sqlite3
import d2manifest

#d2manifest.get_manifest()

con = sqlite3.connect('Manifest_zh.content')
print('Connected')
#create a cursor object
cur = con.cursor()

item_set_name = "DestinyInventoryItemDefinition"
perk_set_name = "DestinyPlugSetDefinition"

cur.execute('SELECT json from '+item_set_name)
print('Generating '+item_set_name+' dictionary....')
item_set = cur.fetchall()
item_set_jsons = [json.loads(item[0]) for item in item_set]

item_set_dict = {}
weapon_set_dict = {}
for each_item in item_set_jsons:
    item_name=each_item["displayProperties"]["name"]
    item_set_dict[item_name]=each_item
    if each_item["itemType"] == 3:
        weapon_set_dict[item_name] = each_item







cur.execute('SELECT json from '+perk_set_name)
print('Generating '+perk_set_name+' dictionary....')
perk_set = cur.fetchall()
perk_set_jsons = [json.loads(item[0]) for item in perk_set]




# test_file = open("zh_DestinyPlugSetDefinition.txt", "w")
# for item in item_set_jsons:
#     print(item, file= test_file)
# test_file.close()

# item_dict = {}
# hash = "itemHash"
# for item in item_jsons:
#     item_dict[item[hash]] = item

# #add that dictionary to our all_data using the name of the table
# #as a key.
# all_data[table_name] = item_dict

# print(all_data)