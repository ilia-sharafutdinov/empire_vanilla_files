import argparse
import os
import pandas as pd

from ..lib import *



def enable_protectorate_diplomacy(protectorate_faction_name: VANILLA_FACTION_KEY_HINTS):
    '''
    example:
        enable_protectorate_diplomacy('thirteen_colonies')
    '''

    assert protectorate_faction_name in FACTION_IDS['name'].to_list(), f"{protectorate_faction_name} is not present in {FACTION_IDS_PATH}."

    # Collecting info

    faction_info = FACTION_IDS[FACTION_IDS['name'].eq(protectorate_faction_name)].iloc[0]

    # Removing protectorate ID

    faction = Faction(os.path.join(OUTPUT_DIR, 'factions', faction_info['path']))

    faction.set_protectorate_id('0')

    # Applying changes

    faction.write_xml()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python enable_protectorate_diplomacy.py thirteen_colonies')
    parser.add_argument('protectorate_faction_name', type=str, help='')
    args = parser.parse_args()

    protectorate_faction_name = args.protectorate_faction_name

    FACTION_IDS = pd.read_csv(FACTION_IDS_PATH, delimiter='\t', dtype=str)

    enable_protectorate_diplomacy(protectorate_faction_name)
