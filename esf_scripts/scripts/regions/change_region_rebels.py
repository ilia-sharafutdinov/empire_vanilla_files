import argparse
import os
import pandas as pd

from ..lib import *



def change_region_rebels(
    region_name: VANILLA_REGION_KEY_HINTS,
    new_rebels_faction_name: VANILLA_FACTION_KEY_HINTS,
    new_rebels_on_screen_name: str = None):
    '''
    example:
        change_region_rebels('flanders', 'westphalia')
    '''

    assert region_name in REGION_IDS['name'].to_list(), f"{region_name} is not present in {REGION_IDS_PATH}."
    assert new_rebels_faction_name in SUPPORTED_FACTION_KEYS, f"{new_rebels_faction_name} is not present in factions_tables."

    # Collecting info

    region_info = REGION_IDS[REGION_IDS['name'].eq(region_name)].iloc[0]

    # Reassigning rebelling faction and on-screen name

    region = Region(os.path.join(OUTPUT_DIR, 'region', region_info['path']))

    region.set_emergent_faction(new_rebels_faction_name)
    if new_rebels_on_screen_name:
        region.set_rebels_on_screen_name(new_rebels_on_screen_name)

    # Applying changes

    region.write_xml()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python change_region_rebels.py flanders westphalia')
    parser.add_argument('region_name', type=str, help='')
    parser.add_argument('new_rebels_faction_name', type=str, help='Faction name as found in db/factions_tables/factions.tsv')
    parser.add_argument('-n', '--new_rebels_on_screen_name', type=str, help='Just any fitting name. Vanilla usually makes use of the region name such as "Bavarian Rebels".')
    args = parser.parse_args()

    region_name = args.region_name
    new_rebels_faction_name = args.new_rebels_faction_name
    new_rebels_on_screen_name = args.new_rebels_on_screen_name

    REGION_IDS = pd.read_csv(REGION_IDS_PATH, delimiter='\t', dtype=str)

    change_region_rebels(region_name, new_rebels_faction_name, new_rebels_on_screen_name)
