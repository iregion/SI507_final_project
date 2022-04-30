

# from inspect import classify_class_attrs
import requests, zipfile, os, pickle, json, sqlite3
import d2manifest

#select language
while True:
    language=input("Please select your language. Input 1 for English or 2 for Chinese\n")
    if language == '1':
        language=0
        break
    elif language == '2':
        language=1
        break
    print('Invalid input')


en={'error input':'Invalid input',
    'refresh':'Do you want to refresh your database if it has existed? 1 for yes or 2 for no',
    'search mode':'Do you want to search single perk or a perk combination? 1 for single or 2 for combination',
    'single perk':'Input the perk name you want to search',
    'double perk one':'Input the first perk name you want to search',
    'double perk two':'Input the second perk name you want to search',
    'bucket':'Which weapon bucket you want to search in, 0 for all, 1 for kinetic, 2 for energy, 3 for power',
    'damage type':'Which damage type you want to search in, 0 for all, 1 for kinetic, 2 for solar, 3 for arc, 4 for void, 5 for stasis',
    'weapon type':'Which weapon type you want to search in, 0 for all, or input weapon type',
    'exit':'Do you want to exit? 1 for yes or any other key for no'
    }
zh={'error input':'非法输入',
    'refresh':'是否需要刷新数据库? 输入 1: 是, 2: 否',
    'search mode':'你想搜索单一perk还是双perk组合? 1: 单一, 2: 组合',
    'single perk':'输入你想要搜索的单一perk的名称',
    'double perk one':'输入你想要搜索的第一个perk的名称',
    'double perk two':'输入你想要搜索的第二个perk的名称',
    'bucket':'你想搜索哪类武器插槽, 0: 所有, 1: 动能武器, 2: 能量武器, 3: 威能武器',
    'damage type':'你想搜索哪种伤害类型, 0: 所有, 1: 动能, 2: 烈日, 3: 电弧, 4: 虚空, 5: 冰影',
    'weapon type':'你想要搜索哪种武器类型, 0: 所有, 或者直接输入武器类型',
    'exit':'是否退出程序? 1: 是  任意键: 否'
    }

language_pack=[en,zh]

# refresh database
while True:
    print(language_pack[language]['refresh'])
    refresh=input()
    if refresh == '1' or refresh == '2':
        break
    print(language_pack[language]['error input'])



if refresh == '1':
    d2manifest.get_manifest(language)
else:
    if (language==0 and os.path.exists('Manifest_en.content')) or (language==1 and os.path.exists('Manifest_zh.content')):
        pass
    else:
        d2manifest.get_manifest(language)

if language == 0:
    con = sqlite3.connect('Manifest_en.content')
else:
    con = sqlite3.connect('Manifest_zh.content')
#print('Connected')
#create a cursor object
cur = con.cursor()

item_set_name = "DestinyInventoryItemDefinition"
perk_set_name = "DestinyPlugSetDefinition"

cur.execute('SELECT json from '+item_set_name)
print('Generating '+item_set_name+' dictionary....')
item_set = cur.fetchall()
item_set_jsons = [json.loads(item[0]) for item in item_set]

item_set_hash_dict = {}
# weapon_set_dict = {}
# weapon_set_list = []
randomized_weapon_set_dict = {}

for each_item in item_set_jsons:
    item_hash=each_item['hash']
    item_name=each_item["displayProperties"]["name"]
    item_set_hash_dict[item_hash]=each_item
    if each_item["itemType"] == 3:
        # weapon_set_list.append(each_item)
        # weapon_set_dict[item_name] = each_item
        if len(each_item['sockets']['socketEntries']) > 5:
            if 'randomizedPlugSetHash' in each_item['sockets']['socketEntries'][3] and 'randomizedPlugSetHash' in each_item['sockets']['socketEntries'][4]:
                randomized_weapon_set_dict[item_name]=each_item


cur.execute('SELECT json from '+perk_set_name)
print('Generating '+perk_set_name+' dictionary....')
perk_set = cur.fetchall()
perk_set_jsons = [json.loads(item[0]) for item in perk_set]

