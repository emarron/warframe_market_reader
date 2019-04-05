import itertools
import json
import pprint
import time
import requests
import xlsxwriter
from tqdm import tqdm

#   json reader
with open('json/Mods.json', 'r', encoding="utf8") as mf:
    mod_file_str = mf.read()
mod_file = json.loads(mod_file_str)
with open('json/Warframes.json', 'r', encoding="utf8") as wff:
    wf_file_str = wff.read()
wf_file = json.loads(wf_file_str)
with open('json/Primary.json', 'r', encoding="utf8") as pf:
    p_file_str = pf.read()
p_file = json.loads(p_file_str)
with open('json/Melee.json', 'r', encoding="utf8") as mef:
    me_file_str = mef.read()
me_file = json.loads(me_file_str)
with open('json/Secondary.json', 'r', encoding="utf8") as sf:
    s_file_str = sf.read()
s_file = json.loads(s_file_str)
# json lists of items, looks for the item fitting a certain criteria, changes the name to 'Looks Like This' to
# 'look_like_this'  and dumps it into a list.
lst_warframe = [x['name'].lower().replace(' ', '_') for x in wf_file if 'Prime' in x['name']]
lst_melee = [x['name'].lower().replace(' ', '_') for x in me_file if 'Prime' in x['name']]
lst_secondary = [x['name'].lower().replace(' ', '_') for x in s_file if 'Prime' in x['name']]
lst_primary = [x['name'].lower().replace(' ', '_') for x in p_file if 'Prime' in x['name']]
lst_mods = [x['name'].lower().replace(' ', '_') for x in mod_file]
lst_mods_prime = [x['name'].lower().replace(' ', '_') for x in mod_file if 'Prime' in x['name']]
lst_derelict = []
lst_nightmare = []
lst_syndicate_mod = []
lst_pet_mod = []
for x in mod_file:
    if 'Syndicate' in x.get('uniqueName'):
            z = x.get('name').lower()
            lst_syndicate_mod.append(z.replace(' ', '_'))
    if 'Pets' in x.get('uniqueName'):
            z = x.get('name').lower()
            lst_pet_mod.append(z.replace(' ', '_'))
    if x.get('drops'):
        for y in x.get('drops'):
            if 'Derelict Vault' in y.get('location'):
                z = x.get('name').lower()
                lst_derelict.append(z.replace(' ', '_'))
            if 'Nightmare' in y.get('location'):
                z = x.get('name').lower()
                lst_nightmare.append(z.replace(' ', '_'))
# wfmarket crawler
protocol = 'https://'
root = 'api.warframe.market/v1'
latest = []
lst = []
endpoint = '/items'
resp = requests.get(protocol + root + endpoint)
latest = resp.json()['payload']['items']['en']
initial_lst = resp.json()['payload']['items']['en']
# Gets the name of all the items on Warframe Market.
for item in initial_lst:
    url_name = item.get('url_name')
    lst.append(url_name)
