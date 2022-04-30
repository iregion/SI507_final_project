import requests, zipfile, os, pickle, json, sqlite3

def get_manifest(language):
    manifest_url = 'http://www.bungie.net/Platform/Destiny2/Manifest/'
    HEADERS = {"X-API-Key":'1930f03ca4fe450684a4efca0c9406f0'}


    #get the manifest location from the json
    r = requests.get(manifest_url, headers=HEADERS)
    manifest = r.json()

    if language == 0:
        mani_url = 'http://www.bungie.net'+manifest['Response']['mobileWorldContentPaths']['en']
    elif language == 1:
        mani_url = 'http://www.bungie.net'+manifest['Response']['mobileWorldContentPaths']['zh-chs']
    else:
        print("Invalid language")
        return

    #Download the file, write it to 'MANZIP'
    r = requests.get(mani_url)

    # file = open("test_result.txt", "w")
    # file.write(r.text)
    # file.close()

    with open("MANZIP", "wb") as zip:
        zip.write(r.content)
    print("Download Complete!")

    #Extract the file contents, and rename the extracted file
    # to 'Manifest.content'
    with zipfile.ZipFile('MANZIP') as zip:
        name = zip.namelist()
        zip.extractall()
    if language == 0:
        os.rename(name[0], 'Manifest_en.content')
    elif language == 1:
        os.rename(name[0], 'Manifest_zh.content')
    else:
        print("Invalid language")
        return

    print('Unzipped!')

# hashes = {
#     'DestinyActivityDefinition': 'activityHash',
#     'DestinyActivityTypeDefinition': 'activityTypeHash',
#     'DestinyClassDefinition': 'classHash',
#     'DestinyGenderDefinition': 'genderHash',
#     'DestinyInventoryBucketDefinition': 'bucketHash',
#     'DestinyInventoryItemDefinition': 'itemHash',
#     'DestinyProgressionDefinition': 'progressionHash',
#     'DestinyRaceDefinition': 'raceHash',
#     'DestinyTalentGridDefinition': 'gridHash',
#     'DestinyUnlockFlagDefinition': 'flagHash',
#     'DestinyHistoricalStatsDefinition': 'statId',
#     'DestinyDirectorBookDefinition': 'bookHash',
#     'DestinyStatDefinition': 'statHash',
#     'DestinySandboxPerkDefinition': 'perkHash',
#     'DestinyDestinationDefinition': 'destinationHash',
#     'DestinyPlaceDefinition': 'placeHash',
#     'DestinyActivityBundleDefinition': 'bundleHash',
#     'DestinyStatGroupDefinition': 'statGroupHash',
#     'DestinySpecialEventDefinition': 'eventHash',
#     'DestinyFactionDefinition': 'factionHash',
#     'DestinyVendorCategoryDefinition': 'categoryHash',
#     'DestinyEnemyRaceDefinition': 'raceHash',
#     'DestinyScriptedSkullDefinition': 'skullHash',
#     'DestinyGrimoireCardDefinition': 'cardId'
# }

# hashes_trunc = {
#     'DestinyInventoryItemDefinition': 'itemHash',
#     'DestinyTalentGridDefinition': 'gridHash',
#     'DestinyHistoricalStatsDefinition': 'statId',
#     'DestinyStatDefinition': 'statHash',
#     'DestinySandboxPerkDefinition': 'perkHash',
#     'DestinyStatGroupDefinition': 'statGroupHash'
# }

# def build_dict(hash_dict):
#     #connect to the manifest
#     con = sqlite3.connect('manifest.content')
#     print('Connected')
#     #create a cursor object
#     cur = con.cursor()

#     all_data = {}
#     #for every table name in the dictionary
#     for table_name in hash_dict.keys():
#         #get a list of all the jsons from the table
#         cur.execute('SELECT json from '+table_name)
#         print('Generating '+table_name+' dictionary....')

#         #this returns a list of tuples: the first item in each tuple is our json
#         items = cur.fetchall()

#         #create a list of jsons
#         item_jsons = [json.loads(item[0]) for item in items]

#         #create a dictionary with the hashes as keys
#         #and the jsons as values
#         item_dict = {}
#         hash = hash_dict[table_name]
#         for item in item_jsons:
#             item_dict[item[hash]] = item

#         #add that dictionary to our all_data using the name of the table
#         #as a key.
#         all_data[table_name] = item_dict

#     print('Dictionary Generated!')
#     return all_data


#check if pickle exists, if not create one.
# if os.path.isfile(r'path\to\file\manifest.content') == False:
#     get_manifest()
#     all_data = build_dict(hashes)
#     with open('manifest.pickle', 'wb') as data:
#         pickle.dump(all_data, data)
#         print("'manifest.pickle' created!\nDONE!")
# else:
#     print('Pickle Exists')

# with open('manifest.pickle', 'rb') as data:
#     all_data = pickle.load(data)

# hash = 1274330687
# ghorn = all_data['DestinyInventoryItemDefinition'][hash]

# print('Name: '+ghorn['itemName'])
# print('Type: '+ghorn['itemTypeName'])
# print('Tier: '+ghorn['tierTypeName'])
# print(ghorn['itemDescription'])