perk_set_hash_dict = {}
for each_item in perk_set_jsons:
    item_hash=each_item['hash']
    perk_set_hash_dict[item_hash]=each_item


# build the top structure of tree
#top
weapon_tree={}
#first layer (bucket)
weapon_tree['kinetic weapon']={}
weapon_tree['energy weapon']={}
weapon_tree['power weapon']={}
#second layer (damage type)
weapon_tree['kinetic weapon']['stasis']={}
weapon_tree['kinetic weapon']['kinetic']={}
weapon_tree['energy weapon']['solar']={}
weapon_tree['energy weapon']['arc']={}
weapon_tree['energy weapon']['void']={}
weapon_tree['power weapon']['solar']={}
weapon_tree['power weapon']['arc']={}
weapon_tree['power weapon']['void']={}
weapon_tree['power weapon']['stasis']={}


# adding third and fourth layer
bucket_hash_table={1498876634:'kinetic weapon', 2465295065:'energy weapon', 953998645: 'power weapon'}
damage_type_table={1:'kinetic', 2:'arc', 3:'solar', 4:'void', 6:'stasis'}

tmp=[]
for each_weapon_name in randomized_weapon_set_dict.keys():
    #base infomation
    each_weapon=randomized_weapon_set_dict[each_weapon_name]
    each_weapon_type=randomized_weapon_set_dict[each_weapon_name]['itemTypeDisplayName']
    each_bucket=bucket_hash_table[randomized_weapon_set_dict[each_weapon_name]['equippingBlock']['equipmentSlotTypeHash']]
    each_damage_type=damage_type_table[randomized_weapon_set_dict[each_weapon_name]['defaultDamageType']]
    #perk infomation
    perk_one_pool_hash=randomized_weapon_set_dict[each_weapon_name]['sockets']['socketEntries'][3]['randomizedPlugSetHash']
    perk_one_pool=perk_set_hash_dict[perk_one_pool_hash]['reusablePlugItems']
    perk_one_pool_name=[]
    for each_perk in perk_one_pool:
        each_perk_hash=each_perk['plugItemHash']
        each_perk_name=item_set_hash_dict[each_perk_hash]["displayProperties"]["name"]
        perk_one_pool_name.append(each_perk_name)       
    perk_two_pool_hash=randomized_weapon_set_dict[each_weapon_name]['sockets']['socketEntries'][4]['randomizedPlugSetHash']
    perk_two_pool=perk_set_hash_dict[perk_two_pool_hash]['reusablePlugItems']
    perk_two_pool_name=[]
    for each_perk in perk_two_pool:
        each_perk_hash=each_perk['plugItemHash']
        each_perk_name=item_set_hash_dict[each_perk_hash]["displayProperties"]["name"]
        perk_two_pool_name.append(each_perk_name)
    leaf_tuple_12=(each_weapon_name, perk_two_pool_name)
    leaf_tuple_21=(each_weapon_name, perk_one_pool_name)
    # add third layer (weapon type)
    if each_weapon_type not in weapon_tree[each_bucket][each_damage_type]:
        weapon_tree[each_bucket][each_damage_type][each_weapon_type]={}
    #add fourth layer (perk one)
    for each_perk_name in perk_one_pool_name:
        if each_perk_name not in weapon_tree[each_bucket][each_damage_type][each_weapon_type]:
            weapon_tree[each_bucket][each_damage_type][each_weapon_type][each_perk_name]=[]
            weapon_tree[each_bucket][each_damage_type][each_weapon_type][each_perk_name].append(leaf_tuple_12)
        else:
            weapon_tree[each_bucket][each_damage_type][each_weapon_type][each_perk_name].append(leaf_tuple_12)
    for each_perk_name in perk_two_pool_name:
        if each_perk_name not in weapon_tree[each_bucket][each_damage_type][each_weapon_type]:
            weapon_tree[each_bucket][each_damage_type][each_weapon_type][each_perk_name]=[]
            weapon_tree[each_bucket][each_damage_type][each_weapon_type][each_perk_name].append(leaf_tuple_21)
        else:
            weapon_tree[each_bucket][each_damage_type][each_weapon_type][each_perk_name].append(leaf_tuple_21)