# dictionary of searches, Remember those lists generated from the json files from the comment at line 24? This checks
# them against the list of items from Warframe Market. Just to make sure we aren't looking for something that doesn't
# exist. Please ignore the spaghetti, I was 'practising' list comprehension.
lst_prime_sets = [item for item in lst if 'set' in item and 'prime' in item]
lst_prime_primary = list(itertools.chain(*list(filter(lambda x: len(x) > 0,[[item for primary in lst_primary if primary in item] for item in lst]))))
lst_prime_secondary = list(itertools.chain(*list(filter(lambda x: len(x) > 0,[[item for secondary in lst_secondary if secondary in item] for item in lst]))))
lst_prime_melee = list(itertools.chain(*list(filter(lambda x: len(x) > 0,[[item for melee in lst_melee if melee in item] for item in lst]))))
lst_prime_warframes = list(itertools.chain(*list(filter(lambda x: len(x) > 0,[[item for warframe in lst_warframe if warframe in item] for item in lst]))))
lst_all_mods = list(itertools.chain(*list(filter(lambda x: len(x) > 0,[[item for mod in lst_mods if mod in item] for item in lst]))))
lst_derelict_mods = list(itertools.chain(*list(filter(lambda x: len(x) > 0,[[item for mod in lst_derelict if mod in item] for item in lst]))))
lst_nightmare_mods = list(itertools.chain(*list(filter(lambda x: len(x) > 0,[[item for mod in lst_nightmare if mod in item] for item in lst]))))
lst_syndicate_mods = list(itertools.chain(*list(filter(lambda x: len(x) > 0,[[item for mod in lst_syndicate_mod if mod in item] for item in lst]))))
lst_pet_mods = list(itertools.chain(*list(filter(lambda x: len(x) > 0,[[item for mod in lst_pet_mod if mod in item] for item in lst]))))
lst_primed_mods = list(itertools.chain(*list(filter(lambda x: len(x) > 0,[[item for mod in lst_mods_prime if mod in item] for item in lst]))))
lst_prime_weapons = lst_prime_primary + lst_prime_secondary + lst_prime_melee
lst_prime_warframes_sets = list(set(lst_prime_sets) & set(lst_prime_warframes))

items = {
    # "all_items": lst,  # god have mercy, don't actually run this. gets info of every item on the site.
    # "all_mods": lst_all_mods,  # don't do this one either, jesus christ.
    "corrupted_mods": lst_derelict_mods,
    "nightmare_mods": lst_nightmare_mods,
    "syndicate_mods": lst_syndicate_mods,
    "pet_mods": lst_pet_mods,
    # the names for these were weird so I did it manually.
    "riven_mods": ['zaw_riven_mod_(veiled)', 'melee_riven_mod_(veiled)', 'rifle_riven_mod_(veiled)',
                   'pistol_riven_mod_(veiled)', 'kitgun_riven_mod_(veiled)', 'shotgun_riven_mod_(veiled)'],
    "primed_mods": lst_primed_mods,
    # end mods, start primes
    "prime_warframe_all": lst_prime_warframes,  # big list.
    "prime_warframe_set": lst_prime_warframes_sets,
    "prime_melee_all": lst_prime_melee,
    "prime_primary_all": lst_prime_primary,
    "prime_secondary_all": lst_prime_secondary,
    "prime_sets": lst_prime_sets,
    "prime_weapons": lst_prime_weapons  # big list.
}
# actual search script
modinfo = {}
while True:
    inp = input('select one of:\n' + '\n'.join(items.keys()) + '\n')
    try:
        item = items[inp]
        break
    except KeyError:
        print('try again')
for i in tqdm(item):
    endpoint = '/items/' + i + '/statistics'
    resp = requests.get(protocol + root + endpoint)
    latest = resp.json()['payload']['statistics_live']['48hours']
    latest = filter(lambda x: x['order_type'] == 'sell', latest)
    try:
        latest = filter(lambda x: x.get('mod_rank', 0) == 0, latest)
    except KeyError:
        pass
    latest = list(latest)
    latest = latest[-1]
    modinfo[i] = {
        'volume': latest['volume'],
        'min': latest['min_price'],
        'max': latest['max_price'],
        # 'avg': latest['avg_price'],   # avg is essentially useless, median is better
        'med': latest['median']
    }
    time.sleep(1 / 3)  # only 3 requests are allowed per second.
workbook = xlsxwriter.Workbook('xlsx/warframe_temp.xlsx')
worksheet = workbook.add_worksheet()
row = 0
col = 0
for k in modinfo.keys():
    for item in modinfo[k]:
        worksheet.write(row, col + 1, item)
        row = 0
        col = col + 1
    col = 0
row = 0
col = 0
for k in modinfo.keys():
    row += 1
    worksheet.write(row, col, k)
    for item in modinfo[k]:
        a = modinfo.get(k, {}).get(item)
        worksheet.write(row, col + 1, a)
        col = col + 1
    col = 0
worksheet.set_column('A:A', 30)
workbook.close()
pprint.pprint(modinfo, width=100)
