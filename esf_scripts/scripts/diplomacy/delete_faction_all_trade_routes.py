import argparse
import os
import pandas as pd

from ..lib import *



def delete_faction_all_trade_routes(faction_name: VANILLA_FACTION_KEY_HINTS):
    '''
    example:
        delete_faction_all_trade_routes('venice')
    '''

    assert faction_name in FACTION_IDS['name'].to_list(), f"{faction_name} is not present in {FACTION_IDS_PATH}."

    # Collecting info

    faction_info = FACTION_IDS[FACTION_IDS['name'].eq(faction_name)].iloc[0]

    # Removing trade route

    international_trade_routes = InternationalTradeRoutes(os.path.join(OUTPUT_DIR, 'international_trade_routes', faction_info['international_trade_path']))

    international_trade_routes.clear_routes()

    # Applying changes

    international_trade_routes.write_xml()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python delete_faction_all_trade_routes.py venice')
    parser.add_argument('faction_name', type=str, help='')
    args = parser.parse_args()

    faction_name = args.faction_name

    FACTION_IDS = pd.read_csv(FACTION_IDS_PATH, delimiter='\t', dtype=str)
    REGION_IDS = pd.read_csv(REGION_IDS_PATH, delimiter='\t', dtype=str)

    delete_faction_all_trade_routes(faction_name)