#print(weapon_tree['kinetic weapon']['kinetic']['手炮']['萤火虫'])
# for each_damage_type in weapon_tree['energy weapon'].keys():
#     print(weapon_tree['energy weapon'][each_damage_type]['霰弹枪']['强力首发'])
    # weapon_tree[each_bucket][each_damage_type][each_weapon_type].append(each_weapon_name)

bucket_input_table={'1':'kinetic weapon', '2':'energy weapon', '3':'power weapon'}
damage_type_input_table={'1':'kinetic', '2':'solar', '3':'arc', '4':'void', '5':'stasis'}


def search_in_weapon(bucket, damage_type, weapon_type, input_perk, search_mode):
    if search_mode == '1':
        if input_perk in weapon_tree[bucket][damage_type][weapon_type].keys():
            for each_weapon in weapon_tree[bucket][damage_type][weapon_type][input_perk]:
                print(each_weapon[0])
    else:
        if input_perk[0] in weapon_tree[bucket][damage_type][weapon_type].keys():
            for each_weapon in weapon_tree[bucket][damage_type][weapon_type][input_perk[0]]:
                if input_perk[1] in each_weapon[1]:
                    print(each_weapon[0])

def search_in_damage(bucket, damage_type, input_weapon_type, input_perk, search_mode):
    if input_weapon_type == '0':
        for each_weapon_type in weapon_tree[bucket][damage_type].keys():
            search_in_weapon(bucket, damage_type, each_weapon_type, input_perk, search_mode)
    else:
        if input_weapon_type in weapon_tree[bucket][damage_type].keys():
            search_in_weapon(bucket, damage_type, input_weapon_type, input_perk, search_mode)
        # else:
        #     print("Don't have this weapon type")

def search_in_bucket(bucket, input_damage_type, input_weapon_type, input_perk, search_mode):
    if input_damage_type == '0':
        for each_damage_type in weapon_tree[bucket].keys():
            search_in_damage(bucket, each_damage_type, input_weapon_type, input_perk, search_mode)
    else:
        damage_type=damage_type_input_table[input_damage_type]
        if damage_type in weapon_tree[bucket].keys():
            search_in_damage(bucket, damage_type, input_weapon_type, input_perk, search_mode)
        # else:
        #     print("Don't have this damage type")




#main interation
while True:
    #select search mode 
    while True:
        print(language_pack[language]['search mode'])
        search_mode=input()
        if search_mode == '1' or search_mode == '2':
            break
        print(language_pack[language]['error input'])

    #for mode 1, single perk
    if search_mode == '1':
        # input single perk name   
        print(language_pack[language]['single perk'])
        input_perk_name=input()

    #for mode 2, perk combination
    else:
        # input two perk name
        input_perk_name=[]
        print(language_pack[language]['double perk one'])
        input_perk_name.append(input())
        print(language_pack[language]['double perk two'])
        input_perk_name.append(input())



    #constrian
    #ask bucket
    while True:
        print(language_pack[language]['bucket'])
        input_bucket=input()
        if input_bucket == '0' or input_bucket == '1' or input_bucket == '2' or input_bucket == '3':
            break
        print(language_pack[language]['error input'])
    #ask damage type
    while True:
        print(language_pack[language]['damage type'])
        input_damage_type=input()
        if input_damage_type == '0' or input_bucket == '1' or input_bucket == '2' or input_bucket == '3' or input_bucket == '4' or input_bucket == '5':
            break
        print(language_pack[language]['error input'])
    #ask weapon type
    print(language_pack[language]['weapon type'])
    input_weapon_type=input()

    print('---------------------------------------------------')
    #answer
    if input_bucket == '0':
        for each_bucket in weapon_tree.keys():
            search_in_bucket(each_bucket, input_damage_type, input_weapon_type, input_perk_name, search_mode)
    else:
        search_in_bucket(bucket_input_table[input_bucket], input_damage_type, input_weapon_type, input_perk_name, search_mode)




    print('---------------------------------------------------')
    #ask to exit
    print(language_pack[language]['exit'])
    whether_exit=input()
    if whether_exit == '1':
        break



    

        
    




