import argparse
import os
import pandas as pd

from ..lib import *



def delete_faction_trade_route(faction_name: VANILLA_FACTION_KEY_HINTS, destination_region: VANILLA_REGION_KEY_HINTS):
    '''
    example:
        delete_faction_trade_route('venice', 'rumelia')
    '''

    assert faction_name in FACTION_IDS['name'].to_list(), f"{faction_name} is not present in {FACTION_IDS_PATH}."
    assert destination_region in REGION_IDS['name'].to_list(), f"{destination_region} is not present in {REGION_IDS}."

    # Collecting info

    faction_info = FACTION_IDS[FACTION_IDS['name'].eq(faction_name)].iloc[0]
    region_info = REGION_IDS[REGION_IDS['name'].eq(destination_region)].iloc[0]

    # Removing trade route

    international_trade_routes = InternationalTradeRoutes(os.path.join(OUTPUT_DIR, 'international_trade_routes', faction_info['international_trade_path']))

    if region_info['id'] in international_trade_routes.get_routes().keys():
        international_trade_routes.remove_route(region_info['id'])
    else:
        raise ValueError(f"Could not find {region_info['id']} in {os.path.join(OUTPUT_DIR, 'international_trade_routes', faction_info['international_trade_path'])}.")

    # Applying changes

    international_trade_routes.write_xml()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python delete_faction_trade_route.py venice rumelia')
    parser.add_argument('faction_name', type=str, help='')
    parser.add_argument('destination_region', type=str, help='')
    args = parser.parse_args()

    faction_name = args.faction_name
    destination_region = args.destination_region

    FACTION_IDS = pd.read_csv(FACTION_IDS_PATH, delimiter='\t', dtype=str)
    REGION_IDS = pd.read_csv(REGION_IDS_PATH, delimiter='\t', dtype=str)

    delete_faction_trade_route(faction_name, destination_region)
