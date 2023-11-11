import argparse
import os
import pandas as pd

from ..lib import *



def change_faction_emergency(faction_name: VANILLA_FACTION_KEY_HINTS, emergent: Literal['yes', 'no']):
    '''
    example:
        change_faction_emergency('punjab', 'no')
    '''

    assert faction_name in FACTION_IDS['name'].to_list(), f"{faction_name} is not present in {FACTION_IDS_PATH}."

    # Collecting info

    faction_info = FACTION_IDS[FACTION_IDS['name'].eq(faction_name)].iloc[0]

    # Reassigning faction emergency

    faction = Faction(os.path.join(OUTPUT_DIR, 'factions', faction_info['path']))

    if emergent == 'yes':
        faction.make_emergent()
    else:
        faction.make_non_emergent()

    # Applying changes

    faction.write_xml()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python change_faction_emergency.py punjab no')
    parser.add_argument('faction_name', type=str, help='')
    parser.add_argument('emergent', type=str, choices=['yes', 'no'], help='')
    args = parser.parse_args()

    faction_name = args.faction_name
    emergent = args.emergent

    FACTION_IDS = pd.read_csv(FACTION_IDS_PATH, delimiter='\t', dtype=str)

    change_faction_emergency(faction_name, emergent)
