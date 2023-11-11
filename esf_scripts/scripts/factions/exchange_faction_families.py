import argparse
import os
import pandas as pd

from ..lib import *



def exchange_faction_families(first_faction_name: VANILLA_FACTION_KEY_HINTS, second_faction_name: VANILLA_FACTION_KEY_HINTS):
    '''
    example:
        exchange_faction_families('greece', 'venice')
    '''

    assert first_faction_name in FACTION_IDS['name'].to_list(), f"{first_faction_name} is not present in {FACTION_IDS_PATH}."
    assert second_faction_name in FACTION_IDS['name'].to_list(), f"{second_faction_name} is not present in {FACTION_IDS_PATH}."

    # Collecting info

    first_faction_info = FACTION_IDS[FACTION_IDS['name'].eq(first_faction_name)].iloc[0]
    second_faction_info = FACTION_IDS[FACTION_IDS['name'].eq(second_faction_name)].iloc[0]

    # Reassigning faction family paths

    first_faction = Faction(os.path.join(OUTPUT_DIR, 'factions', first_faction_info['path']))
    second_faction = Faction(os.path.join(OUTPUT_DIR, 'factions', second_faction_info['path']))

    first_faction_family_path = first_faction.get_family_path()
    second_faction_family_path = second_faction.get_family_path()

    first_faction.set_family_path(second_faction_family_path)
    second_faction.set_family_path(first_faction_family_path)

    # Reassigning family faction IDs

    first_faction_family = Family(os.path.join(OUTPUT_DIR, 'family', first_faction_info['family_path']))

    for family_member in first_faction_family.get_family_members():
        if family_member.get_faction_id_1():
            family_member.set_faction_id_1(second_faction.get_id())
        if family_member.get_faction_id_2():
            family_member.set_faction_id_2(second_faction.get_id())

    second_faction_family = Family(os.path.join(OUTPUT_DIR, 'family', second_faction_info['family_path']))

    for family_member in second_faction_family.get_family_members():
        if family_member.get_faction_id_1():
            family_member.set_faction_id_1(first_faction.get_id())
        if family_member.get_faction_id_2():
            family_member.set_faction_id_2(first_faction.get_id())

    # Applying changes

    first_faction.write_xml()
    second_faction.write_xml()

    first_faction_family.write_xml()
    second_faction_family.write_xml()

    FACTION_IDS.loc[FACTION_IDS['name'].eq(first_faction_info['name']), 'family_path'] = second_faction_family_path
    FACTION_IDS.loc[FACTION_IDS['name'].eq(second_faction_info['name']), 'family_path'] = first_faction_family_path



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python exchange_faction_families.py greece venice')
    parser.add_argument('first_faction_name', type=str, help='')
    parser.add_argument('second_faction_name', type=str, help='')
    args = parser.parse_args()

    first_faction_name = args.first_faction_name
    second_faction_name = args.second_faction_name

    FACTION_IDS = pd.read_csv(FACTION_IDS_PATH, delimiter='\t', dtype=str)

    exchange_faction_families(first_faction_name, second_faction_name)

    FACTION_IDS.to_csv(FACTION_IDS_PATH, sep='\t', index=False)
