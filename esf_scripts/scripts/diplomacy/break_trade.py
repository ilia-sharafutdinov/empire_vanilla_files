import argparse
import os
import pandas as pd

from ..lib import *



def break_trade(first_faction_name: VANILLA_FACTION_KEY_HINTS, second_faction_name: VANILLA_FACTION_KEY_HINTS):
    '''
    example:
        break_trade('courland', 'poland_lithuania')
    '''

    assert first_faction_name in FACTION_IDS['name'].to_list(), f"{first_faction_name} is not present in {FACTION_IDS_PATH}."
    assert second_faction_name in FACTION_IDS['name'].to_list(), f"{second_faction_name} is not present in {FACTION_IDS_PATH}."

    # Collecting info

    first_faction_info = FACTION_IDS[FACTION_IDS['name'].eq(first_faction_name)].iloc[0]
    second_faction_info = FACTION_IDS[FACTION_IDS['name'].eq(second_faction_name)].iloc[0]

    # Setting first diplomatic relationships

    first_diplomacy = Diplomacy(os.path.join(OUTPUT_DIR, 'diplomacy', first_faction_info['diplomacy_path']))

    first_relationship = first_diplomacy.get_relationship(second_faction_info['id'])

    first_relationship.get_attitudes()[5].clear()
    first_relationship.make_non_trading()

    first_relationship.update_overall_attitude()

    # Setting second diplomatic relationships

    second_diplomacy = Diplomacy(os.path.join(OUTPUT_DIR, 'diplomacy', second_faction_info['diplomacy_path']))

    second_relationship = second_diplomacy.get_relationship(first_faction_info['id'])

    second_relationship.get_attitudes()[5].clear()
    second_relationship.make_non_trading()

    second_relationship.update_overall_attitude()

    # Applying changes

    first_diplomacy.write_xml()

    second_diplomacy.write_xml()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python break_trade.py courland poland_lithuania')
    parser.add_argument('first_faction_name', type=str, help='')
    parser.add_argument('second_faction_name', type=str, help='')
    args = parser.parse_args()

    first_faction_name = args.first_faction_name
    second_faction_name = args.second_faction_name

    FACTION_IDS = pd.read_csv(FACTION_IDS_PATH, delimiter='\t', dtype=str)

    break_trade(first_faction_name, second_faction_name)
