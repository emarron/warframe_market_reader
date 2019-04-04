import json
import pprint
import time
import requests
import xlsxwriter
from tqdm import tqdm

#   json reader
mf = open('json/Mods.json', 'r', encoding="utf8")
mod_file_str = mf.read()
mod_file = json.loads(mod_file_str)
wff = open('json/Warframes.json', 'r', encoding="utf8")
wf_file_str = wff.read()
wf_file = json.loads(wf_file_str)
pf = open('json/Mods.json', 'r', encoding="utf8")
p_file_str = pf.read()
p_file = json.loads(p_file_str)
mef = open('json/Melee.json', 'r', encoding="utf8")
me_file_str = mef.read()
me_file = json.loads(me_file_str)
sf = open('json/Melee.json', 'r', encoding="utf8")
s_file_str = sf.read()
s_file = json.loads(s_file_str)
# json lists of items, looks for the item fitting a certain criteria, changes the name to 'Looks Like This' to
# 'look_like_this'  and dumps it into a list.
lst_warframe = []
for x in wf_file:
    if 'Prime' in x.get('name'):
        y = x.get('name').lower()
        lst_warframe.append(y.replace(' ', '_'))
lst_primary = []
for x in p_file:
    if 'Prime' in x.get('name'):
        y = x.get('name').lower()
        lst_primary.append(y.replace(' ', '_'))
lst_melee = []
for x in me_file:
    if 'Prime' in x.get('name'):
        y = x.get('name').lower()
        lst_melee.append(y.replace(' ', '_'))
lst_secondary = []
for x in s_file:
    if 'Prime' in x.get('name'):
        y = x.get('name').lower()
        lst_secondary.append(y.replace(' ', '_'))
lst_mods = []
lst_derelict = []
lst_nightmare = []
lst_mods_prime = []
for x in mod_file:
    z = x.get('name').lower()
    lst_mods.append(z.replace(' ', '_'))
    if 'Primed' in x.get('name'):
        y = x.get('name').lower()
        lst_mods_prime.append(y.replace(' ', '_'))
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
# exist.
lst_prime_warframes = []
lst_prime_primary = []
lst_prime_secondary = []
lst_prime_melee = []
lst_prime_sets = []
lst_nightmare_mods = []
lst_derelict_mods = []
lst_all_mods = []
lst_mods_primed = []
for item in lst:
    if 'set' in item and 'prime' in item:
        lst_prime_sets.append(item)
    for primary in lst_primary:
        if primary in item:
            lst_prime_primary.append(item)
    for secondary in lst_secondary:
        if secondary in item:
            lst_prime_secondary.append(item)
    for melee in lst_melee:
        if melee in item:
            lst_prime_melee.append(item)
    for warframe in lst_warframe:
        if warframe in item:
            lst_prime_warframes.append(item)
    for mod in lst_mods:
        if mod in item:
            lst_all_mods.append(item)
    for mod in lst_derelict:
        if mod in item:
            lst_derelict_mods.append(item)
    for mod in lst_nightmare:
        if mod in item:
            lst_nightmare_mods.append(item)
    for mod in lst_mods_prime:
        if mod in item:
            lst_mods_primed.append(item)
lst_prime_warframes_sets = []
for warframe in lst_prime_warframes:
    for set in lst_prime_sets:
        if set in warframe:
            lst_prime_warframes_sets.append(set)

lst_prime_weapons = lst_prime_primary + lst_prime_secondary + lst_prime_melee

items = {
    # "all_items": lst,  # god have mercy, don't actually run this. gets info of every item on the site.
    # "all_mods": lst_all_mods,  # don't do this one either, jesus christ.
    "corrupted_mods": lst_derelict_mods,
    "nightmare_mods": lst_nightmare_mods,
    # the names for these were weird so I did it manually.
    "riven_mods": ['zaw_riven_mod_(veiled)', 'melee_riven_mod_(veiled)', 'rifle_riven_mod_(veiled)',
                   'pistol_riven_mod_(veiled)', 'kitgun_riven_mod_(veiled)', 'shotgun_riven_mod_(veiled)'],
    "primed_mods": lst_mods_primed,
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
        'avg': latest['avg_price'],
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
