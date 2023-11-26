import argparse
import os
import pandas as pd

from ..lib import *



def make_neutral(first_faction_name: VANILLA_FACTION_KEY_HINTS, second_faction_name: VANILLA_FACTION_KEY_HINTS):
    '''
    example:
        make_neutral('russia', 'ottomans')
    '''

    assert first_faction_name in FACTION_IDS['name'].to_list(), f"{first_faction_name} is not present in {FACTION_IDS_PATH}."
    assert second_faction_name in FACTION_IDS['name'].to_list(), f"{second_faction_name} is not present in {FACTION_IDS_PATH}."

    # Collecting info

    first_faction_info = FACTION_IDS[FACTION_IDS['name'].eq(first_faction_name)].iloc[0]
    second_faction_info = FACTION_IDS[FACTION_IDS['name'].eq(second_faction_name)].iloc[0]

    # Setting protectorate ID

    first_faction = Faction(os.path.join(OUTPUT_DIR, 'factions', second_faction_info['path']))

    if first_faction.get_protectorate_id() == second_faction_info['id']:
        first_faction.set_protectorate_id('0')

    second_faction = Faction(os.path.join(OUTPUT_DIR, 'factions', second_faction_info['path']))

    if second_faction.get_protectorate_id() == first_faction_info['id']:
        second_faction.set_protectorate_id('0')

    # Setting first diplomatic relationships

    first_diplomacy = Diplomacy(os.path.join(OUTPUT_DIR, 'diplomacy', first_faction_info['diplomacy_path']))

    first_relationship = first_diplomacy.get_relationship(second_faction_info['id'])

    first_relationship.set_if_allied_10('0')
    first_relationship.set_if_allied_20('0')
    first_relationship.set_relationship('neutral')
    first_relationship.set_relationship_with_protectorate('neutral')
    first_relationship.get_attitudes()[1].clear()
    first_relationship.get_attitudes()[7].clear()
    first_relationship.set_income_from_protectorate('0')
    first_relationship.set_payment_to_patron('0')

    first_relationship.update_overall_attitude()

    # Setting second diplomatic relationships

    second_diplomacy = Diplomacy(os.path.join(OUTPUT_DIR, 'diplomacy', second_faction_info['diplomacy_path']))

    second_relationship = second_diplomacy.get_relationship(first_faction_info['id'])

    second_relationship.set_if_allied_10('0')
    second_relationship.set_if_allied_20('0')
    second_relationship.set_relationship('neutral')
    second_relationship.set_relationship_with_protectorate('neutral')
    second_relationship.get_attitudes()[1].clear()
    second_relationship.get_attitudes()[7].clear()
    second_relationship.set_income_from_protectorate('0')
    second_relationship.set_payment_to_patron('0')

    second_relationship.update_overall_attitude()

    # Applying changes

    first_diplomacy.write_xml()

    second_diplomacy.write_xml()

    if first_faction.get_protectorate_id() == second_faction_info['id']:
        first_faction.write_xml()

    if second_faction.get_protectorate_id() == first_faction_info['id']:
        second_faction.write_xml()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python make_neutral.py russia ottomans')
    parser.add_argument('first_faction_name', type=str, help='')
    parser.add_argument('second_faction_name', type=str, help='')
    args = parser.parse_args()

    first_faction_name = args.first_faction_name
    second_faction_name = args.second_faction_name

    FACTION_IDS = pd.read_csv(FACTION_IDS_PATH, delimiter='\t', dtype=str)

    make_neutral(first_faction_name, second_faction_name)
