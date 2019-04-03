import pprint
import time

import requests
import xlsxwriter
from tqdm import tqdm

protocol = 'https://'
root = 'api.warframe.market/v1'
modinfo = {}
items = {
    "all_primed_mods": ['primed_continuity', 'primed_ravage', 'primed_flow', 'primed_point_blank', 'primed_fast_hands',
                        'primed_heavy_trauma', 'primed_heated_charge', 'primed_reach', 'primed_pistol_mutation',
                        'primed_slip_magazine', 'primed_pistol_gambit', 'primed_morphic_transformer',
                        'primed_target_cracker', 'primed_rifle_ammo_mutation', 'primed_shotgun_ammo_mutation',
                        'primed_bane_of_infested', 'primed_bane_of_corpus', 'primed_bane_of_grineer',
                        'primed_pressure_point', 'primed_cryo_rounds', 'primed_regen', 'primed_bane_of_corrupted',
                        'primed_fever_strike', 'primed_quickdraw', 'primed_charged_shell', 'primed_expel_corpus',
                        'primed_expel_corrupted', 'primed_expel_grineer', 'primed_expel_infested'],
    "okay_primed_mods": ['primed_continuity', 'primed_flow', 'primed_vigor', 'primed_ravage', 'primed_point_blank',
                         'primed_charged_shell', 'primed_reach', 'primed_fury', 'primed_pressure_point',
                         'primed_fever_strike', 'primed_cryo_rounds, primed_shred', 'primed_heated_charge',
                         'primed_pistol_gambit', 'primed_target_cracker', 'primed_morphic_transformer', 'primed_regen'],
    "good_primed_mods": ['primed_continuity', 'primed_flow', 'primed_point_blank', 'primed_ravage', 'primed_reach',
                         'primed_fury', 'primed_pressure_point', 'primed_pistol_gambit', 'primed_target_cracker'],
    "baro_mods": ['jolt', 'voltaic_strike', 'high_voltage', 'shell_shock', 'fanged_fusillade', 'vermilion_storm',
                  'astral_twilight', 'tempo_royale', 'pummel', 'crash_course', 'full_contact', 'collision_force',
                  'buzz_kill', 'sweeping_serration', 'maim', 'thermite_rounds', 'scattering_inferno', 'scorch',
                  'volcanic_edge'],
    "corrupted_mods": ['blind_rage', 'fleeting_expertise', 'narrow_minded', 'overextended', 'transient_fortitude'],
    "riven_mods": ['zaw_riven_mod_(veiled)', 'melee_riven_mod_(veiled)', 'rifle_riven_mod_(veiled)',
                   'pistol_riven_mod_(veiled)', 'kitgun_riven_mod_(veiled)', 'shotgun_riven_mod_(veiled)'],
    "silver_grove": ['empowered_blades', 'growing_power'],
    # end mods; start warframes

    "all_warframes_prime": ['ash_prime_set', 'banshee_prime_set', 'chroma_prime_set', 'ember_prime_set',
                            'equinox_prime_set', 'frost_prime_set', 'hydroid_prime_set', 'limbo_prime_set',
                            'loki_prime_set', 'mag_prime_set', 'mesa_prime_set', 'mirage_prime_set', 'nekros_prime_set',
                            'nova_prime_set', 'nyx_prime_set', 'oberon_prime_set', 'rhino_prime_set', 'saryn_prime_set',
                            'trinity_prime_set', 'valkyr_prime_set', 'vauban_prime_set', 'volt_prime_set',
                            'zephyr_prime_set'],
    "ash_prime": ['ash_prime_blueprint', 'ash_prime_systems', 'ash_prime_neuroptics', 'ash_prime_chassis',
                  'ash_prime_set'],
    "banshee_prime": ['banshee_prime_blueprint', 'banshee_prime_systems', 'banshee_prime_neuroptics',
                      'banshee_prime_chassis', 'banshee_prime_set'],
    "chroma_prime": ['chroma_prime_blueprint', 'chroma_prime_systems', 'chroma_prime_neuroptics',
                     'chroma_prime_chassis', 'chroma_prime_set'],
    "ember_prime": ['ember_prime_blueprint', 'ember_prime_systems', 'ember_prime_neuroptics', 'ember_prime_chassis',
                    'ember_prime_set'],
    "equinox_prime": ['equinox_prime_blueprint', 'equinox_prime_systems', 'equinox_prime_neuroptics',
                      'equinox_prime_chassis',
                      'equinox_prime_set'],
    "frost_prime": ['frost_prime_blueprint', 'frost_prime_systems', 'frost_prime_neuroptics', 'frost_prime_chassis',
                    'frost_prime_set'],
    "hydroid_prime": ['hydroid_prime_blueprint', 'hydroid_prime_systems', 'hydroid_prime_neuroptics',
                      'hydroid_prime_chassis', 'hydroid_prime_set'],
    "limbo_prime": ['limbo_prime_blueprint', 'limbo_prime_systems', 'limbo_prime_neuroptics', 'limbo_prime_chassis',
                    'limbo_prime_set'],
    "loki_prime": ['loki_prime_blueprint', 'loki_prime_systems', 'loki_prime_neuroptics', 'loki_prime_chassis',
                   'loki_prime_set'],
    "mag_prime": ['mag_prime_blueprint', 'mag_prime_systems', 'mag_prime_neuroptics', 'mag_prime_chassis',
                  'mag_prime_set'],
    "mesa_prime": ['mesa_prime_blueprint', 'mesa_prime_systems', 'mesa_prime_neuroptics', 'mesa_prime_chassis',
                   'mesa_prime_set'],
    "mirage_prime": ['mirage_prime_blueprint', 'mirage_prime_systems', 'mirage_prime_neuroptics',
                     'mirage_prime_chassis', 'mirage_prime_set'],
    "nekros_prime": ['nekros_prime_blueprint', 'nekros_prime_systems', 'nekros_prime_neuroptics',
                     'nekros_prime_chassis', 'nekros_prime_set'],
    "nova_prime": ['nova_prime_blueprint', 'nova_prime_systems', 'nova_prime_neuroptics', 'nova_prime_chassis',
                   'nova_prime_set'],
    "nyx_prime": ['nyx_prime_blueprint', 'nyx_prime_systems', 'nyx_prime_neuroptics', 'nyx_prime_chassis',
                  'nyx_prime_set'],
    "oberon_prime": ['oberon_prime_blueprint', 'oberon_prime_systems', 'oberon_prime_neuroptics',
                     'oberon_prime_chassis', 'oberon_prime_set'],
    "rhino_prime": ['rhino_prime_blueprint', 'rhino_prime_systems', 'rhino_prime_neuroptics', 'rhino_prime_chassis',
                    'rhino_prime_set'],
    "saryn_prime": ['saryn_prime_blueprint', 'saryn_prime_systems', 'saryn_prime_neuroptics', 'saryn_prime_chassis',
                    'saryn_prime_set'],
    "trinity_prime": ['trinity_prime_blueprint', 'trinity_prime_systems', 'trinity_prime_neuroptics',
                      'trinity_prime_chassis', 'trinity_prime_set'],
    "valkyr_prime": ['valkyr_prime_blueprint', 'valkyr_prime_systems', 'valkyr_prime_neuroptics',
                     'valkyr_prime_chassis', 'valkyr_prime_set'],
    "vauban_prime": ['vauban_prime_blueprint', 'vauban_prime_systems', 'vauban_prime_neuroptics',
                     'vauban_prime_chassis', 'vauban_prime_set'],
    "volt_prime": ['volt_prime_blueprint', 'volt_prime_systems', 'volt_prime_neuroptics', 'volt_prime_chassis',
                   'volt_prime_set'],
    "zephyr_prime": ['zephyr_prime_blueprint', 'zephyr_prime_systems', 'zephyr_prime_neuroptics',
                     'zephyr_prime_chassis', 'zephyr_prime_set'],
    # end warframes, start weapons sets
    "primary_weapons": ['boar_prime_set', 'boltor_prime_set', 'braton_prime_set', 'burston_prime_set',
                        'cernos_prime_set', 'latron_prime_set', 'paris_prime_set', 'rubico_prime_set', 'soma_prime_set',
                        'sybaris_prime_set', 'tiberon_prime_set', 'tigris_prime_set', 'vectis_prime_set'],
    "secondary_weapons": ['akbolto_prime_set', 'akbronco_prime_set', 'akjagara_prime_set', 'aklex_prime_set',
                          'akstiletto_prime_set', 'akvasto_prime_set', 'ballistica_prime_set', 'bronco_prime_set',
                          'euphona_prime_set', 'hikou_prime_set', 'lex_prime_set', 'pyrana_prime_set',
                          'sicarus_prime_set', 'spira_prime_set', 'vasto_prime_set'],
    "melee_weapons": ['ankyros_prime_set', 'bo_prime_set', 'dakra_prime_set', 'destreza_prime_set',
                      'dual_kamas_prime_set', 'fang_prime_set', 'fragor_prime_set', 'galatine_prime_set',
                      'glaive_prime_set', 'gram_prime_set', 'kogake_prime_set', 'kronen_prime_set',
                      'nami_skyla_prime_set', 'nikana_prime_set', 'orthos_prime_set', 'reaper_prime_set',
                      'redeemer_prime_set', 'scindo_prime_set', 'silva_and_aegis_prime_set', 'venka_prime_set'],

}
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
